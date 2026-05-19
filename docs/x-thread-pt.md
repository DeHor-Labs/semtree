# X Thread: Semtree e o Contexto para IAs 🌳🚀

1/7 Você já percebeu que quanto mais arquivos você joga no Claude Code ou Cursor, mais confusa a IA fica? Colar texto cru de arquivos destrói o foco do modelo e consome todos os seus tokens. 🧵

2/7 O problema não é a IA, é o ruído. Se você precisa alterar uma rota, o assistente não precisa ler 500 linhas de métodos utilitários, apenas as assinaturas e as docstrings importam. É aqui que entra o **Semtree**.

3/7 O Semtree é uma ferramenta que usa tree-sitter para indexar seu projeto (Python, TS, Go, Rust) e extrair apenas o esqueleto semântico do código. Ele transforma milhares de linhas cruas em um mapa limpo.

4/7 O resultado prático? Uma redução de até 87% no uso de tokens contextuais. Menos tokens significa respostas muito mais rápidas, economia imediata de custos de API e zero perda de contexto (o famoso lost in the middle).

5/7 Além disso, ele inclui metadados importantes que a IA normalmente não vê, como o git blame. O modelo consegue saber quem foi o autor de uma função e quando ela foi modificada, ajudando na compreensão do projeto.

6/7 A integração é instantânea. O Semtree suporta o protocolo MCP nativamente. Com um comando, ele se conecta ao Claude Code ou Cursor e permite que a própria IA consulte os símbolos mantendo-se dentro de um orçamento de tokens seguro.

7/7 Pare de colar arquivos inteiros e comece a enviar contexto inteligente para o seu assistente. O Semtree é open source e fácil de configurar.

Feito por Nikolas de Hor em Goiânia.
Link: https://github.com/nikolasdehor/semtree

#AI #CodingAssistants #ClaudeCode #Cursor #Python #OpenSource
