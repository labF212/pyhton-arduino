#!/usr/bin/env python3          
                                
import pyfirmata                
import time
if __name__ == '__main__':      
    board = pyfirmata.Arduino('/dev/ttyACM0')
    print("Communication Successfully started")
    LED = board.digital[5]
    LED.mode = pyfirmata.PWM
    pwm_counter = 0.01
    increase_pwm = True
    while True:
        if increase_pwm:
            pwm_counter += 0.01
            if pwm_counter >= 1:
                increase_pwm = False
        else:
            pwm_counter -= 0.01
            if pwm_counter <= 0:
                increase_pwm = True
        LED.write(pwm_counter)
        time.sleep(0.1)