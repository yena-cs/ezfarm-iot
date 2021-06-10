#define Vref 4.95 // PH
#define PWMpin 5  // 워터펌프 PWM 제어
#define DIRpin 6  // 워터펌프 방향 제어

int CO_Sensor = A0;
int Soil_Sensor = A2;
int PH_Sensor = A3;
int Water_Sensor = A4;

unsigned long int PHavgValue; //PH 센서 평균 

void setup() {
  Serial.begin(9600);
  pinMode(PH_Sensor, INPUT);
  pinMode(DIRpin, OUTPUT);
}
 
void loop() {
  int PH_Value = readPH();  // PH
  Serial.print("CO2 value:");
  Serial.println(analogRead(CO_Sensor));
  int Soil_Value = analogRead(Soil_Sensor); // 0에 가까울수록 수분이 많고, 1023에 가까울수록 수분이 적다
  if(Soil_Value > 800){
    int Water_Depth = analogRead(Water_Sensor);
    if(Water_Depth < 400){
      Serial.println("water 0");
      Motor(HIGH, 0); 
    }else{
      Motor(HIGH, 255);
    } 
  }else{
    Motor(HIGH, 0);
  }
  Serial.print("Soil Moisture value:");
  Serial.println(Soil_Value);
  Serial.print("PH value:");
  Serial.println(PH_Value);
  delay(10000);
}

int readPH(){
  float sensorValue;
    int m;
    long sensorSum;
    int buf[10];
  for(int i=0;i<10;i++)
  { 
    buf[i]=analogRead(PH_Sensor);
    delay(10);
  }
  for(int i=0;i<9;i++)
  {
    for(int j=i+1;j<10;j++)
    {
      if(buf[i]>buf[j])
      {
        int temp=buf[i];
        buf[i]=buf[j];
        buf[j]=temp;
      }
    }
  }
  PHavgValue=0;
  for(int i=2;i<8;i++)
    PHavgValue+=buf[i];
  sensorValue = PHavgValue/6;
  sensorValue = 7-1000*(sensorValue-365)*Vref/59.16/1023,2;
  return sensorValue;
}

void Motor (boolean DIR, byte Motorspeed) {
  if(DIR){
    analogWrite(PWMpin, 255-Motorspeed);
  }else{
    analogWrite(PWMpin, Motorspeed);
  }
  digitalWrite(DIRpin, DIR);
}
