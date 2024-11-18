from telemetrix import telemetrix
import flet as ft
import threading
import time
import asyncio

# Defina os pinos analógicos
ANALOG_PIN1 = 1
ANALOG_PIN5 = 5

# Crie uma instância do Telemetrix
board = telemetrix.Telemetrix()

# Dicionário para armazenar os valores analógicos e timestamps
analog_values = {ANALOG_PIN1: 0, ANALOG_PIN5: 0}
timestamps = {ANALOG_PIN1: "", ANALOG_PIN5: ""}

# Função de callback para atualizar os valores analógicos
def callback(data):
    pin = data[1]
    value = data[2]
    analog_values[pin] = value
    timestamps[pin] = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(data[3]))

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
    page.theme_mode = ft.ThemeMode.DARK  # Tema escuro

    # Cria os widgets para exibir os valores
    date_text = ft.Text(value="Data: None", size=12, color="white")
    time_text = ft.Text(value="Hora: None", size=12, color="white")
    
    progress_text_a1 = ft.Text(value="0.00 V", size=20, color="white")
    progress_text_a5 = ft.Text(value="0.00 V", size=20, color="white")

    # Labels "Valor analógico"
    label_a1 = ft.Text(value="Valor analógico A1", size=14, color="white")
    label_a5 = ft.Text(value="Valor analógico A5", size=14, color="white")

    # Cria os tanques personalizados (100px de largura)
    bar_width = 100
    bar_height = 200

    bar_a1_value = ft.Text(value="0 V", size=14, color="white")
    bar_a1 = ft.Container(
        content=ft.Stack(
            [
                ft.Container(width=bar_width, height=bar_height, bgcolor="blue"),  # Fundo azul
                ft.Container(width=bar_width, height=0, bgcolor="grey", alignment=ft.alignment.bottom_center),  # Preenchimento cinza
                ft.Container(content=bar_a1_value, alignment=ft.alignment.bottom_center)
            ]
        ),
        width=bar_width,
        height=bar_height,
    )

    bar_a5_value = ft.Text(value="0 V", size=14, color="white")
    bar_a5 = ft.Container(
        content=ft.Stack(
            [
                ft.Container(width=bar_width, height=bar_height, bgcolor="red"),  # Fundo vermelho
                ft.Container(width=bar_width, height=0, bgcolor="grey", alignment=ft.alignment.bottom_center),  # Preenchimento cinza
                ft.Container(content=bar_a5_value, alignment=ft.alignment.bottom_center)
            ]
        ),
        width=bar_width,
        height=bar_height,
    )
    
    # Botão de sair centrado com tema dark
    exit_button = ft.ElevatedButton(
        text="Sair", 
        on_click=lambda _: page.window_close(), 
        icon=ft.icons.EXIT_TO_APP,
    )

    # Adiciona os widgets à página
    page.add(
        ft.Column(
            [
                ft.Row([date_text, time_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row(
                    [
                        ft.Column(
                            [
                                label_a1,
                                bar_a1,
                                progress_text_a1,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Column(
                            [
                                label_a5,
                                bar_a5,
                                progress_text_a5,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=50,  # Espaçamento entre os tanques
                ),
                ft.Container(exit_button, alignment=ft.alignment.center),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    # Loop de atualização periódica
    try:
        while True:
            # Atualiza as alturas dos tanques com os valores analógicos
            bar_a1.content.controls[1].height = (analog_values[ANALOG_PIN1] / 1023) * bar_height  # Altura do preenchimento
            bar_a1.content.controls[2].content.value = f'{analog_values[ANALOG_PIN1] * (5.0 / 1023):.2f} V'
            
            bar_a5.content.controls[1].height = (analog_values[ANALOG_PIN5] / 1023) * bar_height  # Altura do preenchimento
            bar_a5.content.controls[2].content.value = f'{analog_values[ANALOG_PIN5] * (5.0 / 1023):.2f} V'
            
            # Atualiza o texto da data e hora
            timestamp = timestamps[ANALOG_PIN1]
            if timestamp:
                date, time_str = timestamp.split(' ')
                date_text.value = f'Data: {date}'
                time_text.value = f'Hora: {time_str}'

            # Atualiza os textos com os valores analógicos
            progress_text_a1.value = f'{analog_values[ANALOG_PIN1] * (5.0 / 1023):.2f} V'
            progress_text_a5.value = f'{analog_values[ANALOG_PIN5] * (5.0 / 1023):.2f} V'

            page.update()
            await asyncio.sleep(0.1)

    finally:
        # Encerrar a comunicação com o microcontrolador ao fechar a janela
        board.shutdown()

# Inicializa a aplicação Flet
ft.app(target=main)
