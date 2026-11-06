---
id: "gh-issue-1"
title: "Data API Builder (DAB) com MCP."
kind: "research-source"
domain: "uncategorized"
tags:
  - "domain/uncategorized"
  - "source/ai"
ai_provider: "Unknown"
source_issue: 1
source_url: "https://github.com/DevComputaria/knowledge-vault/issues/1"
created: "2026-11-06"
status: "captured"
evidence_status: "unverified"
---

# Data API Builder (DAB) com MCP.

> [!info] Proveniência
> Captura integral da Issue [#1](https://github.com/DevComputaria/knowledge-vault/issues/1). O conteúdo e as referências ainda não foram verificados.

**Domínio:** [[../../30-mocs/domain-uncategorized|uncategorized]]

## Pesquisa original

Estas são as referências oficiais da Microsoft sobre a parte do vídeo que usa o Data API Builder (DAB) com MCP.

- [SQL MCP Server: visão geral](https://learn.microsoft.com/en-us/azure/data-api-builder/mcp/overview): descreve o SQL MCP Server, que faz parte do DAB desde a versão 1.7. Usa RBAC e ferramentas de manipulação de dados (DML) em vez de gerar SQL livre por IA (NL2SQL), o que reforça o determinismo e os guardrails discutidos no vídeo.
- [Ferramentas DML](https://learn.microsoft.com/en-us/azure/data-api-builder/mcp/data-manipulation-language-tools): lista as 7 ferramentas expostas (`describe_entities`, `read_records`, `update_record` e outras). Também mostra como desativar ferramentas, como `delete_record`.
- [Quickstart com VS Code](https://learn.microsoft.com/en-us/azure/data-api-builder/mcp/quickstart-visual-studio-code): cobre instalação local, os transportes stdio e HTTP, o `.vscode/mcp.json` e um teste no Copilot Chat.
- [Documentação do Data API Builder](https://learn.microsoft.com/en-us/azure/data-api-builder/): reúne a CLI, a configuração, a segurança e a autenticação.
- [Quickstart do DAB com SQL Server](https://learn.microsoft.com/en-us/azure/data-api-builder/quickstart/mssql): mostra o uso com SQL Server em Docker e os endpoints REST, como no trecho do vídeo com `curl`.

Não encontrei o repositório do servidor "SQL DBA MCP" com as 28 ferramentas de DMVs que o Anthony apresenta. Ele parece ser um projeto próprio e não faz parte do DAB. Para localizá-lo, veja a descrição do vídeo no YouTube.

Quer que eu monte uma comparação entre o SQL MCP Server do DAB e um MCP customizado de DMVs, como o do vídeo?

## Referências informadas

Nenhuma referência informada.

## Captura bruta da Issue

<details>
<summary>Exibir corpo original</summary>

Estas são as referências oficiais da Microsoft sobre a parte do vídeo que usa o Data API Builder (DAB) com MCP.

- [SQL MCP Server: visão geral](https://learn.microsoft.com/en-us/azure/data-api-builder/mcp/overview): descreve o SQL MCP Server, que faz parte do DAB desde a versão 1.7. Usa RBAC e ferramentas de manipulação de dados (DML) em vez de gerar SQL livre por IA (NL2SQL), o que reforça o determinismo e os guardrails discutidos no vídeo.
- [Ferramentas DML](https://learn.microsoft.com/en-us/azure/data-api-builder/mcp/data-manipulation-language-tools): lista as 7 ferramentas expostas (`describe_entities`, `read_records`, `update_record` e outras). Também mostra como desativar ferramentas, como `delete_record`.
- [Quickstart com VS Code](https://learn.microsoft.com/en-us/azure/data-api-builder/mcp/quickstart-visual-studio-code): cobre instalação local, os transportes stdio e HTTP, o `.vscode/mcp.json` e um teste no Copilot Chat.
- [Documentação do Data API Builder](https://learn.microsoft.com/en-us/azure/data-api-builder/): reúne a CLI, a configuração, a segurança e a autenticação.
- [Quickstart do DAB com SQL Server](https://learn.microsoft.com/en-us/azure/data-api-builder/quickstart/mssql): mostra o uso com SQL Server em Docker e os endpoints REST, como no trecho do vídeo com `curl`.

Não encontrei o repositório do servidor "SQL DBA MCP" com as 28 ferramentas de DMVs que o Anthony apresenta. Ele parece ser um projeto próprio e não faz parte do DAB. Para localizá-lo, veja a descrição do vídeo no YouTube.

Quer que eu monte uma comparação entre o SQL MCP Server do DAB e um MCP customizado de DMVs, como o do vídeo?

</details>
