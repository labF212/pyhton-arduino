import time
from telemetrix import telemetrix

# Configuração dos pinos do HC-SR04
TRIGGER_PIN = 9
ECHO_PIN = 10

# Variável global para armazenar a última distância lida
last_distance = None

# Callback para capturar a distância medida
def sonar_callback(data):
    """
    Callback para lidar com os dados do sensor HC-SR04.
    :param data: [report_type, trigger_pin, distance, timestamp]
    """
    global last_distance
    last_distance = data[2]  # Distância medida em cm

# Função principal para realizar leituras
def perform_readings(board, trigger_pin, echo_pin, num_readings):
    """
    Realiza um número específico de leituras do sensor ultrassônico.
    :param board: Instância do Telemetrix
    :param trigger_pin: Pino TRIGGER no Arduino
    :param echo_pin: Pino ECHO no Arduino
    :param num_readings: Número de leituras a serem realizadas
    """
    # Configura os pinos e o callback
    board.set_pin_mode_sonar(trigger_pin, echo_pin, sonar_callback)

    for i in range(num_readings):
        time.sleep(1)  # Espera 1 segundo entre as leituras
        if last_distance is not None:
            print(f"Leitura {i + 1}: Distância = {last_distance:.2f} cm")
        else:
            print(f"Leitura {i + 1}: Erro ao obter a distância.")
    
    # Desativa o sonar após as leituras
    board.sonar_disable()

# Programa principal
if __name__ == "__main__":
    # Cria a instância da biblioteca Telemetrix
    board = telemetrix.Telemetrix()

    try:
        print("Leituras do sensor HC-SR04...")
        perform_readings(board, TRIGGER_PIN, ECHO_PIN, num_readings=10)
    except KeyboardInterrupt:
        print("Interrompido pelo utilizador.")
    finally:
        # Encerra a comunicação com o Arduino
        board.shutdown()
        print("Programa finalizado.")
