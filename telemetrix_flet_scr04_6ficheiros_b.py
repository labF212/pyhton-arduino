import time
import csv
from telemetrix import telemetrix
import flet as ft
import asyncio

# Configuração dos pinos do HC-SR04
TRIGGER_PIN = 9
ECHO_PIN = 10

# Variáveis globais
last_distance = None
measurements = []  # Lista para armazenar as últimas medições
error_message = ""
min_range = 0
max_range = 400
sample_interval = 5  # Valor inicial do intervalo em segundos
distance_between_measurements = 5  # Distância entre medidas inicial

# Callback para capturar a distância medida
def sonar_callback(data):
    global last_distance, error_message
    last_distance = data[2]  # Distância medida em cm
    error_message = ""  # Limpa a mensagem de erro, pois a leitura foi bem-sucedida

# Função para realizar leituras do sensor em tempo real
def perform_readings(board, trigger_pin, echo_pin):
    board.set_pin_mode_sonar(trigger_pin, echo_pin, sonar_callback)

# Função para atualizar o valor da barra gráfica e o texto da distância
def update_distance(page, bar_a5, bar_a5_value, distance_text):
    global error_message, min_range, max_range
    if last_distance is not None:
        distance_text.value = f"Distância: {last_distance:.2f} cm"
        if min_range <= last_distance <= max_range:
            bar_a5.content.controls[1].width = ((last_distance - min_range) / (max_range - min_range)) * 200
        else:
            bar_a5.content.controls[1].width = 200
            distance_text.value += " - Fora da Gama"

        bar_a5_value.value = f"{last_distance:.2f} cm"
        if len(measurements) >= 5:
            measurements.pop(0)
        current_time = time.strftime('%H:%M:%S', time.localtime())
        measurements.append([current_time, f"{last_distance:.2f} cm"])
    else:
        error_message = "Erro ao obter a distância."
    page.update()

# Função para criar a tabela de medições
def create_measurement_table():
    return [
        ft.DataRow(
            cells=[ft.DataCell(ft.Text(value=str(val))) for val in measurement]
        )
        for measurement in measurements
    ]

# Função para gravar medições
def save_measurements(file_name, page):
    global last_distance, error_message, sample_interval, min_range, max_range, distance_between_measurements

    # Calcula o número de amostras com base no intervalo e na distância entre medidas
    range_span = max_range - min_range  # Gama total de medida
    num_samples = max(1, range_span // distance_between_measurements)  # Número de amostras (pelo menos 1)
    additional_sample = max_range  # Valor final da gama de medida

    current_date = time.strftime('%d-%m-%Y', time.localtime())
    try:
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f'Medidas feitas em: {current_date}'])
            writer.writerow(['Ensaio Nº', 'Hora', 'Distância a Medir (cm)', 'Distância (cm)'])

            # Loop para gravar cada leitura
            for i in range(num_samples):
                time.sleep(sample_interval)  # Respeitar o intervalo entre leituras
                current_time = time.strftime('%H:%M:%S', time.localtime())
                distancia_a_medir = min_range + (i * distance_between_measurements)

                if last_distance is not None and min_range <= last_distance <= max_range:
                    writer.writerow([i + 1, current_time, f'{distancia_a_medir:.2f}', f'{last_distance:.2f}'])
                else:
                    writer.writerow([i + 1, current_time, f'{distancia_a_medir:.2f}', "Erro/Fora do intervalo"])

            # Adicionar a amostra final
            time.sleep(sample_interval)  # Respeitar o intervalo entre leituras
            current_time = time.strftime('%H:%M:%S', time.localtime())

            if last_distance is not None and min_range <= last_distance <= max_range:
                writer.writerow([num_samples + 1, current_time, f'{additional_sample:.2f}', f'{last_distance:.2f}'])
            else:
                writer.writerow([num_samples + 1, current_time, f'{additional_sample:.2f}', "Erro/Fora do intervalo"])

        # Exibir mensagem de sucesso na interface
        page.controls.append(
            ft.Text(value=f"Dados gravados em '{file_name}'.", size=14, color="green")
        )
        page.update()
    except Exception as e:
        # Exibir mensagem de erro na interface
        page.controls.append(
            ft.Text(value=f"Erro ao gravar no ficheiro: {str(e)}", size=14, color="red")
        )
        page.update()



# Função para atualizar o slider de intervalo de leitura
def update_range_slider(range_slider, page, range_slider_title):
    global min_range, max_range
    min_range = int(range_slider.start_value)
    max_range = int(range_slider.end_value)
    range_slider_title.value = f"Escolha a Gama de Medida do sensor ({min_range} cm a {max_range} cm)"
    page.update()

# Atualiza o intervalo de tempo com base no Dropdown
def update_sample_interval(value):
    global sample_interval
    sample_interval = int(value)

# Atualiza a distância entre medidas com base no Dropdown
def update_distance_between_measurements(value):
    global distance_between_measurements
    distance_between_measurements = int(value)

# Função principal do Flet
async def main(page: ft.Page):
    global min_range, max_range, sample_interval, distance_between_measurements

    page.title = "Leitura HC-SR04 com Telemetrix e Flet"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ALWAYS

    distance_text = ft.Text(value="Distância: 0.00 cm", size=16)
    bar_width, bar_height = 280, 50
    bar_a5_value = ft.Text(value="0.00 cm", size=14, color="white")
    bar_a5 = ft.Container(
        content=ft.Stack(
            [
                ft.Container(width=bar_width, height=bar_height, bgcolor="grey"),
                ft.Container(width=0, height=bar_height, bgcolor="red", alignment=ft.alignment.top_left),
                ft.Container(content=bar_a5_value, alignment=ft.alignment.center)
            ]
        ),
        width=bar_width,
        height=bar_height,
    )
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Distância (cm)"))
        ],
        rows=create_measurement_table()
    )

    # Adicionando range slider com valores atualizados dinamicamente
    range_slider_title = ft.Text(
        value=f"Escolha a Gama de Medida do sensor ({min_range} cm a {max_range} cm)", 
        size=16, 
        color=""
    )
    range_slider = ft.RangeSlider(
        min=0,
        max=400,
        start_value=min_range,
        end_value=max_range,
        divisions=40,
        label="{value} cm",
        on_change=lambda e: update_range_slider(range_slider, page, range_slider_title),
    )

    range_slider_container = ft.Container(
        content=range_slider,
        padding=30,  # Define o padding
    )

    # Dropdowns para intervalos e distância entre medidas
    interval_selector = ft.Dropdown(
        label="Intervalo entre amostras (em segundos)",
        value=str(sample_interval),
        options=[ft.dropdown.Option(str(i)) for i in range(1, 10)],  # Opções de 1 a 10 segundos
        on_change=lambda e: update_sample_interval(e.control.value),
    )

    distance_selector = ft.Dropdown(
        label="Distância entre medidas (em cm)",
        value=str(distance_between_measurements),
        options=[ft.dropdown.Option(str(i)) for i in [5, 10]],  # Opções de 5 e 10 cm
        on_change=lambda e: update_distance_between_measurements(e.control.value),
    )

    dropdown_container = ft.Row(
        controls=[interval_selector, distance_selector],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Botões de gravação
    buttons_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row([
                    ft.ElevatedButton(
                        text="Gravar Subida 1", icon=ft.Icons.SAVE, width=200,
                        tooltip="Gravar no ficheiro LeituraSubidaSonar1.csv",
                        on_click=lambda e: save_measurements("LeituraSubidaSonar1.csv", page)
                    ),
                    ft.ElevatedButton(
                        text="Gravar Subida 2", icon=ft.Icons.SAVE, width=200,
                        tooltip="Gravar no ficheiro LeituraSubidaSonar2.csv",
                        on_click=lambda e: save_measurements("LeituraSubidaSonar2.csv", page)
                    ),
                    ft.ElevatedButton(
                        text="Gravar Subida 3", icon=ft.Icons.SAVE, width=200,
                        tooltip="Gravar no ficheiro LeituraSubidaSonar3.csv",
                        on_click=lambda e: save_measurements("LeituraSubidaSonar3.csv", page)
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.ElevatedButton(
                        text="Gravar Descida 1", icon=ft.icons.SAVE, width=200,
                        tooltip="Gravar no ficheiro LeituraDescidaSonar1.csv",
                        on_click=lambda e: save_measurements("LeituraDescidaSonar1.csv", page)
                    ),
                    ft.ElevatedButton(
                        text="Gravar Descida 2", icon=ft.Icons.SAVE, width=200,
                        tooltip="Gravar no ficheiro LeituraDescidaSonar2.csv",
                        on_click=lambda e: save_measurements("LeituraDescidaSonar2.csv", page)
                    ),
                    ft.ElevatedButton(
                        text="Gravar Descida 3", icon=ft.Icons.SAVE, width=200,
                        tooltip="Gravar no ficheiro LeituraDescidaSonar3.csv",
                        on_click=lambda e: save_measurements("LeituraDescidaSonar3.csv", page)
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.ElevatedButton(
                        text="Sair", icon=ft.Icons.EXIT_TO_APP, width=200,
                        tooltip="Sair do Programa",
                        on_click=lambda e: page.window.close()
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
    )

    # Adicionando os elementos à página
    page.add(
        ft.Column([
            distance_text,
            bar_a5,
            range_slider_title,
            range_slider_container,
            dropdown_container,
            table,
            buttons_container
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

    board = telemetrix.Telemetrix()
    perform_readings(board, TRIGGER_PIN, ECHO_PIN)
    try:
        while True:
            update_distance(page, bar_a5, bar_a5_value, distance_text)
            table.rows = create_measurement_table()
            await asyncio.sleep(1.0)
    finally:
        board.shutdown()

ft.app(target=main)
