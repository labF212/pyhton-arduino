#!/usr/bin/env python3

# como correr: sudo /usr/bin/python3 firmata_portas_analogicas_pot_pwd.py
#https://pypi.org/project/pyFirmata/
#https://roboticsbackend.com/control-arduino-with-python-and-pyfirmata-from-raspberry-pi/
#https://www.instructables.com/Control-Your-Arduino-With-Pythons-Pyfirmata-Librar/

#%% import libraries and see if they work
import os

import pyfirmata # or import pyfirmata2

os.system("pip3 install keyboard")
import keyboard

#from pyfirmata import Arduino, util #include<Arduino.h>
import time                         #void setup(){#  Serial.begin(BAUDE_RATE);

# set up board
board = pyfirmata.Arduino('/dev/ttyACM0')

it = pyfirmata.util.Iterator(board)
it.start()


analog_read1 = board.get_pin('a:1:i')
analog_read5 = board.get_pin('a:5:i')

digital_write4 = board.get_pin('d:4:o')
digital_write5 = board.get_pin('d:5:p')
digital_write6 = board.get_pin('d:6:p')


digital_write4.write(0)
time.sleep(0.2) #tempo de espera para que exista o primeiro valor válido
RawValue1 = None
RawValue5 = None


while True:
      
    #RawValue1 = board.analog[1].read()
    #RawValue5 = board.analog[5].read()
    RawValue1 = analog_read1.read()
    RawValue5 = analog_read5.read()
    
    if (RawValue1) is not None:
        #RawValue1 = int(float(RawValue1)*255)
        digital_write6.write(RawValue1)
        
    else:
        print('Sensor 1 não válido')
    if (RawValue5) is not None:
        #RawValue5 = int(float(RawValue5)*255)
        digital_write5.write(RawValue5)
        
    else:
        print('Sensor 2 não válido')
    
    print('a1', int(float(RawValue1)*255))
    print('a5', int(float(RawValue5)*255))
    time.sleep(1.0)
    digital_write4.write(1)

    if keyboard.is_pressed('esc'): # if esc is pressed, quit script
        digital_write4.write(0)
        digital_write5.write(0)
        digital_write6.write(0)
        # Close the serial connection to the Arduino
        board.exit()
        break