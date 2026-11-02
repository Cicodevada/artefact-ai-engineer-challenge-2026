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

## 4. Montando o Prompt 1

Agora substituí o prompt genérico pelo `PROMPT_PASSO_1`. A ideia dele é simples: a IA recebe o histórico da conversa até o momento, olha a última mensagem do cliente e ela só devolve um JSON dizendo quais funções o nosso código Python precisa rodar e com qual parâmetro:
- `get_politicas(topico)`
- `get_produtos(categoria_id)`
- `get_promocoes(termo_busca)`
- `get_pedidos(identificador)`

Usei `temperature=0.0` e `response_mime_type="application/json"` na config do Gemini nesse Passo 1 pra garantir que ele não invente moda nem mande texto fora do padrão JSON na hora do Python fazer o `json.loads()`.

Uma coisa que identifiquei, se eu falar apenas "Oi tudo bem" ele chamaria função vazia e iria pro prompt 2 ainda, acho que ele pode ter uma função de enviar mensagem até pra tipo falar "Perai que vou conferir o estoque meu consagrado" enquanto busca os dados, ou já responder direto no Passo 1 sem gastar outra chamada de API quando for só um "Oi, tudo bem?" ou alguma coisa que não precisa consultar tabela nenhuma.

Outra coisa que pensei pro `get_produtos`: ao invés de buscar produto por texto (que pode dar ruim se o cliente digitar "violões" no plural ou errar o nome), criei a função `get_categorias()` no `funcoes.py` que lê o `categories.csv` e já injeta direto no `PROMPT_PASSO_1` (`... - Categorias disponíveis: + get_categorias() + ...`). Assim a IA sempre passa o ID da categoria pro `get_produtos("5")`, e caso a loja adicione novas categorias na tabela a IA já puxa automático sem precisar ficar mexendo no prompt

---

## 5. Criando as funções (`funcoes.py`) e o Passo 2

Criei o `funcoes.py` lendo os CSVs direto com a biblioteca nativa `csv` do Python:
- `get_politicas`: Como o manual de políticas é pequeno, deixei retornando o `.md` inteiro quando a IA pede pra consultar política, assim não corre risco de cortar alguma regra importante pela metade.
- `get_categorias`: Puxa os IDs, nomes e descrições do `categories.csv` pra montar o prompt dinamicamente.
- `get_produtos`: Filtra os produtos pelos IDs de categoria que a IA pediu.
- `get_promocoes`: Puxa as promoções e já cruza com o `products.csv` pra colocar o nome do produto junto (`product_name`) e facilitar pra IA entender de qual instrumento é aquela promoção.
- `get_pedidos`: Busca pelo ID do pedido, código de rastreio, nome, email ou telefone do cliente, e já junta os dados do cliente (`customers.csv`) e os itens comprados (`order_items.csv` + `products.csv`).

Depois fechei o `PROMPT_PASSO_2`: quando o Passo 1 chama alguma função de busca, o Python pega o dicionário com os retornos, joga pro Passo 2 junto com o histórico da conversa e pede pra IA responder ao cliente usando só aqueles dados.

Um detalhe que percebi testando foi a continuidade da conversa: em todas as mensagens ele tava respondendo "Fala, tudo bem? Aqui é o Hugo". Pra resolver isso, passei a enviar o horário (`datetime`) em todas as mensagens do histórico e coloquei uma regra nos dois prompts falando pra ele só se apresentar se for a primeira mensagem da conversa ou se já tiver passado muito tempo.

---

## 6. Como rodar o projeto

1. Clone o repositório e entre na pasta do projeto.
2. Crie um ambiente virtual (opcional) e instale as dependências:
```bash
pip install -r requirements.txt
```
3. Crie um arquivo `.env` na raiz do projeto (baseado no `.env.example`) e coloque sua chave da API do Google Gemini:
```env
GEMINI_API_KEY=sua_chave_aqui
```
4. Execute o chat no terminal:
```bash
python main.py
```

---

## 7. Limitações conhecidas e o que eu faria com mais tempo

- **Histórico em memória:** Atualmente o histórico da conversa fica salvo na lista `historico` enquanto o `main.py` está rodando. Se fechar o script, a conversa zera. Com mais tempo, salvaria o histórico em um arquivo JSON ou banco SQL separado por cliente/sessão.
- **Volume de dados nos CSVs:** Como o catálogo atual da loja nos CSVs tem poucos produtos por categoria, mandar todos os produtos da categoria escolhida pro Passo 2 funciona super bem e não permite que a IA perca nenhum item. Se a loja crescesse pra milhares de produtos na mesma categoria, eu passaria esses CSVs pra um banco SQLite/PostgreSQL e deixaria a função filtrar também por faixa de preço (`preco_max`, `preco_min`) direto na query.
- **Inconsistência nos dados de cadastro:** Alguns produtos na tabela `products.csv` têm divergência entre o título e a descrição (ex: baixo com nome Music Man e descrição falando Fender). Mantive o agente lendo os dados originais da loja, mas num cenário real criaria uma rotina de validação/limpeza do catálogo junto com a equipe da loja.

---

## 8. Uso de Assistentes de IA

Utilizei assistente de IA (Cico Coding https://cico.diy) que foi desenvolvido por mim mesmo, como parceiro pra discutir a arquitetura, revisar regras de negócio escondidas nos CSVs, estruturar os textos dos prompts e agilizar a escrita do boilerplate em Python, mantendo toda a decisão da lógica em 2 passos, criação das funções (`enviar_mensagem`, `get_categorias`, filtros por ID) e ajustes de comportamento na minha mão.