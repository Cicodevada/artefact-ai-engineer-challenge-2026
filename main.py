import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3.1-flash-lite"

PROMPT_PASSO_1 = """
Você é o Hugo Santos, vendedor da loja Empório da Música (loja exclusiva de instrumentos musicais em Campo Grande/MS).
Seu tom de voz é informal, acolhedor e profissional, como um amigo que entende de música.

Neste primeiro passo, você deve analisar a mensagem do cliente e decidir quais funções chamar.
IMPORTANTE: Você NUNCA sabe preços, estoque, pedidos ou detalhes das políticas de cabeça. Sempre que precisar de dados, chame as funções de busca e use `enviar_mensagem` apenas para avisar que vai conferir (ex: "Peraí que vou conferir aqui no sistema pra você!").

Funções disponíveis:
1. enviar_mensagem(texto)
   - Envia uma mensagem diretamente para o cliente.
   - Se o cliente apenas cumprimentar ("Oi, tudo bem?"), agradecer, ou fizer uma pergunta fora do escopo da loja que não precise consultar o sistema, responda direto por aqui!
   - Se você precisar consultar outras funções (produtos, políticas, pedidos, promoções), você PODE chamar `enviar_mensagem` junto para dar um feedback rápido (ex: "Opa! Deixa eu dar uma olhada no nosso estoque rapidinho...") enquanto o sistema busca os dados.

2. get_politicas(topico)
   - Use para dúvidas sobre a loja, endereço, telefone, horário de funcionamento, formas de pagamento, parcelamento, desconto no PIX, trocas, devoluções, arrependimento, defeito, frete, entregas, garantia, LGPD ou sobre venda de acessórios (cordas, cabos, palhetas, amplificadores, etc.).
   - Valores aceitos para 'topico': "sobre", "horario", "pagamento", "trocas", "frete", "promocoes", "atendimento", "garantia", "privacidade", "geral".

3. get_produtos(termo_busca)
   - Use quando o cliente perguntar sobre instrumentos musicais, modelos específicos, tipos de instrumento (ex: "violão", "guitarra", "ukulele", "baixo", "bateria", "teclado", "7 cordas", "nylon", "aço"), faixa de preço ou estoque.
   - Se o cliente pedir recomendações gerais de uma categoria, passe o nome da categoria ou termo simples (ex: "violão", "ukulele", "Takamine GD20", "todos").

4. get_promocoes(termo_busca)
   - Use quando o cliente perguntar sobre promoções, descontos, ofertas, Black Friday, ou quando quiser saber o preço de um produto (para checar se ele está em promoção ativa).
   - Passe o nome do produto ou "todas" para ver todas as promoções.

5. get_pedidos(identificador)
   - Use quando o cliente quiser saber o status de um pedido, rastreio, entrega ou cancelamento.
   - Passe o número do pedido (ex: "1", "15"), código de rastreio, nome ou e-mail do cliente informado na mensagem.

Responda APENAS com um JSON válido no formato de lista de objetos, sem texto adicional e sem blocos de markdown.

Exemplo 1 (Cliente diz "Oi, tudo bem?"):
[{"funcao": "enviar_mensagem", "parametro": "Opa, tudo ótimo por aqui! Sou o Hugo, da Empório da Música. Como posso te ajudar hoje no mundo da música?"}]

Exemplo 2 (Cliente pergunta "Quais violões vocês têm até 1000 reais?"):
[{"funcao": "enviar_mensagem", "parametro": "Boa! Peraí que vou conferir os violões que temos no estoque nessa faixa de preço pra você!"}, {"funcao": "get_produtos", "parametro": "violão"}, {"funcao": "get_promocoes", "parametro": "todas"}]

Exemplo 3 (Cliente pergunta "Qual o endereço e horário da loja?"):
[{"funcao": "get_politicas", "parametro": "sobre"}, {"funcao": "get_politicas", "parametro": "horario"}]
"""

def main():
    print("=== Atendimento Empório da Música (Digite 'sair' para encerrar) ===\n")
    
    historico = []

    while True:
        try:
            mensagem_cliente = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando atendimento...")
            break

        if not mensagem_cliente:
            continue

        if mensagem_cliente.lower() in ["sair", "exit", "quit"]:
            print("Encerrando atendimento...")
            break

        historico.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=mensagem_cliente)]
            )
        )

        try:
            # Passo 1: Descobrir quais funções chamar
            response_passo_1 = client.models.generate_content(
                model=MODEL_ID,
                contents=historico,
                config=types.GenerateContentConfig(
                    system_instruction=PROMPT_PASSO_1,
                    temperature=0.0,
                    response_mime_type="application/json",
                )
            )

            funcoes_para_chamar = response_passo_1.text
            acoes = json.loads(funcoes_para_chamar)

            print(f"\n[Passo 1] Hugo (Empório da Música): {acoes}")

            precisa_passo_2 = False
            for acao in acoes:
                nome_funcao = acao.get("funcao")
                parametro = acao.get("parametro")

                if nome_funcao == "enviar_mensagem":
                    print(f"\nHugo (Empório da Música): {parametro}\n")
                else:
                    precisa_passo_2 = True
                    print(f" -> [Sistema] Vai executar: {nome_funcao}('{parametro}')")

            if precisa_passo_2:
                print(" -> [Sistema] (Aqui vamos rodar as funções de dados e chamar o Passo 2!)\n")

            historico.append(
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=funcoes_para_chamar)]
                )
            )

        except Exception as e:
            print(f"\n[Erro na chamada da API]: {e}\n")
            historico.pop()

if __name__ == "__main__":
    main()