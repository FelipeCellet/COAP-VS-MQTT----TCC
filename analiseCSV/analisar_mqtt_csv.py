import pandas as pd

# === 1. Carregar os arquivos CSV ===
mqtt_csv = "mqtt30min.csv"
coap_csv = "coap30minantigo.csv"

df_mqtt = pd.read_csv(mqtt_csv)
df_coap = pd.read_csv(coap_csv)

# === 2. Filtrar apenas mensagens relevantes ===
df_mqtt_pub = df_mqtt[df_mqtt["Info"].str.contains("Publish Message", na=False)].copy()
df_coap_post = df_coap[df_coap["Info"].str.contains("POST", na=False)].copy()

# === 3. Calcular intervalo de tempo entre mensagens ===
df_mqtt_pub["Delta_t"] = df_mqtt_pub["Time"].diff()
df_coap_post["Delta_t"] = df_coap_post["Time"].diff()

# === 4. Calcular métricas para MQTT ===
tempo_total_mqtt = df_mqtt_pub["Time"].iloc[-1] - df_mqtt_pub["Time"].iloc[0]
qtd_mqtt = len(df_mqtt_pub)
pacotes_por_segundo_mqtt = qtd_mqtt / tempo_total_mqtt
media_tempo_mqtt = df_mqtt_pub["Delta_t"].mean()
desvio_tempo_mqtt = df_mqtt_pub["Delta_t"].std()
media_tamanho_mqtt = df_mqtt_pub["Length"].mean()

# === 5. Calcular métricas para CoAP ===
tempo_total_coap = df_coap_post["Time"].iloc[-1] - df_coap_post["Time"].iloc[0]
qtd_coap = len(df_coap_post)
pacotes_por_segundo_coap = qtd_coap / tempo_total_coap
media_tempo_coap = df_coap_post["Delta_t"].mean()
desvio_tempo_coap = df_coap_post["Delta_t"].std()
media_tamanho_coap = df_coap_post["Length"].mean()

# === 5.5 Verificar se o tempo total de captura foi igual ===
print("\n⏱️ Duração total da captura:")
print(f"MQTT: {tempo_total_mqtt:.2f} segundos")
print(f"CoAP: {tempo_total_coap:.2f} segundos")

if abs(tempo_total_mqtt - tempo_total_coap) < 1:
    print("✅ Os tempos de captura são praticamente iguais.")
else:
    print("⚠️ Diferença detectada nos tempos de captura! Pode afetar a comparação.")


# === 6. Exibir os resultados comparativos ===
print("\n📊 Métricas Comparativas entre MQTT e CoAP:")
print(f"{'Protocolo':<10} {'Qtd Pacotes':>12} {'Pacotes/s':>12} {'Tempo Médio (s)':>18} {'Desvio Padrão (s)':>20} {'Tamanho Médio (bytes)':>26}")
print("-" * 100)
print(f"{'MQTT':<10} {qtd_mqtt:>12} {pacotes_por_segundo_mqtt:>12.3f} {media_tempo_mqtt:>18.4f} {desvio_tempo_mqtt:>20.4f} {media_tamanho_mqtt:>26.1f}")
print(f"{'CoAP':<10} {qtd_coap:>12} {pacotes_por_segundo_coap:>12.3f} {media_tempo_coap:>18.4f} {desvio_tempo_coap:>20.4f} {media_tamanho_coap:>26.1f}")
