import asyncio
import sys
from aiocoap import *

# === Ajuste para Windows (evita erro "event loop is closed") ===
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# === IP do ESP32 (ajuste conforme necessário) ===
esp32_ip = "192.168.3.131"  # <-- substitua pelo IP do seu ESP32

# === Função para ler temperatura e umidade ===
async def test_get_temperature():
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri=f'coap://{esp32_ip}/current/measure')

    try:
        response = await protocol.request(request).response
        print("\n📡 Resposta do ESP32 (Temperatura/Umidade):")
        print(response.payload.decode())
    except Exception as e:
        print("❌ Erro ao solicitar dados:", e)

# === Função para enviar cor RGB ===
async def test_set_led_color(r, g, b):
    protocol = await Context.create_client_context()
    payload = f"{r},{g},{b}".encode('utf-8')
    request = Message(code=POST, uri=f'coap://{esp32_ip}/led/control', payload=payload)

    try:
        response = await protocol.request(request).response
        print("\n💡 Resposta do ESP32 (Controle LED):")
        print(response.payload.decode())
    except Exception as e:
        print("❌ Erro ao enviar comando RGB:", e)

# === Menu principal ===
def main_menu():
    while True:
        print("\n=== MENU CoAP - Teste com ESP32 ===")
        print("1. Ler temperatura e umidade")
        print("2. Definir cor do LED RGB")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            asyncio.run(test_get_temperature())

        elif escolha == "2":
            try:
                r = int(input("Valor de R (0-1023): "))
                g = int(input("Valor de G (0-1023): "))
                b = int(input("Valor de B (0-1023): "))
                asyncio.run(test_set_led_color(r, g, b))
            except ValueError:
                print("❌ Entrada inválida. Digite números inteiros de 0 a 1023.")

        elif escolha == "3":
            print("Encerrando...")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")

# === Execução ===
if __name__ == "__main__":
    main_menu()
