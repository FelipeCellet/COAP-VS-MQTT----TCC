import network
import time
import dht
from machine import Pin
from microcoapy import Coap

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

# --- Inicialização do cliente CoAP ---
coap = Coap()
coap.start()

# IP do servidor CoAP
coap_server_ip = "192.168.18.96"  # IP do seu PC
coap_resource = "/sensor"
coap_port = 5683

# --- Loop de envio periódico ---
while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        payload = f"temp={temp}&hum={hum}"
        print("📤 Enviando CoAP POST:", payload)
        coap.post(coap_server_ip, coap_port, coap_resource, payload)
    except Exception as e:
        print("❌ Erro:", e)
    
    time.sleep(5)

