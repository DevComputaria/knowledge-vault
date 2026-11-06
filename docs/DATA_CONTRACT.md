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

## Nota de comentário

Um comentário iniciado por `/knowledge` possui ID estável
`gh-comment-<id-do-comentário>` e fica em
`vault/10-sources/github/comments`. Ele herda `domain` e `tags` da nota pai e
adiciona `source/github-comment`.

Além dos campos comuns, seu frontmatter contém:

| Campo | Tipo | Semântica |
| --- | --- | --- |
| `kind` | string | `research-comment` |
| `source_comment` | inteiro | ID imutável do comentário no GitHub |
| `parent_id` | string | ID `gh-issue-N` da pesquisa pai |
| `author` | string | login do autor no GitHub |
| `updated` | data ISO | data da última edição capturada |

Editar o comentário atualiza a mesma entrada. Remover `/knowledge` não apaga
automaticamente uma captura já publicada; exclusões exigem revisão explícita.

## Manifest

`data/manifest.json` usa `schema_version: 1` e uma lista `sources` que pode
conter Issues e comentários. Cada item repete os metadados necessários para
reconstruir MOCs. Consumidores devem
rejeitar versões desconhecidas em vez de adivinhar compatibilidade.

## Contrato futuro de enriquecimento

Objetos semânticos terão ID, tipo, nome canônico, aliases, links às fontes e
status de revisão. Uma `Evidence` registra referência e verificação; um
`Finding` registra afirmação, evidências, confiança e validade temporal. Uma
`Relationship` terá sujeito, predicado, objeto, fonte e status. Saída de IA é
sempre proposta, nunca evidência verificada por si só.
