import flet as ft
import threading
from telemetrix import telemetrix
import time

# some globals
# make sure to select a PWM pin
DIGITAL_PIN6 = 6
DIGITAL_PIN5 = 5

# Create a Telemetrix instance
board = telemetrix.Telemetrix()

# Set the DIGITAL_PIN as an output pin
board.set_pin_mode_analog_output(DIGITAL_PIN6)
board.set_pin_mode_analog_output(DIGITAL_PIN5)

# Function to update the LED brightness on Arduino
def update_led_brightness(pwm_value1, pwm_value2):
    board.analog_write(DIGITAL_PIN6, pwm_value1)
    board.analog_write(DIGITAL_PIN5, pwm_value2)

# Thread for the automatic LED control
def automatic_control(page, led6_text, led5_text):
    global a
    # Fading up and down...
    for i in range(255):
        if not a:
            break
        board.analog_write(DIGITAL_PIN6, i)
        board.analog_write(DIGITAL_PIN5, 255 - i)  # Inverse value for pin 5
        time.sleep(0.05)
        led6_text.value = f'{i} PWD'
        led5_text.value = f'{255 - i} PWD'
        page.update()

    for i in range(255, -1, -1):
        if not a:
            break
        board.analog_write(DIGITAL_PIN6, i)
        board.analog_write(DIGITAL_PIN5, 255 - i)  # Inverse value for pin 5
        time.sleep(0.05)
        led6_text.value = f'{255 - i} PWD'
        led5_text.value = f'{i} PWD'
        page.update()

def main(page: ft.Page):
    global a
    a = False  # this is a var control - it stops the threading and the for cycle

    # Event handler for button clicks
    def on_exit(e):
        global a
        a = False
        board.analog_write(DIGITAL_PIN6, 0)
        board.analog_write(DIGITAL_PIN5, 0)
        board.shutdown()
        page.window_close()

    def on_slider_change(e):
        if manual_control.value == 'manual':
            value_slider1 = int(slider1.value * 2.55)
            value_slider2 = int(slider2.value * 2.55)
            update_led_brightness(value_slider1, value_slider2)
            led6_text.value = f'{value_slider1} PWD'
            led5_text.value = f'{value_slider2} PWD'
            page.update()

    def on_radio_change(e):
        global a
        if manual_control.value == 'manual':
            a = False
            slider1.visible = True
            slider2.visible = True
        else:
            a = True
            slider1.visible = False
            slider2.visible = False
            threading.Thread(target=automatic_control, args=(page, led6_text, led5_text), daemon=True).start()
        page.update()

    # Create UI components
    led6_text = ft.Text('None')
    led5_text = ft.Text('None')
    slider1 = ft.Slider(min=0, max=100, value=0, on_change=on_slider_change)
    slider2 = ft.Slider(min=0, max=100, value=0, on_change=on_slider_change)
    manual_control = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value='manual', label='Manual'),
            ft.Radio(value='automatic', label='Automatic')
        ]),
        value='manual',
        on_change=on_radio_change
    )
    exit_button = ft.ElevatedButton(text='Exit', on_click=on_exit)

    # Define layout
    layout = ft.Column([
        ft.Text('LED in pin 6'),
        ft.Row([slider1, led6_text]),
        ft.Text('LED in pin 5'),
        ft.Row([slider2, led5_text]),
        manual_control,
        exit_button
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Add layout to the page
    page.add(layout)

    # Handle window close event to cleanup
    page.on_window_close = on_exit

# Run the app
ft.app(target=main)
