import pandas as pd
import matplotlib.pyplot as plt

# === Caminho do arquivo CSV exportado do Wireshark ===
csv_path = "mqtt30min.csv"  # Altere se necessário

# === 1. Carregar o CSV ===
df = pd.read_csv(csv_path)

# === 2. Filtrar apenas mensagens MQTT do tipo Publish ===
df_publish = df[df["Info"].str.contains("Publish Message", na=False)].copy()

# === 3. Calcular intervalo de tempo entre mensagens consecutivas ===
df_publish["Delta_t"] = df_publish["Time"].diff()

# === 4. Limpar dados nulos do primeiro Delta_t ===
df_publish_clean = df_publish.dropna(subset=["Delta_t"]).copy()

# === 5. Calcular estatísticas principais ===
media_intervalo = df_publish_clean["Delta_t"].mean()
desvio_intervalo = df_publish_clean["Delta_t"].std()
media_tamanho = df_publish_clean["Length"].mean()

print("=== Estatísticas MQTT Publish ===")
print(f"📊 Média do tempo entre mensagens (Δt): {media_intervalo:.2f} s")
print(f"📉 Desvio padrão do tempo (Δt): {desvio_intervalo:.2f} s")
print(f"📦 Tamanho médio dos pacotes: {media_tamanho:.0f} bytes")

# === 6. Gráfico: Intervalo entre mensagens (Δt) ===
plt.figure(figsize=(10, 4))
plt.plot(df_publish_clean["Time"], df_publish_clean["Delta_t"], marker='o', linestyle='-', color='tab:blue')
plt.title("Intervalo entre mensagens MQTT Publish (Δt)")
plt.xlabel("Tempo absoluto (s)")
plt.ylabel("Intervalo Δt (s)")
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_mqtt_intervalo.png")

# === 7. Gráfico: Tamanho dos pacotes ao longo do tempo ===
plt.figure(figsize=(10, 4))
plt.plot(df_publish_clean["Time"], df_publish_clean["Length"], marker='s', linestyle='-', color='tab:green')
plt.title("Tamanho dos pacotes MQTT Publish ao longo do tempo")
plt.xlabel("Tempo absoluto (s)")
plt.ylabel("Tamanho (bytes)")
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_mqtt_tamanho.png")

# === 8. Gráfico: Boxplot do tamanho dos pacotes ===
plt.figure(figsize=(4, 6))
plt.boxplot(df_publish_clean["Length"])
plt.title("Boxplot do tamanho dos pacotes MQTT Publish")
plt.ylabel("Tamanho (bytes)")
plt.tight_layout()
plt.savefig("grafico_mqtt_boxplot.png")

# === 9. (Opcional) Salvar dados limpos em CSV ===
df_publish_clean.to_csv("mqtt_publish_analise_pronta.csv", index=False)

print("\n✅ Análise finalizada. Gráficos e CSV salvos com sucesso!")
