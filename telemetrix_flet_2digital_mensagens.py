import flet as ft
from telemetrix import telemetrix

# Define a function to control the LEDs and update text
def control_led(pin, state, text_widget):
    if state == "ON":
        board.digital_write(pin, 1)  # Turn LED on
        text_widget.value = "A avançar" if pin == PIN_4 else "A recuar"
    elif state == "OFF":
        board.digital_write(pin, 0)  # Turn LED off
        text_widget.value = ""
    text_widget.update()

# Create an instance of Telemetrix
board = telemetrix.Telemetrix()

# Define the pins
PIN_4 = 4
PIN_5 = 5

# Set pin modes
board.set_pin_mode_digital_output(PIN_4)
board.set_pin_mode_digital_output(PIN_5)

def main(page: ft.Page):
    # Define the layout of the GUI
    page.title = "LED Controller"

    # Text widgets to display the state
    text_avancar = ft.Text('', width=100)
    text_recuar = ft.Text('', width=100)

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
            text_avancar
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
            text_recuar
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=20),  # Adds spacing between the rows and the exit button
        ft.Container(height=20),
        ft.Row([
            ft.ElevatedButton(
                'Exit',
                icon=ft.icons.EXIT_TO_APP,
                on_click=lambda e: page.window_close(),
                style=ft.ButtonStyle(padding=20)
            )
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Add the layout to the page
    page.add(layout)

    # Handle window close event to cleanup
    def on_window_close(e):
        board.shutdown()
    page.on_window_close = on_window_close

# Run the app
ft.app(target=main)
