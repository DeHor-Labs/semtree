# Instalação

## Pré-requisitos

- **Python 3.11+** (verifique com `python --version`)
- macOS, Linux ou Windows com WSL

## Métodos suportados

=== "pipx (recomendado)"

    ```bash
    pipx install semtree
    ```

    Isola o pacote em ambiente próprio. Após instalar, `semtree` fica no PATH.

=== "uv tool"

    ```bash
    uv tool install semtree
    ```

    Mais rápido que pipx, mesmo resultado.

=== "pip (em venv)"

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install semtree
    ```

=== "Como dependência"

    ```bash
    uv add semtree
    # ou
    pip install semtree
    ```

## Verificar instalação

```bash
semtree --version
semtree --help
```

## Próximos passos

- [Quickstart](quickstart.md)
- [Integrações com Claude/Cursor/Copilot](integrations.md)
