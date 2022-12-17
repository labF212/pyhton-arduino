#https://www.youtube.com/watch?v=4i-bMzAXieQ&list=PL7CjOZ3q8fMdJMjAu9wP5XgkBiDAZdpok&index=2
#usar mem

from pyfirmata import Arduino, util
import time

                                #void setup(){
Uno = Arduino('/dev/ttyACM0')
                                     # Serial.begin(9600);
print('Olá Mundo!')                  # Serial.println("Olá Mundo!");   
                                #}

tempo = 0

while True:                     # void loop(){

    tempo = tempo + 0.1
    Uno.digital[13].write(1)         # digitalWrite(13, HIGH);
    print('LED ligado', tempo)              # Serial.println("LED ligado");
    time.sleep(tempo)                    # delay(1000);

    Uno.digital[13].write(0)         # digitalWrite(13, LOW);
    print('LED desligado')           # Serial.println("LED desligado");
    time.sleep(tempo)                    # delay(1000);
    if tempo > 2:
        tempo=0

                                #}
