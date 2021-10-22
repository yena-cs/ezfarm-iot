#include  <Stepper.h>
#define Vref 4.95 // PH
const int stepsPerRevolution=600;

Stepper myStepper(stepsPerRevolution, 9, 10, 11, 12);

int CO_Sensor = A0;
int Soil_Sensor = A2;
int PH_Sensor = A3;
int Water_Sensor = A4;
int Water_Pump = 5;
int water_read = 1, window_read = 1;
unsigned long int PHavgValue; //PH 센서 평균 

void setup() {
  myStepper.setSpeed(60);
  Serial.begin(9600);
  //pinMode(PH_Sensor, INPUT);
  pinMode(Water_Pump, OUTPUT);
}
 
void loop() {
  int PH_Value = readPH();  // PH
  int Soil_Value = analogRead(Soil_Sensor); // 0에 가까울수록 수분이 많고, 1023에 가까울수록 수분이 적다
  int CO_Value = analogRead(CO_Sensor);
  delay(10000);
  Serial.println("1,"+String(CO_Value)+","+String(Soil_Value)+","+String(PH_Value));
  if(Serial.available()>0){
    String type = Serial.readStringUntil('\n');
    if(type.charAt(0) == '<' and type.charAt(type.length()-2) == '>'){
      int first = type.indexOf("<");
      int second = type.indexOf(",",first+1);
      int third = type.indexOf(">",second);
//      String water = type.substring(first+1,second);
//      water_read = water.toInt();
      String window = type.substring(second+1,third);
      window_read = window.toInt();
    }
  }
  if(water_read == 1){
    int Water_Depth = analogRead(Water_Sensor);
    if(Water_Depth < 10){
      digitalWrite(Water_Pump, LOW); 
    }else{
      digitalWrite(Water_Pump, HIGH);
    } 
  }else if(water_read == 0){
    digitalWrite(Water_Pump, LOW);
  }
  
  if(window_read == 1){
    while(window_read == 0){
      myStepper.step(-stepsPerRevolution);
      delay(100);
    }
    window_read = -1;
  }
  else if(window_read == 0){
    while(window_read == 1){
      myStepper.step(stepsPerRevolution);
      delay(100);
    }
    window_read = -1;
  }
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
