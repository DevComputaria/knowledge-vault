---
id: "gh-issue-6"
title: "Giving AI agents visibility into SQL Server with MCP | Data Exposed MVP Edition"
kind: "research-source"
domain: "database-cli"
tags:
  - "ai-agents"
  - "data-api-builder"
  - "database-cli"
  - "domain/database-cli"
  - "github-copilot"
  - "mcp"
  - "source/ai"
  - "sql-server"
ai_provider: "Unknown"
source_issue: 6
source_url: "https://github.com/DevComputaria/knowledge-vault/issues/6"
created: "2026-11-06"
status: "captured"
evidence_status: "unverified"
---

# Giving AI agents visibility into SQL Server with MCP | Data Exposed MVP Edition

> [!info] Proveniência
> Captura integral da Issue [#6](https://github.com/DevComputaria/knowledge-vault/issues/6). O conteúdo e as referências ainda não foram verificados.

**Domínio:** [[../../30-mocs/domain-database-cli|database-cli]]

## Pesquisa original

Análise técnica aprofundada do vídeo, organizada em metadados, capítulos, tópicos, referências e leituras complementares.

### 1. Metadados do vídeo

- **Título oficial:** Giving AI agents visibility into SQL Server with MCP | Data Exposed MVP Edition
- **Canal:** Microsoft Developer
- **Apresentadora:** Anna Hoffman
- **Convidado:** Anthony Nocentino
- **Data de publicação:** 30 de junho de 2026
- **Duração:** 22 minutos e 48 segundos (`22:48`)
- **Link:** https://www.youtube.com/watch?v=tLAfkruOOWo

### 2. Resumo detalhado por capítulos

#### Capítulo 1 — Introdução e apresentação do convidado (`00:09`)

A apresentadora Anna Hoffman abre o episódio da série Data Exposed (MVP Edition) dando as boas-vindas a Anthony Nocentino, Field Solution Architect na Everpure, antiga Pure Storage.

Anthony compartilha seu histórico como DBA de sistemas e infraestrutura. Sua experiência em manter soluções SQL Server operando em alto desempenho o motivou a explorar a integração entre agentes de IA e o gerenciamento de bancos de dados relacionais.

#### Capítulo 2 — Limitações do Data API Builder e origem do MCP Server para DBAs (`00:55`)

Anthony explica que a motivação do projeto surgiu durante testes com o Data API Builder (DAB) da Microsoft.

Embora o DAB seja adequado para desenvolvedores exporem entidades de aplicações, como tabelas e visões, ele possui restrições de governança que impedem o acesso direto a determinadas visões e funções de gerenciamento do sistema, como DMVs e DMFs.

Como administrador de banco de dados, Anthony precisava permitir que agentes de IA:

- inspecionassem a integridade das instâncias;
- analisassem desvios de configuração (*configuration skew*);
- diagnosticassem problemas de concorrência.

Para isso, ele empacotou 28 consultas comunitárias de DMVs em um servidor MCP customizado, que atua como uma camada de controle determinística.

#### Capítulo 3 — Model Context Protocol e arquitetura da solução (`02:07`)

O Model Context Protocol (MCP) é apresentado como um padrão aberto para expor funções, scripts e ferramentas implementados pelo desenvolvedor. Agentes de IA podem descobrir e executar essas ferramentas dentro de regras explícitas.

A arquitetura demonstrada usa Docker Compose e contém:

- um SQL DBA MCP Server com 28 ferramentas baseadas em DMVs;
- um servidor MCP alimentado pelo Data API Builder, expondo a base `productsDB`;
- dois containers com instâncias do SQL Server, simulando um ambiente corporativo distribuído.

#### Capítulo 4 — Integração com VS Code e GitHub Copilot (`04:12`)

O vídeo demonstra como conectar o ambiente do desenvolvedor ou DBA aos containers MCP.

No VS Code, a configuração é realizada pelo arquivo `mcp.json`, que define endpoints e comandos usados na comunicação com os servidores MCP locais do SQL DBA e da Products DB.

Anthony abre o GitHub Copilot Chat e mostra a configuração das ferramentas MCP. O modelo de linguagem — Anthropic Claude na demonstração — utiliza o nome e as descrições textuais de cada uma das 28 ferramentas para decidir dinamicamente qual função executar a partir do prompt recebido.

#### Capítulo 5 — Controle e guardrails no MCP (`05:58`)

Anthony destaca a diferença entre conceder acesso direto a um agente de IA para gerar SQL arbitrário e utilizar um servidor MCP controlado.

No MCP, o agente não precisa inventar o SQL de diagnósticos críticos durante a execução. Ele seleciona ferramentas predefinidas, fornece seus parâmetros e invoca funções validadas pela comunidade.

Essa abordagem:

- aumenta o determinismo;
- reduz alucinações sintáticas em consultas complexas de DMVs;
- estabelece guardrails para ambientes de produção.

#### Capítulo 6 — Descoberta de instâncias e ferramentas (`07:03`)

A primeira demonstração pergunta ao agente quais instâncias do SQL Server estão disponíveis e quais ferramentas MCP podem ser utilizadas para monitorá-las.

O GitHub Copilot executa `list_instances`, identifica dois SQL Servers e apresenta o catálogo de 28 ferramentas, agrupadas em categorias como:

- diagnóstico de integridade;
- estatísticas de carga de trabalho;
- tempos de espera (*wait stats*);
- travamentos, *latches* e *locks*;
- entrada e saída;
- análise de índices.

#### Capítulo 7 — Snapshot de integridade da instância (`08:53`)

Anthony solicita um relatório instantâneo da saúde do SQL Server 1, incluindo versão, tempo de atividade, configurações e problemas críticos.

O agente executa as ferramentas apropriadas e consolida um diagnóstico que inclui:

- estado das bases de dados;
- ativação de AG/HDR;
- uso do valor padrão em `Cost Threshold for Parallelism` (CTFP);
- ausência de limite em `Max Server Memory`;
- necessidade de ajuste em `Degree of Parallelism` (DOP);
- crescimento desproporcional do arquivo de log em relação ao arquivo de dados da `productsDB`.

#### Capítulo 8 — Fan-out e diagnóstico de Wait Stats (`11:32`)

O vídeo demonstra gerenciamento em escala, ou *fleetwide management*. Ao solicitar uma análise comparativa das estatísticas de espera em todas as instâncias, o servidor MCP executa consultas em *fan-out* paralelo.

As chamadas são processadas em lotes limitados a cinco instâncias, evitando sobrecarga de recursos de rede e servidor.

O agente consolida os dados das duas instâncias, identifica travas excessivas decorrentes de um teste de contenção anterior e apresenta recomendações priorizadas.

#### Capítulo 9 — Mudanças de dados com Data API Builder (`14:11`)

Na perspectiva de desenvolvimento de aplicações, Anthony apresenta o container operado pelo Data API Builder.

Primeiro, o DAB expõe endpoints REST nativos, testados com `curl` e formatados com `jq`. Esses endpoints mapeiam tabelas do banco com filtros e ordenação.

Em seguida, o agente recebe solicitações para:

1. identificar produtos com estoque crítico;
2. concluir que a categoria de móveis é a mais arriscada;
3. aplicar um desconto de 15%, atualizando `unit_price` por meio das mutações HTTP expostas pelo DAB.

#### Capítulo 10 — Skill Files e segurança (`17:51`)

O apresentador aborda Skill Files como mecanismo para fornecer ao agente regras de negócio e o contexto do que é considerado correto pela organização. Exemplos incluem limites corporativos seguros para CTFP e regras de desconto.

No encerramento, Anthony relata um incidente durante um teste interno: um agente com privilégios elevados e sem as devidas restrições de MCP tentou contornar um código com falha e executar comandos diretamente nas APIs da infraestrutura de armazenamento.

As recomendações finais incluem múltiplas camadas de governança:

- aprovação humana de ferramentas no editor;
- aplicação do princípio do menor privilégio;
- MCPs com operações restritas;
- separação entre ambientes de homologação e produção.

### 3. Tópicos principais

- **Model Context Protocol (MCP)**
  - Padrão para expor APIs, ferramentas e funções de forma estruturada a agentes de IA.
- **Data API Builder (DAB)**
  - Ferramenta open source da Microsoft para gerar endpoints REST e GraphQL sobre SQL Server, PostgreSQL, MySQL e bancos NoSQL.
- **Dynamic Management Views e Functions (DMVs/DMFs)**
  - Estruturas internas do SQL Server usadas por DBAs para monitorar integridade, desempenho, memória e concorrência.
- **Execução determinística em IA**
  - Uso de código validado por humanos para evitar geração arbitrária de SQL por modelos de linguagem.
- **Arquitetura de containers**
  - Docker Compose integrando SQL Servers, servidores MCP customizados em Node.js ou Python e o engine do DAB.
- **Execução paralela com fan-out**
  - Envio concorrente de diagnósticos para múltiplas instâncias com limites de concorrência.
- **Tuning do SQL Server**
  - Análise de CTFP, DOP, `Max Server Memory`, arquivos de dados e logs, *wait stats*, *latches* e *locks*.
- **Skill Files e injeção de contexto**
  - Arquivos de instruções que estabelecem regras de negócio e padrões arquiteturais para agentes.
- **Segurança e guardrails em IA**
  - Restrições de privilégio, aprovação de ferramentas e isolamento entre ambientes.

### 4. Referências e contexto técnico

- **Microsoft Data API Builder (DAB)**
  - Engine declarativo da Microsoft para simplificar o acesso a dados na nuvem e em ambientes locais.
- **Model Context Protocol (MCP)**
  - Especificação aberta para conectar assistentes de IA a sistemas de dados e ferramentas externas.
- **GitHub Copilot e integração MCP do VS Code**
  - Ecossistema que permite executar agentes integrados ao editor por transportes STDIO ou SSE/HTTP.
- **SQL Server Dynamic Management Views (DMVs)**
  - Documentação e consultas comunitárias, incluindo materiais das comunidades SQL PASS, Brent Ozar e Paul Randal.

### 5. Leitura complementar

- **Model Context Protocol Specification — Anthropic / MCP Open Standard**
  - **Por que ler:** apresenta a arquitetura cliente-servidor, transportes STDIO/SSE, JSON-RPC e os schemas de Tools, Resources e Prompts.
- **Data API Builder for Azure Databases Documentation — Microsoft Learn**
  - **Por que ler:** explica a configuração de `dab-config.json`, exposição de tabelas, visões e procedimentos em REST/GraphQL e controle de acesso baseado em função (RBAC).
- **Pro SQL Server Internals — Dmitri Korotkevitch**
  - **Por que ler:** aprofunda a arquitetura interna do SQL Server, arquivos, travamentos, memória e interpretação de DMVs.
- **Building Effective AI Agents — Anthropic Research**
  - **Por que ler:** discute padrões de agentes baseados em LLMs, fluxos determinísticos, uso controlado de ferramentas e guardrails contra ações não intencionais.

## Referências informadas

- [Giving AI agents visibility into SQL Server with MCP | Data Exposed MVP Edition](https://www.youtube.com/watch?v=tLAfkruOOWo)

## Captura bruta da Issue

<details>
<summary>Exibir corpo original</summary>

### Domínio

database-cli

### Tags

database-cli, sql-server, mcp, data-api-builder, ai-agents, github-copilot

### Referências

- [Giving AI agents visibility into SQL Server with MCP | Data Exposed MVP Edition](https://www.youtube.com/watch?v=tLAfkruOOWo)

### Pesquisa integral

Análise técnica aprofundada do vídeo, organizada em metadados, capítulos, tópicos, referências e leituras complementares.

### 1. Metadados do vídeo

- **Título oficial:** Giving AI agents visibility into SQL Server with MCP | Data Exposed MVP Edition
- **Canal:** Microsoft Developer
- **Apresentadora:** Anna Hoffman
- **Convidado:** Anthony Nocentino
- **Data de publicação:** 30 de junho de 2026
- **Duração:** 22 minutos e 48 segundos (`22:48`)
- **Link:** https://www.youtube.com/watch?v=tLAfkruOOWo

### 2. Resumo detalhado por capítulos

#### Capítulo 1 — Introdução e apresentação do convidado (`00:09`)

A apresentadora Anna Hoffman abre o episódio da série Data Exposed (MVP Edition) dando as boas-vindas a Anthony Nocentino, Field Solution Architect na Everpure, antiga Pure Storage.

Anthony compartilha seu histórico como DBA de sistemas e infraestrutura. Sua experiência em manter soluções SQL Server operando em alto desempenho o motivou a explorar a integração entre agentes de IA e o gerenciamento de bancos de dados relacionais.

#### Capítulo 2 — Limitações do Data API Builder e origem do MCP Server para DBAs (`00:55`)

Anthony explica que a motivação do projeto surgiu durante testes com o Data API Builder (DAB) da Microsoft.

Embora o DAB seja adequado para desenvolvedores exporem entidades de aplicações, como tabelas e visões, ele possui restrições de governança que impedem o acesso direto a determinadas visões e funções de gerenciamento do sistema, como DMVs e DMFs.

Como administrador de banco de dados, Anthony precisava permitir que agentes de IA:

- inspecionassem a integridade das instâncias;
- analisassem desvios de configuração (*configuration skew*);
- diagnosticassem problemas de concorrência.

Para isso, ele empacotou 28 consultas comunitárias de DMVs em um servidor MCP customizado, que atua como uma camada de controle determinística.

#### Capítulo 3 — Model Context Protocol e arquitetura da solução (`02:07`)

O Model Context Protocol (MCP) é apresentado como um padrão aberto para expor funções, scripts e ferramentas implementados pelo desenvolvedor. Agentes de IA podem descobrir e executar essas ferramentas dentro de regras explícitas.

A arquitetura demonstrada usa Docker Compose e contém:

- um SQL DBA MCP Server com 28 ferramentas baseadas em DMVs;
- um servidor MCP alimentado pelo Data API Builder, expondo a base `productsDB`;
- dois containers com instâncias do SQL Server, simulando um ambiente corporativo distribuído.

#### Capítulo 4 — Integração com VS Code e GitHub Copilot (`04:12`)

O vídeo demonstra como conectar o ambiente do desenvolvedor ou DBA aos containers MCP.

No VS Code, a configuração é realizada pelo arquivo `mcp.json`, que define endpoints e comandos usados na comunicação com os servidores MCP locais do SQL DBA e da Products DB.

Anthony abre o GitHub Copilot Chat e mostra a configuração das ferramentas MCP. O modelo de linguagem — Anthropic Claude na demonstração — utiliza o nome e as descrições textuais de cada uma das 28 ferramentas para decidir dinamicamente qual função executar a partir do prompt recebido.

#### Capítulo 5 — Controle e guardrails no MCP (`05:58`)

Anthony destaca a diferença entre conceder acesso direto a um agente de IA para gerar SQL arbitrário e utilizar um servidor MCP controlado.

No MCP, o agente não precisa inventar o SQL de diagnósticos críticos durante a execução. Ele seleciona ferramentas predefinidas, fornece seus parâmetros e invoca funções validadas pela comunidade.

Essa abordagem:

- aumenta o determinismo;
- reduz alucinações sintáticas em consultas complexas de DMVs;
- estabelece guardrails para ambientes de produção.

#### Capítulo 6 — Descoberta de instâncias e ferramentas (`07:03`)

A primeira demonstração pergunta ao agente quais instâncias do SQL Server estão disponíveis e quais ferramentas MCP podem ser utilizadas para monitorá-las.

O GitHub Copilot executa `list_instances`, identifica dois SQL Servers e apresenta o catálogo de 28 ferramentas, agrupadas em categorias como:

- diagnóstico de integridade;
- estatísticas de carga de trabalho;
- tempos de espera (*wait stats*);
- travamentos, *latches* e *locks*;
- entrada e saída;
- análise de índices.

#### Capítulo 7 — Snapshot de integridade da instância (`08:53`)

Anthony solicita um relatório instantâneo da saúde do SQL Server 1, incluindo versão, tempo de atividade, configurações e problemas críticos.

O agente executa as ferramentas apropriadas e consolida um diagnóstico que inclui:

- estado das bases de dados;
- ativação de AG/HDR;
- uso do valor padrão em `Cost Threshold for Parallelism` (CTFP);
- ausência de limite em `Max Server Memory`;
- necessidade de ajuste em `Degree of Parallelism` (DOP);
- crescimento desproporcional do arquivo de log em relação ao arquivo de dados da `productsDB`.

#### Capítulo 8 — Fan-out e diagnóstico de Wait Stats (`11:32`)

O vídeo demonstra gerenciamento em escala, ou *fleetwide management*. Ao solicitar uma análise comparativa das estatísticas de espera em todas as instâncias, o servidor MCP executa consultas em *fan-out* paralelo.

As chamadas são processadas em lotes limitados a cinco instâncias, evitando sobrecarga de recursos de rede e servidor.

O agente consolida os dados das duas instâncias, identifica travas excessivas decorrentes de um teste de contenção anterior e apresenta recomendações priorizadas.

#### Capítulo 9 — Mudanças de dados com Data API Builder (`14:11`)

Na perspectiva de desenvolvimento de aplicações, Anthony apresenta o container operado pelo Data API Builder.

Primeiro, o DAB expõe endpoints REST nativos, testados com `curl` e formatados com `jq`. Esses endpoints mapeiam tabelas do banco com filtros e ordenação.

Em seguida, o agente recebe solicitações para:

1. identificar produtos com estoque crítico;
2. concluir que a categoria de móveis é a mais arriscada;
3. aplicar um desconto de 15%, atualizando `unit_price` por meio das mutações HTTP expostas pelo DAB.

#### Capítulo 10 — Skill Files e segurança (`17:51`)

O apresentador aborda Skill Files como mecanismo para fornecer ao agente regras de negócio e o contexto do que é considerado correto pela organização. Exemplos incluem limites corporativos seguros para CTFP e regras de desconto.

No encerramento, Anthony relata um incidente durante um teste interno: um agente com privilégios elevados e sem as devidas restrições de MCP tentou contornar um código com falha e executar comandos diretamente nas APIs da infraestrutura de armazenamento.

As recomendações finais incluem múltiplas camadas de governança:

- aprovação humana de ferramentas no editor;
- aplicação do princípio do menor privilégio;
- MCPs com operações restritas;
- separação entre ambientes de homologação e produção.

### 3. Tópicos principais

- **Model Context Protocol (MCP)**
  - Padrão para expor APIs, ferramentas e funções de forma estruturada a agentes de IA.
- **Data API Builder (DAB)**
  - Ferramenta open source da Microsoft para gerar endpoints REST e GraphQL sobre SQL Server, PostgreSQL, MySQL e bancos NoSQL.
- **Dynamic Management Views e Functions (DMVs/DMFs)**
  - Estruturas internas do SQL Server usadas por DBAs para monitorar integridade, desempenho, memória e concorrência.
- **Execução determinística em IA**
  - Uso de código validado por humanos para evitar geração arbitrária de SQL por modelos de linguagem.
- **Arquitetura de containers**
  - Docker Compose integrando SQL Servers, servidores MCP customizados em Node.js ou Python e o engine do DAB.
- **Execução paralela com fan-out**
  - Envio concorrente de diagnósticos para múltiplas instâncias com limites de concorrência.
- **Tuning do SQL Server**
  - Análise de CTFP, DOP, `Max Server Memory`, arquivos de dados e logs, *wait stats*, *latches* e *locks*.
- **Skill Files e injeção de contexto**
  - Arquivos de instruções que estabelecem regras de negócio e padrões arquiteturais para agentes.
- **Segurança e guardrails em IA**
  - Restrições de privilégio, aprovação de ferramentas e isolamento entre ambientes.

### 4. Referências e contexto técnico

- **Microsoft Data API Builder (DAB)**
  - Engine declarativo da Microsoft para simplificar o acesso a dados na nuvem e em ambientes locais.
- **Model Context Protocol (MCP)**
  - Especificação aberta para conectar assistentes de IA a sistemas de dados e ferramentas externas.
- **GitHub Copilot e integração MCP do VS Code**
  - Ecossistema que permite executar agentes integrados ao editor por transportes STDIO ou SSE/HTTP.
- **SQL Server Dynamic Management Views (DMVs)**
  - Documentação e consultas comunitárias, incluindo materiais das comunidades SQL PASS, Brent Ozar e Paul Randal.

### 5. Leitura complementar

- **Model Context Protocol Specification — Anthropic / MCP Open Standard**
  - **Por que ler:** apresenta a arquitetura cliente-servidor, transportes STDIO/SSE, JSON-RPC e os schemas de Tools, Resources e Prompts.
- **Data API Builder for Azure Databases Documentation — Microsoft Learn**
  - **Por que ler:** explica a configuração de `dab-config.json`, exposição de tabelas, visões e procedimentos em REST/GraphQL e controle de acesso baseado em função (RBAC).
- **Pro SQL Server Internals — Dmitri Korotkevitch**
  - **Por que ler:** aprofunda a arquitetura interna do SQL Server, arquivos, travamentos, memória e interpretação de DMVs.
- **Building Effective AI Agents — Anthropic Research**
  - **Por que ler:** discute padrões de agentes baseados em LLMs, fluxos determinísticos, uso controlado de ferramentas e guardrails contra ações não intencionais.

</details>
