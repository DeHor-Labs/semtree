# Cursor Integration

Semtree gives Cursor a compact map of the codebase before a chat or agent task.
Use the MCP server when your Cursor version supports MCP, or paste CLI context
into chat as a fallback.

## Install

```bash
pip install "semtree[all]"
cd /path/to/your/project
semtree index
semtree setup --target cursor
```

This writes `.cursor/mcp.json` with a `semtree` server entry.

## Manual MCP config

```json
{
  "mcpServers": {
    "semtree": {
      "command": "semtree-mcp",
      "args": [],
      "env": {
        "SEMTREE_ROOT": "/path/to/your/project"
      }
    }
  }
}
```

Restart Cursor after changing MCP config.

## Suggested workflow

1. Run `semtree index` after large branch changes.
2. Ask Cursor Agent to call `get_context` before editing.
3. Keep the token budget small for focused changes and larger for refactors.

Example prompt:

```text
Use semtree get_context for "move auth checks into middleware" with a 5000 token budget, then update the relevant files.
```

CLI fallback:

```bash
semtree context "move auth checks into middleware" --budget 5000 > /tmp/semtree-context.md
```

Paste `/tmp/semtree-context.md` into Cursor chat before asking for the edit.
