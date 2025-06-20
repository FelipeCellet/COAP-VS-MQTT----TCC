import paho.mqtt.client as mqtt
import time

# === Configuração do broker e tópicos ===
BROKER = "test.mosquitto.org"
TOPIC_GET_DADOS = "esp32/felipe/get_dados"
TOPIC_RESPOSTA = "esp32/felipe/retorno_dados"
TOPIC_LED = "esp32/felipe/led"

# === Callback para resposta do ESP32 ===
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        temp, hum = payload.split(",")
        print(f"\nTemperatura: {temp}°C | Umidade: {hum}%")
    except:
        print(f"\n Resposta recebida: {payload}")

# === Setup MQTT ===
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC_RESPOSTA)
client.loop_start()

# === Menu interativo ===
def menu():
    while True:
        print("\n=== MENU MQTT CLIENTE ===")
        print("1. Solicitar temperatura e umidade")
        print("2. Definir cor do LED RGB")
        print("3. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            client.publish(TOPIC_GET_DADOS, "?")
            print("📤 Comando enviado. Aguardando resposta...\n")
            time.sleep(2)

        elif opcao == "2":
            try:
                r = int(input(" Valor de R (0–1023): "))
                g = int(input(" Valor de G (0–1023): "))
                b = int(input(" Valor de B (0–1023): "))
                if any(x < 0 or x > 1023 for x in (r, g, b)):
                    print(" Valores devem estar entre 0 e 1023.")
                    continue
                client.publish(TOPIC_LED, f"{r},{g},{b}")
                print(f"📤 Cor enviada: R={r} G={g} B={b}")
            except:
                print(" Entrada inválida. Digite apenas números inteiros.")

        elif opcao == "3":
            break
        else:
            print(" Opção inválida.")

# === Executar menu ===
try:
    menu()
finally:
    client.loop_stop()
    client.disconnect()
    print(" Desconectado do broker MQTT.")
