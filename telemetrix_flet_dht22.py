import time
import threading
import asyncio
import flet as ft
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from telemetrix import telemetrix

# Pino do DHT11
DHT_PIN = 2

# Criação da placa
board = telemetrix.Telemetrix()

# Variáveis globais para armazenar leituras
temperature = 0.0
humidity = 0.0

# Callback do DHT11
def dht_callback(data):
    global humidity, temperature
    humidity = data[2]
    temperature = data[3]

# Inicialização do DHT11
board.set_pin_mode_dht(DHT_PIN, dht_type=22, callback=dht_callback)

# Thread que mantém o programa vivo para leitura contínua do DHT
def maintain_readings():
    while True:
        time.sleep(2)

threading.Thread(target=maintain_readings, daemon=True).start()

# Função principal Flet
async def main(page: ft.Page):
    page.title = "Temperatura e Humidade - Flet + Telemetrix"
    page.theme_mode = ft.ThemeMode.DARK

    bar_width, bar_height = 280, 50

    temp_text = ft.Text(value="Temperatura: 0.0 ºC", size=16)
    humid_text = ft.Text(value="Humidade: 0.0 %", size=16)

    temp_value_text = ft.Text(value="0.0 ºC", size=14)
    humid_value_text = ft.Text(value="0.0 %", size=14)

    temp_bar = ft.Container(
        content=ft.Stack([
            ft.Container(width=bar_width, height=bar_height, bgcolor="grey"),
            ft.Container(width=0, height=bar_height, bgcolor="red", alignment=ft.alignment.top_left),
            ft.Container(content=temp_value_text, alignment=ft.alignment.center),
        ]),
        width=bar_width,
        height=bar_height,
    )

    humid_bar = ft.Container(
        content=ft.Stack([
            ft.Container(width=bar_width, height=bar_height, bgcolor="grey"),
            ft.Container(width=0, height=bar_height, bgcolor="blue", alignment=ft.alignment.top_left),
            ft.Container(content=humid_value_text, alignment=ft.alignment.center),
        ]),
        width=bar_width,
        height=bar_height,
    )

    times = list(range(100))
    temp_data = [0] * 100
    humid_data = [0] * 100

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.set_ylim(0, 100)
    ax.set_title("Leituras em tempo real")
    ax.set_xlabel("Amostras")
    ax.set_ylabel("Valor")
    line_temp, = ax.plot(times, temp_data, label="Temperatura (ºC)", color='red')
    line_humid, = ax.plot(times, humid_data, label="Humidade (%)", color='blue')
    ax.legend()
    ax.grid(True)

    chart = MatplotlibChart(fig, expand=True)

    exit_btn = ft.ElevatedButton(
        text="Sair", 
        on_click=lambda _: page.window.close(),
        icon=ft.Icons.EXIT_TO_APP,
    )

    page.add(
        ft.Column([
            temp_text,
            temp_bar,
            humid_text,
            humid_bar,
            ft.Container(content=chart, padding=10, width=600, height=300),
            exit_btn
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    while True:
        # Atualiza texto
        temp_text.value = f"Temperatura: {temperature:.1f} ºC"
        humid_text.value = f"Humidade: {humidity:.1f} %"

        temp_value_text.value = f"{temperature:.1f} ºC"
        humid_value_text.value = f"{humidity:.1f} %"

        # Atualiza barras
        temp_bar.content.controls[1].width = (temperature / 120) * bar_width
        humid_bar.content.controls[1].width = ((humidity - 20) / 60) * bar_width

        # Atualiza gráfico
        temp_data.append(temperature)
        humid_data.append(humidity)
        temp_data.pop(0)
        humid_data.pop(0)
        line_temp.set_ydata(temp_data)
        line_humid.set_ydata(humid_data)
        chart.update()

        page.update()
        await asyncio.sleep(2)

# Executa a aplicação
ft.app(target=main)
