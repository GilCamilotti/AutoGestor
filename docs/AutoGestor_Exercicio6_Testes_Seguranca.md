# AutoGestor 1.0 — Testes, segurança e apresentação

## Escopo da entrega

Versão operacional local em Python e SQLite. Cadastra clientes e veículos, abre ordens de serviço (OS), lança serviços, soma valores, controla o status e consulta o histórico. A conclusão registra a data e hora de saída no histórico. A interface web, a API e os perfis permanecem no plano evolutivo do E5.

## Plano de testes

| ID e nível | Pré-condição e ação | Resultado esperado | Evidência |
|---|---|---|---|
| TU-01 · Unidade | Normalizar placas clássica e Mercosul e uma entrada com ß. | Aceitar os formatos válidos e rejeitar o caractere fora do alfabeto permitido. | Dois testes passaram. |
| TU-02 · Unidade | Converter 100,05 e entradas de valor inválidas. | Obter 10005 centavos e rejeitar valores fora do formato. | Aprovado. |
| TI-01 · Integração | Tentar inserir veículo sem cliente e repetir a mesma placa. | O SQLite rejeita os registros inválidos. | Aprovado. |
| TS-01 · Sistema | Abrir OS, registrar dois serviços, concluir e consultar em outro processo. | Total de R$ 110,30, data de saída e histórico em ordem. | Aprovado. |
| TS-02 · Sistema | Tentar concluir sem serviço e saltar diretamente de Aberta para Concluída. | A transição é rejeitada e o histórico não muda. | Aprovado. |
| TS-03 · Sistema | Abrir uma base no esquema 0.1 e atualizar uma ordem existente. | A OS continua acessível e pode receber novos eventos. | Aprovado. |
| TA-01 · Aceitação | Demonstrar cadastro, abertura, lançamento, conclusão e consulta à dupla ou ao avaliador. | A pessoa responsável confirma que o histórico e o total atendem ao fluxo proposto. | Roteiro de demonstração. O teste TS-01 verifica os mesmos critérios técnicos. |

A execução foi feita com `python -m unittest discover -s tests -v`. O [log da execução](evidencia-e6.txt) registra 7 testes aprovados.

## Defeito encontrado e corrigido

**BUG-01 · Conversão indevida de caracteres na placa.** Na versão 0.1, a validação convertia para maiúsculas antes da checagem. A chamada `plate("aß1234")` devolvia `ASS1234` e aceitava uma placa diferente da digitada. A versão 1.0 verifica o conjunto de caracteres antes da conversão. O teste unitário de regressão confirma a rejeição dessa entrada.

## Segurança

| Tema | Aplicação no AutoGestor 1.0 |
|---|---|
| Dados pessoais | Nome, telefone e e-mail são pessoais. Placa e histórico tornam-se identificáveis quando vinculados ao proprietário. Use registros fictícios na demonstração. |
| Autenticação | O acesso ao terminal e ao arquivo depende da conta local do sistema operacional. A aplicação local não mantém contas nem senhas. |
| Autorização | Qualquer pessoa com acesso de escrita ao arquivo pode alterá-lo. Uma versão compartilhada exige autorização por perfil e por vínculo com a OS. |
| Entradas e persistência | A aplicação valida os campos essenciais, usa parâmetros nas consultas e ativa chaves estrangeiras. As transições são verificadas antes de gravar os eventos. |
| Segredos | A versão não usa tokens ou chaves de serviços externos. O arquivo do banco fica fora do Git. |
| Dependências | A execução usa a biblioteca padrão do Python, incluindo SQLite. A manutenção depende de versões atualizadas do Python e do sistema operacional. |
| Riscos residuais | O arquivo SQLite não tem criptografia própria. Permissões do sistema, armazenamento protegido e cópias restritas são necessários para uso com dados reais. |

## Roteiro de apresentação

1. Apresentar o problema e explicar como cliente, veículo e OS se relacionam.
2. Abrir uma OS fictícia, lançá-la como Em andamento e demonstrar a regra que bloqueia a conclusão sem serviço.
3. Registrar um serviço, concluir e consultar o total, as datas e a sequência de status.
4. Mostrar a execução dos testes, o bug corrigido e explicar como o arquivo SQLite é protegido no ambiente local.
5. Mostrar o CHANGELOG e o commit da versão final.
