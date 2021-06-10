#include  <DHT.h>  //  온습도 센서를 사용하기 위한 라이브러리
#include  <SoftwareSerial.h>

#define DHTPIN 3
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

int CDS_Sensor = A0;
int Fan_Sensor = 7;
int light_Sensor = 8;
int RXPIN = 8;
int TXPIN = 9;
SoftwareSerial ESP_wifi(RXPIN, TXPIN);
void setup() {
  Serial.begin(9600);
  ESP_wifi.begin(9600);
  ESP_wifi.setTimeout(5000);
  dht.begin();
  //pinMode(Fan_Sensor, OUTPUT);
  //pinMode(light_Sensor, OUTPUT);
}

void loop() {
  int h_Sensor = dht.readHumidity();     // 습도   
  int t_Sensor = dht.readTemperature();  // 온도
  int CDS_Value = analogRead(CDS_Sensor); // 조도

  if(Serial.available()){
    ESP_wifi.write(Serial.read());
  }
  if(ESP_wifi.available()){
    Serial.write(ESP_wifi.read());
  }
  /*Serial.print("CDS value:"); // 광량과 수치는 반비례
  Serial.println(CDS_Value);
  Serial.print("humidity value:");
  Serial.println(h_Sensor);
  Serial.print("temperature value:");
  Serial.println(t_Sensor);*/
  /*if(t_Sensor > 25){
    digitalWrite(Fan_Sensor, HIGH);
  }else{
    digitalWrite(Fan_Sensor, LOW);
  }
  digitalWrite(light_Sensor, HIGH);*/
  delay(3000);
}
