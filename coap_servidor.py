import asyncio
from aiocoap import *
from aiocoap import resource
import logging

logging.basicConfig(level=logging.INFO)

class LedControlResource(resource.Resource):
    async def render_post(self, request):
        rgb = request.payload.decode().strip()
        print(f"💡 Comando recebido para LED RGB: {rgb}")
        return Message(payload=b"Comando recebido!", code=CONTENT)

async def main():
    root = resource.Site()
    root.add_resource(['led', 'control'], LedControlResource())
    await Context.create_server_context(root, bind=('192.168.18.96', 5683))
    print("🖥️ Servidor CoAP pronto e escutando em 192.168.18.96:5683")
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
