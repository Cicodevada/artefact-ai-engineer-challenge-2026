import csv

def ler_csv(nome_arquivo):
    caminho = "data/" + nome_arquivo
    dados = []
    with open(caminho, mode="r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            dados.append(linha)
    return dados


def get_politicas(topico=""):
    with open("data/politicas_da_loja.md", mode="r", encoding="utf-8") as arquivo:
        return arquivo.read()


def get_produtos(categoria_id=""):
    produtos = ler_csv("desafio_tecnico_ai_eng - products.csv")

    categoria_id = str(categoria_id).strip().lower()
    if categoria_id == "" or categoria_id == "todas" or categoria_id == "todos":
        return produtos

    ids_busca = categoria_id.split(",")
    ids_limpos = []
    for id_cat in ids_busca:
        ids_limpos.append(id_cat.strip())

    resultado = []
    for produto in produtos:
        if produto["category_id"] in ids_limpos:
            resultado.append(produto)

    return resultado


def get_promocoes(termo_busca=""):
    promocoes = ler_csv("desafio_tecnico_ai_eng - promotions.csv")
    produtos = ler_csv("desafio_tecnico_ai_eng - products.csv")

    # Coloca o nome do produto dentro da promocao pra facilitar pra IA
    for promo in promocoes:
        promo["product_name"] = "Desconhecido"
        for prod in produtos:
            if prod["product_id"] == promo["product_id"]:
                promo["product_name"] = prod["name"]
                break

    termo = str(termo_busca).strip().lower()
    if termo == "" or termo == "todas" or termo == "todos":
        return promocoes

    resultado = []
    for promo in promocoes:
        if (
            termo == promo["product_id"].lower()
            or termo in promo["product_name"].lower()
            or termo in promo["description"].lower()
        ):
            resultado.append(promo)

    if len(resultado) == 0:
        return promocoes

    return resultado


def get_pedidos(identificador=""):
    pedidos = ler_csv("desafio_tecnico_ai_eng - orders.csv")
    clientes = ler_csv("desafio_tecnico_ai_eng - customers.csv")
    produtos = ler_csv("desafio_tecnico_ai_eng - products.csv")
    itens = ler_csv("desafio_tecnico_ai_eng - order_items.csv")

    termo = str(identificador).strip().lower()
    resultados = []

    for pedido in pedidos:
        # Acha o cliente do pedido
        cliente_do_pedido = {}
        for cliente in clientes:
            if cliente["customer_id"] == pedido["customer_id"]:
                cliente_do_pedido = cliente
                break

        # Acha os itens do pedido e o nome de cada produto
        itens_do_pedido = []
        for item in itens:
            if item["order_id"] == pedido["order_id"]:
                nome_produto = ""
                for prod in produtos:
                    if prod["product_id"] == item["product_id"]:
                        nome_produto = prod["name"]
                        break

                itens_do_pedido.append({
                    "product_id": item["product_id"],
                    "product_name": nome_produto,
                    "quantity": item["quantity"]
                })

        pedido["customer"] = cliente_do_pedido
        pedido["items"] = itens_do_pedido

        if termo == "":
            resultados.append(pedido)
            continue

        nome_cliente = cliente_do_pedido.get("name", "").lower()
        email_cliente = cliente_do_pedido.get("email", "").lower()
        telefone_cliente = cliente_do_pedido.get("phone", "").lower()
        rastreio = pedido["tracking_code"].lower()

        if (
            termo == pedido["order_id"].lower()
            or (rastreio != "" and termo in rastreio)
            or termo in nome_cliente
            or termo in email_cliente
            or termo in telefone_cliente
        ):
            resultados.append(pedido)

    return resultados