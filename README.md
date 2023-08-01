# SPI_Sender
A simple GUI for sending SPI data from a computer using an arduino as interface, to an SLM.

## Requirements
Python 3.8+ is required in addition to below libraries:
- pyserial
- crc8
- customtkinter
- all-escapes

## Hardware Setup
To use this app you'll need an MCU that can utilise the Arduino library. This app was designed around the NodeMCU board with an ESP8266 microprocessor. While other MCUs should work fine too, no guarantees are given. 

To set up the hardware first change the CLK, DATA, and EN definitions at the top of the main.cpp file to match the correct pins for your application. Then upload the contents of the src/ directory to your MCU of choice. Leave the device connected to your PC as this app talks to your device over USB. 

## Software Usage

1. Run GUI.py to bring up the app.
2. From the drop down menu on the top left pick your board. On OSX/Linux the name should be something like /dev/cu.usb-XXXX. On Windows it would be something like COM X.
3. If you have changed the baud rate for serial communication in main.cpp make sure to pick the correct baud rate from the dropdown just below device selection. If you don't know what that means, you don't need to do anything.
4. Using the center panel of the app enter the data you wish to send out, and the parameters for the SPI. There is a more detailed explanation of the options below.
5. Press the big green upload button. If all goes well your board will start to send the data you wish on the SPI ports you picked during hardware setup.
6. To send something else, just redo steps 4 and 5 again.

## Options
Here are the explanations for the data options.
### Invert Signal
If you select this option your SPI data will be NOTted, that is the output will look like you've ran it through a NOT gate.
### Number of Pixels
This is the number of pixels that your SLM has. Eg. If your SLM has 30 pixels the program will send 30 bits of data on the SPI bus, with 30 accompanying clock pulses.
### SPI Frequency
This is simply the frequency of the SPI clock signal and data rate. Usually after 30kHz the signal degrades but depending on your MCU you might be able to go higher. Unless you need the speed, you don't really need to change this setting.
### Send Frequency
Once you press upload, the board will repeadedly send out the data. This option is to set how often your data is repeated.
### Pixel Pattern as HEX
This is simply the data the board will send. To find this number simply write the on-off pattern you wanna put on your pixels as binary, and translate into hex. Please don't add 0x at the beginning of the data.