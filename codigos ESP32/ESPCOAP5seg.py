import asyncio
from aiocoap import resource, Context, Message, Code
import logging

logging.basicConfig(level=logging.INFO)

class SensorResource(resource.Resource):
    async def render_post(self, request):
        dados = request.payload.decode().strip()
        print(f"📥 Dados recebidos do ESP32: {dados}")
        return Message(code=Code.VALID)  # Resposta neutra obrigatória

async def main():
    root = resource.Site()
    root.add_resource(['sensor'], SensorResource())

    await Context.create_server_context(root, bind=('192.168.3.103', 5683))
    print("🖥️ Servidor CoAP rodando em udp://192.168.3.103:5683/sensor (resposta mínima obrigatória)")

    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
