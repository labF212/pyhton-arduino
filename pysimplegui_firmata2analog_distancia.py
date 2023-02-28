#/usr/bin/env python3

# como correr: sudo /usr/bin/python3 firmata_portas_analogicas_pot_pwd.py
#https://pypi.org/project/pyFirmata/
#https://roboticsbackend.com/control-arduino-with-python-and-pyfirmata-from-raspberry-pi/
#https://www.instructables.com/Control-Your-Arduino-With-Pythons-Pyfirmata-Librar/

import PySimpleGUI as sg

import pyfirmata # or import pyfirmata2


#from pyfirmata import Arduino, util #include<Arduino.h>
import time                         #void setup(){#  Serial.begin(BAUDE_RATE);

# set up board
board = pyfirmata.Arduino('/dev/ttyACM0')

it = pyfirmata.util.Iterator(board)
it.start()

analog_read1 = board.get_pin('a:1:i')
analog_read5 = board.get_pin('a:5:i')

#digital_write4 = board.get_pin('d:4:o')
#digital_write5 = board.get_pin('d:5:p')
#digital_write6 = board.get_pin('d:6:p')


#digital_write4.write(0)
time.sleep(0.2) #tempo de espera para que exista o primeiro valor válido
RawValue1 = None
RawValue5 = None

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [
            [sg.Text('Sensor Sharp 2Y0A21 F 44'),
            sg.Text('None',expand_x=True,key='-TEXTAI1-',justification='right',auto_size_text=True)],
            [sg.ProgressBar(100, orientation='h', size=(50,12), key='-progressbar_AI1-',expand_x=True)],
            [sg.Text('Sensor DFRobot'),
            sg.Text('None',expand_x=True,key='-TEXTAI5-',justification='right',auto_size_text=True)],
            [sg.ProgressBar(100, orientation='h', size=(50,12), key='-progressbar_AI5-',expand_x=True)],
            [sg.Push(),sg.Button('Ok'), sg.Button('Sair'),sg.Push()]
            ]

# Create the Window
window = sg.Window('Medição de Distância (cm)', layout)
# Event Loop to process "events" and get the "values" of the inputs


while True:
    event, values = window.read(timeout=1000)
    
    progressbar_AI1=window['-progressbar_AI1-']
    progressbar_AI5=window['-progressbar_AI5-']
    
    
    RawValue1 = analog_read1.read()
    RawValue5 = analog_read5.read()
    #print('a1', int(float(RawValue1)*5))
    #print('a5', int(float(RawValue5)*5))
    
    
    #time.sleep(1.0)
    
    
    
    
    if event == sg.WIN_CLOSED or event == 'Sair': # if user closes window or clicks cancel
        # Close the serial connection to the Arduino
        board.exit()
        break
        
        

    if event == 'Ok':
        #janela que aparece
        sg.popup('Programa escrito em Python', 'GUI - PysimpleGui','Pyfirmata', title='Informação')
        
    progressbar_AI1.UpdateBar(RawValue1*100)
    progressbar_AI5.UpdateBar(RawValue5*100)
    window['-TEXTAI1-'].update(str(round(RawValue1*5*100,2)) + ' cm')
    window['-TEXTAI5-'].update(str(round(RawValue5*5*100,2)) + ' cm')
    
    
    
    
window.close()

