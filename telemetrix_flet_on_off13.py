import flet as ft
from telemetrix import telemetrix

# Define a function to control the LED
def control_led(state):
    if state == "ON":
        board.digital_write(13, 1)  # Turn LED on
    elif state == "OFF":
        board.digital_write(13, 0)  # Turn LED off

# Create an instance of Telemetrix
board = telemetrix.Telemetrix()

def main(page: ft.Page):
    # Define the layout of the GUI
    page.title = "LED Controller"

    # Define the event handler for buttons
    def on_button_click(event):
        control_led(event.control.text)

    # Create the layout
    layout = ft.Column([
        ft.Text('LED Controller'),
        ft.ElevatedButton('ON', on_click=on_button_click),
        ft.ElevatedButton('OFF', on_click=on_button_click),
        ft.ElevatedButton('Exit', on_click=lambda e: page.window_close())
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Add the layout to the page
    page.add(layout)

    # Handle window close event to cleanup
    def on_window_close(e):
        board.shutdown()
    page.on_window_close = on_window_close

# Run the app
ft.app(target=main)
