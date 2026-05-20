# Servidor MCP

O Semtree expõe três tools via MCP (Model Context Protocol) para uso por agentes de IA.

## Tools registradas

### `index_project`

Indexa um projeto pelo path.

```json
{
  "name": "index_project",
  "arguments": {
    "path": "/Users/nikolas/code/meu-app",
    "force": false
  }
}
```

Retorna estatísticas do índice criado (símbolos por tipo, linguagens, tempo de indexação).

### `get_context`

Gera contexto otimizado para uma query.

```json
{
  "name": "get_context",
  "arguments": {
    "query": "implementar logout no endpoint /auth",
    "limit": 10
  }
}
```

Retorna símbolos relevantes ordenados por score BM25.

### `search_symbols`

Busca por nome de símbolo.

```json
{
  "name": "search_symbols",
  "arguments": {
    "pattern": "AuthHandler",
    "kind": "class"
  }
}
```

## Setup do cliente

Veja [Integrações](getting-started/integrations.md) para configurar Claude Desktop, Cursor, Codex.

## Transport

Por padrão usa **stdio** (padrão MCP, ideal para clientes desktop).

Para HTTP (útil em CI ou ambientes containerizados):

```bash
semtree mcp --transport http --port 8000
```

Endpoint MCP-compatível em `http://localhost:8000/mcp`.

## Workflow tipico

Em uma conversa com Claude:

1. Usuário: "ajude a refatorar a função login"
2. Claude chama `index_project(".")` se ainda não indexado
3. Claude chama `get_context("refatorar login")` para entender a função e suas dependências
4. Claude lê só os símbolos retornados (200-500 tokens)
5. Resposta cirúrgica, sem o ruído de arquivos inteiros

Tudo isso acontece automaticamente: você só faz a pergunta em linguagem natural.
