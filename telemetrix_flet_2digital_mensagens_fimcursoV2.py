import flet as ft
from telemetrix import telemetrix
import signal

# Create an instance of Telemetrix
board = telemetrix.Telemetrix()

# Define the pins
PIN_4 = 4
PIN_5 = 5
ANALOG_PIN2 = 2
ANALOG_PIN3 = 3

# Initialize the analog values dictionary
analog_values = {ANALOG_PIN2: 0, ANALOG_PIN3: 0}


# Define a function to control the LEDs and update text
def control_led(pin, state, text_widget):
    if state == "ON":
        board.digital_write(pin, 1)  # Turn LED on
        text_widget.value = "A avançar" if pin == PIN_4 else "A recuar"
    elif state == "OFF":
        board.digital_write(pin, 0)  # Turn LED off
        text_widget.value = ""
    text_widget.update()


# Function to update analog values and LED colors
def update_analog_values(pin, led_avancar, led_recuar):
    # Verifying that the LEDs are already added to the page
    if led_avancar and led_recuar:
        if pin == ANALOG_PIN2:
            value = analog_values[ANALOG_PIN2]
            led_avancar.color = "red" if value > 512 else "green"
            led_avancar.update()  # Update the LED after page setup
        elif pin == ANALOG_PIN3:
            value = analog_values[ANALOG_PIN3]
            led_recuar.color = "red" if value > 512 else "green"
            led_recuar.update()  # Update the LED after page setup


# Telemetrix callback functions
def analog_callback(data):
    pin = data[1]
    value = data[2]
    analog_values[pin] = value
    # Only update if the LEDs are initialized
    update_analog_values(pin, led_avancar_global, led_recuar_global)


# Function to handle cleanup on exit
def cleanup(*args):
    board.digital_write(PIN_4, 0)  # Turn off PIN_4
    board.digital_write(PIN_5, 0)  # Turn off PIN_5
    board.shutdown()


# Set pin modes
board.set_pin_mode_digital_output(PIN_4)
board.set_pin_mode_digital_output(PIN_5)
board.set_pin_mode_analog_input(ANALOG_PIN2, callback=analog_callback)
board.set_pin_mode_analog_input(ANALOG_PIN3, callback=analog_callback)


# Global variables for LEDs
led_avancar_global = None
led_recuar_global = None


def main(page: ft.Page):
    page.title = "Comando de Arduino através de Python/Telemetrix/Flet"
    global led_avancar_global, led_recuar_global

    # Text widgets to display the state
    text_avancar = ft.Text("", width=100)
    text_recuar = ft.Text("", width=100)

    # LED widgets to indicate state (ensure they are created here)
    led_avancar_global = ft.Icon(name="fiber_manual_record", color="green", size=40, tooltip="Pin 2 Analógico")
    led_recuar_global =  ft.Icon(name="fiber_manual_record", color="green", size=40, tooltip="Pin 3 Analógico")

    # Add the title at the top of the page
    page.add(ft.Text("Avanço e Recuo do Cilindro", style="headlineLarge", weight="bold", color="White"))

    # "Comando" container (onde os botões e frases estarão)
    comando_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Circuito de Comando", style="headlineSmall", weight="bold", color="black"),
                ft.Row(
                    [
                        # Frases
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Avanço do cilindro", color="black"),
                                    ft.Text("Recuo do cilindro", color="black"),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=10,
                        ),
                        # Botões (em layout 2x2)
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "ON",
                                                on_click=lambda e: control_led(PIN_4, "ON", text_avancar),
                                                tooltip="Pin 4 Digital",
                                            ),
                                            ft.ElevatedButton(
                                                "OFF",
                                                on_click=lambda e: control_led(PIN_4, "OFF", text_avancar),
                                            ),
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "ON",
                                                on_click=lambda e: control_led(PIN_5, "ON", text_recuar),
                                                tooltip="Pin 5 Digital",
                                            ),
                                            ft.ElevatedButton(
                                                "OFF",
                                                on_click=lambda e: control_led(PIN_5, "OFF", text_recuar),
                                            ),
                                        ]
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            bgcolor="blue",
                            padding=10,
                            border_radius=8,
                        ),
                        # Ações
                        ft.Container(
                            content=ft.Column(
                                [
                                    text_avancar,
                                    text_recuar,
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=10,
                        ),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        bgcolor="red",
        height=170,
        padding=20,
        border_radius=8,
    )

    # "Sensor" container (onde os LEDs vão ser mostrados)
    sensor_container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Sensor", style="headlineSmall", weight="bold", color="black"),
                ft.Container(
                    content=ft.Column(
                        [
                            # Only two LEDs displayed here
                            ft.Row([ft.Text("Avançado:", color="black", width=80), led_avancar_global]),
                            ft.Row([ft.Text("Recuado:", color="black", width=80), led_recuar_global]),
                        ],
                        spacing=10,
                    ),
                    padding=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor="yellow",
        height=170,
        padding=20,
        border_radius=8,
    )

    # Main layout
    layout = ft.Row(
        [
            comando_container,
            ft.Container(width=20),  # Espaço central
            sensor_container,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    # Adiciona o layout à página
    page.add(layout)

    # Handle window close event to cleanup
    page.on_window_close = cleanup


# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, cleanup)

# Run the app
ft.app(target=main)
