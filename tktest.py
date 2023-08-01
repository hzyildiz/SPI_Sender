import customtkinter
import serial
from serial.tools import list_ports

ports = list_ports.comports()
portlist = [x.device for x in ports]


app = customtkinter.CTk()
def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

optionmenu_var = customtkinter.StringVar(value=portlist[0])
optionmenu = customtkinter.CTkOptionMenu(app,values=portlist,
                                         command=optionmenu_callback,
                                         variable=optionmenu_var)
optionmenu.grid()

app.mainloop()