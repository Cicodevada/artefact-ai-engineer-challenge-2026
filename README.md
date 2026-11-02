# Technical Challenge - Empório da Música

## 1. Initial Idea

Reading the challenge and looking at the files in the `data/` folder (the CSVs for products, orders, customers, promotions, and the store's policy manual), I thought about solving the problem by splitting the agent's flow into two very straightforward steps, without overcomplicating things with a bunch of frameworks right off the bat:

The idea is to create specific functions in Python to fetch only what matters for each case:
- `get_politicas("trocas")` (or business hours, shipping, payment, etc.) [This `get_politicas` is a bit silly tbh, personally I'd just send the whole policy in the `system_prompt` since it's pretty small, but to demonstrate RAG it might be worth doing, and well, let's say it saves a tiny bit of tokens]
- `get_produtos("")`
- `get_promocoes("")`
- `get_pedidos("")`

### How the conversation with the AI is going to work:

**Step 1 (Figuring out what to fetch):**
When the customer sends a message, I initially send a prompt to the AI explaining:
> "You are Hugo Santos, a salesperson at Empório da Música, your customer sent this message, reply only with the functions we are going to use..."

**Step 2 (Getting the data and building the reply for the user):**
After Python runs those functions and grabs the real data from the files, I send a second prompt:
> "You are Hugo Santos, a salesperson at Empório da Música, your customer sent this message. Reply using only the data provided (returned by the function), which is: [...]"

This way the AI doesn't make up prices, doesn't make up exchange rules, and only replies based on what the functions returned (doing the job of RAG + Function Calling from scratch, with full control over what goes in and out. I could use the Gemini SDK to do native Function Calling doing the 2 steps in 1, but idk, I think I'll keep it like this for now).

I also have to remember to include the conversation history.

---

## 2. Things I noticed so far

Taking a look at the CSVs and the policy manual before starting to code, I already noticed a few things that our functions will need to handle:
- **Promotions (`promotions.csv`):** There are several promotions in there, but most of them have `is_active = 0`. The `get_promocoes` function will need to check this so we don't give out expired discounts. It also says that the 5% PIX discount doesn't stack with promotions.
- **Products (`products.csv`):** There are out-of-stock products (`stock_quantity = 0`), discontinued products (`discontinued`), and products arriving soon (`coming_soon`). There are also some products (like a few basses and keyboards) where the name says one brand and the description says another (I honestly don't know how I'd fix this, it's a catalog registration error, so I'll treat it as the store's responsibility and not mine, and just keep the thing working).
- **Store scope (`politicas_da_loja.md`):** The store only sells musical instruments. It doesn't sell accessories (strings, picks, cables, cases, pedals, amplifiers). I need a good prompt so the AI doesn't just answer anything and stuff.

---

## 3. Base Gemini chat

Before touching the data and the functions, I built the first part just to have the base running: a simple terminal chat using Python's `input()` connected to the Gemini API using the SDK, because then if I want to use function calling later on, it's easy.

- I put a very simple initial `SYSTEM_PROMPT` just to test the Empório da Música salesperson persona.

---

## 4. Building Prompt 1

Now I replaced the generic prompt with `PROMPT_PASSO_1`. The idea behind it is simple: the AI gets the conversation history so far, looks at the customer's last message, and only returns a JSON telling which functions our Python code needs to run and with what parameter:
- `get_politicas(topico)`
- `get_produtos(categoria_id)`
- `get_promocoes(termo_busca)`
- `get_pedidos(identificador)`

I used `temperature=0.0` and `response_mime_type="application/json"` in Gemini's config for Step 1 to make sure it doesn't get creative or send text outside the JSON format when Python runs `json.loads()` (Note: later when switching to Gemma due to free tier limits on Gemini 3.1, I removed the `response_mime_type` since Gemma doesn't support it natively in the API and handled the markdown strip in Python).

One thing I noticed: if I just say "Hi how are you", it would call an empty function and still go to Prompt 2. I figured it should have a send message function, even to say things like "Hold on, let me check the stock for you my friend" while it fetches the data, or just reply directly in Step 1 without wasting another API call when it's just a "Hi, how are you?" or something that doesn't need to query any table.

Another thing I thought about for `get_produtos`: instead of searching for a product by text (which can go wrong if the customer types "violões" in the plural or misspells the name), I created the `get_categorias()` function in `funcoes.py` that reads `categories.csv` and injects it straight into `PROMPT_PASSO_1` (`... - Categorias disponíveis: + get_categorias() + ...`). That way the AI always passes the category ID to `get_produtos("5")`, and if the store adds new categories to the spreadsheet, the AI pulls them automatically without having to touch the prompt.

---

## 5. Creating the functions (`funcoes.py`) and Step 2

I created `funcoes.py` reading the CSVs directly with Python's native `csv` library:
- `get_politicas`: Since the policy manual is small, I left it returning the whole `.md` when the AI asks to check the policies, so there's no risk of cutting an important rule in half.
- `get_categorias`: Pulls the IDs, names, and descriptions from `categories.csv` to build the prompt dynamically.
- `get_produtos`: Filters the products by the category IDs that the AI requested.
- `get_promocoes`: Pulls the promotions and cross-references them with `products.csv` to attach the product info (`product_name`, `price_brl`, `stock_quantity`, `status`) so it's easier for the AI to understand which instrument that promotion belongs to.
- `get_pedidos`: Searches by order ID, tracking code, customer name, email, or phone number, and joins the customer data (`customers.csv`) and the purchased items (`order_items.csv` + `products.csv`).

Then I wrapped up `PROMPT_PASSO_2`: when Step 1 calls any search function, Python takes the dictionary with the returned data, sends it to Step 2 along with the conversation history, and asks the AI to reply to the customer using only that data.

One detail I noticed while testing was conversation continuity: in every single message it was replying "Hey, how's it going? This is Hugo". To fix this, I started sending the timestamp (`datetime`) on every message in the history and added a rule in both prompts telling it to only introduce itself if it's the very first message of the conversation or if a lot of time has passed.

---

## 6. How to run the project

1. Clone the repository and enter the project folder.
2. Create a virtual environment (optional) and install the dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file in the project root (based on `.env.example`) and put your Google Gemini API key:
```env
GEMINI_API_KEY=your_key_here
```
4. Run the chat in the terminal:
```bash
python main.py
```

*(Interaction examples can be found in `exemplo_interacao.md`)*.

---

## 7. Known limitations and what I would do with more time

- **More info in the base prompt:** Give a bit more basic store info to the AI and tweak the prompts so that sometimes it doesn't even need to trigger the RAG, though I'd test this out to see the best balance. Because for example, right now sometimes it goes "Hold on let me check if there's a PIX discount" -> Calls Policy Function -> "Yes, there's 5%", when that could be more direct, you know? But as a prototype I think it's solid.
- **In-memory history:** Right now the conversation history is saved in the `historico` list while `main.py` is running. If you close the script, the conversation resets. With more time, I would save the history in a JSON file or SQL database separated by customer/session.
- **Data volume in the CSVs:** Since the store's current catalog in the CSVs only has a few products per category, sending all products from the chosen category to Step 2 works great and ensures the AI doesn't miss any item. If the store grew to thousands of products in the same category, I would move these CSVs to a SQLite/PostgreSQL database and let the function filter by price range (`max_price`, `min_price`) directly in the query.
- **Data inconsistency in the catalog:** Some products in the `products.csv` table have a mismatch between the title and the description (e.g., a bass named Music Man with a description talking about Fender). I kept the agent reading the store's original data, but in a real-world scenario I would create a catalog validation/cleaning routine with the store's team.

---

## 8. Use of AI Assistants

I used an AI assistant (Cico Coding https://cico.diy), which was developed by myself, as a coding partner to discuss the architecture, review business rules hidden in the CSVs, structure the prompt texts, and speed up writing the Python boilerplate, while keeping all the decisions around the 2-step logic, function design (`enviar_mensagem`, `get_categorias`, ID filtering), and behavior tweaks in my own hands.