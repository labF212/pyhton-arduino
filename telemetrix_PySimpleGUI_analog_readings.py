import PySimpleGUI as sg
from telemetrix import telemetrix
import time
import threading

# Some globals
# Make sure to select the analog pin numbers (A1 and A5)
ANALOG_PIN1 = 1
ANALOG_PIN5 = 5

# Create a Telemetrix instance
board = telemetrix.Telemetrix()

# Dictionary to store the analog values
analog_values = {ANALOG_PIN1: 0, ANALOG_PIN5: 0}

# Function to read and update the analog values
def read_analog_values():
    while True:
        # Read analog values from Arduino
        
        analog_values[ANALOG_PIN1] = board.analog_read(ANALOG_PIN1) #Wrong function
        analog_values[ANALOG_PIN5] = board.analog_read(ANALOG_PIN5)
        time.sleep(0.5)

# Start the thread to read the analog values in the background
read_analog_thread = threading.Thread(target=read_analog_values, daemon=True)
read_analog_thread.start()

# Creates a layout with two progress bars, showing the analog readings
layout = [
    [sg.Text('Analog Reading in Pin A1:'), sg.ProgressBar(1024, orientation='h', size=(20, 20), key='-VALUE1-'),
     sg.Text('None', expand_x=True, key='-VALUEA1-', justification='right', auto_size_text=True)],
    [sg.Text('Analog Reading in Pin A5:'), sg.ProgressBar(1024, orientation='h', size=(20, 20), key='-VALUE5-'),
     sg.Text('None', expand_x=True, key='-VALUEA5-', justification='right', auto_size_text=True)],
    [sg.Push(), sg.Button('Exit'), sg.Push()]
]

# Creates a window title
window = sg.Window('Arduino Analog Readings', layout, resizable=True, finalize=True)

# Main GUI loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        board.shutdown()
        break

    # Update the analog values of the Progress Bars
    window['-VALUE1-'].update(analog_values[ANALOG_PIN1])
    window['-VALUE5-'].update(analog_values[ANALOG_PIN5])

    # Update the analog values and show them converted in numbers (Volts)
    window['-VALUEA1-'].update(f'{analog_values[ANALOG_PIN1]:.2f} V')
    window['-VALUEA5-'].update(f'{analog_values[ANALOG_PIN5]:.2f} V')

window.close()
