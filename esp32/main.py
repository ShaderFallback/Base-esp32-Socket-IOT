#-------------------------------------------------------------
# Please flash the MicroPython firmware first
#-------------------------------------------------------------

from machine import Pin, I2C
import time
import socket
import sys
import _thread

p22 = Pin(22, Pin.OUT)
p19 = Pin(19, Pin.OUT)
p19.value(0)
p22.value(1)
addressIp = ""

def getTime():
    t = time.gmtime()
    timeY = str(t[0]) #year
    timeM = str(t[1]) #month
    timeD = str(t[2]) #day
    timeHour = str(t[3]) #hour
    timeMinute = str(t[4]) #minute
    timeSecond = str(t[5]) #seconds
    return str(timeY+"/"+timeM+"/"+timeD +" "+timeHour+":"+timeMinute+":"+timeSecond)

def do_connect():
    global addressIp
    try:
        import network
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect('you wifi Name', 'you wifi password')
            while not wlan.isconnected():
                pass
        print('network config:', wlan.ifconfig())
        addressIp = str(wlan.ifconfig())
    except:
        pass
    
do_connect()#Connect Wifi
port = 5001

addressIp = addressIp.replace("(","")
addressIp = addressIp.replace(")","")
addressIp = addressIp.replace("'","")
addressIp = addressIp.split(",")

print("IP: "+addressIp[0]+ " Port: "+ str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((addressIp[0], port))
s.listen(100)

def fbiOpenDoor():
    p22.value(0) #On Led
    p19.value(1)
    time.sleep(1)
    p19.value(0)
    p22.value(1) #Off Led

while(True):
    try:
        print(getTime() + " Listening...")
        clientsocket, addr = s.accept()
        data = clientsocket.recv(1024)
        stringKey = data.decode("utf-8")
        print(getTime()+" Received messages..."+ stringKey)
        if stringKey == "UnlockDoor":
            _thread.start_new_thread(fbiOpenDoor,())
            msg = "Successes!"
            clientsocket.send(msg.encode("utf-8"))
            print(getTime()+" messages..."+ msg)
        clientsocket.close()
        time.sleep(0.1)
    except:
        print(getTime()+" Disconnect...")
        clientsocket.close()
        time.sleep(0.1)


