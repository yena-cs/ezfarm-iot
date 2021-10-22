#include  <DHT.h>  //  온습도 센서를 사용하기 위한 라이브러리

#define DHTPIN 5
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

int CDS_Sensor = A0;
int pad_Sensor = 7;
int light_Sensor = 8;

int pan_Sensor = 10;
float temp_read = 100.0;
int led_read = 1;
int read_pan = 0;
int read_pad = 1;
int r=4;
int g=3;
int b=2;

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(pan_Sensor, OUTPUT);
  pinMode(pad_Sensor, OUTPUT);
  pinMode(light_Sensor, OUTPUT);
  pinMode(r, OUTPUT);
  pinMode(g, OUTPUT);
  pinMode(b, OUTPUT);
}

void loop() {
  int h_Sensor = dht.readHumidity();     // 습도   
  int t_Sensor = dht.readTemperature();  // 온도
  int CDS_Value = analogRead(CDS_Sensor); // 조도
  delay(5000);
  Serial.println("2,"+String(CDS_Value)+","+String(h_Sensor)+","+String(t_Sensor));
  if(Serial.available()>0){
    String type = Serial.readStringUntil('\n');
    if(type.charAt(0) == '<' and type.charAt(type.length()-2) == '>'){
      int first = type.indexOf("<");
      int second = type.indexOf(",",first+1);
      int third = type.indexOf(">",second);
      String tmp = type.substring(first+1,second);
      temp_read = tmp.toFloat();
      String led = type.substring(second+1,third);
      led_read = led.toInt();
    }
  }
  analogWrite(r, 255);
  analogWrite(g, 0);
  analogWrite(b, 0);
  if(temp_read != 100 and t_Sensor > temp_read){
    digitalWrite(pad_Sensor, HIGH);
  }else{
    digitalWrite(pad_Sensor, LOW);
  }
  if(temp_read != 100 and t_Sensor < temp_read){
    digitalWrite(pad_Sensor, HIGH);
  }else{
    digitalWrite(pad_Sensor, LOW);
  }
  if(read_pan == 1){
    digitalWrite(pan_Sensor, HIGH);
  }else{
    digitalWrite(pan_Sensor, LOW);
  }
  if(read_pad == 1){
    digitalWrite(pad_Sensor, HIGH);
  }else{
    digitalWrite(pad_Sensor, LOW);
  }
  if(led_read == 1){
    digitalWrite(light_Sensor, HIGH);
  }else if(led_read ==0){
    digitalWrite(light_Sensor, LOW);
  }
}
 
