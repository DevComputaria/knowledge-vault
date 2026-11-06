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
- captura opt-in de comentários iniciados por `/knowledge`;
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
python3 scripts/process_issue.py --event tests/fixtures/comment.json --root . --comment
```

O segundo comando cria uma nota em `vault/10-sources/github`, atualiza
`data/manifest.json` e reconstrói os MOCs em `vault/30-mocs`.

Para simular outra pesquisa, copie o fixture e altere `issue.number`, título e
corpo. A execução local exige a label `knowledge/ready`; use `--allow-unready`
apenas em desenvolvimento. No GitHub, a label é aplicada automaticamente ao
abrir uma Issue.

## Uso no GitHub

1. Crie uma Issue pelo formulário **Nova pesquisa** ou com conteúdo livre.
2. O workflow adiciona `knowledge/ready` automaticamente.
3. O mesmo job executa os testes e abre/atualiza uma PR da Issue.
4. Revise o diff, referências e metadados antes do merge.
5. Abra a pasta `vault` como um vault no Obsidian.

### Complementar uma pesquisa por comentário

Depois que a Issue pai estiver publicada no vault, crie um comentário cujo
primeiro conteúdo seja o comando em uma linha própria:

```markdown
/knowledge

Conteúdo complementar da pesquisa...
```

O comentário herda domínio e tags da Issue, recebe ID estável pelo ID do
comentário e cria uma nota em `vault/10-sources/github/comments`. Editar um
comentário mantendo `/knowledge` atualiza a mesma nota em uma nova PR.
Comentários comuns, comentários em Pull Requests e comandos de autores sem
permissão de colaboração no repositório são ignorados.

O workflow usa permissões explícitas para conteúdo, Pull Requests e Issues. O
título, o corpo e os comentários são lidos de `event.json` por Python e nunca
interpolados como shell. Em produção, habilite proteção da branch e revisão
obrigatória.

## Estrutura

```text
.github/                 formulário e workflow
scripts/process_issue.py ingestão determinística
vault/10-sources/        Issues e comentários preservados por origem
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
