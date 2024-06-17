import flet as ft
from telemetrix import telemetrix
import signal
import sys

# Create an instance of Telemetrix
board = telemetrix.Telemetrix()

# Define the pins
PIN_4 = 4
PIN_5 = 5
ANALOG_PIN2 = 2
ANALOG_PIN3 = 3

# Initialize the analog values dictionary
analog_values = {ANALOG_PIN2: 0, ANALOG_PIN3: 0}

# Global variables for LED widgets
led_avancar = None
led_recuar = None

# Define a function to control the LEDs and update text
def control_led(pin, state, text_widget):
    if state == "ON":
        board.digital_write(pin, 1)  # Turn LED on
        text_widget.value = "A avançar" if pin == PIN_4 else "A recuar"
    elif state == "OFF":
        board.digital_write(pin, 0)  # Turn LED off
        text_widget.value = ""
    text_widget.update()

# Function to update analog values
def update_analog_values(data, pin):
    analog_values[pin] = data[2]
    update_leds()

# Function to update LED colors based on analog values
def update_leds():
    if led_avancar is not None:
        led_avancar.color = 'red' if analog_values[ANALOG_PIN2] > 512 else 'green'
        led_avancar.update()
    if led_recuar is not None:
        led_recuar.color = 'red' if analog_values[ANALOG_PIN3] > 512 else 'green'
        led_recuar.update()

# Function to handle cleanup on exit
def cleanup(*args):
    board.digital_write(PIN_4, 0)  # Turn off PIN_4
    board.digital_write(PIN_5, 0)  # Turn off PIN_5
    board.shutdown()
    # If not exiting via signal, close the Flet page
    if args and isinstance(args[0], ft.ControlEvent):
        args[0].page.window_close()

# Set pin modes
board.set_pin_mode_digital_output(PIN_4)
board.set_pin_mode_digital_output(PIN_5)
board.set_pin_mode_analog_input(ANALOG_PIN2, callback=lambda data: update_analog_values(data, ANALOG_PIN2))
board.set_pin_mode_analog_input(ANALOG_PIN3, callback=lambda data: update_analog_values(data, ANALOG_PIN3))

def main(page: ft.Page):
    global led_avancar, led_recuar

    # Define the layout of the GUI
    page.title = "LED Controller"

    # Text widgets to display the state
    text_avancar = ft.Text('', width=100)
    text_recuar = ft.Text('', width=100)

    # LED widgets to indicate state
    led_avancar = ft.Icon(name="fiber_manual_record", color="green", size=24)
    led_recuar = ft.Icon(name="fiber_manual_record", color="green", size=24)

    # Define the event handler for buttons
    def on_button_click(event):
        text = event.control.text
        pin = event.control.data['pin']
        text_widget = event.control.data['text_widget']
        control_led(pin, text, text_widget)

    # Create the layout
    layout = ft.Column([
        ft.Text('LED Controller', style='headlineSmall', weight='bold'),
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text('Avanço do cilindro'),
                        ft.ElevatedButton('ON', on_click=on_button_click, data={'pin': PIN_4, 'text_widget': text_avancar}),
                        ft.ElevatedButton('OFF', on_click=on_button_click, data={'pin': PIN_4, 'text_widget': text_avancar})
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ),
            text_avancar,
            led_avancar
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text('Recuo do cilindro'),
                        ft.ElevatedButton('ON', on_click=on_button_click, data={'pin': PIN_5, 'text_widget': text_recuar}),
                        ft.ElevatedButton('OFF', on_click=on_button_click, data={'pin': PIN_5, 'text_widget': text_recuar})
                    ], alignment=ft.MainAxisAlignment.CENTER)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ),
            text_recuar,
            led_recuar
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=20),  # Adds spacing between the rows and the exit button
        ft.Container(height=20),
        ft.Row([
            ft.ElevatedButton(
                'Exit',
                icon=ft.icons.EXIT_TO_APP,
                on_click=cleanup,
                style=ft.ButtonStyle(padding=20)
            )
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Add the layout to the page
    page.add(layout)

    # Handle window close event to cleanup
    page.on_window_close = cleanup

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, cleanup)

# Run the app
ft.app(target=main)
