import network
import time
import dht
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# --- Conexão Wi-Fi ---
ssid = 'Felipe_2.4GHz'
password = 'cellet185'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)

while not sta_if.isconnected():
    print("Conectando ao WiFi...")
    time.sleep(1)

print("✅ Conectado:", sta_if.ifconfig())

# --- Sensor DHT11 ---
sensor = dht.DHT11(Pin(4))

# --- LED RGB ---
red = PWM(Pin(18), freq=1000)
green = PWM(Pin(19), freq=1000)
blue = PWM(Pin(21), freq=1000)

def set_color(r, g, b):
    red.duty(r)
    green.duty(g)
    blue.duty(b)

# --- Configuração MQTT ---
SERVER = "test.mosquitto.org"  # Broker público
CLIENT_ID = "esp32_felipe"
TOPIC = b"esp32/felipe/dados"

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()
print("🔗 Conectado ao broker MQTT público.")

# --- Loop principal ---
while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print(f"🌡️ Temp: {temp}°C | 💧 Umidade: {hum}%")

        # Define a cor do LED de acordo com a temperatura
        if temp < 20:
            set_color(0, 0, 1023)  # Azul
        elif temp <= 28:
            set_color(0, 1023, 0)  # Verde
        else:
            set_color(1023, 0, 0)  # Vermelho

        # Envia dados via MQTT
        payload = f"{temp},{hum}"
        client.publish(TOPIC, payload)
        print("📤 Enviado:", payload)

    except Exception as e:
        print("❌ Erro:", e)

    time.sleep(5)

