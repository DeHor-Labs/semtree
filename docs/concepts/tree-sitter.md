# Por que tree-sitter

[Tree-sitter](https://tree-sitter.github.io/tree-sitter/) é um parser generator open source criado no GitHub. Substituiu o velho Atom Linter e hoje é a base do syntax highlighting do Neovim, Helix e várias IDEs.

## Vantagens

### Velocidade

Parser incremental em C: ao editar 1 caractere, ele atualiza só os nós afetados da AST. Em projetos de 100k+ linhas, isso significa indexação inicial em segundos, atualizações em milissegundos.

### Multi-linguagem com gramáticas comunitárias

Mais de 100 linguagens suportadas via gramáticas mantidas por contribuidores. O Semtree usa as principais:

- python, typescript, javascript, tsx
- go, rust, ruby, java
- c, cpp, csharp

Adicionar nova linguagem é instalar a gramática:

```bash
pip install tree-sitter-elixir
```

E registrar no `config.py`. Sem código novo.

### Estrutural, não texto

LSPs entendem semântica completa (imports cruzados, type checking). Tree-sitter entende **estrutura**: "isso é uma função, isso é uma classe, isso é um import". Suficiente para extrair símbolos sem precisar do compilador.

### Sem dependências de runtime

Para parsear Python, o Semtree não precisa de um interpretador Python no PATH. Tree-sitter parseia o arquivo via gramática, ponto. Indexação portátil.

## Alternativas consideradas

### Por que não LSP

- Cada linguagem precisa de servidor próprio (pyright, gopls, rust-analyzer)
- Servidores são pesados (centenas de MB de RAM cada)
- Setup complexo (precisa de Node, runtimes)
- Lentidão acumulada em projetos grandes

### Por que não ast (Python stdlib)

- Só funciona pra Python
- Não tem versão incremental
- Não tem suporte a queries declarativas

### Por que não regex

- Frágil em código complexo
- Não entende escopo (função dentro de classe, etc)
- Cobertura ruim em linguagens com sintaxe rica

## Como usamos

O indexer do Semtree usa **queries declarativas** do tree-sitter:

```scheme
; Captura definições de função em Python
(function_definition
  name: (identifier) @name
  parameters: (parameters) @params
  body: (block) @body
) @function

; Captura classes
(class_definition
  name: (identifier) @name
  superclasses: (argument_list)? @bases
  body: (block) @body
) @class
```

Essas queries são compiladas uma vez e aplicadas em cada arquivo. Resultado: símbolos com posição (linha início, linha fim), nome, assinatura, docstring.

Veja `src/semtree/indexer/queries/` para todas as queries por linguagem.
