import PySimpleGUI as sg
import time
import threading
from telemetrix import telemetrix

# Some globals
# Make sure to select the analog pin numbers (A1 and A5)
ANALOG_PIN1 = 1
ANALOG_PIN5 = 5

# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

# Create a Telemetrix instance
board = telemetrix.Telemetrix()

# Function to update the analog value in the GUI
def update_analog_value(window, value, key):
    window[key].update(value)

# Callback function to update the analog value
def the_callback(data, key):
    global analog_values
    global current_time
    global date
    analog_values[data[CB_PIN]] = data[CB_VALUE]
    voltage = analog_values[data[CB_PIN]]
    date = time.strftime('%Y-%m-%d', time.localtime(data[CB_TIME]))
    current_time = time.strftime('%H:%M:%S', time.localtime(data[CB_TIME]))
    # update_analog_value(window, f'{voltage:.2f} V', key)

def analog_in(my_board, window, pin, key):
    """
     This function establishes the pin as an
     analog input. Any changes on this pin will
     be reported through the call back function.

     :param my_board: a telemetrix instance
     :param window: PySimpleGUI window
     :param pin: Arduino pin number
     :param key: Key for the element to update in the GUI
     """

    # set the pin mode
    my_board.set_pin_mode_analog_input(pin, differential=0, callback=lambda data: the_callback(data, key))

    '''
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        my_board.shutdown()
        sys.exit(0)
    '''

# Creates a layout with two progress bars, showing the analog readings
layout = [
    [sg.Text((''), key='-DATE-'), sg.Push(), sg.Text((''), key='-TIME-')],
    [sg.Text('Analog Reading in Pin A1:'), sg.ProgressBar(1024, orientation='h', size=(20, 20), key='-VALUE1-'),
     sg.Text('None', expand_x=True, key='-VALUEA1-', justification='right', auto_size_text=True)],
    [sg.Text('Analog Reading in Pin A5:'), sg.ProgressBar(1024, orientation='h', size=(20, 20), key='-VALUE5-'),
     sg.Text('None', expand_x=True, key='-VALUEA5-', justification='right', auto_size_text=True)],
    [sg.Push(), sg.Button('Exit'), sg.Push()]
]

# Creates a window title
window = sg.Window('Arduino Analog Readings', layout, resizable=True, finalize=True)

# Dictionary to store the analog values
analog_values = {ANALOG_PIN1: 0, ANALOG_PIN5: 0}

# Start the threads to read the analog values in the background
analog_in_thread1 = threading.Thread(target=analog_in, args=(board, window, ANALOG_PIN1, '-VALUEA1-'), daemon=True)
analog_in_thread1.start()

analog_in_thread5 = threading.Thread(target=analog_in, args=(board, window, ANALOG_PIN5, '-VALUEA5-'), daemon=True)
analog_in_thread5.start()

# Main GUI loop
while True:
    event, values = window.read(1000)

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        board.shutdown()
        break
    
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
