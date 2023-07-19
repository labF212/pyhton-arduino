#import sys
import time
import PySimpleGUI as sg

from telemetrix import telemetrix

"""
Setup a pin for output and fade its intensity
"""

# some globals
# make sure to select a PWM pin
DIGITAL_PIN = 6
#DIGITAL_PIN = 4

# Create a Telemetrix instance.
board = telemetrix.Telemetrix()

# Set the DIGITAL_PIN as an output pin
board.set_pin_mode_analog_output(DIGITAL_PIN)


# When hitting control-c to end the program
# in this loop, we are likely to get a KeyboardInterrupt
# exception. Catch the exception and exit gracefully.

layout = [
    [sg.Text('LED in pin 6'),
     sg.Text('None', expand_x=True, key='-LED6-', justification='right', auto_size_text=True)],
    [sg.Slider((0,100), orientation='h', s=(50,15),disable_number_display=True,key='-SLIDER1-', expand_x=True)],
    [sg.Text('LED in pin 4'),
     sg.Text('None', expand_x=True, key='-LED64-', justification='right', auto_size_text=True)],
    [sg.Slider((0,100), orientation='h', s=(50,15),disable_number_display=True,key='-SLIDER2-', expand_x=True)],
    
]

window = sg.Window('Arduino LED Light Control', layout, resizable=True, finalize=True)

while True:
    event, values = window.read(timeout=500)

    if event == sg.WINDOW_CLOSED or event == 'Sair':
        board.shutdown()
        break

    value_slider1= int ((values['-SLIDER1-'])*2.55)
    value_slider2= int ((values['-SLIDER2-'])*2.55)
    
    board.analog_write(DIGITAL_PIN, value_slider1)
    #DIGITAL_PIN.write(value_slider2)
    #window['-LED6-'].update(str(int(values['-SLIDER1-']))+" ")
    window['-LED6-'].update(str(value_slider1)+" PWD")
    #window['-TRANS2-'].update(str(int(values['-SLIDER2-']))+" ")

'''
try:
    print('Fading up...')
    for i in range(255):
        board.analog_write(DIGITAL_PIN, i)
        time.sleep(.005)
    print('Fading down...')
    for i in range(255, -1, -1):
        board.analog_write(DIGITAL_PIN, i)
        time.sleep(.005)
'''

    
window.close()
