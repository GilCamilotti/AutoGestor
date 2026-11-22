# Changelog do AutoGestor

## 1.0 — Versão final da entrega

### Adicionado

- Lançamento de serviços e cálculo do total em centavos.
- Controle de status, histórico de eventos e data de saída na conclusão.
- Critérios de conclusão, plano de testes, evidências de execução e roteiro da defesa.
- Compatibilidade com bancos SQLite do incremento 0.1.

### Corrigido

- Entradas com caracteres Unicode que se expandiam na conversão para maiúsculas passaram a ser rejeitadas antes da normalização da placa.

## 0.1.0 — Primeiro incremento funcional

### Adicionado

- Cadastro local de clientes e veículos, com vínculo entre os registros.
- Abertura de ordem de serviço com observações, data de entrada e status inicial.
- Consulta de status e data de entrada por número da ordem.
- Persistência em SQLite, usando somente a biblioteca padrão do Python.
- Plano incremental e instruções de execução no README.

### Melhoria

- A placa é normalizada no cadastro e na abertura da OS. A restrição de unicidade impede cadastros duplicados por variação de caixa, espaços ou hífen. A validação aceita os padrões clássico e Mercosul.

## Evolução planejada

- Interface web, API e acesso por perfil.
