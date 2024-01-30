import PySimpleGUI as sg
import time
from telemetrix import telemetrix
import sys


# Format of the current time
TIME_FORMAT = "%H:%M:%S"
 
# Format of the current date
DATE_FORMAT = "%d/%m/%Y"

# Some globals
# Make sure to select the analog pin numbers (A1 and A5)
ANALOG_PIN3 = 0 #sensor de temperatura analógico em A3
ANALOG_PIN5 = 2 #sensor de temperatura analógico em A5
# make sure to select a PWM pin
DIGITAL_PIN5 = 5 #mudar para 9   Relé liga/desliga válvula esq
DIGITAL_PIN6 = 6 #mudar para 10 Relé liga/desliga válvula dir



# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3

# Dictionary to store the analog values
analog_values = {ANALOG_PIN3: 0, ANALOG_PIN5: 0}
digital_values = {DIGITAL_PIN5: 0, DIGITAL_PIN6: 0}


sg.theme('DarkAmber')

layout = [
    [sg.Text((''), key='-DATE-'), sg.Push(), sg.Text((''), key='-TIME-')],
    #sliders
    [sg.Text('LED in pin 6'), sg.Text('None', expand_x=True, key='-LED6-', justification='right', auto_size_text=True)],
    [sg.Slider((0, 100), orientation='h', s=(50, 15), disable_number_display=True, key='-SLIDER1-', expand_x=True)],
    [sg.Text('LED in pin 5'), sg.Text('None', expand_x=True, key='-LED5-', justification='right', auto_size_text=True)],
    [sg.Slider((0, 100), orientation='h', s=(50, 15), disable_number_display=True, key='-SLIDER2-', expand_x=True)],
    
    #Leitura de temperaturas
    [sg.Text('Sensor de Temperatura 1 TMP36GT9Z - (-40 a 125ºC))'),
     sg.Text('None', expand_x=True, key='-TEMP1-', justification='right', auto_size_text=True)],
    [sg.ProgressBar(100, orientation='h', size=(50, 15), key='-AI1-', expand_x=True)],
    [sg.Text('Sensor de Temperatura 2 TMP36GT9Z - (-40 a 125ºC))'),
     sg.Text('None', expand_x=True, key='-TEMP2-', justification='right', auto_size_text=True)],
    [sg.ProgressBar(100, orientation='h', size=(50, 15), key='-AI5-', expand_x=True)],
    
     

    [sg.Push(), sg.Button('Sobre'),sg.Button('Exit'), sg.Push()]
]


def the_callback(data):
    analog_values[data[CB_PIN]] = data[CB_VALUE]
    digital_values[data[CB_PIN]] = data[CB_VALUE]
    
    global date
    global current_time
    date = time.strftime('%Y-%m-%d', time.localtime(data[CB_TIME]))
    current_time = time.strftime('%H:%M:%S', time.localtime(data[CB_TIME]))

# Create a Telemetrix instance
board = telemetrix.Telemetrix()
board.set_pin_mode_analog_input(ANALOG_PIN3, callback=the_callback)
board.set_pin_mode_analog_input(ANALOG_PIN5, callback=the_callback)

# Set the DIGITAL_PIN as an output pin
board.set_pin_mode_digital_output(DIGITAL_PIN5)
board.set_pin_mode_digital_output(DIGITAL_PIN6)

# Function to update the LED brightness on Arduino
def update_led_brightness(pwm_value1, pwm_value2):
    board.analog_write(DIGITAL_PIN5, pwm_value1)
    board.analog_write(DIGITAL_PIN6, pwm_value2)

# creates a window Title
window = sg.Window('Controlo Manual de Temperatura', layout, resizable=True,
                   finalize=True)
while True:
    event, values = window.read(1000)  # window refresh time

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        board.shutdown()
        sys.exit(0)

    if event == 'Sobre':
        sg.popup('Programa escrito em Python', 'GUI - PysimpleGui', 'Comunicação Arduino - Telemetrix', title='Informação')

      #Capture the values of the slider (0 to 100)    
    value_slider1 = values['-SLIDER1-']
    value_slider2 = values['-SLIDER2-']

    window['-LED6-'].update(f'{value_slider1/20:.1f} V')
    window['-LED5-'].update(f'{value_slider2/20:.1f} V')
    
    #Escrever os valores do pwd para as saídas digitais 
    #board.analog_write(DIGITAL_PIN6, value_slider1)
    #board.analog_write(DIGITAL_PIN5, value_slider2)
    
    '''Calculate temperature sensor TMP36GT9Z range -40 a 125ºC
    
    analog values 0 to 1023
    convert to 0-5V - divide by 5: 1023/5 = 6,2
    Calculo do range:  -40 to 125ºC range= 125+40 = 165
        
        mapped value= 165/5 = 33
        offset = -40
        temperatura = tensao*33 - (165-40/(33)) 
    
    '''

    #Leitura da Temperatura
    voltage1 = analog_values[ANALOG_PIN3]      
    window['-AI1-'].update(voltage1/6.2)
    temperatura1=(voltage1/204.6*33)-((165-40)/33)   
    window['-TEMP1-'].update(f'{temperatura1:.1f} ºC')   
  
    voltage5 = analog_values[ANALOG_PIN5]
    window['-AI5-'].update(voltage5/6.22)
    temperatura5=(voltage5/204.6*33)-((165-40)/33)
    
    window['-TEMP2-'].update(f'{temperatura5:.1f} ºC')
    
    window['-TIME-'].update(current_time)
    window['-DATE-'].update(date)

window.close()