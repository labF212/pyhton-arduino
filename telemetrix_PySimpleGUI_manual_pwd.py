'''
This program is for controling LED's with Arduino, using Python and Telemetrix  
https://github.com/labF212/pyhton-arduino/edit/master/telemetrix_PySimpleGUI_manual_pwd.py
'''

import PySimpleGUI as sg #gui for Python
from telemetrix import telemetrix #protocol for connect devices, like Arduino


# some globals
# make sure to select a PWM pin
DIGITAL_PIN6 = 6
DIGITAL_PIN5 = 5

# Create a Telemetrix instance.
board = telemetrix.Telemetrix()

# Set the DIGITAL_PIN as an output pin
board.set_pin_mode_analog_output(DIGITAL_PIN6)
board.set_pin_mode_analog_output(DIGITAL_PIN5)


#Creates a layout with two sliders, with a description and present values of PWM

layout = [
    [sg.Text('LED in pin 6'),
     sg.Text('None', expand_x=True, key='-LED6-', justification='right', auto_size_text=True)],
    [sg.Slider((0,100), orientation='h', s=(50,15),disable_number_display=True,key='-SLIDER1-', expand_x=True)],
    [sg.Text('LED in pin 5'),
     sg.Text('None', expand_x=True, key='-LED5-', justification='right', auto_size_text=True)],
    [sg.Slider((0,100), orientation='h', s=(50,15),disable_number_display=True,key='-SLIDER2-', expand_x=True)],
    [sg.Push(),sg.Button('Exit'),sg.Push()]   
    ]

#creates a window Title
window = sg.Window('Arduino LED Light Manual Control)', layout, resizable=True, finalize=True)

#creates a window and refresh all data in 0,5s
while True:
    event, values = window.read(timeout=500)

    #Close app when click cross or botton Exit
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        board.shutdown()
        break

    #Capture the values of the slider (0 to 100)
    value_slider1= int ((values['-SLIDER1-'])*2.55)
    value_slider2= int ((values['-SLIDER2-'])*2.55)
    
    #Write the converted values to arduino PWD pins
    board.analog_write(DIGITAL_PIN6, value_slider1)
    board.analog_write(DIGITAL_PIN5, value_slider2)
    
    #Update the PWD values of the slider in the screen 
    window['-LED6-'].update(str(value_slider1)+" PWD")
    window['-LED4-'].update(str(value_slider2)+" PWD")
    
    
window.close()
