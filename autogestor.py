"""AutoGestor 1.0, versão de terminal. Use --help para ver os comandos."""

import argparse
from decimal import Decimal
from contextlib import closing
from datetime import datetime
from pathlib import Path
import re
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS cliente (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS veiculo (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES cliente(id),
    placa TEXT NOT NULL UNIQUE,
    modelo TEXT NOT NULL,
    ano INTEGER NOT NULL CHECK (ano BETWEEN 1000 AND 9999)
);
CREATE TABLE IF NOT EXISTS ordem (
    id INTEGER PRIMARY KEY,
    veiculo_id INTEGER NOT NULL REFERENCES veiculo(id),
    entrada TEXT NOT NULL,
    observacoes TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Aberta' CHECK (status = 'Aberta')
);
CREATE TABLE IF NOT EXISTS servico (
    id INTEGER PRIMARY KEY,
    ordem_id INTEGER NOT NULL REFERENCES ordem(id),
    descricao TEXT NOT NULL,
    valor_centavos INTEGER NOT NULL CHECK (valor_centavos >= 0)
);
CREATE TABLE IF NOT EXISTS evento_ordem (
    id INTEGER PRIMARY KEY,
    ordem_id INTEGER NOT NULL REFERENCES ordem(id),
    status TEXT NOT NULL CHECK (status IN ('Em andamento', 'Concluída')),
    data_hora TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_servico_ordem ON servico(ordem_id);
CREATE INDEX IF NOT EXISTS idx_evento_ordem ON evento_ordem(ordem_id, id);
"""

TRANSICOES = {"Aberta": "Em andamento", "Em andamento": "Concluída"}


def required(value):
    cleaned = value.strip()
    if not cleaned:
        raise argparse.ArgumentTypeError("informe um valor preenchido")
    return cleaned


def plate(value):
    normalized = re.sub(r"[\s-]+", "", value)
    if not normalized.isascii():
        raise argparse.ArgumentTypeError("use apenas letras ASCII e números na placa")
    normalized = normalized.upper()
    if not re.fullmatch(r"[A-Z]{3}[0-9][0-9A-Z][0-9]{2}", normalized):
        raise argparse.ArgumentTypeError("use placa no padrão ABC1234 ou ABC1D23")
    return normalized


def year(value):
    if not re.fullmatch(r"[0-9]{4}", value) or int(value) < 1000:
        raise argparse.ArgumentTypeError("informe um ano com quatro dígitos")
    return int(value)


def cents(value):
    if not re.fullmatch(r"[0-9]{1,9}(?:[.,][0-9]{1,2})?", value):
        raise argparse.ArgumentTypeError("informe um valor não negativo com até duas casas decimais")
    return int(Decimal(value.replace(",", ".")) * 100)


def money(amount):
    reais, centavos = divmod(amount, 100)
    return f"R$ {reais},{centavos:02d}"


def timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def find_order(db, order_id):
    order = db.execute(
        """SELECT o.id, v.placa, o.entrada, COALESCE(
               (SELECT e.status FROM evento_ordem e WHERE e.ordem_id = o.id
                ORDER BY e.id DESC LIMIT 1), o.status) AS status
           FROM ordem o JOIN veiculo v ON v.id = o.veiculo_id WHERE o.id = ?""",
        (order_id,),
    ).fetchone()
    if order is None:
        raise ValueError("Ordem de serviço não encontrada.")
    return order


def build_parser():
    parser = argparse.ArgumentParser(description="AutoGestor 1.0 — ordens de serviço")
    parser.add_argument("--banco", type=Path, default=Path("autogestor.sqlite3"))
    commands = parser.add_subparsers(dest="comando", required=True)

    client = commands.add_parser("cliente", help="Cadastrar um cliente")
    client.add_argument("nome", type=required)
    client.add_argument("--telefone", default="")
    client.add_argument("--email", default="")

    vehicle = commands.add_parser("veiculo", help="Cadastrar um veículo")
    vehicle.add_argument("cliente_id", type=int)
    vehicle.add_argument("placa", type=plate)
    vehicle.add_argument("modelo", type=required)
    vehicle.add_argument("ano", type=year)

    order = commands.add_parser("abrir-os", help="Abrir uma ordem para a placa")
    order.add_argument("placa", type=plate)
    order.add_argument("observacoes", type=required)

    status = commands.add_parser("consultar-os", help="Consultar status e data de entrada")
    status.add_argument("os_id", type=int)
    service = commands.add_parser("servico", help="Registrar um serviço na OS")
    service.add_argument("os_id", type=int)
    service.add_argument("descricao", type=required)
    service.add_argument("valor", type=cents)

    update = commands.add_parser("status-os", help="Atualizar o status de uma OS")
    update.add_argument("os_id", type=int)
    update.add_argument("status", choices=tuple(TRANSICOES.values()))
    return parser


def run(db, args):
    if args.comando == "cliente":
        cursor = db.execute(
            "INSERT INTO cliente(nome, telefone, email) VALUES (?, ?, ?)",
            (args.nome, args.telefone.strip(), args.email.strip()),
        )
        return f"Cliente cadastrado. Código: {cursor.lastrowid}"

    if args.comando == "veiculo":
        if db.execute("SELECT id FROM cliente WHERE id = ?", (args.cliente_id,)).fetchone() is None:
            raise ValueError("Cliente não encontrado.")
        cursor = db.execute(
            "INSERT INTO veiculo(cliente_id, placa, modelo, ano) VALUES (?, ?, ?, ?)",
            (args.cliente_id, args.placa, args.modelo, args.ano),
        )
        return f"Veículo cadastrado. Código: {cursor.lastrowid}"

    if args.comando == "abrir-os":
        vehicle = db.execute("SELECT id FROM veiculo WHERE placa = ?", (args.placa,)).fetchone()
        if vehicle is None:
            raise ValueError("Veículo não encontrado.")
        now = timestamp()
        cursor = db.execute(
            "INSERT INTO ordem(veiculo_id, entrada, observacoes) VALUES (?, ?, ?)",
            (vehicle[0], now, args.observacoes),
        )
        return f"OS {cursor.lastrowid} aberta."

    order_id, vehicle_plate, opened_at, status = find_order(db, args.os_id)

    if args.comando == "servico":
        if status == "Concluída":
            raise ValueError("A ordem concluída não aceita novos serviços.")
        db.execute(
            "INSERT INTO servico(ordem_id, descricao, valor_centavos) VALUES (?, ?, ?)",
            (order_id, args.descricao, args.valor),
        )
        return f"Serviço registrado na OS {order_id}."

    if args.comando == "status-os":
        if TRANSICOES.get(status) != args.status:
            raise ValueError(f"Transição inválida a partir de {status}.")
        if args.status == "Concluída" and db.execute(
            "SELECT 1 FROM servico WHERE ordem_id = ? LIMIT 1", (order_id,)
        ).fetchone() is None:
            raise ValueError("A ordem precisa ter pelo menos um serviço para ser concluída.")
        db.execute(
            "INSERT INTO evento_ordem(ordem_id, status, data_hora) VALUES (?, ?, ?)",
            (order_id, args.status, timestamp()),
        )
        return f"OS {order_id} atualizada para {args.status}."

    services = db.execute(
        "SELECT descricao, valor_centavos FROM servico WHERE ordem_id = ? ORDER BY id", (order_id,)
    ).fetchall()
    events = db.execute(
        "SELECT status, data_hora FROM evento_ordem WHERE ordem_id = ? ORDER BY id", (order_id,)
    ).fetchall()
    total = sum(value for _, value in services)
    lines = [
        f"OS {order_id} | Placa: {vehicle_plate} | Status: {status}",
        f"Entrada: {opened_at}",
        f"Total: {money(total)}",
    ]
    if status == "Concluída":
        lines.append(f"Saída registrada: {events[-1][1]}")
    lines.append("Serviços:")
    lines.extend(f"  {description} — {money(value)}" for description, value in services)
    lines.append("Histórico:")
    lines.append(f"  {opened_at} — Aberta")
    lines.extend(f"  {when} — {state}" for state, when in events)
    return "\n".join(lines)

def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        with closing(sqlite3.connect(args.banco)) as db:
            db.execute("PRAGMA foreign_keys = ON")
            db.executescript(SCHEMA)
            with db:
                db.execute("BEGIN" if args.comando == "consultar-os" else "BEGIN IMMEDIATE")
                result = run(db, args)
    except sqlite3.IntegrityError as error:
        if error.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
            parser.exit(1, "Erro: placa já cadastrada.\n")
        parser.exit(1, f"Erro de integridade dos dados: {error}\n")
    except (ValueError, sqlite3.Error) as error:
        parser.exit(1, f"Erro: {error}\n")
    print(result)


if __name__ == "__main__":
    main()
