import asyncio
from aiocoap import *

async def main():
    while True:
        print("\nMenu:")
        print("1 - Solicitar temperatura")
        print("2 - Acender LED RGB")
        print("0 - Sair")
        escolha = input("Escolha: ")

        if escolha == "1":
            context = await Context.create_client_context()
            request = Message(code=GET, uri='coap://192.168.18.76/current/measure')
            response = await context.request(request).response
            print("Temperatura recebida:", response.payload.decode())

        elif escolha == "2":
            context = await Context.create_client_context()
            rgb = input("Digite os valores R,G,B (0-1023), separados por vírgula: ")
            request = Message(code=PUT, uri='coap://192.168.18.76/led/control', payload=rgb.encode())
            response = await context.request(request).response
            print("💡 Resposta do LED:", response.payload.decode())

        elif escolha == "0":
            break

        else:
            print("Escolha inválida")

if __name__ == "__main__":
    asyncio.run(main())
