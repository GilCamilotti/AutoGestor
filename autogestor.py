"""Primeiro incremento do AutoGestor. Use --help para ver os comandos."""

import argparse
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
"""


def required(value):
    cleaned = value.strip()
    if not cleaned:
        raise argparse.ArgumentTypeError("informe um valor preenchido")
    return cleaned


def plate(value):
    normalized = re.sub(r"[\s-]+", "", value).upper()
    if not re.fullmatch(r"[A-Z]{3}[0-9][0-9A-Z][0-9]{2}", normalized):
        raise argparse.ArgumentTypeError("use placa no padrão ABC1234 ou ABC1D23")
    return normalized


def year(value):
    if not re.fullmatch(r"[0-9]{4}", value) or int(value) < 1000:
        raise argparse.ArgumentTypeError("informe um ano com quatro dígitos")
    return int(value)


def build_parser():
    parser = argparse.ArgumentParser(description="AutoGestor — cadastro e abertura de ordens")
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
        now = datetime.now().astimezone().isoformat(timespec="seconds")
        cursor = db.execute(
            "INSERT INTO ordem(veiculo_id, entrada, observacoes) VALUES (?, ?, ?)",
            (vehicle[0], now, args.observacoes),
        )
        return f"OS {cursor.lastrowid} aberta."

    order = db.execute(
        """SELECT o.id, v.placa, o.status, o.entrada
           FROM ordem o JOIN veiculo v ON v.id = o.veiculo_id WHERE o.id = ?""",
        (args.os_id,),
    ).fetchone()
    if order is None:
        raise ValueError("Ordem de serviço não encontrada.")
    return f"OS {order[0]} | Placa: {order[1]} | Status: {order[2]} | Entrada: {order[3]}"


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        with closing(sqlite3.connect(args.banco)) as db:
            db.execute("PRAGMA foreign_keys = ON")
            db.executescript(SCHEMA)
            with db:
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
