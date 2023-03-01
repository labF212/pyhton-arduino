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

# Tabela com as últimas 10 leituras
table_layout = [[sg.Text('Data', size=(10,1)), sg.Text('Hora', size=(10,1)), sg.Text('Sensor 1', size=(10,1)), sg.Text('Sensor 2', size=(10,1))]]
for i in range(10):
    table_layout.append([sg.Text('', size=(10,1), key=f'-DATE{i}-'), sg.Text('', size=(10,1), key=f'-TIME{i}-'), sg.Text('', size=(10,1), key=f'-SENSOR1{i}-'), sg.Text('', size=(10,1), key=f'-SENSOR2{i}-')])

layout = [
    [sg.Text(datetime.datetime.now().strftime(f'{DATE_FORMAT}'), font=('Helvetica', 14), key='-DATE-'),sg.Push(),
    sg.Text(datetime.datetime.now().strftime(f'{TIME_FORMAT}'), font=('Helvetica', 14), key='-TIME-')],
    [sg.Text('Sensor Radio-Frequência Infravermelho - Sharp  2Y0A21 F 44 (10cm a 80cm)'),
     sg.Text('None', expand_x=True, key='-TEXTAI1-', justification='right', auto_size_text=True)],
    [sg.ProgressBar(100, orientation='h', size=(50, 12), key='-progressbar_AI1-', expand_x=True)],
    [sg.Text('Sensor Ultrassónico - DFRobot SEN0307 (2cm a 500cm)'),
     sg.Text('None', expand_x=True, key='-TEXTAI5-', justification='right', auto_size_text=True)],
    [sg.ProgressBar(100, orientation='h', size=(50, 12), key='-progressbar_AI5-', expand_x=True)],
    [sg.Push(), sg.Button('Sobre'), sg.Button('Sair'), sg.Button('', key='alarme', button_color=('white', 'green'),size=(15,1)),
     sg.Push()],
    [sg.Push(),sg.Table(values=[], headings=['  Data  ', '  Hora  ', 'Sensor 1', 'Sensor 2'], max_col_width=25, background_color='grey',
          auto_size_columns=True, display_row_numbers=False, justification='center',
          num_rows=10, key='-TABLE-', row_height=25, tooltip='Últimas 10 leituras'),sg.Push()],
]



window = sg.Window('Medição de Distância (cm)', layout,resizable=True,finalize = True)

window.bind("<Escape>", "-ESCAPE-")
window.bind("<s>", "-SOBRE-")

dados = []

while True:
    event, values = window.read(timeout=1000)

    progressbar_AI1 = window['-progressbar_AI1-']
    progressbar_AI5 = window['-progressbar_AI5-']

    RawValue1 = analog_read1.read()
    RawValue5 = analog_read5.read()

    if event in (sg.WINDOW_CLOSED, "-ESCAPE-",'Sair'):
    #if event == sg.WIN_CLOSED or event == 'Sair' or event =='-ESCAPE-':
        board.exit()
        break

    if event == 'S&obre' or event == '-SOBRE-':
        sg.popup('Programa escrito em Python', 'GUI - PysimpleGui',
                 'Pyfirmata - Biblioteca de comunicação com o arduino',
                 'Standard Firmata - Programa carregado no arduino', 
                 title='Informação')
        
    progressbar_AI1.UpdateBar(RawValue1 * 100)
    progressbar_AI5.UpdateBar(RawValue5 * 100)
    
    valor_medido_sensorAI1= round((6762/(RawValue1 * 1023-9)-4),2) #em cm
    valor_medido_sensorAI5= round((RawValue5 * 5 * 100),2) #em cm
    
    window['-TEXTAI1-'].update(str(valor_medido_sensorAI1) + ' cm')
    #window['-TEXTAI1-'].update(str(round(RawValue1 * 5 * 100, 2)) + ' cm')
    #cmValue = (6762/(sensorValue-9))-4
    window['-TEXTAI5-'].update(str(valor_medido_sensorAI5) + ' cm')

    # verifica o status do LED 13 e atualiza o botão de alarme
    # Acender LED no pino digital 13 se o valor lido do pino analógico A5 for superior a 0.8
    if valor_medido_sensorAI5 < 10 or valor_medido_sensorAI5 > 80:
        digital_write13.write(1)
        window['alarme'].update('Alarme Ligado   ', button_color=('white', 'red'))
    else:
        digital_write13.write(0)
        window['alarme'].update('Alarme Desligado', button_color=('white', 'green'))
        
    
    
    # atualiza a hora atual e a data
    now = datetime.datetime.now()
    window['-DATE-'].update(now.strftime(f'{DATE_FORMAT}'))
    window['-TIME-'].update(now.strftime(f'{TIME_FORMAT}'))
    
    # Adiciona os dados à lista
    dados.append([datetime.datetime.now().strftime("%Y-%m-%d"), datetime.datetime.now().strftime("%H:%M:%S"), f"{valor_medido_sensorAI1:.1f}", f"{valor_medido_sensorAI5:.1f}"])

    # Atualiza a tabela com as últimas 10 leituras
    window["-TABLE-"].update(values=dados[-10:])

window.close()
