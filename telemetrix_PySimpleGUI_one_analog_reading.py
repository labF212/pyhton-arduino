import PySimpleGUI as sg
import time
import threading
from telemetrix import telemetrix

# Some globals
# Make sure to select the analog pin number (A1)
ANALOG_PIN = 1

# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

# Create a Telemetrix instance
board = telemetrix.Telemetrix()

# Function to update the analog value in the GUI
def update_analog_value(window, value):
    window['-VALUE-'].update(value)

# Callback function to update the analog value
def the_callback(data):
    global analog_value
    analog_value = data[CB_VALUE]
    update_analog_value(window, analog_value)

def analog_in(my_board, window, pin):
    """
     This function establishes the pin as an
     analog input. Any changes on this pin will
     be reported through the call back function.

     :param my_board: a telemetrix instance
     :param window: PySimpleGUI window
     :param pin: Arduino pin number
     """

    # set the pin mode
    my_board.set_pin_mode_analog_input(pin, differential=5, callback=the_callback)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_board.shutdown()
        sys.exit(0)

# Creates a layout with a progress bar, showing the analog reading
layout = [
    [sg.Text('Analog Reading in Pin A1:'), sg.ProgressBar(1024, orientation='h', size=(20, 20), key='-VALUE-'),
     sg.Text('None', expand_x=True, key='-VALUEA1-', justification='right', auto_size_text=True)],
    [sg.Push(), sg.Button('Exit'), sg.Push()]
]

# Creates a window title
window = sg.Window('Arduino Analog Reading', layout, resizable=True, finalize=True)

# Start the thread to read the analog value in the background
analog_in_thread = threading.Thread(target=analog_in, args=(board, window, ANALOG_PIN), daemon=True)
analog_in_thread.start()

# Main GUI loop
while True:
    event, values = window.read(1000)

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        board.shutdown()
        break

    # Update the analog value and show it converted in numbers (Volts)
    voltage = analog_value / (1023/5)
    window['-VALUEA1-'].update(f'{voltage:.2f} V')

window.close()

