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


