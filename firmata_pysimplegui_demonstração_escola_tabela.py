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

analog_read1 = board.get_pin('a:1:i')
analog_read5 = board.get_pin('a:5:i')
digital_write13 = board.get_pin('d:13:o')

RawValue1 = None
RawValue5 = None

sg.theme('DarkAmber')

data = [['', '', '', ''] for _ in range(10)]  # Initial data for the table
table_header = ['Data', 'Hora', 'Sensor 1', 'Sensor 2']

table_layout = [
    [sg.Table(values=data, headings=table_header, max_col_width=25,
              auto_size_columns=True, justification='left',
              display_row_numbers=False, num_rows=10, key='-TABLE-')]
]

table_window = sg.Window('Últimas 10 leituras', table_layout,finalize=True)

layout = [
    [sg.Text(datetime.datetime.now().strftime(f'{DATE_FORMAT}'), font=('Helvetica', 14), key='-DATE-'), sg.Push(),
     sg.Text(datetime.datetime.now().strftime(f'{TIME_FORMAT}'), font=('Helvetica', 14), key='-TIME-')],
    [sg.Text('Sensor Radio-Frequência Infravermelho - Sharp  2Y0A21 F 44 (10cm a 80cm)'),
     sg.Text('None', expand_x=True, key='-TEXTAI1-', justification='right', auto_size_text=True)],
    [sg.ProgressBar(100, orientation='h', size=(50, 12), key='-progressbar_AI1-', expand_x=True)],
    [sg.Text('Sensor Ultrassónico - DFRobot SEN0307 (2cm a 500cm)'),
     sg.Text('None', expand_x=True, key='-TEXTAI5-', justification='right', auto_size_text=True)],
    [sg.ProgressBar(100, orientation='h', size=(50, 12), key='-progressbar_AI5-', expand_x=True)],
    [sg.Push(), sg.Button('Sobre'), sg.Button('Sair'), sg.Button('', key='alarme', button_color=('white', 'green')),
     sg.Push()]
]

window = sg.Window('Medição de Distância (cm)', layout, resizable=True)

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
        progressbar_AI1.UpdateBar(RawValue1 * 100)
        valor_medido_sensorAI1 = round((6762 / (RawValue1 * 1023 - 9) - 4), 2)  # em cm
        window['-TEXTAI1-'].update(str(valor_medido_sensorAI1) + ' cm')

    if RawValue5 is not None:
        progressbar_AI5.UpdateBar(RawValue5 * 100)
        valor_medido_sensorAI5 = round((RawValue5 * 5 * 100), 2)  # em cm
        window['-TEXTAI5-'].update(str(valor_medido_sensorAI5) + ' cm')

    # verifica o status do LED 13 e atualiza o botão de alarme
    # Acender LED no pino digital 13 se o valor lido do pino analógico A5 for superior a 0.8
    if RawValue5 is not None and valor_medido_sensorAI5 < 10:
        digital_write13.write(1)
        window['alarme'].update('Alarme Ligado', button_color=('white', 'red'))
    else:
        digital_write13.write(0)
        window['alarme'].update('Alarme Desligado', button_color=('white', 'green'))

    # atualiza a hora atual e a data
    now = datetime.datetime.now()
    window['-DATE-'].update(now.strftime(f'{DATE_FORMAT}'))
    window['-TIME-'].update(now.strftime(f'{TIME_FORMAT}'))

    # Update the table with the last 10 readings
    if len(last_readings) >= 10:
        last_readings.pop(0)  # Remove the oldest reading

    current_reading = {
        'date': now.strftime(DATE_FORMAT),
        'time': now.strftime(TIME_FORMAT),
        'sensor1': str(valor_medido_sensorAI1) + ' cm',
        'sensor2': str(valor_medido_sensorAI5) + ' cm'
    }
    last_readings.append(current_reading)

    table_data = [[reading['date'], reading['time'], reading['sensor1'], reading['sensor2']] for reading in last_readings]
    table_window['-TABLE-'].update(table_data)

table_window.close()
window.close()
