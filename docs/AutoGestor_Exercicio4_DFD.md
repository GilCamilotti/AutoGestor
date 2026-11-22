# AutoGestor — Exercício 4

## 1. Revisão intermediária

A revisão usa o README e o [Exercício 2](AutoGestor_Exercicio2_Arquitetura_UML.md) no commit `cc285d69c3f7a7644131458890e89c372891d22f`. A devolutiva específica do professor está pendente. Foram mantidos o cadastro de clientes e veículos, as ordens de serviço (OS), as datas de entrada e saída, o acompanhamento e o histórico. A autenticação e o banco de dados constam no planejamento do E2.

## 2. Diagrama de contexto

```mermaid
flowchart LR
  A[Atendente] -->|Credenciais, dados cadastrais e abertura da OS| S((AutoGestor))
  S -->|Resultado do acesso, cadastros e número da OS| A
  M[Mecânico] -->|Credenciais, serviços e atualização da OS| S
  S -->|Resultado do acesso, serviços e status| M
  C[Cliente] -->|Identificação da OS| S
  S -->|Andamento da OS| C
  G[Gerente] -->|Credenciais e filtro de histórico| S
  S -->|Resultado do acesso e histórico de manutenção| G
```

## 3. DFD nível 0

```mermaid
flowchart TB
  A[Atendente]
  M[Mecânico]
  C[Cliente]
  G[Gerente]
  P0([1. Verificar acesso])
  P1([2. Manter cadastros])
  P2([3. Abrir OS])
  P3([4. Registrar serviços e andamento])
  P4([5. Consultar andamento e histórico])
  D0[(D1 Usuários e perfis)]
  D1[(D2 Clientes e veículos)]
  D2[(D3 Ordens de serviço)]
  D3[(D4 Serviços e histórico)]
  A & M & G -->|Credenciais| P0
  D0 -->|Conta e perfil| P0
  P0 -->|Resultado do acesso| A & M & G
  P0 -->|Identidade e perfil verificados| P1 & P2 & P3 & P4
  A -->|Dados cadastrais| P1
  D1 -->|Cadastros existentes| P1
  P1 -->|Cadastro validado| D1
  P1 -->|Resultado do cadastro| A
  A -->|Veículo, data de entrada e observações| P2
  D1 -->|Vínculo do veículo| P2
  P2 -->|Nova ordem| D2
  P2 -->|Número da OS| A
  M -->|Serviço, status e data de saída quando aplicável| P3
  D2 -->|Ordem e status atual| P3
  P3 -->|Ordem atualizada| D2
  P3 -->|Serviço ou evento| D3
  P3 -->|Serviço registrado e status atual| M
  C -->|Identificação da OS| P4
  G -->|Filtro de histórico| P4
  D1 -->|Veículo vinculado| P4
  D2 -->|Ordens e datas| P4
  D3 -->|Serviços e eventos| P4
  P4 -->|Andamento da OS| C
  P4 -->|Histórico de manutenção| G
```

O diagrama propõe que a consulta do cliente retorne somente os dados da OS que ele estiver autorizado a consultar. O mecanismo de comprovação desse vínculo precisa ser definido antes de implementar a consulta.

## 4. Dicionário de dados

| Item | Campos ou formato | Uso e regras |
|---|---|---|
| Cliente | id inteiro, nome, telefone e e-mail em texto | Identifica o proprietário. Nome obrigatório. |
| Veículo | id, cliente_id, placa, modelo, ano | Placa única. Cliente existente. Ano em quatro dígitos. |
| Ordem de serviço | id, veiculo_id, entrada, saída opcional, status, observações | Veículo existente. Saída igual ou posterior à entrada. |
| Serviço | id, os_id, descrição, valor decimal | Ordem existente, descrição preenchida e valor não negativo. |
| Status da OS | Aberta, Em andamento, Concluída | Valores propostos para acompanhar a ordem. |
| Evento de status | os_id, status, data e hora, usuário_id | Registra a mudança e seu responsável. |
| Conta de acesso | id, usuário, hash da senha, perfil | Usuário único. Perfil de gerente, atendente ou mecânico. |
| Consulta de andamento | identificador da OS e comprovação de vínculo | Retorna apenas os dados autorizados da ordem. |
| Filtro de histórico | veículo e intervalo de datas opcional | Seleciona ordens e serviços do veículo. |
| Histórico de manutenção | ordens, datas, serviços, valores e eventos | Apresenta os atendimentos em ordem cronológica. |

## 5. Comparação com a implementação

A branch `main`, na revisão indicada na seção 1, contém README e documentos do projeto. Não há código da interface, da API ou do banco de dados. O DFD e o dicionário foram comparados com os requisitos e a modelagem versionados. Os fluxos de cadastro, abertura e atualização de OS e histórico têm respaldo no E2. Autenticação, persistência e regras de consulta ainda precisam de validação em um protótipo executável.

## 6. Relatório de ajustes

Foram incluídos os fluxos de acesso e as datas de entrada e saída. O histórico passou a indicar a ligação entre veículo, ordem, serviço e mudança de status. Os depósitos representam os grupos de dados previstos na arquitetura do E2. O modelo define os campos e regras que precisam ser conferidos quando a implementação estiver disponível.

## 7. Registro no repositório

Esta página registra o diagrama de contexto, o DFD nível 0, o dicionário e o relatório de ajustes do E4 no histórico do AutoGestor.
