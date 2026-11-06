# Knowledge Vault

Um segundo cérebro Markdown-first: GitHub Issues capturam pesquisas, GitHub
Actions transforma cada captura em uma nota rastreável e o Obsidian oferece a
interface de exploração.

O MVP preserva o texto original, normaliza metadados, mantém um manifesto
determinístico e reconstrói Maps of Content (MOCs). Toda ingestão abre uma Pull
Request: nenhuma interpretação é publicada sem revisão humana.

## O que já funciona

- Issue Form com campos para domínio, provedor, tags, referências e pesquisa;
- ingestão segura e idempotente de eventos `issues` do GitHub;
- notas-fonte com YAML frontmatter e proveniência;
- tags hierárquicas normalizadas e links para MOCs;
- manifesto JSON usado como índice canônico da automação;
- MOCs por domínio reconstruídos de forma determinística;
- dashboard para o plugin nativo Bases do Obsidian;
- workflow que testa, processa e cria uma PR de revisão;
- testes somente com a biblioteca padrão do Python.

Notas atômicas geradas por IA, relações tipadas, embeddings e busca híbrida
fazem parte do roadmap e ainda não são apresentados como funcionalidades do
MVP.

## Uso local

Requer Python 3.10 ou posterior.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/process_issue.py --event tests/fixtures/issue.json --root .
```

O segundo comando cria uma nota em `vault/10-sources/github`, atualiza
`data/manifest.json` e reconstrói os MOCs em `vault/30-mocs`.

Para simular outra pesquisa, copie o fixture e altere `issue.number`, título e
corpo. A ingestão exige a label `knowledge/ready`; use `--allow-unready` apenas
em desenvolvimento local.

## Uso no GitHub

1. Crie uma Issue pelo formulário **Nova pesquisa**.
2. Revise a captura e adicione a label `knowledge/ready`.
3. O workflow executa os testes e abre/atualiza uma PR específica da Issue.
4. Revise o diff, referências e metadados antes do merge.
5. Abra a pasta `vault` como um vault no Obsidian.

O workflow usa apenas `contents: write` e `pull-requests: write`. O título e o
corpo da Issue são lidos de `event.json` por Python e nunca interpolados como
shell. Em produção, habilite proteção da branch e revisão obrigatória.

## Estrutura

```text
.github/                 formulário e workflow
scripts/process_issue.py ingestão determinística
vault/10-sources/        capturas integrais e imutáveis por origem
vault/20-notes/          notas atômicas revisadas (futuro)
vault/30-mocs/           mapas de conteúdo gerados
data/manifest.json       índice da automação
docs/                    arquitetura, contratos, roadmap e backlog
tests/                   testes e fixtures
```

Consulte [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) para decisões e limites.

## Contribuição

Issues e Pull Requests são bem-vindas. Mudanças na serialização devem incluir
testes de idempotência e preservar compatibilidade com notas já publicadas.

Licenciado sob MIT.
