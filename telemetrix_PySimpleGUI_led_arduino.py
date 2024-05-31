import PySimpleGUI as sg
from telemetrix import telemetrix

# Define a function to control the LED
def control_led(state):
    if state == "ON":
        board.digital_write(13, 1)  # Turn LED on
    elif state == "OFF":
        board.digital_write(13, 0)  # Turn LED off

# Create an instance of Telemetrix
board = telemetrix.Telemetrix()

# Define the layout of the GUI
layout = [
    [sg.Text('LED Controller')],
    [sg.Button('ON'), sg.Button('OFF')],
    [sg.Exit()]
]

# Create the window
window = sg.Window('LED Controller', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event in ('ON', 'OFF'):
        control_led(event)

# Close the window and cleanup
window.close()
board.shutdown()
