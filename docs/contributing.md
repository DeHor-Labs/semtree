# Contribuir

Contribuições são bem-vindas. Algumas formas de ajudar:

## Como ajudar

- **Issues**: reporte bugs ou peça features em [github.com/nikolasdehor/semtree/issues](https://github.com/nikolasdehor/semtree/issues)
- **Pull requests**: fork, branch, PR
- **Novas linguagens**: adicionar gramática + queries para mais linguagens
- **Casos de uso reais**: compartilhe como você usa o Semtree

## Setup de dev

```bash
git clone https://github.com/nikolasdehor/semtree
cd semtree

# Instalar uv (https://docs.astral.sh/uv/)
curl -LsSf https://astral.sh/uv/install.sh | sh

uv sync --all-extras
```

## Comandos

```bash
# Testes
uv run pytest

# Lint + format
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Type check
uv run mypy --strict src/

# Build
uv build

# Docs locais
uv run mkdocs serve
```

## Adicionar suporte a nova linguagem

1. Instale a gramática: `uv add tree-sitter-<lang>`
2. Adicione queries em `src/semtree/indexer/queries/<lang>.scm`
3. Registre no `src/semtree/indexer/__init__.py`
4. Adicione testes em `tests/test_indexer_<lang>.py`
5. Atualize a tabela de linguagens em `docs/concepts/tree-sitter.md`

## Padrões

- PEP 8 + ruff format
- mypy --strict no código novo
- Testes pytest, cobertura mínima 80%
- Mensagens de commit em imperativo, sem AI footers
- Português pt-BR com acentos em strings/docs user-facing, inglês em código
