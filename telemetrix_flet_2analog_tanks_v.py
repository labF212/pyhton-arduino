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

# Placa
board = telemetrix.Telemetrix()
analog_values = {TEMP_PIN: 0, HUMIDITY_PIN: 0}

# Callback
def callback(data):
    pin = data[1]
    value = data[2]
    analog_values[pin] = value

board.set_pin_mode_analog_input(TEMP_PIN, callback=callback)
board.set_pin_mode_analog_input(HUMIDITY_PIN, callback=callback)

def read_analog_values():
    while True:
        time.sleep(0.1)

threading.Thread(target=read_analog_values, daemon=True).start()

def voltage_to_temperature(voltage):
    return (voltage / 5.0) * 120

def voltage_to_humidity(voltage):
    return 20 + (voltage / 5.0) * 60

async def main(page: ft.Page):
    page.title = "Temperatura e Humidade - Barras Verticais"
    page.theme_mode = ft.ThemeMode.DARK

    max_temp = 120
    min_humid = 20
    max_humid = 80

    bar_width = 50
    bar_max_height = 200

    # Textos
    temp_value_text = ft.Text(value="0.0 ºC", size=14)
    humid_value_text = ft.Text(value="0.0 %", size=14)

    # Barras verticais
    temp_bar = ft.Container(
        content=ft.Column([
            ft.Container(height=bar_max_height, width=bar_width, bgcolor="grey",
                content=ft.Column([
                    ft.Container(height=0, width=bar_width, bgcolor="red", alignment=ft.alignment.bottom_center),
                ], alignment=ft.MainAxisAlignment.END)
            ),
            temp_value_text
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    )

    humid_bar = ft.Container(
        content=ft.Column([
            ft.Container(height=bar_max_height, width=bar_width, bgcolor="grey",
                content=ft.Column([
                    ft.Container(height=0, width=bar_width, bgcolor="blue", alignment=ft.alignment.bottom_center),
                ], alignment=ft.MainAxisAlignment.END)
            ),
            humid_value_text
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    )

    # Referências para mudar dinamicamente
    temp_fill = temp_bar.content.controls[0].content.controls[0]
    humid_fill = humid_bar.content.controls[0].content.controls[0]

    # Gráfico
    times = list(range(100))
    temp_data = [0] * 100
    humid_data = [0] * 100

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.set_ylim(0, 130)
    ax.set_title("Leituras em tempo real")
    ax.set_xlabel("Amostras")
    ax.set_ylabel("Valor")
    line_temp, = ax.plot(times, temp_data, label="Temperatura (ºC)", color='red')
    line_humid, = ax.plot(times, humid_data, label="Humidade (%)", color='blue')
    ax.legend()
    ax.grid(True)

    chart = MatplotlibChart(fig, expand=True)

    # Layout com barras ao lado do gráfico
    ft.Column([
    ft.Row([
        ft.Column([ft.Text("Temperatura"), temp_bar], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Column([ft.Text("Humidade"), humid_bar], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
    ], alignment=ft.MainAxisAlignment.CENTER)
])

    # Botão de saída
    exit_btn = ft.ElevatedButton(
        text="Sair",
        icon=ft.Icons.EXIT_TO_APP,  # <-- Correto!
        on_click=lambda _: (board.shutdown(), page.window.close())
    )

    layout = ft.Row([
            ft.Column([
                ft.Row([
                    ft.Column([ft.Text("Temperatura"), temp_bar], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Column([ft.Text("Humidade"), humid_bar], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ], alignment=ft.MainAxisAlignment.CENTER)
            ]),
            ft.Container(content=chart, padding=10, width=600, height=300),
        ], alignment=ft.MainAxisAlignment.CENTER)

    page.add(layout, exit_btn)

    # Atualização
    while True:
        v_temp = analog_values[TEMP_PIN] * (5.0 / 1023)
        v_hum = analog_values[HUMIDITY_PIN] * (5.0 / 1023)

        temperature = voltage_to_temperature(v_temp)
        humidity = voltage_to_humidity(v_hum)

        # Atualiza texto
        temp_value_text.value = f"{temperature:.1f} ºC"
        humid_value_text.value = f"{humidity:.1f} %"

        # Atualiza altura das barras
        temp_fill.height = (temperature / max_temp) * bar_max_height
        humid_fill.height = ((humidity - min_humid) / (max_humid - min_humid)) * bar_max_height

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

ft.app(target=main)
