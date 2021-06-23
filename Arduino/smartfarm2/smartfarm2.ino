#include  <DHT.h>  //  온습도 센서를 사용하기 위한 라이브러리

#define DHTPIN 3
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

int CDS_Sensor = A0;
int prop_SensorA = 5;
int prop_SensorB = 6;
int pad_Sensor = 7;
int light_Sensor = 8;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(prop_SensorA, OUTPUT);
  pinMode(prop_SensorB, OUTPUT);
  pinMode(pad_Sensor, OUTPUT);
  pinMode(light_Sensor, OUTPUT);
}

void loop() {
  int h_Sensor = dht.readHumidity();     // 습도   
  int t_Sensor = dht.readTemperature();  // 온도
  int CDS_Value = analogRead(CDS_Sensor); // 조도

  Serial.println(String(CDS_Value)+" "+String(h_Sensor)+" "+String(t_Sensor));
  digitalWrite(prop_SensorA, LOW);
  digitalWrite(prop_SensorB, LOW);
  if(t_Sensor > 30){
    digitalWrite(prop_SensorA, HIGH);
    digitalWrite(prop_SensorB, LOW);
  }else{
    digitalWrite(prop_SensorA, LOW);
    digitalWrite(prop_SensorB, LOW);
  }
  if(t_Sensor < 25){
    digitalWrite(pad_Sensor, HIGH);
  }else{
    digitalWrite(pad_Sensor, LOW);
  }
  if(CDS_Value > 500){
    digitalWrite(light_Sensor, HIGH);
  }else{
    digitalWrite(light_Sensor, LOW);
  }
  delay(3000);
}
 
