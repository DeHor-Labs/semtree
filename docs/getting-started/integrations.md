# Integrações

O Semtree expõe-se como **servidor MCP** padrão, funcionando com qualquer cliente compatível.

## Claude Code (desktop)

Edite `claude_desktop_config.json`:

=== "macOS / Linux"

    `~/Library/Application Support/Claude/claude_desktop_config.json`

    ```json
    {
      "mcpServers": {
        "semtree": {
          "command": "semtree",
          "args": ["mcp"]
        }
      }
    }
    ```

=== "Windows"

    `%APPDATA%\Claude\claude_desktop_config.json`

    ```json
    {
      "mcpServers": {
        "semtree": {
          "command": "semtree.exe",
          "args": ["mcp"]
        }
      }
    }
    ```

Reinicie o Claude Desktop. As tools `index_project`, `get_context`, `search_symbols` aparecem disponíveis.

## Claude Code (CLI)

```bash
claude mcp add semtree semtree mcp
```

## Cursor

Settings -> MCP Servers:

```json
{
  "mcpServers": {
    "semtree": {
      "command": "semtree",
      "args": ["mcp"]
    }
  }
}
```

## GitHub Copilot (via VS Code MCP)

Se você usa o GitHub Copilot Chat com [MCP extension](https://marketplace.visualstudio.com/) habilitado, adicione no `settings.json`:

```json
{
  "mcp.servers": {
    "semtree": {
      "command": "semtree",
      "args": ["mcp"]
    }
  }
}
```

## Codex (OpenAI)

Codex CLI v0.130+ suporta MCP. Veja `examples/integrations/codex.md` no repo.

## Uso em prompts

Independente do cliente, formule o prompt assim:

> "Use o semtree para indexar esse projeto e me dar contexto sobre como fazer X"

Ou diretamente:

> "Procure no semtree todas as funções que tocam autenticação"

O assistente chama as tools certas automaticamente.
