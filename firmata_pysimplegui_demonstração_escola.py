import PySimpleGUI as sg
import pyfirmata
import datetime

# Formato da hora atual
TIME_FORMAT = "%H:%M:%S"

# Formato da data atual
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

layout = [
    [sg.Text(datetime.datetime.now().strftime(f'{DATE_FORMAT} - {TIME_FORMAT}'), font=('Helvetica', 14), justification='center', key='-DATE_TIME-')],
    [sg.Text('Sensor Sharp 2Y0A21 F 44'),
     sg.Text('None', expand_x=True, key='-TEXTAI1-', justification='right', auto_size_text=True)],
    [sg.ProgressBar(100, orientation='h', size=(50, 12), key='-progressbar_AI1-', expand_x=True)],
    [sg.Text('Sensor DFRobot'),
     sg.Text('None', expand_x=True, key='-TEXTAI5-', justification='right', auto_size_text=True)],
    [sg.ProgressBar(100, orientation='h', size=(50, 12), key='-progressbar_AI5-', expand_x=True)],
    [sg.Push(), sg.Button('Ok'), sg.Button('Sair'), sg.Button('', key='alarme', button_color=('white', 'green')),
     sg.Push()]
]

window = sg.Window('Medição de Distância (cm)', layout)

while True:
    event, values = window.read(timeout=1000)

    progressbar_AI1 = window['-progressbar_AI1-']
    progressbar_AI5 = window['-progressbar_AI5-']

    RawValue1 = analog_read1.read()
    RawValue5 = analog_read5.read()

    if event == sg.WIN_CLOSED or event == 'Sair':
        board.exit()
        break

    if event == 'Ok':
        sg.popup('Programa escrito em Python', 'GUI - PysimpleGui', 'Pyfirmata', title='Informação')

    progressbar_AI1.UpdateBar(RawValue1 * 100)
    progressbar_AI5.UpdateBar(RawValue5 * 100)
    window['-TEXTAI1-'].update(str(round(RawValue1 * 5 * 100, 2)) + ' cm')
    window['-TEXTAI5-'].update(str(round(RawValue5 * 5 * 100, 2)) + ' cm')

    # verifica o status do LED 13 e atualiza o botão de alarme
    # Acender LED no pino digital 13 se o valor lido do pino analógico A5 for superior a 0.8
    if RawValue5 > 0.8:
        digital_write13.write(1)
        window['alarme'].update('Alarme Ligado', button_color=('white', 'red'))
    else:
        digital_write13.write(0)
        window['alarme'].update('Alarme Desligado', button_color=('white', 'green'))
        
    
    
    # atualiza a hora atual e a data
    now = datetime.datetime.now()
    window['-DATE_TIME-'].update(now.strftime(f'{DATE_FORMAT} - {TIME_FORMAT}'))
    
window.close()
