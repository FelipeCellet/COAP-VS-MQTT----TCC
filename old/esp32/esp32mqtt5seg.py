import network
import time
import dht
from machine import Pin
from umqtt.simple import MQTTClient

# --- Configuração da rede Wi-Fi ---
ssid = 'Felipe_2.4GHz'
password = 'cellet185'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)
while not sta_if.isconnected():
    print("Conectando...")
    time.sleep(1)
print("✅ Conectado:", sta_if.ifconfig())

# --- Inicialização do sensor DHT11 ---
sensor = dht.DHT11(Pin(4))

# --- Configuração do cliente MQTT ---
broker = "test.mosquitto.org"  # Ou IP local, se quiser comparar
client_id = "esp32_felipe"
mqtt_topic = b"esp32/felipe/dht"

client = MQTTClient(client_id, broker)
client.connect()
print("🔗 Conectado ao broker MQTT")

# --- Loop de envio periódico ---
while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        payload = f"temp={temp}&hum={hum}"
        print("📤 Enviando MQTT:", payload)
        client.publish(mqtt_topic, payload)
    except Exception as e:
        print("❌ Erro:", e)

    time.sleep(5)
