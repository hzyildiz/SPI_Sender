import serial
from serial.tools import list_ports
import crc8
import time
from tkinter import *
import customtkinter
from threading import Thread
import math 
import all_escapes

class DataPacket():
    hash8 = crc8.crc8()
    def __init__(self):
        self._not = 0
        self.size = 30
        self.spiDelay = 100
        self.sendDelay = 100
        self.outdata = b'\x00\x00\x00\x00'

    @property
    def send_representation(self):
        data = self._not.to_bytes(1,byteorder="little" ,signed=False) + \
                self.size.to_bytes(1,byteorder="little" ,signed=False) + \
                self.spiDelay.to_bytes(2,byteorder="big" ,signed=False) + \
                self.sendDelay.to_bytes(2,byteorder="big" ,signed=False) + \
                self.outdata
        self.hash8.reset()
        self.hash8.update(data)
        out = b'\xDE\xDE' + data + self.hash8.digest() + b'\xDE\xAD'
        print((out).decode("all-escapes"))
        return out

class SliderWithEntry():
    def __init__(self, parent,slidersettings = dict(), entrysettings = dict(),  default = 0, _type = int):
        self.frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        self.var = customtkinter.StringVar(self.frame, value=str(_type(default)))
        self.slider = customtkinter.CTkSlider(self.frame, command=self.slider_event, **slidersettings)
        self.slider.set(default)
        self.slider.grid(row= 0,column=0)
        self.entry = customtkinter.CTkEntry(self.frame, textvariable= self.var, **entrysettings)
        self.entry.configure(validatecommand=(self.entry.register(self.entry_validation), "%P"))
        self.entry.grid(row= 0,column=1)
        self.type = _type

    def slider_event(self,value,):
        self.var.set(str(self.type(value)))
    def entry_validation(self, value):
        if value == "": return True
        try:
            value = self.type(value)
        except:
            return False
        self.slider.set(value)
        return True
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    @property
    def value(self):
        return self.type(self.var.get())

data = DataPacket()
ports = []
def  print_log(text):
    log_text.configure(state="normal")
    log_text.insert(index="end", text=text)
    log_text.see("end")
    log_text.configure(state="disabled")

def print_error(text):
    error_text.configure(state="normal")
    error_text.delete("0.0","end")
    error_text.insert(index="end", text=text)
    error_text.configure(state="disabled")


def find_ports():
    ports.extend([d.device for d in list_ports.comports()])
    portmenu.configure(values = ports)

def compile_data_packet():
    data._not = invert.get()
    data.size = size.value
    data.spiDelay = int(500//spi_delay.value)
    data.sendDelay = int(1000//send_delay.value)
    print(hex(int(spi_data_var.get(),16)))
    data.outdata = int(spi_data_var.get(),16).to_bytes(8, byteorder="big")

def upload_helper(port):
    compile_data_packet()
    print_log(f"Connecting to Port {port}\n")
    try:
        ser = serial.Serial(port, baudrate=int(baudmenu_var.get()), timeout=1)
    except Exception as e:
        print_log("Couldn't connect to port\n")
        print_log(e.__repr__()+ "\n")
        return
    print_log("Connected! Sending Data Packet\n")

    #TODO Add Timeout
    while True:
        ser.write(data.send_representation)
        time.sleep(0.2)
        while line:= str(ser.read_until(), "ascii").replace("\r",""):
            print_log(line)
            print(line)
            if line == "OK!\n":
                ser.close()
                return
    
def upload_button_press():
    upload_button.configure(fg_color="darkred", state="disabled", text="Uploading...")
    if not check_outdata():
        print_error("Pixel pattern is wrong, make sure it is a valid hex number of appropiate size")
        reset_upload_button()
        return
    t = Thread(target= upload)
    t.start()

def reset_upload_button():
    upload_button.configure(fg_color="darkgreen",state="normal", text="Upload")
def upload():
    port = portmenu_var.get()
    if (port == ""):
        print_log("Please select port\n")
    else:
        upload_helper(port)
    reset_upload_button()

def check_outdata():
    new_text = spi_data_var.get()
    if not new_text: return True
    try:
        spi_data_to_send = int(new_text,16)
    except:
        return False
    else:
        print(spi_data_to_send)
        if len(new_text) > math.ceil(size.value / 4):
             return False
        if spi_data_to_send == 0:
            return False
        return True


#
# GUI Layout Below
#

customtkinter.set_default_color_theme("green")
GUI = customtkinter.CTk()
#GUI.geometry("600x500+0+0")
GUI.title("SPI Sender")
GUI.resizable(False,False)
GUI.after(200, find_ports)

#
# Status Bar on Left
#

status = customtkinter.CTkFrame(GUI, height=350)
status.grid(row= 0,rowspan=2 ,column=0, sticky=NS)

portmenu_var = customtkinter.StringVar()
portmenu = customtkinter.CTkOptionMenu(status, dynamic_resizing=False, width= 200, font=("Helvetica", 16), dropdown_font=("Helvetica", 16),variable=portmenu_var)
portmenu.grid(row=0, column=0, pady = 5)

baudmenu_var = customtkinter.StringVar(value="115200")
baudmenu = customtkinter.CTkOptionMenu(status, dynamic_resizing=False, values= ["9600","19200","28800","57600","115200","230400","460800","921600"], width= 100, font=("Helvetica", 16), dropdown_font=("Helvetica", 16),variable=baudmenu_var)
baudmenu.grid(row=1, column=0, pady=5, sticky=E)
baudlabel = customtkinter.CTkLabel(status, text="Baudrate:", font=("Helvetica", 16)).grid(row=1, column=0, sticky =W, padx = 5)

error_text = customtkinter.CTkTextbox(status, text_color="red", fg_color="transparent", state=DISABLED, wrap="word")
error_text.grid(row=2, column=0)

#
# MAIN SETTINGS FRAME IN THE MIDDLE
#

settings = customtkinter.CTkFrame(GUI)
settings.grid(row=0, column=1,rowspan=2, padx= 10, pady= 10, sticky=NS)

invert = customtkinter.CTkCheckBox(settings,text="")
invert.grid(row=0, column = 1, pady=10, padx=10, sticky=EW)
invert_label = customtkinter.CTkLabel(settings,text="Invert Signal", font=("Helvetica",20), padx = 20).grid(row = 0, column= 0)

size = SliderWithEntry(settings,default= 30 ,slidersettings={"from_":0, "to":50, "number_of_steps":50}, entrysettings={"font":("Helvetica",20),"width":55,"validate":"all"}, _type=int)
size.grid(row = 1, column = 1, padx = 10, pady= 10)
size_label = customtkinter.CTkLabel(settings,text="Number of Pixels", font=("Helvetica",20), padx = 20).grid(row = 1, column= 0)

spi_delay = SliderWithEntry(settings, default=5, slidersettings={"from_":0.5, "to":50, "number_of_steps":99}, entrysettings={"font":("Helvetica",20),"width":55,"validate":"all"}, _type=float)
spi_delay.grid(row=2, column= 1, padx = 10, pady= 10)
spi_delay_label = customtkinter.CTkLabel(settings,text="SPI Frequency (kHz)", font=("Helvetica",20), padx = 20).grid(row = 2, column= 0)

send_delay = SliderWithEntry(settings, default=10 ,slidersettings={"from_":1, "to":100, "number_of_steps":99}, entrysettings={"font":("Helvetica",20),"width":55,"validate":"all"}, _type=int)
send_delay.grid(row=3, column= 1, padx = 10, pady= 10)
send_delay_label = customtkinter.CTkLabel(settings,text="Send Frequncy (Hz)", font=("Helvetica",20), padx = 20).grid(row = 3, column= 0)

spi_data_var = customtkinter.StringVar(value="0")
spi_data = customtkinter.CTkEntry(settings,textvariable= spi_data_var)
spi_data.grid(row = 4, column =1, padx=10, pady=10)
spi_data_label = customtkinter.CTkLabel(settings, text="Pixel Pattern as HEX (no 0x)", font=("Helvetica",20),padx=20).grid(row=4, column=0)



#
#  LOG ON THE RIGHT
#

log_fr = customtkinter.CTkFrame(GUI)
log_fr.grid(row= 0, column=2, sticky=NS, padx=10, pady=10)

log_text = customtkinter.CTkTextbox(log_fr, state="disabled", width=250, wrap="word")
log_text.grid(padx=10, pady=10, sticky=NSEW)

#
# UPLOAD BUTTON LOGIC
#

upload_button = customtkinter.CTkButton(GUI, width=200, height= 100,text="Upload" ,fg_color="darkgreen", hover_color="green",font=("Helvetica",32), command=upload_button_press)
upload_button.grid(row= 1,column=2, padx=10, pady= 10)

GUI.mainloop()