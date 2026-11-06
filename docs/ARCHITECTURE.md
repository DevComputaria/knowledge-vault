# Arquitetura

## Objetivo

O Knowledge Vault converte capturas isoladas em um acervo Markdown versionado,
rastreável e progressivamente enriquecível. GitHub Issues são a porta de
entrada; Git registra revisão e histórico; o diretório `vault` é a fonte
canônica publicada; Obsidian é uma interface local, não uma dependência do
pipeline.

## Fluxo do MVP

```text
Issue + knowledge/ready
          │
          ▼
evento JSON ──► validação ──► nota-fonte ──► manifest ──► MOCs
                                │                          │
                                └──────── PR de revisão ──┘

Comentário /knowledge ──► herança do pai ──► nota-comentário ──┘
```

1. Ao abrir uma Issue, o workflow adiciona automaticamente a label exata
   `knowledge/ready` e realiza a ingestão no mesmo job. Isso evita depender de
   eventos recursivos, que o `GITHUB_TOKEN` não dispara.
2. O script lê o payload JSON e valida número, título e corpo. Na abertura, a
   label acabou de ser aplicada e o payload original é aceito explicitamente;
   execuções posteriores continuam exigindo a label.
3. Os campos do Issue Form são normalizados; o corpo completo é preservado na
   nota, separado do recorte exibido como pesquisa.
4. A nota-fonte recebe ID estável `gh-issue-N`. Reprocessamento atualiza a mesma
   nota, inclusive quando o título muda.
5. O manifest é escrito atomicamente e ordenado pelo número da Issue.
6. MOCs são reconstruídos do manifest, eliminando deriva de índices manuais.
7. A mudança segue para uma PR; branch protection deve impedir merge sem revisão.

Comentários em Issues seguem o mesmo pipeline quando começam exatamente com
`/knowledge`. O pai precisa existir no manifest. A nota recebe ID
`gh-comment-N`, herda domínio e tags, aponta para a nota pai e produz backlinks
no Obsidian. Edições atualizam o mesmo path; conversas comuns e comentários em
Pull Requests não são capturados.

## Níveis de conhecimento

| Nível | Representação | Estado no MVP |
| --- | --- | --- |
| Captura | GitHub Issue ou comentário opt-in | implementado |
| Fonte | Markdown integral com proveniência | implementado |
| Conhecimento | notas atômicas tipadas | diretório e contrato planejados |
| Síntese | MOCs, Bases e relações | MOCs/Bases implementados; relações futuras |

## Decisões

### Markdown como fonte canônica

O sistema não exige banco para leitura ou portabilidade. Índices futuros
(SQLite, vetores ou grafo) serão derivados e reconstruíveis. A revisão humana
acontece em diffs comuns.

### Manifest como índice da automação

`data/manifest.json` não substitui as notas. Ele contém apenas metadados
necessários para reconstruir índices sem interpretar YAML. O schema é
versionado e uma versão desconhecida causa falha explícita.

### Separação entre fonte e interpretação

Uma captura nasce com `status: captured` e `evidence_status: unverified`.
Extrações futuras não poderão reescrever silenciosamente o texto original;
conceitos, findings e evidências terão IDs próprios e apontarão para a fonte.

### Escrita determinística

Ordenação estável, paths preservados e escrita atômica tornam o reprocessamento
idempotente. MOCs podem ser reconstruídos completamente. Para reduzir conflitos
entre PRs simultâneas, a evolução prevista é manter índices por fragmentos ou
executar um reconciliador após merge.

## Limites atuais

- não há chamada a LLM, extração semântica ou deduplicação por embeddings;
- referências são preservadas, mas não verificadas;
- o manifest compartilhado ainda pode gerar conflitos entre PRs concorrentes;
- comentários dependem de a nota da Issue pai já estar publicada;
- o workflow real deve ser validado no repositório GitHub;
- o arquivo `.base` requer uma versão do Obsidian com o plugin Bases.

## Componentes futuros

O contrato proposto para enriquecimento usa objetos `Concept`, `Technology`,
`Pattern`, `Relationship`, `Evidence` e `Finding`. A saída do modelo deverá ser
JSON validado por schema; só depois será convertida em Markdown numa PR. Busca
FTS5, vetores e motores de grafo serão projeções descartáveis do vault.
