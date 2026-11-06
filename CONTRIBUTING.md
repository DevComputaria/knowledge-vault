# Contribuindo

Use Python 3.10 ou posterior e rode antes de abrir uma Pull Request:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/process_issue.py
```

Mudanças no formato persistido devem atualizar `docs/DATA_CONTRACT.md`, manter
compatibilidade ou fornecer migração e incluir testes de idempotência. Não
edite MOCs gerados para corrigir um problema de origem; corrija o manifest, a
nota ou o gerador.
