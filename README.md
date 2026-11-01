# Desafio Técnico - Empório da Música

## 1. Ideia Inicial

Lendo o desafio e olhando os arquivos na pasta `data/` (os CSVs de produtos, pedidos, clientes, promoções e o manual de políticas da loja), pensei em resolver o problema dividindo o fluxo do agente em duas etapas bem diretas, sem complicar com vários frameworks logo de cara:

A ideia é criar funções específicas no Python pra buscar só o que interessa em cada caso:
- `get_politicas("trocas")` (ou horários, frete, pagamento, etc.) [Esse get_politicas é meio bobo, por mim enviaria a politica inteira, ela é bem pequena no system_prompt só que pra demonstrar o rag talvez vale fazer e bem digamos que economiza um pouquinho de tokens]
- `get_produtos("")`
- `get_promocoes("")`
- `get_pedidos("")`

### Como vai funcionar a conversa com a IA:

**Passo 1 (Descobrir o que buscar):**
Quando o cliente manda uma mensagem, inicialmente mando pra IA um prompt explicando:
> "Você é o Hugo Santos, vendedor da loja Empório da Música, seu cliente mandou tal mensagem, responda apenas com as funções que vamos utilizar..."

**Passo 2 (Pegar os dados e montar a resposta pro usuário):**
Depois que o Python roda essas funções e pega os dados reais dos arquivos, envio um segundo prompt:
> "Você é o Hugo Santos, vendedor da loja Empório da Música, seu cliente mandou tal mensagem. Responda apenas com os dados para utilizar (retornados da função), que são esses: [...]"

Assim a IA não inventa preço, não inventa regra de troca e responde só em cima do que as funções retornaram (fazendo o papel do RAG + Function Calling na unha, com total controle do que entra e sai, eu posso usar o SDK do gemini pra fazer o Function Calling real dando os 2 passos em 1, mas sei lá acho que vou manter assim por hora).

Tenho que lembrar de colocar o historico da conversa tbm

---

## 2. Pontos de atenção que vi até agora

Dando uma olhada nos CSVs e no manual de políticas antes de começar a codar, já deu pra notar algumas coisas que as nossas funções vão precisar tratar:
- **Promoções (`promotions.csv`):** Tem várias promoções lá, mas a maioria está com `is_active = 0`. A função `get_promocoes` vai precisar checar isso pra não dar desconto que já expirou. Tbm fala que o desconto de 5% no PIX não acumula com promoção.
- **Produtos (`products.csv`):** Tem produto sem estoque (`stock_quantity = 0`), produto descontinuado (`discontinued`) e produto chegando (`coming_soon`). Também tem uns produtos (tipo alguns baixos e teclados) onde o nome fala uma marca e a descrição fala outra (Real não sei como eu posso corrigir isso, mas é um erro de cadastro, então vou tratar como responsabilidade da loja e não minha e so manter a parada funcionando).
- **Escopo da loja (`politicas_da_loja.md`):** A loja só vende instrumentos musicais. Não vende acessórios (cordas, palhetas, cabos, cases, pedais, amplificadores). Tenho que ter um bom prompt pra IA não responder qualquer coisa e tallz


---

## 3. Base do chat do gemini

Antes de mexer nos dados e nas funções, fiz a primeira parte só pra ter a base rodando: um chat simples no terminal usando `input()` do Python conectado na API do Gemini usando o SDK, pq ai se eu quiser usar o function calling em breve dá.

- Coloquei um `SYSTEM_PROMPT` inicial bem simples só pra testar a persona do vendedor da Empório da Música.

---

## 4. Próximos Passos

- Montar o esquema dos 2 prompts (Passo 1 decidindo quais funções chamar e Passo 2 respondendo com os dados).
- Começar a codar as funções `get_politicas`, `get_produtos`, `get_promocoes` e `get_pedidos`.