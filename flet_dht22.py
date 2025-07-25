import time
import threading
import asyncio
import serial
import flet as ft
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart

# === CONFIGURAÇÃO SERIAL ===
SERIAL_PORT = "/dev/ttyACM0"  # <-- Substitua conforme necessário
BAUD_RATE = 115200

# === VARIÁVEIS GLOBAIS ===
temperature = 0.0
humidity = 0.0
sensor_status = "A aguardar dados..."
read_error = False

# === FUNÇÃO DE LEITURA SERIAL ===
def serial_reader():
    global temperature, humidity, sensor_status, read_error
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Tempo para o Arduino reiniciar

        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if line.startswith("OK"):
                try:
                    parts = line.split(',')
                    humidity = float(parts[1])
                    temperature = float(parts[2])
                    sensor_status = "Leitura OK"
                    read_error = False
                except:
                    sensor_status = "Erro ao interpretar dados"
                    read_error = True
            elif "error" in line.lower():
                sensor_status = f"Erro no sensor: {line}"
                read_error = True
            time.sleep(2)
    except serial.SerialException as e:
        sensor_status = f"Erro na porta serial: {e}"
        read_error = True

# Inicia thread da leitura
threading.Thread(target=serial_reader, daemon=True).start()

# === INTERFACE FLET ===
async def main(page: ft.Page):
    page.title = "Temperatura e Humidade - via Serial"
    page.theme_mode = ft.ThemeMode.DARK

    bar_width, bar_height = 280, 50

    temp_text = ft.Text(value="Temperatura: 0.0 ºC", size=16)
    humid_text = ft.Text(value="Humidade: 0.0 %", size=16)
    status_text = ft.Text(value=sensor_status, size=14, color="red")

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

    fig, ax = plt.subplots(figsize=(6, 4))
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
            status_text,
            temp_text,
            temp_bar,
            humid_text,
            humid_bar,
            ft.Container(content=chart, padding=10, width=600, height=500),
            exit_btn
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    while True:
        if read_error:
            status_text.value = sensor_status
            status_text.color = "red"
        else:
            status_text.value = sensor_status
            status_text.color = "green"

        temp_text.value = f"Temperatura: {temperature:.1f} ºC"
        humid_text.value = f"Humidade: {humidity:.1f} %"

        temp_value_text.value = f"{temperature:.1f} ºC"
        humid_value_text.value = f"{humidity:.1f} %"

        temp_bar.content.controls[1].width = (temperature / 100) * bar_width
        humid_bar.content.controls[1].width = (humidity / 100) * bar_width

        temp_data.append(temperature)
        humid_data.append(humidity)
        temp_data.pop(0)
        humid_data.pop(0)
        line_temp.set_ydata(temp_data)
        line_humid.set_ydata(humid_data)
        chart.update()

        page.update()
        await asyncio.sleep(1.5)

# Executa a aplicação
ft.app(target=main)
