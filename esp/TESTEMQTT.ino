#include <WiFi.h>
#include <PubSubClient.h>

// Credenciais Wi-Fi
const char* ssid = "Fagner Irineu (2)";
const char* password = "fagner123";

// Configuração do broker MQTT
const char* mqtt_server = "172.20.10.2"; // Substitua pelo IP do seu broker
const int mqtt_port = 1883;               // Porta do broker (padrão 1883)

// Configuração do cliente MQTT
WiFiClient espClient;
PubSubClient client(espClient);

// Função para conectar ao Wi-Fi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando ao Wi-Fi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Wi-Fi conectado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

// Função para conectar ao broker MQTT
void reconnect_mqtt() {
  while (!client.connected()) {
    Serial.print("Conectando ao broker MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("Conectado!");
    } else {
      Serial.print("Falha na conexão. Código de erro: ");
      Serial.println(client.state());
      Serial.println("Tentando novamente em 5 segundos...");
      delay(5000);
    }
  }
}

// Setup
void setup() {
  Serial.begin(9600);

  // Conectar ao Wi-Fi
  setup_wifi();

  // Configurar o broker MQTT
  client.setServer(mqtt_server, mqtt_port);
}

// Loop principal
void loop() {
  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();

  // Publicar mensagem no tópico
  String message = "Deu certo porra!";
  client.publish("test/topic", message.c_str());
  Serial.println("Mensagem publicada: " + message);

  delay(1000); // Aguarde 1 segundo antes de publicar novamente
}