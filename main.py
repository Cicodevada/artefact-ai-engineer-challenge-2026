import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3.1-flash-lite"

PROMPT_PASSO_1 = """
Você é o Hugo Santos, vendedor da loja Empório da Música (loja exclusiva de instrumentos musicais).
Seu objetivo neste primeiro passo NÃO é responder ao cliente ainda, mas sim decidir quais funções do sistema precisamos consultar para responder à mensagem dele com precisão.

Funções disponíveis:
1. get_politicas(topico)
   - Use para dúvidas sobre a loja, endereço, telefone, horário de funcionamento, formas de pagamento, parcelamento, desconto no PIX, trocas, devoluções, arrependimento, defeito, frete, entregas, garantia, LGPD ou sobre venda de acessórios.
   - Valores aceitos para 'topico': "sobre", "horario", "pagamento", "trocas", "frete", "promocoes", "atendimento", "garantia", "privacidade", "geral".

2. get_produtos( termo_busca )
   - Use quando o cliente perguntar sobre instrumentos musicais, modelos específicos, tipos de instrumento (ex: "violão", "guitarra", "ukulele", "baixo", "bateria", "teclado", "7 cordas", "nylon", "aço"), faixa de preço ou estoque.
   - Se o cliente pedir recomendações gerais de uma categoria, passe o nome da categoria ou termo simples (ex: "violão", "ukulele", "Takamine GD20", "todos").

3. get_promocoes( termo_busca )
   - Use quando o cliente perguntar sobre promoções, descontos, ofertas, Black Friday, ou quando quiser saber o preço de um produto (para checar se ele está em promoção ativa).
   - Passe o nome do produto ou "todas" para ver todas as promoções.

4. get_pedidos( identificador )
   - Use quando o cliente quiser saber o status de um pedido, rastreio, entrega ou cancelamento.
   - Passe o número do pedido (ex: "1", "15"), código de rastreio, nome ou e-mail do cliente informado na mensagem.

Responda APENAS com um JSON válido no formato de lista de objetos, sem texto adicional e sem blocos de markdown.
Exemplo 1 (Cliente pergunta "Quais violões vocês têm até 1000 reais?"):
[{"funcao": "get_produtos", "parametro": "violão"}, {"funcao": "get_promocoes", "parametro": "todas"}]

Exemplo 2 (Cliente pergunta "Qual o endereço e horário da loja?"):
[{"funcao": "get_politicas", "parametro": "sobre"}, {"funcao": "get_politicas", "parametro": "horario"}]

Exemplo 3 (Cliente apenas cumprimenta "Oi, bom dia!"):
[]
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
            print(f"\n[Passo 1] Hugo (Empório da Música): {funcoes_para_chamar}\n")

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