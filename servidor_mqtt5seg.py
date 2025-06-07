import paho.mqtt.client as mqtt

# --- Configurações do broker ---
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "esp32/felipe/ambientedata"

# --- Callback quando conectado ---
def on_connect(client, userdata, flags, rc):
    print("✅ Conectado ao broker com código:", rc)
    client.subscribe(TOPIC)
    print(f"📡 Inscrito no tópico: {TOPIC}")

# --- Callback quando mensagem recebida ---
def on_message(client, userdata, msg):
    print(f"📥 Mensagem recebida: {msg.payload.decode()}")

# --- Inicialização do cliente ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, keepalive=60)

print("🔄 Aguardando mensagens...")
client.loop_forever()
