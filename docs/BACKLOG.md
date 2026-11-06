# Backlog inicial

Estas propostas podem ser copiadas para GitHub Issues. A numeração expressa uma
ordem sugerida, não IDs reais do GitHub.

## 1. Validar o workflow em um repositório real

**Objetivo:** confirmar gatilho, permissões e criação/atualização da PR.

**Aceite:** uma Issue de teste gera nota, manifest e MOC; rerun não cria diff;
logs não expõem conteúdo sensível ou token.

## 2. Adicionar JSON Schema para objetos semânticos

**Objetivo:** definir `Concept`, `Technology`, `Pattern`, `Relationship`,
`Evidence` e `Finding`.

**Aceite:** schemas versionados, exemplos válidos/inválidos e testes locais.

## 3. Extrair notas atômicas com revisão humana

**Objetivo:** transformar propostas estruturadas em Markdown sob `20-notes`.

**Aceite:** IDs estáveis, aliases, links à fonte e nenhuma sobrescrita da captura.

## 4. Resolver entidades e aliases

**Objetivo:** unificar grafias como `OTel` e `OpenTelemetry`.

**Aceite:** tabela de aliases revisável, colisões reportadas e links migráveis.

## 5. Detectar duplicatas exatas e próximas

**Objetivo:** alertar antes de criar nota redundante.

**Aceite:** hash para igualdade, métrica documentada para similaridade e nenhum
merge automático destrutivo.

## 6. Verificar referências

**Objetivo:** separar referência declarada, acessível e tecnicamente verificada.

**Aceite:** estados explícitos, timestamp da checagem e falhas sem remover URLs.

## 7. Implementar SQLite FTS5

**Objetivo:** busca textual local reconstruível.

**Aceite:** índice fora da fonte canônica, comando rebuild e filtros por campo.

## 8. Implementar embeddings opcionais

**Objetivo:** busca semântica e sugestões de conexão.

**Aceite:** provedor configurável, cache por hash, exclusão de conteúdo privado e
funcionamento do vault sem embeddings.

## 9. Modelar relações tipadas

**Objetivo:** registrar `integra_com`, `depende_de`, `implementa` e `substitui`.

**Aceite:** vocabulário versionado, proveniência por aresta e validação de IDs.

## 10. Projetar o grafo para Neo4j

**Objetivo:** habilitar consultas arquiteturais sem mover a fonte de verdade.

**Aceite:** exportação idempotente e recriação completa a partir do vault.

## 11. Detectar contradições e obsolescência

**Objetivo:** comparar findings sobre a mesma entidade ao longo do tempo.

**Aceite:** alertas citam ambas as fontes e nunca resolvem divergências sozinhos.

## 12. Eliminar conflitos de índices concorrentes

**Objetivo:** evitar que duas PRs de ingestão disputem manifest e MOCs.

**Aceite:** teste com duas ingestões paralelas e reconciliação determinística sem
perda de entradas.

## 13. Criar CLI de consulta e manutenção

**Objetivo:** comandos `ingest`, `search`, `rebuild`, `validate` e `doctor`.

**Aceite:** help, códigos de saída estáveis e testes em Linux/macOS/Windows.

## 14. Expor servidor MCP somente leitura

**Objetivo:** permitir que agentes pesquisem fontes e relações com citações.

**Aceite:** respostas incluem paths/IDs, limites de acesso e nenhuma mutação por
padrão.

## 15. Definir integração com Code Intelligence

**Objetivo:** ligar conceitos e decisões a repositórios, componentes e
dependências sem acoplar os produtos.

**Aceite:** contrato versionado, IDs externos opacos e exemplo ponta a ponta.
