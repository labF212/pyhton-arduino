import flet as ft
from telemetrix import telemetrix
import time
import threading

# Cria uma instância de Telemetrix para comunicação com o Arduino
board = telemetrix.Telemetrix()

# Define os pinos para os LEDs
PIN_RED = 4
PIN_YELLOW = 5
PIN_GREEN = 6

# Configura os pinos como saídas digitais
for pin in [PIN_RED, PIN_YELLOW, PIN_GREEN]:
    board.set_pin_mode_digital_output(pin)

# Variável de controle para a execução das sequências
running_sequence = None

# Função para atualizar o estado de um LED
def update_led(pin, color, led_icon):
    board.digital_write(pin, 1 if color else 0)
    led_icon.color = color if color else "black"
    led_icon.update()

# Função para desligar todos os LEDs
def desligar_todos(leds):
    for led in leds:
        update_led(led['pin'], None, led['icon'])

# Função para parar qualquer sequência em execução
def stop_all_sequences(leds):
    global running_sequence
    running_sequence = False
    time.sleep(0.1)  # Pequeno delay para garantir que a sequência atual pare
    desligar_todos(leds)

# Função para a sequência de "Semáforo"
def semaforo_sequence(leds):
    global running_sequence
    running_sequence = True
    while running_sequence:
        # Liga vermelho
        update_led(PIN_RED, "red", leds[0]['icon'])
        time.sleep(5)
        
        if not running_sequence:
            break

        # Liga amarelo e desliga vermelho
        update_led(PIN_RED, None, leds[0]['icon'])
        update_led(PIN_YELLOW, "yellow", leds[1]['icon'])
        time.sleep(2)

        if not running_sequence:
            break

        # Liga verde e desliga amarelo
        update_led(PIN_YELLOW, None, leds[1]['icon'])
        update_led(PIN_GREEN, "green", leds[2]['icon'])
        time.sleep(3)

        if not running_sequence:
            break

        # Desliga verde e volta ao vermelho
        update_led(PIN_GREEN, None, leds[2]['icon'])

# Função para "Avariado" (piscar o amarelo)
def avariado_sequence(leds):
    global running_sequence
    running_sequence = True
    while running_sequence:
        update_led(PIN_YELLOW, "yellow", leds[1]['icon'])
        time.sleep(0.5)
        update_led(PIN_YELLOW, None, leds[1]['icon'])
        time.sleep(0.5)

# Função para "Testar Semáforo" (pisca todos os LEDs 3 vezes)
def testar_semaforo(leds):
    global running_sequence
    running_sequence = True
    for _ in range(3):
        if not running_sequence:
            break
        for led in leds:
            update_led(led['pin'], led['color'], led['icon'])
        time.sleep(0.5)
        desligar_todos(leds)
        time.sleep(0.5)
    running_sequence = False  # Termina a sequência de teste

# Função principal da interface
def main(page: ft.Page):
    page.title = "Controlo de Semáforo"
    page.theme_mode = ft.ThemeMode.DARK

    # Título principal
    title = ft.Text("Controlo de Semáforo", size=24, weight="bold")

    # Define LEDs com cores e pinos específicos
    leds = [
        {"color": "red", "pin": PIN_RED, "icon": ft.Icon(name=ft.icons.CIRCLE, color="black", size=60)},
        {"color": "yellow", "pin": PIN_YELLOW, "icon": ft.Icon(name=ft.icons.CIRCLE, color="black", size=60)},
        {"color": "green", "pin": PIN_GREEN, "icon": ft.Icon(name=ft.icons.CIRCLE, color="black", size=60)}
    ]

    # Label do Semáforo e contêiner
    semaforo_label = ft.Text("Semáforo", size=18, weight="bold", text_align=ft.TextAlign.CENTER)
    semaforo_container = ft.Container(
        content=ft.Column(
            [led["icon"] for led in leds],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        padding=10,
        bgcolor="grey",
        border_radius=8,
        width=100,
        height=300,
        alignment=ft.alignment.center
    )

    # Funções dos botões
    def start_avariado(e):
        stop_all_sequences(leds)
        threading.Thread(target=avariado_sequence, args=(leds,)).start()

    def start_semaforo(e):
        stop_all_sequences(leds)
        threading.Thread(target=semaforo_sequence, args=(leds,)).start()

    def start_testar(e):
        stop_all_sequences(leds)
        threading.Thread(target=testar_semaforo, args=(leds,)).start()

    def stop_semaforo(e):
        stop_all_sequences(leds)

    # Define a largura máxima dos botões
    button_width = 180  # Exemplo, ajustar conforme necessidade

    # Label do Painel de Controlo
    comando_label = ft.Text("Painel de Controlo", size=18, weight="bold", text_align=ft.TextAlign.CENTER)
    avariado_button = ft.ElevatedButton("Avariado", on_click=start_avariado, width=button_width)
    semaforo_button = ft.ElevatedButton("Semáforo", on_click=start_semaforo, width=button_width)
    testar_button = ft.ElevatedButton("Testar Semáforo", on_click=start_testar, width=button_width)
    desligar_button = ft.ElevatedButton("Desligar Semáforo", on_click=stop_semaforo, width=button_width)

    # Contêiner para os botões
    buttons_container = ft.Container(
        content=ft.Column(
            [avariado_button, semaforo_button, testar_button, desligar_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        padding=10,
        bgcolor="yellow",
        border_radius=8,
        width=button_width + 40,
        alignment=ft.alignment.center
    )

    # Layout da página com os rótulos e contêineres alinhados
    page.add(
        title,
        ft.Row(
            [
                # Coluna para Painel de Controlo
                ft.Column(
                    [
                        comando_label,  # Label "Painel de Controlo" acima do contêiner de botões
                        buttons_container
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                # Coluna para Semáforo
                ft.Column(
                    [
                        semaforo_label,  # Label "Semáforo" acima do contêiner de LEDs
                        semaforo_container
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=50
        )
    )

    # Função para limpar na saída
    page.on_window_close = lambda e: board.shutdown()

# Run the app
ft.app(target=main)
