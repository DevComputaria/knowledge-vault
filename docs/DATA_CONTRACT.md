# Contrato de dados

## Nota-fonte

Cada Issue possui um ID estável `gh-issue-<número>` e uma nota em
`vault/10-sources/github`. O path criado na primeira ingestão é preservado em
reprocessamentos para não quebrar links.

Campos obrigatórios do frontmatter:

| Campo | Tipo | Semântica |
| --- | --- | --- |
| `id` | string | identidade estável da captura |
| `title` | string | título revisável |
| `kind` | string | sempre `research-source` neste schema |
| `domain` | slug | domínio normalizado |
| `tags` | lista | tags hierárquicas normalizadas |
| `ai_provider` | string | provedor declarado pelo autor |
| `source_issue` | inteiro | número da Issue |
| `source_url` | URL/string | endereço de proveniência |
| `created` | data ISO | data original da Issue |
| `status` | enum | `captured` no MVP |
| `evidence_status` | enum | `unverified` no MVP |

## Manifest

`data/manifest.json` usa `schema_version: 1` e uma lista `sources`. Cada item
repete os metadados necessários para reconstruir MOCs. Consumidores devem
rejeitar versões desconhecidas em vez de adivinhar compatibilidade.

## Contrato futuro de enriquecimento

Objetos semânticos terão ID, tipo, nome canônico, aliases, links às fontes e
status de revisão. Uma `Evidence` registra referência e verificação; um
`Finding` registra afirmação, evidências, confiança e validade temporal. Uma
`Relationship` terá sujeito, predicado, objeto, fonte e status. Saída de IA é
sempre proposta, nunca evidência verificada por si só.
