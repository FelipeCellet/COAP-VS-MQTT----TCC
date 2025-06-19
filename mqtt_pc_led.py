import network
import time
import dht
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# --- Wi-Fi ---
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
TOPIC_SETPOINT = b"esp32/felipe/setpoint"
TOPIC_LED = b"esp32/felipe/led"

setpoint_temp = None
override_rgb = None  # se definido, ignora controle automático

# --- Callback para mensagens recebidas ---
def on_message(topic, msg):
    global setpoint_temp, override_rgb
    print(f"📥 Mensagem recebida no tópico {topic}: {msg}")

    try:
        if topic == TOPIC_SETPOINT:
            setpoint_temp = int(msg)
            override_rgb = None  # desativa override quando recebe novo setpoint
            print(f"🎯 Novo setpoint de temperatura: {setpoint_temp}°C")

        elif topic == TOPIC_LED:
            r, g, b = map(int, msg.decode().split(","))
            override_rgb = (r, g, b)
            print(f"🎨 Comando manual: R={r} G={g} B={b}")
    except Exception as e:
        print("⚠️ Erro ao interpretar mensagem:", e)

# --- Setup MQTT ---
client = MQTTClient(CLIENT_ID, BROKER)
client.set_callback(on_message)
client.connect()
client.subscribe(TOPIC_SETPOINT)
client.subscribe(TOPIC_LED)
print("🔗 Conectado e inscrito nos tópicos.")

# --- Loop principal ---
last_pub_time = time.time()

while True:
    client.check_msg()  # Verifica mensagens recebidas

    if time.time() - last_pub_time >= 5:
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            print(f"🌡️ Temp: {temp}°C | 💧 Umidade: {hum}%")

            # Controle de LED
            if override_rgb is not None:
                set_color(*override_rgb)
            elif setpoint_temp is not None:
                if temp < setpoint_temp:
                    set_color(0, 0, 1023)  # Azul
                elif temp == setpoint_temp:
                    set_color(0, 1023, 0)  # Verde
                else:
                    set_color(1023, 0, 0)  # Vermelho
            else:
                set_color(0, 0, 0)  # Sem setpoint = LED apagado

            # Publicar dados
            payload = f"{temp},{hum}"
            client.publish(TOPIC_PUB, payload)
            print("📤 Publicado:", payload)

        except Exception as e:
            print("❌ Erro ao medir/publicar:", e)

        last_pub_time = time.time()

    time.sleep(0.1)

