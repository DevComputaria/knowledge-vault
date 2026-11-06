# Segurança

## Modelo de ameaça

Título, corpo, labels, URLs e anexos de Issues são entrada não confiável. O
pipeline não deve interpolar esses valores em comandos shell, expressões do
workflow ou nomes de branch. O MVP entrega o payload como arquivo JSON ao
Python e usa o número inteiro da Issue nos identificadores.

## Controles implementados

- permissões explícitas e mínimas no workflow;
- Actions de terceiros fixadas por SHA e anotadas com a versão correspondente;
- processamento apenas da label exata `knowledge/ready`;
- nenhuma execução de conteúdo da Issue;
- escrita dentro de paths construídos por slugs normalizados;
- escrita atômica de notas, manifest e MOCs;
- PR de revisão antes de publicar na branch principal;
- proveniência e estado `unverified` visíveis na nota.

## Configuração recomendada do repositório

Proteja `main`, exija ao menos uma revisão, bloqueie force pushes, habilite
secret scanning e análise de dependências e restrinja quem pode aplicar a label
`knowledge/ready`. Revise periodicamente os SHAs das Actions antes de atualizar.

O projeto não inclui um secret scanner próprio. Não cole credenciais, tokens,
dados pessoais ou material confidencial nas Issues. Se um segredo for
publicado, revogue-o antes de limpar o histórico.

## Relato de vulnerabilidades

Não publique detalhes exploráveis numa Issue pública. Use o canal privado de
security advisories do repositório GitHub.
