#https://github.com/labF212/pyhton-arduino/blob/master/telemetrix_PySimpleGUI_automatic_pwd.py
import PySimpleGUI as sg
#import threading
from telemetrix import telemetrix
import time


# some globals
# make sure to select a PWM pin
DIGITAL_PIN6 = 6
DIGITAL_PIN5 = 5

# Create a Telemetrix instance
board = telemetrix.Telemetrix()

# Set the DIGITAL_PIN as an output pin
board.set_pin_mode_analog_output(DIGITAL_PIN6)
board.set_pin_mode_analog_output(DIGITAL_PIN5)

# Function to update the LED brightness on Arduino
def update_led_brightness(pwm_value1, pwm_value2):
    board.analog_write(DIGITAL_PIN6, pwm_value1)
    board.analog_write(DIGITAL_PIN5, pwm_value2)

#Creates a layout with two sliders, with a description and present values of PWM
layout = [
    [sg.Text('LED in pin 6'), sg.Text('None', expand_x=True, key='-LED6-', justification='right', auto_size_text=True)],
    [sg.Slider((0, 100), orientation='h', s=(50, 15), disable_number_display=True, key='-SLIDER1-', expand_x=True)],
    [sg.Text('LED in pin 5'), sg.Text('None', expand_x=True, key='-LED5-', justification='right', auto_size_text=True)],
    [sg.Slider((0, 100), orientation='h', s=(50, 15), disable_number_display=True, key='-SLIDER2-', expand_x=True)],
    [sg.Push(),sg.Radio('Manual', 'control', default=True, key='manual'),
     sg.Radio('Automatic', 'control', key='automatic'), sg.Push()],
    [sg.Push(), sg.Button('Exit'), sg.Push()]
]

#creates a window Title
window = sg.Window('Arduino LED Light Control', layout, resizable=True, finalize=True)

#creates a window and refresh all data in 0,5s
while True:
    event, values = window.read(timeout=500)

    #Close app when click cross or botton Exit
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        board.shutdown()
        break
    
    #Capture the values of the slider (0 to 100)    
    value_slider1 = int(values['-SLIDER1-'] * 2.55)
    value_slider2 = int(values['-SLIDER2-'] * 2.55)

    #Write the converted values to arduino PWD pins
    if values['manual']:
        window.Element('-SLIDER1-').Update(visible=True)
        window.Element('-SLIDER2-').Update(visible=True)
        update_led_brightness(value_slider1, value_slider2)
        window['-LED6-'].update(f'{value_slider1} PWD')
        window['-LED5-'].update(f'{value_slider2} PWD')
    elif values['automatic']:
        #threading.Thread(target=Automatic,daemon=True).start()
        window.Element('-SLIDER1-').Update(visible=False)
        window.Element('-SLIDER2-').Update(visible=False)
        
        # Implement the automatic control logic here
        
        #Fading up and down...
        for i in range(255):
            board.analog_write(DIGITAL_PIN6, i)
            board.analog_write(DIGITAL_PIN5, 255 - i)  # Inverse value for pin 5
            time.sleep(.05)
            window['-LED6-'].update(i)  # Show the value of 
            window['-LED5-'].update(255-i)  # Update GUI to show that automatic mode is active
            window.refresh()
        
        for i in range(255, -1, -1):
            board.analog_write(DIGITAL_PIN6, i)
            board.analog_write(DIGITAL_PIN5, 255 - i)  # Inverse value for pin 5
            time.sleep(.05)
            window['-LED5-'].update(i)  # Update GUI to show that automatic mode is active
            window['-LED6-'].update(255-i)  # Update GUI to show that automatic mode is active
            window.refresh()
window.close()
