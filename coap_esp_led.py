import network
import time
from machine import Pin, PWM
import microcoapy
import dht

# Conexão WiFi
ssid = 'Wi-Fi Cellet Time Capsule'
password = 'cellet185'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    time.sleep(1)
print("Conectado ao WiFi:", station.ifconfig())

# LED RGB nos pinos D18, D19, D21
red = PWM(Pin(18), freq=1000)
green = PWM(Pin(19), freq=1000)
blue = PWM(Pin(21), freq=1000)

def set_color(r, g, b):
    red.duty(r)
    green.duty(g)
    blue.duty(b)

# Inicializa DHT11 no pino D4
dht_sensor = dht.DHT11(Pin(4))

# CoAP
client = microcoapy.Coap()

def measureCurrent(packet, senderIp, senderPort):
    print('Pedido GET recebido de:', senderIp)
    try:
        dht_sensor.measure()
        temperatura = dht_sensor.temperature()
        umidade = dht_sensor.humidity()
        payload = "Temperatura: {}°C, Umidade: {}%".format(temperatura, umidade)
    except Exception as e:
        payload = "Erro ao ler sensores: {}".format(str(e))
    client.sendResponse(senderIp, senderPort, packet.messageid,
                        payload, microcoapy.COAP_RESPONSE_CODE.COAP_CONTENT,
                        microcoapy.COAP_CONTENT_FORMAT.COAP_TEXT_PLAIN, packet.token)

def ledControl(packet, senderIp, senderPort):
    print('Pedido para controle de LED:', packet.payload)
    try:
        r, g, b = map(int, packet.payload.decode().split(","))
        set_color(r, g, b)
        response = "LED set to R:{} G:{} B:{}".format(r, g, b)
    except:
        response = "Erro ao interpretar comando RGB"
    client.sendResponse(senderIp, senderPort, packet.messageid,
                        response, microcoapy.COAP_RESPONSE_CODE.COAP_CONTENT,
                        microcoapy.COAP_CONTENT_FORMAT.COAP_TEXT_PLAIN, packet.token)

client.addIncomingRequestCallback('current/measure', measureCurrent)
client.addIncomingRequestCallback('led/control', ledControl)

client.start()
print("Servidor CoAP aguardando...")

try:
    while True:
        client.poll(1000)
except KeyboardInterrupt:
    client.stop()
    print("Servidor encerrado")
