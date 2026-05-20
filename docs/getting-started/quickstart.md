# Quickstart

5 minutos para sentir o que o Semtree faz.

## 1. Indexar seu projeto

```bash
cd ~/projects/meu-projeto
semtree index .
```

Tree-sitter parseia os arquivos, extrai símbolos (funções, classes, métodos, imports) e armazena em SQLite local (`.semtree/index.db`).

## 2. Ver o contexto cirúrgico

```bash
semtree context "implementar autenticação OAuth"
```

Saída: lista de símbolos relevantes com assinaturas + docstrings, sem código inteiro.

```python
# Exemplo de saída
auth/handlers.py
class AuthHandler:
    def login(self, username: str, password: str) -> Token
    def logout(self, token: Token) -> None

auth/oauth.py
def oauth_callback(provider: str, code: str) -> User
    """Exchange OAuth code for user data."""

config.py
OAUTH_PROVIDERS: dict[str, ProviderConfig]
```

## 3. Buscar símbolos

```bash
semtree search "validate_token"
```

Retorna todos os lugares onde aparece, com contexto.

## 4. Usar via Claude Code

Após [configurar o MCP server](integrations.md):

> "Use o semtree para entender esse projeto e me ajudar a adicionar uma feature de logout"

O Claude vai chamar `index_project`, `get_context` e `search_symbols` automaticamente, recebendo só o que importa.

## Próximos passos

- [Como funciona internamente](../concepts/how-it-works.md)
- [Integrações com mais assistentes](integrations.md)
