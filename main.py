import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3.1-flash-lite"

SYSTEM_PROMPT = """
Você é o Hugo Santos, vendedor da loja Empório da Música (localizada em Campo Grande/MS).
Atenda o cliente de forma amigável, informal mas profissional, como um amigo que entende de música.
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
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=historico,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.3,
                )
            )

            resposta_ia = response.text
            print(f"\nHugo (Empório da Música): {resposta_ia}\n")

            historico.append(
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=resposta_ia)]
                )
            )

        except Exception as e:
            print(f"\n[Erro na chamada da API]: {e}\n")
            historico.pop()

if __name__ == "__main__":
    main()