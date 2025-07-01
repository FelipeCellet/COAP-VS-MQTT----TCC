import asyncio
from aiocoap import *
from aiocoap import resource
import logging

logging.basicConfig(level=logging.INFO)

class SensorResource(resource.Resource):
    async def render_post(self, request):
        dados = request.payload.decode().strip()
        print(f"📥 Dados recebidos do ESP32: {dados}")
        return Message(payload=b"Dados recebidos com sucesso!", code=CHANGED)

async def main():
    root = resource.Site()
    root.add_resource(['sensor'], SensorResource())

    # Substitua pelo IP local da sua máquina se necessário
    await Context.create_server_context(root, bind=('192.168.18.96', 5683))

    print("🖥️ Servidor CoAP pronto em 192.168.18.96:5683/sensor")
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
