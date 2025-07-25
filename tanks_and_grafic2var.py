import time
import threading
import asyncio
import flet as ft
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from telemetrix import telemetrix

# Pinos analógicos
TEMP_PIN = 1
HUMIDITY_PIN = 5

# Criação da placa
board = telemetrix.Telemetrix()
analog_values = {TEMP_PIN: 0, HUMIDITY_PIN: 0}

# Callback para atualizar leitura
def callback(data):
    pin = data[1]
    value = data[2]
    analog_values[pin] = value

# Configuração dos pinos
board.set_pin_mode_analog_input(TEMP_PIN, callback=callback)
board.set_pin_mode_analog_input(HUMIDITY_PIN, callback=callback)

# Thread para manter leitura
def read_analog_values():
    while True:
        time.sleep(0.1)

threading.Thread(target=read_analog_values, daemon=True).start()

# Conversão
def voltage_to_temperature(voltage):
    return (voltage / 5.0) * 120  # 0 a 120 ºC

def voltage_to_humidity(voltage):
    return 20 + (voltage / 5.0) * 60  # 20 a 80 %

# Função principal
async def main(page: ft.Page):
    page.title = "Temperatura e Humidade - Flet + Telemetrix"
    page.theme_mode = ft.ThemeMode.DARK

    bar_width, bar_height = 280, 50

    # Textos
    temp_text = ft.Text(value="Temperatura: 0.0 ºC", size=16)
    humid_text = ft.Text(value="Humidade: 0.0 %", size=16)

    # Barras visuais
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

    # Gráfico (diminuído)
    times = list(range(100))
    temp_data = [0] * 100
    humid_data = [0] * 100

    fig, ax = plt.subplots(figsize=(6, 3))  # Reduzido: 600px x 300px aproximadamente
    ax.set_ylim(0, 130)
    ax.set_title("Leituras em tempo real")
    ax.set_xlabel("Amostras")
    ax.set_ylabel("Valor")
    line_temp, = ax.plot(times, temp_data, label="Temperatura (ºC)", color='red')
    line_humid, = ax.plot(times, humid_data, label="Humidade (%)", color='blue')
    ax.legend()
    ax.grid(True)

    chart = MatplotlibChart(fig, expand=True)

    # Botão de sair centrado com tema dark
    exit_btn = ft.ElevatedButton(
        text="Sair", 
        on_click=lambda _: page.window.close(),  # Altere para Page.window.close()
        icon=ft.Icons.EXIT_TO_APP,
)

    # Layout
    page.add(
        ft.Column([
            temp_text,
            temp_bar,
            humid_text,
            humid_bar,
            ft.Container(content=chart, padding=10, width=600, height=300),  # Gráfico compacto
            exit_btn
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    # Loop de atualização
    while True:
        # Conversão
        voltage_temp = analog_values[TEMP_PIN] * (5.0 / 1023)
        voltage_humid = analog_values[HUMIDITY_PIN] * (5.0 / 1023)

        temperature = voltage_to_temperature(voltage_temp)
        humidity = voltage_to_humidity(voltage_humid)

        # Atualiza texto
        temp_text.value = f"Temperatura: {temperature:.1f} ºC"
        humid_text.value = f"Humidade: {humidity:.1f} %"

        temp_value_text.value = f"{temperature:.1f} ºC"
        humid_value_text.value = f"{humidity:.1f} %"

        # Atualiza largura das barras
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
        await asyncio.sleep(0.5)

# Executa a aplicação
ft.app(target=main)
