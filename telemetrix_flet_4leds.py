import flet as ft
from telemetrix import telemetrix

# Cria uma instância de Telemetrix para comunicar com o Arduino
board = telemetrix.Telemetrix()

# Define os pinos para os relés
PIN_4 = 4
PIN_5 = 5
PIN_6 = 6
PIN_13 = 13

# Configura os pinos como saídas digitais
for pin in [PIN_4, PIN_5, PIN_6, PIN_13]:
    board.set_pin_mode_digital_output(pin)

# Define uma função para controlar os LEDs
def control_led(pin, state, led_icon):
    if state == "ON":
        board.digital_write(pin, 1)  # Liga o LED
        led_icon.color = "green"  # Define o LED para verde
    elif state == "OFF":
        board.digital_write(pin, 0)  # Desliga o LED
        led_icon.color = "red"  # Define o LED para vermelho
    led_icon.update()

def main(page: ft.Page):
    page.title = "Controlo de Relés"
    page.theme_mode = ft.ThemeMode.DARK

    # Título
    title = ft.Text("Controlo de Relés", size=24, weight="bold")

    # Função auxiliar para criar um conjunto de botões e LED para cada relé
    def create_rele_controls(rele_number, pin):
        # LED ícone e rótulo
        led_icon = ft.Icon(name=ft.icons.CIRCLE, color="red", size=60)
        led_label = ft.Text(f"Relé {rele_number}", size=14, color="black")

        # Contêiner para o LED e o rótulo
        led_container = ft.Container(
            content=ft.Column(
                [led_icon, led_label],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=10,
            bgcolor="yellow",
            border_radius=8,
            width=120,
            height=100,
            alignment=ft.alignment.center
        )

        # Botões para ligar e desligar o relé
        ligar_button = ft.ElevatedButton(
            f"Ligar Relé {rele_number}",
            on_click=lambda e: control_led(pin, "ON", led_icon),
            icon=ft.icons.POWER,
            icon_color="green600",
            tooltip=f"Liga o Relé {rele_number}"
        )

        desligar_button = ft.ElevatedButton(
            f"Desligar Relé {rele_number}",
            on_click=lambda e: control_led(pin, "OFF", led_icon),
            icon=ft.icons.POWER_OFF,
            icon_color="red600",
            tooltip=f"Desliga o Relé {rele_number}"
        )

        # Contêiner para os botões
        buttons_container = ft.Container(
            content=ft.Row(
                [ligar_button, desligar_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            padding=10,
            bgcolor="yellow",
            border_radius=8,
            width=350,
            height=100,
            alignment=ft.alignment.center
        )

        # Retorna uma linha com os botões e o LED do relé
        return ft.Row(
            [buttons_container, led_container],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

    # Adiciona o título e as linhas de controle para cada relé à página
    page.add(
        title,
        ft.Row(
            [
                ft.Container(
                    content=ft.Text("Entradas", size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    width=350
                ),
                ft.Container(
                    content=ft.Text("Saídas", size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    width=120
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        create_rele_controls(1, PIN_4),
        create_rele_controls(2, PIN_5),
        create_rele_controls(3, PIN_6),
        create_rele_controls(4, PIN_13)
    )

    # Botão para fechar a aplicação
    exit_button = ft.ElevatedButton(
        'Exit',
        icon=ft.icons.EXIT_TO_APP,
        on_click=lambda e: page.window_close(),
        style=ft.ButtonStyle(padding=20)
    )

    # Adiciona o botão de saída
    page.add(ft.Row([exit_button], alignment=ft.MainAxisAlignment.CENTER))

    # Handle window close event to cleanup
    def on_window_close(e):
        board.shutdown()
    page.on_window_close = on_window_close

# Run the app
ft.app(target=main)
