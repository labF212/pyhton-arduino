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

digital_write4 = board.get_pin('d:4:o')
digital_write5 = board.get_pin('d:5:p')
digital_write6 = board.get_pin('d:6:p')


digital_write4.write(0)
time.sleep(0.2) #tempo de espera para que exista o primeiro valor válido
RawValue1 = None
RawValue5 = None

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [
            [sg.Text('Potenciómetro AI1:'),
            sg.Text('None',expand_x=True,key='-TEXTAI1-',justification='center',auto_size_text=True)],
            [sg.ProgressBar(100, orientation='h', size=(50,12), key='progressbar_AI1',expand_x=True)],
            [sg.Text('Potenciómetro AI5:'),
            sg.Text('None',expand_x=True,key='-TEXTAI5-',justification='center',auto_size_text=True)],
            [sg.ProgressBar(100, orientation='h', size=(50,12), key='progressbar_AI5',expand_x=True)],
            [sg.Push(),sg.Button((' LED VERDE  '),key="led1"), sg.Button((' LED AMARELO  '),key="led2"), sg.Button((' LED VERMELHO  '),key="led3"),sg.Push()],
            [sg.Push(),sg.Button('Ok'), sg.Button('Sair'),sg.Push()]
            ]

# Create the Window
window = sg.Window('Variação da intensidade dos Leds através de Potenciómetros', layout)
# Event Loop to process "events" and get the "values" of the inputs


while True:
    event, values = window.read(timeout=1000)
    
    progressbar_AI1=window['progressbar_AI1']
    progressbar_AI5=window['progressbar_AI5']
    
    
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
    #time.sleep(1.0)
    digital_write4.write(1)
    window["led1"].update(button_color='green')
    
    
    
    if  RawValue1<=0.1:
         window["led2"].update(button_color=sg.theme_button_color_background())
    else:
        window["led2"].update(button_color='yellow')
    
    
    if  RawValue5<=0.1:
         window["led3"].update(button_color=sg.theme_button_color_background()) 
         
    else:
        #https://www.colorhexa.com/8b0000 tint color variation
        #ffeded,#ffd9d9,#ffc6c6,#ffb2b2,#ff9f9f
        s= "0000"
        a=  "D80000" # '#8B0000' '#a50000´
        b= int(float(RawValue5)*255)+40000
        # hex(int(a, 16)
        var_color = hex(int (a,16)+b)
        print("#"+var_color[2:])
        window["led3"].update(button_color="#"+var_color[2:]) #'red'
    
    
    if event == sg.WIN_CLOSED or event == 'Sair': # if user closes window or clicks cancel
        digital_write4.write(0)
        digital_write5.write(0)
        digital_write6.write(0)
        # Close the serial connection to the Arduino
        board.exit()
        break
        
        

    if event == 'Ok':
        #janela que aparece
        sg.popup('Programa escrito em Python', 'GUI - PysimpleGui','Pyfirmata', title='Informação')
        
    progressbar_AI1.UpdateBar(RawValue1*100)
    progressbar_AI5.UpdateBar(RawValue5*100)
    
    window['-TEXTAI1-'].update(str(round(RawValue1*5,2)) + 'V')
    window['-TEXTAI5-'].update(str(round(RawValue5*5,2)) + 'V')

window.close()