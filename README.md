#  Projeto ESP32 com Comunicação CoAP e MQTT

Este repositório reúne os códigos utilizados para demonstrar e comparar os protocolos **CoAP** e **MQTT** aplicados à Internet das Coisas (IoT), usando um **ESP32** como dispositivo embarcado e um **PC** como servidor e broker.

---

## Objetivo

Este projeto visa demonstrar:
- O funcionamento prático dos protocolos **CoAP** (Constrained Application Protocol) e **MQTT** (Message Queuing Telemetry Transport);
- A troca de dados entre dispositivos IoT de forma eficiente;
- A visualização das mensagens CoAP/MQTT capturadas via **Wireshark**;
- A influência dos protocolos no consumo de energia, confiabilidade e complexidade.

---

##  Estrutura do Repositório



---

##  Funcionalidades

###  ESP32
- Conecta à rede Wi-Fi;
- Lê **temperatura e umidade** com sensor **DHT11**;
- Controla **LED RGB** conforme a temperatura:
  - Azul: < 20°C
  - Verde: 20–28°C
  - Vermelho: > 28°C
- Envia os dados a cada 5 segundos:
  - Via **CoAP** para um servidor Python
  - Via **MQTT** para um broker público ou local

###  PC

#### CoAP
- Servidor implementado com a biblioteca `aiocoap`;
- Aceita apenas método `POST` no recurso `/sensor/dados`;
- Exibe os dados recebidos e responde com `ACK`.

#### MQTT
- Subscriber configurado com a biblioteca `paho-mqtt`;
- Assina o tópico `esp32/felipe/dados`;
- Exibe os dados recebidos no terminal.

---

##  Tipos de Mensagens CoAP

Foram implementadas e testadas no ESP32 as seguintes mensagens:

| Tipo      | Código | Descrição                              |
|-----------|--------|----------------------------------------|
| `CON`     | 0      | Confirmável (gera resposta `ACK`)       |
| `NON`     | 1      | Não confirmável                        |
| `ACK`     | 2      | Resposta confirmando recebimento       |
| `RST`     | 3      | Rejeição ou não entendimento da msg    |

Todas foram capturadas com **Wireshark** para análise prática do protocolo.

---

##  Como executar

###  Pré-requisitos
- Python 3.10+
- ESP32 com MicroPython instalado
- `pip install aiocoap paho-mqtt`
- Broker MQTT (usamos `test.mosquitto.org`)

###  ESP32 (Thonny)
1. Faça upload dos arquivos `coap_client.py` ou `mqtt_client.py` (um de cada vez);
2. Verifique se `microcoapy` está no sistema de arquivos (caso use CoAP);
3. Modifique o IP de destino conforme necessário;
4. Rode o script no Thonny.

### Servidor CoAP
```bash
python pc/coap_server.py
```

###  Subscriber MQTT
```bash
python pc/mqtt_subscriber.py
```

---

##  Análise com Wireshark

Capturamos pacotes das mensagens:
- **CoAP:** `CON`, `NON`, `ACK`, `RST`
- **MQTT:** `CONNECT`, `PUBLISH`, `SUBSCRIBE`, `ACK`
- Foram aplicados filtros como:
  ```
  coap
  mqtt
  ip.addr == 192.168.x.x
  udp.port == 5683
  tcp.port == 1883
  ```

---

---

## 📈 Resultados Experimentais

As capturas foram realizadas por 30 minutos usando o Wireshark, com envio periódico de mensagens a cada 5 segundos pelo ESP32. Abaixo estão os dados extraídos e analisados com Python:

### ⏱️ Duração da Captura

| Protocolo | Tempo Total (s) |
|-----------|-----------------|
| MQTT      | 1799.65         |
| CoAP      | 1795.19         |

> ⚠️ A pequena diferença ocorre porque o último pacote CoAP foi registrado antes dos 30 minutos completos. O próximo envio ocorreria após esse tempo, o que justifica a diferença de ~4 segundos. A validade da comparação permanece, já que ambos os conjuntos têm praticamente a mesma quantidade de mensagens.

### 📊 Métricas Comparativas

| Protocolo | Qtd. Pacotes | Pacotes/s | Tempo Médio (s) | Desvio Padrão (s) | Tamanho Médio (bytes) |
|-----------|--------------|-----------|------------------|--------------------|------------------------|
| MQTT      | 342          | 0.190     | 5.2776           | 0.4082             | 88.0                   |
| CoAP      | 341          | 0.190     | 5.2800           | 0.0082             | 83.0                   |

> As métricas mostram cadência estável de envio (~5 s) em ambos os protocolos. O MQTT apresentou maior variação entre pacotes, enquanto o CoAP se manteve mais regular. O tamanho médio das mensagens CoAP também foi ligeiramente menor, o que pode favorecer aplicações com limitação de banda ou energia.

> ℹ️ **Nota sobre o MQTT:**  
> Durante a captura, pacotes de controle do tipo `PINGREQ` e `PINGRESP` (mecanismo de keep-alive do protocolo MQTT) também foram identificados. Esses pacotes foram **ignorados na análise**, pois não carregam dados úteis do sensor e não são equivalentes ao comportamento do CoAP, que não exige esse tipo de verificação periódica por padrão.  
> Apenas mensagens do tipo `PUBLISH` foram consideradas para cálculo das métricas, garantindo uma comparação justa com os `POST` do CoAP.




## Comparativo MQTT x CoAP

| Critério                    | MQTT                                | CoAP                               |
|----------------------------|--------------------------------------|-------------------------------------|
| Arquitetura                | Centralizada (Broker)                | Descentralizada (P2P)              |
| Modelo de comunicação      | Publish/Subscribe                    | Request/Response (RESTful)         |
| Transporte                 | TCP                                  | UDP                                 |
| Confiabilidade             | Alta (TCP + QoS 0/1/2)                | Moderada (CON/ACK opcional)        |
| Segurança                  | TLS/SSL                              | DTLS                                |



---

##  Conclusão

Este projeto demonstrou, de forma prática e educativa:
- Como dois dos principais protocolos IoT operam na prática;
- Suas vantagens e desvantagens;
- A facilidade de integração com o ESP32;
- A relevância do entendimento do nível de aplicação para projetos de IoT.

---

##  Autores

- Felipe Siqueira Mohallem Cellet  
- Leonardo Santos Pereira  
- Samuel Baraldi Mafra  

---


