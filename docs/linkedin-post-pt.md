# LinkedIn Post: Semtree e a Otimização de Contexto

Seu assistente de código com IA está consumindo tokens demais e entregando respostas confusas?

Muitos desenvolvedores reclamam que, em repositórios grandes, ferramentas como Claude Code ou Cursor começam a ignorar regras, reinventar implementações ou demorar muito para responder. A causa quase sempre é a mesma: contexto inchado.

Fornecer arquivos inteiros de código fonte para a IA processar é ineficiente. A maior parte das linhas lidas são implementações auxiliares que só servem como ruído para a tarefa atual.

Para resolver esse desperdício de contexto, lancei o **Semtree**.

O Semtree é um indexador semântico que melhora a comunicação entre o seu repositório e o seu assistente de IA. Em vez de entregar arquivos brutos, ele usa análise de AST (via tree-sitter) para extrair e fornecer apenas o esqueleto crítico do código: assinaturas de funções, tipos, docstrings e contexto do Git.

Impacto prático na sua rotina:
✅ **Economia massiva de Tokens:** Redução comprovada de até 87% nos tokens de contexto.
✅ **Respostas mais rápidas:** Com menos texto para processar, o LLM responde em uma fração do tempo.
✅ **Maior Precisão:** Ao eliminar o ruído visual, a IA mantém o foco estrito nas assinaturas relevantes, melhorando as sugestões e evitando o problema de perda de contexto.
✅ **Integração MCP nativa:** Funciona de forma transparente com Claude Code, Cursor e Copilot, permitindo que a própria IA pesquise os símbolos sem exceder o orçamento estipulado.

Trabalhar com IA não exige jogar todo o repositório na tela. Exige entregar o contexto certo.

O Semtree é de código aberto e já está disponível para testes. Convido todos a conferir o repositório no GitHub.

---
**Nikolas de Hor**
Desenvolvedor | Goiânia, Brasil
Projeto: https://github.com/nikolasdehor/semtree

#SoftwareDevelopment #ArtificialIntelligence #ClaudeCode #CursorAI #OpenSource #Produtividade #Semtree
