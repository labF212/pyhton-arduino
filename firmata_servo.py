#%% import libraries
import time
import keyboard
import pyfirmata

# set up arduino board
board = pyfirmata.Arduino('/dev/ttyACM0')

#%% setup servo on pin 2
angle  = 90                     # initial angle
da = 5                          # initial speed (degrees per keypress)
servo1 = board.get_pin('d:2:s') # pin to communicate to the servo with
servo1.write(angle)             # set servo to initial angle

# set up a function that will tell the servo to move to a specific position when called
def move_servo(angle):  # define function
    servo1.write(angle) # move servo to specified angle

#%% while loop 
while True:

    if keyboard.is_pressed('a'): # check if a is pressed
        if angle + da < 180:     # check to make sure new angle will not exceed 180 degrees
            angle = angle + da   # if new angle is OK, change to it
            move_servo(angle)    # set servo position to new angle by calling the function we made earlier
            time.sleep(0.1)      # wait a little bit (0.1 seconds) before checking again

    elif keyboard.is_pressed('d'): 
        if angle - da > 0:         # check to make sure new angle will not exceed 0 degrees
            angle = angle - da     
            move_servo(angle)      
            time.sleep(0.1)        
    
    elif keyboard.is_pressed('w'): # if w is pressed, increase da by 1
        if da + 1 < 180:
            da = da + 1
            time.sleep(0.1)
   
    elif keyboard.is_pressed('s'): # if s is pressed, decrease da by 1
        if da - 1 > 0:
            da = da - 1
            time.sleep(0.1)