from telemetrix import telemetrix
import flet as ft
from threading import Thread
import asyncio

# Variável global para armazenar o valor lido
analog_value = 0

def read_analog_data():
    global analog_value

    # Cria uma instância da classe Telemetrix
    board = telemetrix.Telemetrix()

    # Define o pino analógico que deseja ler
    analog_pin = 1  # Por exemplo, A0 no Arduino

    def analog_read_callback(data):
        """
        Callback function to process the analog read data.
        """
        global analog_value
        analog_value = data[2]
    
    # Configura o callback para o pino analógico
    board.set_pin_mode_analog_input(analog_pin, callback=analog_read_callback)

    # Mantém o script rodando para permitir a leitura contínua
    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Encerra a comunicação com o microcontrolador
        board.shutdown()

# Thread para leitura dos dados analógicos
analog_thread = Thread(target=read_analog_data)
analog_thread.daemon = True
analog_thread.start()

async def main(page: ft.Page):
    # Título da página
    page.title = "Leitura Analógica com Telemetrix e Flet"

    # Texto para exibir o valor analógico
    analog_text = ft.Text(value="Valor Analógico: 0", size=30)

    # Adiciona o texto à página
    page.add(analog_text)

    # Loop de atualização periódica
    while True:
        analog_text.value = f"Valor Analógico: {analog_value}"
        page.update()
        await asyncio.sleep(0.5)

# Inicializa a aplicação Flet
ft.app(target=main)
