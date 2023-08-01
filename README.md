# SPI_Sender
A simple GUI for sending SPI data from a computer using an arduino as interface.

## Requirements
Python 3.8+ is required in addition to below libraries:
- pyserial
- crc8
- customtkinter
- all-escapes

## Hardware Setup
To use this app you'll need an MCU that can utilise the Arduino library. This app was designed around the NodeMCU board with an ESP8266 microprocessor. While other MCUs should work fine too, no guarantees are given. 

To set up the hardware first change the CLK, DATA, and EN definitions at the top of the ==main.cpp== 