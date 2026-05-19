# Claude Code Integration

Semtree can run as an MCP server for Claude Code. The MCP tools let Claude
index the project, search symbols, and request task-specific context before
editing code.

## Install

```bash
pip install "semtree[all]"
cd /path/to/your/project
semtree index
semtree setup --target claude
```

Restart Claude Code after setup so it reloads `.claude/mcp.json`.

## Manual MCP config

If you prefer to create the config yourself, add this to `.claude/mcp.json`:

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

## Available tools

- `index_project`: index or re-index the repository.
- `get_context`: return token-budgeted context for a task query.
- `search_symbols`: search indexed functions, classes, methods, constants, and types.

## Example queries

Ask Claude Code to use Semtree before implementation:

```text
Use semtree to get context for "add rate limiting to the login endpoint", then implement the change.
```

```text
Use semtree search_symbols to find payment retry code and summarize the relevant files.
```

```text
Use semtree get_context with a 4000 token budget for "refactor invoice generation".
```

## CLI fallback

When MCP is unavailable, run the same retrieval manually:

```bash
semtree context "add rate limiting to the login endpoint" --budget 4000
semtree search "PaymentService" --json
```
