import time
import csv
from telemetrix import telemetrix
import flet as ft
import asyncio
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart

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

# Função principal do Flet
async def main(page: ft.Page):
    global min_range, max_range, sample_interval, distance_between_measurements

    page.title = "Leitura HC-SR04 com Telemetrix e Flet"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ALWAYS

    distance_text = ft.Text(value="Distância: 0.00 cm", size=16)
    bar_width, bar_height = 280, 50
    bar_a5_value = ft.Text(value="0.00 cm", size=14)
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

    # Criar gráfico de distância
    num_samples = 100
    times = list(range(num_samples))
    distances = [0] * num_samples

    fig, ax = plt.subplots()
    ax.set_xlim(0, num_samples - 1)
    ax.set_ylim(min_range, max_range)
    ax.set_title("Distância em Tempo Real")
    ax.set_xlabel("Tempo (amostras)")
    ax.set_ylabel("Distância (cm)")
    line, = ax.plot(times, distances, label="Distância", color='blue')
    ax.grid(axis='y', color='lightgrey', linestyle='--', linewidth=0.7)
    ax.set_yticks(range(min_range, max_range + 1, 20))
    ax.legend(loc="upper right")

    chart = MatplotlibChart(fig, expand=True)

    # Container com o gráfico
    graph_container = ft.Container(
        content=chart,
        padding=5,
        border_radius=10,
        border=ft.border.all(2),
        width=800,
        height=400
    )

    # Tabela de medições
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Distância (cm)")
        )],
        rows=create_measurement_table()
    )

    table_container = ft.Container(
        content=table,
        padding=5,
        border_radius=10,
        border=ft.border.all(2),
        width=350,
        height=400
    )

    buttons_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row([
                    ft.ElevatedButton(
                        text="Sair", icon=ft.Icons.EXIT_TO_APP, width=200,
                        tooltip="Sair do Programa",
                        on_click=lambda e: page.window.close()
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
    )

    page.add(
        ft.Column([
            distance_text,
            bar_a5,
            ft.Row([
                table_container,  # Container da tabela
                graph_container,  # Container com o gráfico
            ], alignment=ft.MainAxisAlignment.START),
            buttons_container
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

    board = telemetrix.Telemetrix()
    perform_readings(board, TRIGGER_PIN, ECHO_PIN)

    try:
        while True:
            # Atualiza a distância e o gráfico
            update_distance(page, bar_a5, bar_a5_value, distance_text)

            # Atualiza o gráfico com a nova distância
            distances.append(last_distance)
            distances.pop(0)
            line.set_ydata(distances)
            chart.update()

            # Atualiza a tabela de medições
            table.rows = create_measurement_table()

            await asyncio.sleep(0.5)
    finally:
        board.shutdown()

ft.app(target=main)