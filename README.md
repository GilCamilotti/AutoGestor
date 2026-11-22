# AutoGestor

Sistema de gerenciamento de oficina mecânica desenvolvido no Projeto Integrador da disciplina Projeto de Software.

## Objetivo

Organizar informações de clientes, veículos e serviços de pequenas oficinas mecânicas, facilitando o acompanhamento dos consertos e o acesso ao histórico de manutenção.

## Problema identificado

Pequenas oficinas frequentemente utilizam anotações em papel, cadernos e mensagens para registrar clientes, veículos e serviços. Isso pode causar perda de dados, dificuldade de consulta, atrasos e falta de controle sobre os consertos.

## Usuários

- Proprietário ou gerente da oficina
- Atendentes
- Mecânicos
- Clientes

## Funcionalidades iniciais

- Cadastro de clientes e veículos
- Registro de serviços e ordens de serviço
- Atualização do status dos serviços
- Consulta do histórico de manutenção
- Registro das datas de entrada e saída dos veículos

## Requisitos não funcionais

- Interface simples e fácil de utilizar
- Acesso administrativo protegido por login e senha
- Consultas e cadastros com resposta em tempo adequado
- Armazenamento confiável das informações

## Arquitetura e modelagem

O E2 organiza o sistema em cinco blocos: interface web, API e regras de negócio, módulo de clientes e veículos, módulo de ordens de serviço e banco de dados.

Os requisitos revisados, a arquitetura, os diagramas UML, as interfaces, os dados, os riscos e o plano de acompanhamento estão em [`docs/AutoGestor_Exercicio2_Arquitetura_UML.md`](docs/AutoGestor_Exercicio2_Arquitetura_UML.md).

## Escopo inicial

### Incluído

Cadastro e consulta de clientes e veículos, registro de serviços, criação de ordens de serviço, atualização do andamento, histórico de manutenção e datas de entrada e saída.

### Fora do escopo

Pagamento online, emissão de notas fiscais, estoque de peças, integração com aplicativos de mensagens, aplicativo móvel exclusivo e gestão financeira completa.

## Equipe

- Gilberto de Araújo Camilotti
- Gabrielle Vitória da Silva Martins

## Disciplina

Projeto de Software — Professor Jefferson Brandão Moreira

## Análise estruturada

O [Exercício 4](docs/AutoGestor_Exercicio4_DFD.md) reúne o diagrama de contexto, o DFD nível 0, o dicionário de dados e o relatório de ajustes.

## Instalação e execução da versão 1.0

Baixe ou clone o repositório e entre na pasta do projeto. Use Python 3.11 ou superior, com o módulo SQLite da biblioteca padrão. Nenhum pacote do pip é necessário.

O exemplo usa um banco novo e dados fictícios. Se já existir um banco com esse nome, escolha outro para que os identificadores do exemplo comecem em 1.

```sh
python autogestor.py --banco demo.sqlite3 cliente "Cliente exemplo"
python autogestor.py --banco demo.sqlite3 veiculo 1 ABC-1234 "Modelo A" 2020
python autogestor.py --banco demo.sqlite3 abrir-os ABC1234 "Revisão"
python autogestor.py --banco demo.sqlite3 status-os 1 "Em andamento"
python autogestor.py --banco demo.sqlite3 servico 1 "Inspeção" 90.10
python autogestor.py --banco demo.sqlite3 status-os 1 "Concluída"
python autogestor.py --banco demo.sqlite3 consultar-os 1
```

O banco padrão é `autogestor.sqlite3`. A versão 1.0 cria as tabelas adicionais quando abre um banco da 0.1. O encerramento da OS registra a data de saída, exige pelo menos um serviço e bloqueia novos lançamentos. O sistema local depende das permissões do arquivo SQLite.

Execute os testes com `python -m unittest discover -s tests -v`. Veja o [plano de testes, análise de segurança e roteiro da defesa](docs/AutoGestor_Exercicio6_Testes_Seguranca.md), a [evidência de execução](docs/evidencia-e6.txt), o [plano incremental](docs/AutoGestor_Exercicio5_Incrementos.md) e o [CHANGELOG](CHANGELOG.md).

## Status

A versão 1.0 local permite cadastrar clientes e veículos, conduzir uma OS, registrar serviços e consultar o histórico.

## Repositório

https://github.com/GilCamilotti/AutoGestor

## Commits do Exercício 2

- `docs: atualizar README com arquitetura e UML do E2`
- `docs: adicionar arquitetura, diagramas UML e plano do E2`
- `docs: adicionar PDF do exercício 2`
