# CLI

`semtree` é a única binary do projeto. Todos os comandos abaixo são subcomandos.

## Comandos principais

### `semtree index <path>`

Indexa um projeto.

```bash
semtree index .                 # projeto atual
semtree index ~/code/meu-app    # projeto específico
semtree index . --force         # reconstrói do zero
```

Cria `.semtree/index.db` na raiz do projeto. Reuse a indexação em runs subsequentes (incremental).

### `semtree context <query>`

Gera contexto cirúrgico para uma query.

```bash
semtree context "implementar paginação"
semtree context "como funciona auth" --limit 10
semtree context "validar input" --format json
```

Saída padrão: lista de símbolos relevantes com assinatura + docstring. `--format json` para uso programático.

### `semtree search <pattern>`

Busca símbolos por nome exato ou padrão.

```bash
semtree search "validate_token"
semtree search "Auth*"               # wildcard
semtree search "login" --kind function
```

`--kind` filtra por tipo: `function`, `class`, `method`, `constant`.

### `semtree mcp`

Inicia servidor MCP (stdio). Use através de cliente MCP (Claude, Cursor, etc).

```bash
semtree mcp                      # stdio padrão
semtree mcp --transport http     # HTTP transport
```

## Comandos utilitários

### `semtree stats`

Estatísticas do índice atual.

```bash
semtree stats
# Symbols:     5,234
# Functions:   2,103
# Classes:     412
# Languages:   python (4,521), typescript (713)
# Size:        2.3 MB
```

### `semtree clean`

Remove o índice. Útil quando o projeto muda muito.

```bash
semtree clean       # remove .semtree/
semtree clean -y    # sem confirmação
```

## Configuração

Variáveis de ambiente:

| Variável | Default | Descrição |
|----------|---------|-----------|
| `SEMTREE_INDEX_PATH` | `.semtree` | Diretório do índice |
| `SEMTREE_LANGUAGES` | auto-detect | Lista CSV de linguagens (ex: `python,typescript`) |
| `SEMTREE_MAX_FILE_SIZE` | `1048576` | Tamanho máximo de arquivo (1MB default) |
| `SEMTREE_LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## Casos de uso comuns

### Pre-commit hook

Reindexa antes de cada commit:

```bash
# .git/hooks/pre-commit
#!/bin/sh
semtree index . --quiet
```

### CI

Verifica que o índice está atualizado:

```yaml
- name: Re-index for review tools
  run: |
    pip install semtree
    semtree index .
```

### Integração programática

```bash
# Pega contexto e passa pro Claude via API
context=$(semtree context "$task" --format json)
claude --tools <(echo "$context") "implemente"
```
