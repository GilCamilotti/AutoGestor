# AutoGestor - Exercício 2

## Projeto, arquitetura, UML e plano

**Equipe:** Gilberto de Araújo Camilotti e Gabrielle Vitória da Silva Martins  
**Disciplina:** Projeto de Software  
**Curso:** Análise e Desenvolvimento de Sistemas  
**Professor:** Jefferson Brandão  
**Data:** 05/11/2026

## A. Exercícios de fixação

### 1. Requisito x projeto

“O sistema deve permitir agendar consultas” descreve um requisito funcional, ou seja, uma capacidade que o sistema precisa oferecer ao usuário. Já “o sistema terá uma interface web, uma API e um banco de dados” descreve uma decisão de projeto e arquitetura, indicando como a solução será organizada tecnicamente para atender aos requisitos.

### 2. UML

- **(a) Atores e funcionalidades:** diagrama de casos de uso, pois mostra quem utiliza o sistema e quais funções cada usuário pode realizar.
- **(b) Classes e relacionamentos:** diagrama de classes, pois representa as entidades, seus atributos, operações e relações.
- **(c) Sequência de mensagens:** diagrama de sequência, pois apresenta a ordem das mensagens trocadas entre objetos ou componentes.
- **(d) Fluxo de atividades:** diagrama de atividades, pois representa as etapas de um processo e suas decisões.

### 3. Arquitetura de uma biblioteca

Uma arquitetura simples poderia conter os blocos abaixo:

1. **Interface web:** telas utilizadas por leitores e funcionários.
2. **API ou camada de aplicação:** recebe solicitações, aplica regras e coordena as operações.
3. **Módulo de empréstimos:** controla empréstimos, devoluções, reservas e atrasos.
4. **Banco de dados:** armazena leitores, livros, exemplares e movimentações.
5. **Autenticação:** controla login, perfis e permissões de acesso.

### 4. Riscos

- **Requisitos incompletos:** realizar reuniões curtas de validação com os usuários e revisar os requisitos antes do desenvolvimento.
- **Atraso na entrega:** dividir as tarefas em pequenas etapas, definir responsáveis e acompanhar o progresso semanalmente.
- **Perda ou inconsistência de dados:** validar entradas, manter cópias de segurança e testar as operações principais.

## B. Aplicação no Projeto Integrador

### 1. Revisão dos requisitos do E1

Os requisitos do AutoGestor foram revisados para utilizar frases objetivas, com o padrão “O sistema deve permitir...”. O escopo permanece concentrado em clientes, veículos, serviços, ordens de serviço, status e histórico de manutenção.

### 2. Arquitetura de alto nível

O AutoGestor será organizado em cinco blocos:

1. **Interface web:** telas para cadastro, consulta e atualização dos serviços.
2. **API e regras de negócio:** valida os dados, aplica permissões e coordena as operações.
3. **Módulo de clientes e veículos:** mantém os dados dos proprietários e seus veículos.
4. **Módulo de ordens de serviço:** registra serviços, datas, status e histórico.
5. **Banco de dados:** armazena os registros do sistema com integridade e segurança.

### 3. Diagramas UML

#### Diagrama de casos de uso

O diagrama representa os atores e suas principais funções: proprietário ou gerente gerencia usuários e consultas; atendente cadastra clientes, veículos e ordens de serviço; mecânico atualiza serviços e status; cliente consulta o andamento.

#### Diagrama de classes

- **Cliente:** id, nome, telefone e e-mail.
- **Veículo:** id, placa, modelo e ano.
- **Ordem de serviço:** id, datas de entrada e saída e status.
- **Serviço:** id, descrição e valor.
- **Relacionamentos:** um cliente possui veículos; um veículo possui ordens de serviço; uma ordem registra um ou mais serviços.

### 4. Interfaces principais e dados manipulados

| Interface | Dados principais | Operações |
|---|---|---|
| Clientes | nome, telefone, e-mail | cadastrar, editar, consultar |
| Veículos | placa, modelo, ano, cliente | cadastrar, vincular, consultar |
| Ordens de serviço | datas, status, observações | criar, atualizar, concluir |
| Histórico | veículo, serviços, datas e valores | consultar e filtrar |
| Acesso | usuário, senha e perfil | autenticar e controlar permissões |

### 5. Equipe, recursos, riscos e acompanhamento

**Equipe:** Gilberto de Araújo Camilotti e Gabrielle Vitória da Silva Martins.

**Recursos:** GitHub, documentação em Markdown e PDF, editor de código, ferramenta de modelagem UML e reuniões da dupla.

**Estratégia:** revisar os requisitos, modelar a solução, validar os diagramas e registrar cada etapa no repositório.

**Riscos e respostas:**

- Requisitos pouco claros: validar cada requisito antes de criar novas telas ou módulos.
- Diagrama incompatível com o escopo: comparar os diagramas com o README e os requisitos do E1.
- Falta de acompanhamento: registrar tarefas, responsáveis e situação no repositório.
- Alterações sem organização: usar commits separados e mensagens objetivas.

### 6. Organização do repositório


autoGestor/
├── README.md
└── docs/
    └── AutoGestor_Exercicio2_Arquitetura_UML.md

### 7. Commits realizados

- docs: atualizar README com arquitetura e UML do E2
- docs: adicionar arquitetura, diagramas UML e plano do E2
- docs: adicionar PDF do exercício 2
