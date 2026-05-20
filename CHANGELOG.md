# Changelog

## [0.1.0] - 2026-05-19

### Added

- Versão inicial do Semtree
- Indexador baseado em tree-sitter para Python, TypeScript, JavaScript, Go, Rust, Ruby, Java, C, C++
- Armazenamento em SQLite local com índice FTS5 (BM25)
- CLI com comandos `index`, `context`, `search`, `mcp`, `stats`, `clean`
- Servidor MCP com tools `index_project`, `get_context`, `search_symbols`
- Suporte a transport stdio e HTTP no servidor MCP
- Benchmarks em `benchmarks/run.py`
- Exemplos de integração com Claude Code, Cursor, Codex em `examples/integrations/`

### Notas

Versão inicial focada em entregar valor para times pequenos que querem reduzir custo de tokens em interações com AI assistants. Sem dependências externas além do tree-sitter e SQLite (stdlib).
