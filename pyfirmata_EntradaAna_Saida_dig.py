from pyfirmata import Arduino, util
import time

# void setup
uno = Arduino('/dev/ttyACM0')
iterator = util.Iterator(uno)
iterator.start()

pinLDR = uno.get_pin('a:1:i')
pinLED = uno.get_pin('d:5:o')
pinLDR.enable_reporting()

def loop():
   while True:
        leitura = pinLDR.read()
        try:
            if leitura < 0.40:
                pinLED.write(1)
            else:
                pinLED.write(0)
        except:
           pass
           # não faz nada
           #print('')
        print('Sensor placa:', leitura)
        time.sleep(1)

if __name__ == '__main__':
   loop()
