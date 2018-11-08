#usar abelha_simples.ino
import serial # import Serial Library
#import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *
 
tempC= []
LDR=[]
sonar=[]
arduinoData = serial.Serial('/dev/ttyUSB0', 115200) #Creating our serial object named arduinoData
plt.ion() #Tell matplotlib you want interactive mode to plot live data
cnt=0
 
def makeFig(): #Create a function that makes our desired plot
    plt.ylim(10,40)                                 #Set y min and max values
    plt.title('My Live Streaming Sensor Data')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Temp C')                            #Set ylabels
    plt.plot(tempC, 'ro-', label='Degrees C')       #plot the temperature
    plt.legend(loc='upper left')                    #plot the legend
    plt2=plt.twinx()                                #Create a second y axis
    plt.ylim(400,700)                           #Set limits of second y axis- adjust to readings you are getting
    plt2.plot(LDR, 'b^-', label='LDR') #plot pressure data
    plt2.set_ylabel('LDR')                    #label second y axis
    plt2.ticklabel_format(useOffset=False)           #Force matplotlib to NOT autoscale y axis
    plt2.legend(loc='upper right')                  #plot the legend
    #plt2=plt.twinx()
    #plt2.plot(sonar, 'ro-', label='Distância Cm')       #plot the distance
 
while True: # While loop that loops forever
    while (arduinoData.inWaiting()==0): #Wait here until there is data
        pass #do nothing
    arduinoString = arduinoData.readline().decode("utf-8") #read the line of text from the serial port
    dataArray = arduinoString.split(',')   #Split it into an array called dataArray
    R =    float( dataArray[0])            #Convert second element to floating number and put in R
    temp = float( dataArray[1])            #Convert first element to floating number and put in temp
    dist = float( dataArray[2])
    LDR.append(R)                          #Building our pressure array by appending R readings
    tempC.append(temp)                     #Build our tempC array by appending temp readings                            
    sonar.append(dist)
    drawnow(makeFig)                       #Call drawnow to update our live graph
    plt.pause(.000001)                     #Pause Briefly. Important to keep drawnow from crashing
    cnt=cnt+1
    if(cnt>50):                            #If you have 50 or more points, delete the first one from the array
        LDR.pop(0)                       #This allows us to just see the last 50 data points
        tempC.pop(0)