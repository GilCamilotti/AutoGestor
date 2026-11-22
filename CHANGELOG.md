# Changelog do AutoGestor

## 0.1.0 — Primeiro incremento funcional

### Adicionado

- Cadastro local de clientes e veículos, com vínculo entre os registros.
- Abertura de ordem de serviço com observações, data de entrada e status inicial.
- Consulta de status e data de entrada por número da ordem.
- Persistência em SQLite, usando somente a biblioteca padrão do Python.
- Plano incremental e instruções de execução no README.

### Melhoria

- A placa é normalizada no cadastro e na abertura da OS. A restrição de unicidade impede cadastros duplicados por variação de caixa, espaços ou hífen. A validação aceita os padrões clássico e Mercosul.

## Próximos incrementos

- 0.2.0 — Registro de serviços, transições de status, histórico e data de saída.
- 0.3.0 — Interface web, API e acesso por perfil.
