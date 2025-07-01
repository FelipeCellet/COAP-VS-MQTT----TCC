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

# --- MQTT ---
BROKER = "test.mosquitto.org"
CLIENT_ID = "esp32_felipe"
TOPIC_PUB = b"esp32/felipe/dados"
TOPIC_SUB = b"esp32/felipe/setpoint"

setpoint_temp = None  # Temperatura desejada vinda do PC

def on_message(topic, msg):
    global setpoint_temp
    print(f"📥 Mensagem recebida no tópico {topic}: {msg}")
    try:
        setpoint_temp = int(msg)
        print(f"🎯 Novo setpoint de temperatura: {setpoint_temp}°C")
    except:
        print("⚠️ Erro ao interpretar o setpoint.")

client = MQTTClient(CLIENT_ID, BROKER)
client.set_callback(on_message)
client.connect()
client.subscribe(TOPIC_SUB)
print("🔗 Conectado ao broker e inscrito no tópico de setpoint.")

# --- Loop principal ---
last_pub_time = time.time()

while True:
    client.check_msg()  # Verifica se há nova mensagem do tópico SUB

    # Publica a cada 5 segundos
    if time.time() - last_pub_time >= 5:
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            print(f"🌡️ Temp: {temp}°C | 💧 Umidade: {hum}%")

            # Cor do LED baseada na temperatura atual vs setpoint
            if setpoint_temp is not None:
                if temp < setpoint_temp:
                    set_color(0, 0, 1023)  # Azul
                elif temp == setpoint_temp:
                    set_color(0, 1023, 0)  # Verde
                else:
                    set_color(1023, 0, 0)  # Vermelho
            else:
                set_color(0, 0, 0)  # Desliga o LED se sem setpoint

            payload = f"{temp},{hum}"
            client.publish(TOPIC_PUB, payload)
            print("📤 Enviado:", payload)

        except Exception as e:
            print("❌ Erro ao medir/publicar:", e)

        last_pub_time = time.time()

    time.sleep(0.1)
