#include <Arduino.h>
#include "commontypes.hpp"

#define BUFFER_LENGTH 31

extern char readBuffer[BUFFER_LENGTH];

struct Data{
    SPIConfig conf;
    uint64_t outdata;
};

struct DataPacket
{
  int8_t valid;
  Data data;
};
struct DataFrame
{
  int8_t found;
  int8_t begin;
  int8_t end;
};

void setCRC();
DataPacket parseBuffer(char* buff);
DataFrame findPacket(char* buff);
int checkCRC(DataFrame frame, char* buff);