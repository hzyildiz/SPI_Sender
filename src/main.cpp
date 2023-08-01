#include <Arduino.h>
#include "commontypes.hpp"
#include "communication.hpp"

#define CLK 14
#define DATA 12
#define EN 13

SPIConfig defaultConfig = {_not:0, size:30, spiDelay: 100, sendDelay:100};
/*uint32_t allones = 0xFFFFFFFF;
uint32_t allzero = 0;
uint32_t threefives = 0x07070707;
uint32_t alternate = 0x55555555;
uint32_t few = 0x00010000; */

SPIConfig activeConfig = defaultConfig;
uint32_t activeOutData = 0x00000000;




// put function declarations here:
void spiwrite(uint32_t, SPIConfig);

// put your setup code here, to run once:
void setup() {
  setCRC();
  pinMode(CLK,OUTPUT);
  pinMode(DATA,OUTPUT);
  pinMode(EN,OUTPUT);
  Serial.begin(115200);
  Serial.setTimeout(500);
}

void loop() {

  if (Serial.available() >= 17){
    Serial.readBytes(readBuffer, BUFFER_LENGTH);
    //Serial.print("Read ");
    //Serial.print(r, DEC);
    //Serial.println(" bytes.");
    DataPacket parsed = parseBuffer(readBuffer);
    //Serial.print("Parse validiy is ");
    //Serial.println(parsed.valid);
    if (parsed.valid > 0){
      activeConfig = parsed.data.conf;
      activeOutData = parsed.data.outdata;
      //Serial.print(parsed.data.conf._not, HEX);
      //Serial.print(", ");
      //Serial.print(parsed.data.conf.size, HEX);
      //Serial.print(", ");
      //Serial.print(parsed.data.conf.spiDelay, HEX);
      Serial.print(", DATA:");
      Serial.println(parsed.data.outdata,HEX);
      Serial.println("OK!");
      
    }
  }
  spiwrite(activeOutData, activeConfig);
  delay(activeConfig.sendDelay);
}


void spiwrite(uint32_t outdata, SPIConfig config){

  digitalWrite(EN,config._not);

  for(int i = 0;i < config.size;i++){
    digitalWrite(CLK,config._not);
    digitalWrite(DATA,(((outdata >> i) & 1) != config._not));
    //digitalWrite(DATA,(((p == i)) != _not));
    delayMicroseconds(config.spiDelay);
    digitalWrite(CLK,!config._not);
    delayMicroseconds(config.spiDelay);
  }
  digitalWrite(EN,!config._not);

}