import paho.mqtt.client as mqtt

# --- Configurações ---
broker = "test.mosquitto.org"  # Ou o IP local do broker, se estiver rodando Mosquitto no seu PC
topic = "esp32/felipe/dht"

# --- Callback quando uma mensagem é recebida ---
def on_message(client, userdata, msg):
    print(f"📥 Mensagem recebida em {msg.topic}: {msg.payload.decode()}")

# --- Criação do cliente MQTT ---
client = mqtt.Client()
client.on_message = on_message

print("🔗 Conectando ao broker MQTT...")
client.connect(broker, 1883, 60)

# --- Inscrição no tópico ---
client.subscribe(topic)
print(f"📡 Inscrito no tópico: {topic}")

# --- Loop de escuta ---
client.loop_forever()
