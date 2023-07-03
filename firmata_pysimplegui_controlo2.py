import PySimpleGUI as sg
import pyfirmata
import datetime

# Format of the current time
TIME_FORMAT = "%H:%M:%S"

# Format of the current date
DATE_FORMAT = "%d/%m/%Y"

board = pyfirmata.Arduino('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)
it.start()

analog_read1 = board.get_pin('a:0:i') #mudar para a0
analog_read5 = board.get_pin('a:1:i') #mudar para a1
digital_write3 = board.get_pin('d:3:p') #mudar para d3
digital_write5 = board.get_pin('d:5:p') 
digital_write13 = board.get_pin('d:13:0')

RawValue1 = None
RawValue5 = None


sg.theme('DarkAmber')

data = [['', '', '', ''] for _ in range(10)]  # Initial data for the table
table_header = ['Data', 'Hora', 'Sensor 1', 'Sensor 2']

layout = [
    [sg.Text(datetime.datetime.now().strftime(f'{DATE_FORMAT}'), font=('Helvetica', 14), key='-DATE-'), sg.Push(),
     sg.Text(datetime.datetime.now().strftime(f'{TIME_FORMAT}'), font=('Helvetica', 14), key='-TIME-')],
    [sg.Text('Controlo de corrente do Transistor 1 - NPN TIP31C'),
     sg.Text('None', expand_x=True, key='-TRANS1-', justification='right', auto_size_text=True)],
    [sg.Slider((0,100), orientation='h', s=(50,15),disable_number_display=True,key='-SLIDER1-', expand_x=True)],
    [sg.Text('Controlo de corrente do Transistor 2 - NPN TIP31C'),
     sg.Text('None', expand_x=True, key='-TRANS2-', justification='right', auto_size_text=True)],
    [sg.Slider((0,100), orientation='h', s=(50,15),disable_number_display=True,key='-SLIDER2-', expand_x=True)],
    [sg.Text('Sensor de Temperatura 1 TMP36GT9Z - (-40 a 125ºC))'),
     sg.Text('None', expand_x=True, key='-TEMP1-', justification='right', auto_size_text=True)],
    [sg.ProgressBar(100, orientation='h', size=(50, 15), key='-progressbar_AI1-', expand_x=True)],
    [sg.Text('Sensor de Tempratura 2 TMP36GT9Z - (-40 a 125ºC))'),
     sg.Text('None', expand_x=True, key='-TEMP2-', justification='right', auto_size_text=True)],
    [sg.ProgressBar(100, orientation='h', size=(50, 15), key='-progressbar_AI5-', expand_x=True)],
    [sg.Push()],
    [sg.Column([[sg.Text(('Tabela de dados'), font=('Helvetica', 14), justification='center',expand_x=True)],
                [sg.Table(values=data, headings=table_header, max_col_width=500,
                          auto_size_columns=False, justification='center', expand_x=False,
                          display_row_numbers=False, num_rows=10, key='-TABLE-')]], justification='center')],
    [sg.Push(), sg.Button('Sobre'), sg.Button('Sair'), sg.Button('', key='alarme1', button_color=('white', 'green')),
     sg.Button('', key='alarme2', button_color=('white', 'green')),
     sg.Push()]
]                                                                                                                                                         


window = sg.Window('Controlo de Temperatura', layout, resizable=True, finalize=True)

last_readings = []  # List with the last 10 readings

while True:
    event, values = window.read(timeout=1000)

    progressbar_AI1 = window['-progressbar_AI1-']
    progressbar_AI5 = window['-progressbar_AI5-']

    RawValue1 = analog_read1.read()
    RawValue5 = analog_read5.read()

    if event == sg.WINDOW_CLOSED or event == 'Sair':
        board.exit()
        break

    if event == 'Sobre':
        sg.popup('Programa escrito em Python', 'GUI - PysimpleGui', 'Pyfirmata', title='Informação')

    if RawValue1 is not None:
        
        #-40 to 125ºC range= 125+40 = 165
        #rawvalue *5 * 100 --> 0 a 500
        # mapped value= 500/165 = 3,03
        #offset = -40
        #progressbar_AI1.UpdateBar(RawValue1 * 100) # 0 a 100%
        #valor_medido_sensorAI1 = round((RawValue1 * 5 * 100/3.03)-40, 2)
        #window['-TEMP1-'].update(str(valor_medido_sensorAI1) + ' ºC')
        
        #https://botland.store/content/147-Read-temperature-with-an-Arduino-and-sensor-TMP36GT9Z
        progressbar_AI1.UpdateBar(RawValue1 * 100) #conversao para 0 a 100%
        #TEMP = (VOLTS - 0.5) * 100; //conversion from voltage to temperature, the resolution of the sensor is 10 mV per degree, in addition, you should use an offset of 500 mV 
        valor_medido_sensorAI1 = round(((RawValue1 * 5) - 0.5)*100, 2)
        window['-TEMP1-'].update(str(valor_medido_sensorAI1) + ' ºC')

    

    if RawValue5 is not None:
        progressbar_AI5.UpdateBar(RawValue5 * 100)
        valor_medido_sensorAI5 = round(((RawValue5 * 5) - 0.5)*100, 2)
        window['-TEMP2-'].update(str(valor_medido_sensorAI5) + ' ºC')
        

    # Check the status of LED 13 and update the alarm button
    # Turn on LED on digital pin 13 if the value read from analog pin A5 is above 0.8
    if RawValue1 is not None and valor_medido_sensorAI1 > 100:
        #digital_write13.write(1)
        window['alarme1'].update('Alarme Ligado1   ', button_color=('white', 'red'))
    else:
        #digital_write13.write(0)
        window['alarme1'].update('Alarme Desligado1', button_color=('white', 'green'))
        
    if RawValue5 is not None and valor_medido_sensorAI5 > 100:
        #digital_write13.write(1)
        window['alarme2'].update('Alarme Ligado2   ', button_color=('white', 'red'))
    else:
        #digital_write13.write(0)
        window['alarme2'].update('Alarme Desligado2', button_color=('white', 'green'))
        
    


    # Update the current time and date
    now = datetime.datetime.now()
    window['-DATE-'].update(now.strftime(f'{DATE_FORMAT}'))
    window['-TIME-'].update(now.strftime(f'{TIME_FORMAT}'))
    window['-TRANS1-'].update(str(int(values['-SLIDER1-'])/20)+" V")
    window['-TRANS2-'].update(str(int(values['-SLIDER2-'])/20)+" V")

    # Update the table with the last 10 readings
    if len(last_readings) >= 10:
        last_readings.pop(0)  # Remove the oldest reading

    current_reading = {
        'date': now.strftime(DATE_FORMAT),
        'time': now.strftime(TIME_FORMAT),
        '-TEMP1-': str(valor_medido_sensorAI1) + ' ºC',
        '-TEMP2-': str(valor_medido_sensorAI5) + ' ºC'
    }
    last_readings.append(current_reading)

    for i, reading in enumerate(last_readings):
        data[i] = [reading['date'], reading['time'], reading['-TEMP1-'], reading['-TEMP2-']]
        window['-TABLE-'].update(data)

    if event == sg.WINDOW_CLOSED or event == 'Sair':
        board.exit()
        break


window.close()