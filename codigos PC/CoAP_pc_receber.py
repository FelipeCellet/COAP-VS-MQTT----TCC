import asyncio
from aiocoap import resource, Context
import logging

logging.basicConfig(level=logging.INFO)

class SensorResource(resource.Resource):
    async def render_post(self, request):
        dados = request.payload.decode().strip()
        print(f"📥 Dados recebidos do ESP32: {dados}")
        return None  # NÃO envia resposta

async def main():
    root = resource.Site()
    root.add_resource(['sensor'], SensorResource())

    # Substitua pelo IP local da sua máquina
    await Context.create_server_context(root, bind=('192.168.3.103', 5683))

    print("🖥️ Servidor CoAP rodando em udp://192.168.3.103:5683/sensor (sem resposta)")
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
