import PySimpleGUI as sg
import time
from telemetrix import telemetrix
import sys

# Some globals
# Make sure to select the analog pin numbers (A1 and A5)
ANALOG_PIN1 = 1
ANALOG_PIN5 = 5

# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

# Dictionary to store the analog values
analog_values = {ANALOG_PIN1: 0, ANALOG_PIN5: 0}

layout = [
    [sg.Text((''), key='-DATE-'), sg.Push(), sg.Text((''), key='-TIME-')],
    [sg.Text('Analog Reading in Pin A1:'),
     sg.ProgressBar(1024, orientation='h', size=(20, 20), key='-VALUE1-'),
     sg.Text('None', expand_x=True, key='-VALUEA1-', justification='right',
             auto_size_text=True)],
    [sg.Text('Analog Reading in Pin A5:'),
     sg.ProgressBar(1024, orientation='h', size=(20, 20), key='-VALUE5-'),
     sg.Text('None', expand_x=True, key='-VALUEA5-', justification='right',
             auto_size_text=True)],
    [sg.Push(), sg.Button('Exit'), sg.Push()]
]


def the_callback(data):
    analog_values[data[CB_PIN]] = data[CB_VALUE]
    
    global date
    global current_time
    date = time.strftime('%Y-%m-%d', time.localtime(data[CB_TIME]))
    current_time = time.strftime('%H:%M:%S', time.localtime(data[CB_TIME]))

# Create a Telemetrix instance
board = telemetrix.Telemetrix()
board.set_pin_mode_analog_input(ANALOG_PIN1, callback=the_callback)
board.set_pin_mode_analog_input(ANALOG_PIN5, callback=the_callback)
# creates a window Title
window = sg.Window('Arduino LED Light Manual Control)', layout, resizable=True,
                   finalize=True)
while True:
    event, values = window.read(10)  # faster refresh time

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        board.shutdown()
        sys.exit(0)

    voltage1 = analog_values[ANALOG_PIN1]
    window['-VALUE1-'].update(voltage1)
    voltage1a = voltage1 / (1023 / 5)
    window['-VALUEA1-'].update(f'{voltage1a:.2f} V')

    voltage5 = analog_values[ANALOG_PIN5]
    window['-VALUE5-'].update(voltage5)
    voltage5a = voltage5 / (1023 / 5)
    window['-VALUEA5-'].update(f'{voltage5a:.2f} V')
    
    window['-TIME-'].update(current_time)
    window['-DATE-'].update(date)

window.close()
