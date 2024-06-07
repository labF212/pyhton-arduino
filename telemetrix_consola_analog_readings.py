from telemetrix import telemetrix

# Cria uma instância da classe Telemetrix
board = telemetrix.Telemetrix()

# Define o pino analógico que deseja ler
analog_pin = 1  # Por exemplo, A0 no Arduino

def analog_read_callback(data):
    """
    Callback function to process the analog read data.
    """
    pin = data[1]
    value = data[2]
    print(f'Pin: {pin}, Value: {value}')

# Configura o callback para o pino analógico
board.set_pin_mode_analog_input(analog_pin, callback=analog_read_callback)

# Mantém o script rodando para permitir a leitura contínua
try:
    while True:
        pass
except KeyboardInterrupt:
    # Encerra a comunicação com o microcontrolador
    board.shutdown()