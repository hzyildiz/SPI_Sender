#ifndef COMMONYTPES_H // include guard
#define COMMONYTPES_H

#include <Arduino.h>

struct SPIConfig {
  uint8_t _not;
  uint8_t size;
  uint16_t spiDelay;
  uint16_t sendDelay;
};

extern SPIConfig defaultConfig;

#endif 