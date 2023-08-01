#include <Arduino.h>
#include "communication.hpp"
#include <CRC8.h>

char readBuffer[BUFFER_LENGTH];

CRC8 crc;
void setCRC(){
  crc.setPolynome(0x07);
}

DataPacket parseBuffer(char * buff){
  DataPacket out = {.valid = -1};
  DataFrame frame = findPacket(buff);
  //Serial.print("Found status is ");
  //Serial.println(frame.found, DEC);
  if (frame.found == -1) return out;
  int c = checkCRC(frame, buff);
  //Serial.print("CRC check is ");
  //Serial.println(c, DEC);
  if (c == 0) return out;
  out.data.conf._not = buff[frame.begin];
  out.data.conf.size = buff[frame.begin + 1];
  out.data.conf.spiDelay = (buff[frame.begin + 2] << 8) | buff[frame.begin + 3];
  out.data.conf.sendDelay = (buff[frame.begin + 4] << 8) | buff[frame.begin + 5];
  out.data.outdata = (buff[frame.begin + 6] << 56) | (buff[frame.begin + 7] << 48) | (buff[frame.begin + 8] << 40) | (buff[frame.begin + 9] << 32) | (buff[frame.begin + 10] << 24)|
  (buff[frame.begin + 11] << 16) | (buff[frame.begin + 12] << 8) | (buff[frame.begin+13]);
  out.valid = frame.found;
  return out;
}

DataFrame findPacket(char* buff){
  DataFrame out = {found: -1, begin: 0, end: 0};

  while((buff[out.begin] != 0xDE) && (out.begin < (BUFFER_LENGTH - 1))) out.begin++;
  if ((out.begin > (int8_t)(BUFFER_LENGTH - sizeof(Data) - 3)) || (buff[out.begin + 1] != 0xDE)) return out;
  //Serial.print("Beginning is ");
  //Serial.println(out.begin);
  out.end = out.begin = out.begin + 2;

  while((buff[out.end] != 0xDE) && (out.end < (BUFFER_LENGTH - 1))) out.end++;
  if ((out.end == (BUFFER_LENGTH - 1)) || (buff[out.end + 1] != 0xAD)) return out;
  //Serial.print("End is ");
  //Serial.println(out.end);
  out.found = out.end - out.begin;
  return out;
}

int checkCRC(DataFrame frame, char* buff){
  crc.restart();
  crc.add((uint8_t *) buff + frame.begin, frame.found - 1);
  return (crc.getCRC() == buff[frame.end - 1])? 1:-1;
}