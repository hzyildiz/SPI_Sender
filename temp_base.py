import serial
import crc8
from time import sleep

class DataPacket():
    hash8 = crc8.crc8()
    def __init__(self):
        self._not = 0
        self.size = 30
        self.spiDelay = 100
        #self.sendDelay = 100
        self.outdata = b'\x00\x00\x00\x00'

    @property
    def send_representation(self):
        data = self._not.to_bytes(1,byteorder="little" ,signed=False) + \
                self.size.to_bytes(1,byteorder="little" ,signed=False) + \
                self.spiDelay.to_bytes(2,byteorder="little" ,signed=False) + \
                self.outdata#self.sendDelay.to_bytes(2,byteorder="little" ,signed=False) + \
        self.hash8.reset()
        self.hash8.update(data)
        return b'\xDE\xDE' + data + self.hash8.digest() + b'\xDE\xAD'
data = DataPacket()

ser = serial.Serial("/dev/cu.usbserial-1440",baudrate=115200)

def send(outdata):
    data.outdata = outdata
    while True:
        ser.write(data.send_representation)
        line = ser.readline() 
        if (line == b'OK!\r\n'): break
        sleep(.3)

    print("OK!")

alternate = b'\x55\x55\x55\x55'
allones = b'\xFF\xFF\xFF\xFF'
allzeros = b'\x00\x00\x00\x00'
threefive = b'\x07\x07\x07\x07'