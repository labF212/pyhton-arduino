import time
import csv
from telemetrix import telemetrix
import flet as ft
import threading
import asyncio

# Configuração dos pinos do HC-SR04
TRIGGER_PIN = 9
ECHO_PIN = 10

# Variáveis globais
last_distance = None
measurements = []  # Lista para armazenar as últimas medições
error_message = ""

# Callback para capturar a distância medida
def sonar_callback(data):
    """
    Callback para lidar com os dados do sensor HC-SR04.
    :param data: [report_type, trigger_pin, distance, timestamp]
    """
    global last_distance, error_message
    last_distance = data[2]  # Distância medida em cm
    error_message = ""  # Limpa a mensagem de erro, pois a leitura foi bem-sucedida

# Função para realizar leituras do sensor em tempo real
def perform_readings(board, trigger_pin, echo_pin):
    """
    Realiza leituras contínuas do sensor ultrassônico.
    :param board: Instância do Telemetrix
    :param trigger_pin: Pino TRIGGER no Arduino
    :param echo_pin: Pino ECHO no Arduino
    """
    # Configura os pinos e o callback
    board.set_pin_mode_sonar(trigger_pin, echo_pin, sonar_callback)

# Função para atualizar o valor da barra gráfica e o texto da distância
def update_distance(page, bar_a5, bar_a5_value, distance_text):
    global error_message
    if last_distance is not None:
        # Atualiza o texto com a distância
        distance_text.value = f"Distância: {last_distance:.2f} cm"
        
        # Atualiza a barra horizontal com base na distância
        if last_distance > 100:
            bar_a5.content.controls[1].width = 200  # Limita a barra a 100 cm
            distance_text.value += " - Fora da Gama"
        else:
            bar_a5.content.controls[1].width = (last_distance / 100) * 200  # Ajusta a largura com base na distância

        # Atualiza o valor exibido na barra
        bar_a5_value.value = f"{last_distance:.2f} cm"

        error_message = ""  # Limpa a mensagem de erro após uma leitura válida

        # Adiciona a medição à lista das últimas leituras
        if len(measurements) >= 10:
            measurements.pop(0)  # Remove a medição mais antiga, se houver mais de 10
        current_time = time.strftime('%H:%M:%S', time.localtime())
        measurements.append([current_time, f"{last_distance:.2f} cm"])
    else:
        # Se a distância não foi lida, mostra a mensagem de erro
        error_message = "Erro ao obter a distância."
    
    # Atualiza a interface
    page.update()

# Função para criar a tabela de medições
def create_measurement_table():
    table_data = []
    for measurement in measurements:
        # Cada "measurement" será uma linha da tabela
        row = ft.DataRow(
            cells=[ft.DataCell(ft.Text(value=str(val), size=14, color="white")) for val in measurement]
        )
        table_data.append(row)
    return table_data

# Função principal do Flet
async def main(page: ft.Page):
    page.title = "Leitura HC-SR04 com Telemetrix e Flet"
    page.theme_mode = ft.ThemeMode.DARK  # Tema escuro

    # Texto para mostrar a distância
    distance_text = ft.Text(value="Distância: 0.00 cm", size=16, color="white")

    # Tamanho da barra
    bar_width = 200
    bar_height = 50

    # Barra personalizada para mostrar a distância
    bar_a5_value = ft.Text(value="0.00 cm", size=14, color="white")
    bar_a5 = ft.Container(
        content=ft.Stack(
            [
                ft.Container(width=bar_width, height=bar_height, bgcolor="red"),  # Fundo vermelho
                ft.Container(width=0, height=bar_height, bgcolor="grey", alignment=ft.alignment.top_left),  # Preenchimento cinza
                ft.Container(content=bar_a5_value, alignment=ft.alignment.center)
            ]
        ),
        width=bar_width,
        height=bar_height,
    )

    # Tabela para exibir as últimas medições
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Distância (cm)"))
        ],
        rows=create_measurement_table()
    )

    # Botão para gravar dados
    save_button = ft.ElevatedButton(text="Ler e Gravar Dados", on_click=lambda e: read_and_save_data(page))

    # Botão para sair
    exit_button = ft.ElevatedButton(text="Sair", on_click=lambda e: page.window.close())

    # Adiciona o texto, a barra, a tabela e os botões na página
    page.add(
        ft.Column([
            distance_text,
            bar_a5,
            table,
            save_button,
            exit_button
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

    # Cria a instância do Telemetrix
    board = telemetrix.Telemetrix()

    # Inicia as leituras contínuas
    perform_readings(board, TRIGGER_PIN, ECHO_PIN)

    # Loop de atualização periódica
    try:
        while True:
            # Atualiza o valor da distância em tempo real
            update_distance(page, bar_a5, bar_a5_value, distance_text)
            table.rows = create_measurement_table()  # Atualiza a tabela com as últimas medições
            await asyncio.sleep(0.5)  # Espera 0,5 segundo entre as atualizações
    finally:
        # Encerra a comunicação com o Telemetrix ao fechar a janela
        board.shutdown()

# Função para ler e gravar dados ao pressionar o botão
def read_and_save_data(page):
    global last_distance, error_message

    # Nome do arquivo CSV
    csv_filename = "leituras_sonar.csv"

    # Registra a data para colocar como título no CSV
    current_date = time.strftime('%d-%m-%Y', time.localtime())

    # Cria e escreve o título no arquivo CSV
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f'Medidas feitas em: {current_date}'])
        writer.writerow(['Hora', 'Distância (cm)'])

        # Realiza 20 leituras e escreve no CSV
        for i in range(20):
            time.sleep(0.5)  # Espera 0,5 segundo entre as leituras
            if last_distance is not None:
                current_time = time.strftime('%H:%M:%S', time.localtime())
                writer.writerow([current_time, f'{last_distance:.2f}'])
            else:
                error_message = f"Leitura {i + 1}: Erro ao obter a distância."
                page.update()  # Atualiza a interface para exibir a mensagem de erro

    # Atualiza a interface com a mensagem
    page.add(ft.Text(value=f"Dados gravados em '{csv_filename}'."))
    page.update()

# Inicializa a aplicação Flet
ft.app(target=main)
