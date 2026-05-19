# Otimizando o Contexto para IAs de Programação com Semtree

Se você usa assistentes de inteligência artificial como Claude Code, Cursor ou GitHub Copilot no seu dia a dia, provavelmente já passou por isso: você pede para a IA implementar uma nova funcionalidade, mas ela se perde no meio do caminho. A resposta demora, o código sugerido tenta reinventar a roda ou ignora padrões que já existem no seu repositório.

O problema na maioria das vezes não está na capacidade do modelo de IA, mas na forma como alimentamos o contexto dele.

## O problema do "Contexto Inchado"

Quando colamos arquivos inteiros no prompt ou deixamos que o assistente leia livremente o diretório "src", estamos cometendo um erro fundamental. Arquivos de código contêm muito "ruído": dezenas de imports que não importam para a tarefa atual, implementações detalhadas de métodos auxiliares e linhas em branco.

Isso causa dois problemas severos. Primeiro, o uso de tokens explode, encarecendo chamadas de API e esgotando limites diários. Segundo, sofremos com a degradação de atenção (o famoso "lost in the middle"). Quando a IA recebe 45.000 tokens de texto cru, ela tem muito mais dificuldade para focar nas três ou quatro assinaturas de função que realmente importam para o bug que você quer corrigir.

## A solução: Contexto Cirúrgico com Semtree

Para resolver esse gargalo, criei o **Semtree**, uma biblioteca em Python desenhada especificamente para melhorar a qualidade do contexto de assistentes de IA. 

O Semtree abandona a ideia de passar texto cru. Em vez disso, ele utiliza o *tree-sitter* para analisar a sintaxe de dezenas de linguagens (Python, TypeScript, Go, Rust, Java, entre outras) e construir um índice semântico do seu projeto. 

O que isso significa na prática? Quando você pede para o assistente "adicionar rate limiting na rota de login", o Semtree atua como um filtro inteligente. Em vez de ler todo o arquivo de autenticação, ele extrai apenas as informações cruciais:
- Assinaturas de classes e métodos
- Docstrings
- Metadados do Git (quem alterou o arquivo pela última vez e quando)

## Redução drástica de Tokens

A vantagem mais imediata do Semtree é a economia computacional. Em testes reais, substituir a leitura bruta de arquivos pelo resumo semântico do Semtree resulta em uma redução de até 87% no uso de tokens.

Por exemplo, um diretório que consumiria 45.000 tokens ao ser colado inteiramente no contexto passa a consumir cerca de 6.000 tokens com a extração focada. Essa economia permite que o modelo de IA responda muito mais rápido, reduz drasticamente seus custos com APIs pagas e mantém o modelo focado estritamente no que interessa.

## Integração nativa via MCP

Ferramentas excelentes não devem exigir fluxos de trabalho complexos. O Semtree foi projetado para operar nos bastidores. Ele implementa o protocolo MCP (Model Context Protocol) de forma nativa. 

Ao rodar um simples comando de setup no seu terminal, o Semtree configura automaticamente os arquivos necessários para o Claude Code, Cursor ou Copilot. A partir desse momento, o seu assistente de IA ganha três novas ferramentas para consultar o código de maneira estruturada, gerenciando um "orçamento de tokens" que você define.

## Conclusão

O desenvolvimento assistido por IA deixou de ser apenas sobre geração de código e passou a ser sobre gerenciamento de contexto. Entregar menos código, porém com mais relevância semântica, é o caminho para obter sugestões mais inteligentes e rápidas.

Se você está cansado de ver sua IA se perder em repositórios grandes, o Semtree oferece uma solução prática e de código aberto para organizar o caos.

---
**Sobre o autor:**
Nikolas de Hor é desenvolvedor de software em Goiânia.
Contato: nikolasdehor79@gmail.com
Link do projeto: https://github.com/nikolasdehor/semtree
