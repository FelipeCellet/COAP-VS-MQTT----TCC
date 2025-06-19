import paho.mqtt.client as mqtt
import time

BROKER = "test.mosquitto.org"
TOPIC_LED = "esp32/felipe/led"
TOPIC_DADOS = "esp32/felipe/dados"

monitorando = False  # Flag de controle do modo monitoramento

# --- Callback: ao receber mensagem do ESP32 ---
def on_message(client, userdata, msg):
    if monitorando:
        try:
            payload = msg.payload.decode()
            temp, hum = payload.split(",")
            print(f"📡 Temperatura: {temp}°C | Umidade: {hum}%")
        except:
            print(f"⚠️ Mensagem recebida: {msg.payload.decode()}")

# --- Envia comando RGB ---
def enviar_cor_rgb(r, g, b):
    payload = f"{r},{g},{b}"
    client.publish(TOPIC_LED, payload)
    print(f"📤 Cor enviada: R={r} G={g} B={b}")

# --- Modo de monitoramento contínuo ---
def iniciar_monitoramento():
    global monitorando
    monitorando = True
    print("\n=== MODO MONITORAMENTO ===")
    print("Recebendo dados do ESP32... (pressione Ctrl+C para sair)\n")

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n🔙 Retornando ao menu principal...")
        monitorando = False
        time.sleep(1)

# --- Menu principal ---
def menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Enviar cor RGB para o LED")
        print("2. Iniciar monitoramento de temperatura/umidade")
        print("3. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            entrada = input("Digite R,G,B (0-1023): ").strip()
            try:
                r, g, b = map(int, entrada.split(","))
                if any(x < 0 or x > 1023 for x in (r, g, b)):
                    print("❌ Valores devem estar entre 0 e 1023.")
                else:
                    enviar_cor_rgb(r, g, b)
            except:
                print("⚠️ Entrada inválida. Use o formato: 255,128,64")

        elif opcao == "2":
            iniciar_monitoramento()

        elif opcao == "3":
            print("🛑 Encerrando conexão MQTT...")
            break

        else:
            print("❌ Opção inválida.")

# --- Setup MQTT ---
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC_DADOS)
client.loop_start()

# --- Executa menu principal ---
try:
    menu()
finally:
    client.loop_stop()
    client.disconnect()
    print("🛑 Desconectado do broker MQTT.")
