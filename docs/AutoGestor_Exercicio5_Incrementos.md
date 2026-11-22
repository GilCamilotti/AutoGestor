# AutoGestor — Exercício 5

## Modelo de processo

O desenvolvimento será incremental. O primeiro fluxo liga cliente, veículo e ordem de serviço. Os passos seguintes acrescentam o atendimento completo e o acesso pela web, preservando a possibilidade de testar cada entrega de forma independente.

## Plano de incrementos

| Versão | Escopo | Critério de aceite |
|---|---|---|
| 0.1.0 | Cadastro de cliente e veículo, abertura e consulta de OS no terminal, persistência SQLite. | Abrir e localizar uma OS após reiniciar o programa. |
| 0.2.0 | Serviços, mudanças de status, data de saída e histórico de manutenção. | Registrar um serviço e reconstruir o andamento de uma OS, do início à conclusão. |
| 0.3.0 | Interface web, API, perfis e autorização de consulta do cliente. | Restringir operações conforme o perfil e o vínculo com a OS. |

## Versionamento

A branch `feature/e5-mvp` registra o incremento funcional. A `main` recebe entregas integradas. O [CHANGELOG](../CHANGELOG.md) apresenta o conteúdo de cada versão. Use o histórico de commits e a área de tags do repositório para conferir os marcos publicados.

## Melhoria e verificação

A placa pode chegar com letras minúsculas, espaço ou hífen. A entrada é normalizada nos comandos de cadastro e abertura da OS. O SQLite aplica unicidade à forma normalizada. O teste no terminal confirmou a abertura de uma OS usando a mesma placa com grafias diferentes, o bloqueio de duplicata e a consulta em uma nova execução.
