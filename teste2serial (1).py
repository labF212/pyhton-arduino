#!/usr/bin/env python
# coding: utf-8

# <h1>Comunicação com Arduino através de Porta Série</h1>
# 
# <h2><i>Impressão das variáveis medidas em Gráfico</i></h2>

# In[14]:


#http://arduino-er.blogspot.com/2015/04/python-to-plot-graph-of-serial-data.html
#!/usr/bin/env python3

#get_ipython().run_line_magic('matplotlib', 'inline')
#%config InlineBackend,figure_format = 'svg'

import serial
import matplotlib.pyplot as plt
from drawnow import *
from pylab import *
import atexit

values = []
values1 = []
values2 = []

plt.ion()
cnt=0
valueInInt=0
valueInInt1=0
valueInInt2=0





serialArduino = serial.Serial('/dev/ttyUSB0', 115200)

#https://www.youtube.com/watch?v=Hr4yh1_4GlQ
def plotValues():
    #https://jakevdp.github.io/PythonDataScienceHandbook/04.01-simple-line-plots.html
    plt.title('Medição das Variáveis')
    plt.grid(True)
    plt.plot(values, 'rx-', label='LDR')
    plt.plot(values1, '-g', label='TEMP')
    plt.plot(values2, '-.k', label='DIST')
    plt.legend(loc='upper left')
    #plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1, loc='upper left')
    plt.ylabel('Valores Lidos (escala 0 a 1024)')
    plt.xlabel('nº de Amostras')
    plt.pause(0.2)
    #plt.savefig("test1.png")
   
    #fig.canvas.flush_events()
    

    plt.ioff()
    #plt.show()
    
    #plt.savefig("test1.png")    
    

def doAtExit():
    serialArduino.close()
    print("Close serial")
    print("serialArduino.isOpen() = " + str(serialArduino.isOpen()))

atexit.register(doAtExit)

print("serialArduino.isOpen() = " + str(serialArduino.isOpen()))

#pre-load dummy data
#for i in range(0,26):
#    values.append(0)
#    values1.append(0)
#    values2.append(0)
    
while True:
    while (serialArduino.inWaiting()==0):
        pass
#    print("readline()")
    valueRead = serialArduino.readline(500)
#    print(valueRead)
#    if valueRead=

    #check if valid value can be casted
    try:
        #if valueRead ==  #se for =LDR faz o seguinte:
        #if 'LDR' in (valueRead[0:len(valueRead)-2].decode("utf-8")):
        if 'LDR' in valueRead.decode("utf-8"):
            valueInInt = int (float(valueRead[5:len(valueRead)-2].decode("utf-8")))
            #print ("LDR:", valueInInt)
            
            if valueInInt <= 1024:
                    if valueInInt >= 0: #>0
                        values.append(valueInInt)
                        #print(">0 ",valueInInt1)
                        #drawnow(plotValues)
                    else:
                        print("Invalid! negative number1",valueInInt)
            
        else:
            if 'Temp' in valueRead.decode("utf-8"):
                valueInInt1 = int (float(valueRead[5:len(valueRead)-2].decode("utf-8")))
                #print("TEMP:",valueInInt1)
                
                if valueInInt1 <= 1024:
                    if valueInInt1 >= 0: #>0
                        values1.append(valueInInt1)
                        #print(">0 ",valueInInt1)
                        #drawnow(plotValues1)
                    else:
                        print("Invalid! negative number1",valueInInt1)
                    #else:
                     #   print("Invalid! too large")    
                
            else:
                if 'Dist' in valueRead.decode("utf-8"):
                    valueInInt2 = int (float(valueRead[5:len(valueRead)-2].decode("utf-8")))
                 #   print("DIST:",valueInInt2)
                    
                    if valueInInt2 <= 1024:
                        if valueInInt2 >= 0: #>0
                            values2.append(valueInInt2)
                         #   print(">0 ",valueInInt2)
                        #drawnow(plotValues1)
                    else:
                        print("Invalid! negative number2",valueInInt2)
             
                else:
                    message=valueRead.decode("utf-8")
                  #  print(message)
        drawnow(plotValues)
        #if valueInInt <= 1024:
         #   if valueInInt >=0: #>0
          #      values.append(valueInInt)
           #     print(">0 ",valueInInt)
            #    drawnow(plotValues)
           # else:
            #    print("Invalid! negative number",valueInInt)
       # else:
        #    print("Invalid! too large")
        
        
    except ValueError:
        print("Invalid! cannot cast")


# In[ ]:




