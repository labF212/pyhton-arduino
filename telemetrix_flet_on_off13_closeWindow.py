import flet as ft
from telemetrix import telemetrix

# Create an instance of Telemetrix
board = telemetrix.Telemetrix()

# Set pin mode for digital output
board.set_pin_mode_digital_output(13)

# Function to control LED
def control_led(state):
    if state == "Ligar":
        board.digital_write(13, 1)
    elif state == "Desligar":
        board.digital_write(13, 0)

def main(page: ft.Page):
    page.title = "Controlo do LED 13"

    # Prevent auto-close
    page.window.prevent_close = True

    # Confirmation dialog definition
    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Aviso"),
        content=ft.Text("Deseja mesmo sair do programa?"),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[
            ft.ElevatedButton("Sim", on_click=lambda e: (board.shutdown(), page.window.destroy())),
            ft.OutlinedButton("Não", on_click=lambda e: (page.close(confirm_dialog), page.update()))
        ]
    )

    # Window close event handler
    def window_event(e):
        if e.data == "close":
            page.open(confirm_dialog)
            page.update()

    page.window.on_event = window_event

    # Button click handler
    def on_button_click(event):
        control_led(event.control.text)

    # UI layout
    layout = ft.Column([
        ft.Text("Controlo do LED 13 (interno)"),
        ft.ElevatedButton("Ligar", on_click=on_button_click),
        ft.ElevatedButton("Desligar", on_click=on_button_click),
        ft.ElevatedButton("Sair", on_click=lambda e: page.open(confirm_dialog))
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Add to page
    page.add(layout)

ft.app(target=main)
