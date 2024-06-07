from telemetrix import telemetrix
import flet as ft
import threading
import time
import asyncio  # Importa o módulo asyncio

# Defina os pinos analógicos
ANALOG_PIN1 = 1
ANALOG_PIN5 = 5

# Crie uma instância do Telemetrix
board = telemetrix.Telemetrix()

# Dicionário para armazenar os valores analógicos
analog_values = {ANALOG_PIN1: 0, ANALOG_PIN5: 0}

# Função de callback para atualizar os valores analógicos
def callback(data):
    pin = data[1]
    value = data[2]
    analog_values[pin] = value

# Configurar os pinos analógicos com callback
board.set_pin_mode_analog_input(ANALOG_PIN1, callback=callback)
board.set_pin_mode_analog_input(ANALOG_PIN5, callback=callback)

# Função para ler e atualizar os valores analógicos
def read_analog_values():
    while True:
        time.sleep(0.1)

# Iniciar a thread para ler os valores analógicos em segundo plano
read_analog_thread = threading.Thread(target=read_analog_values, daemon=True)
read_analog_thread.start()

# Função principal do Flet
async def main(page: ft.Page):
    # Configura o título da página
    page.title = "Leitura Analógica com Telemetrix e Flet"

    # Cria as barras de progresso e textos para exibir os valores
    progress_bar_a1 = ft.ProgressBar(value=0, width=400, color="blue")
    progress_text_a1 = ft.Text(value="None", size=20)
    
    progress_bar_a5 = ft.ProgressBar(value=0, width=400, color="blue")
    progress_text_a5 = ft.Text(value="None", size=20)
    
    exit_button = ft.ElevatedButton(text="Exit", on_click=lambda _: page.window_close())

    # Adiciona os widgets à página
    page.add(
        ft.Row([ft.Text("Analog Reading in Pin A1:"), progress_bar_a1, progress_text_a1], alignment="center"),
        ft.Row([ft.Text("Analog Reading in Pin A5:"), progress_bar_a5, progress_text_a5], alignment="center"),
        ft.Row([ft.Container(), exit_button, ft.Container()], alignment="center")
    )

    # Loop de atualização periódica
    while True:
        progress_bar_a1.value = analog_values[ANALOG_PIN1] / 1024
        progress_text_a1.value = f'{analog_values[ANALOG_PIN1] * (5.0 / 1023):.2f} V'
        
        progress_bar_a5.value = analog_values[ANALOG_PIN5] / 1024
        progress_text_a5.value = f'{analog_values[ANALOG_PIN5] * (5.0 / 1023):.2f} V'
        
        page.update()
        await asyncio.sleep(0.1)

    # Encerrar a comunicação com o microcontrolador ao fechar a janela
    board.shutdown()

# Inicializa a aplicação Flet
ft.app(target=main)
