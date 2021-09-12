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
    timeY = str(t[0]) #年
    timeM = str(t[1]) #月
    timeD = str(t[2]) #日
    timeHour = str(t[3]) #时
    timeMinute = str(t[4]) #分
    timeSecond = str(t[5]) #秒
    return str(timeY+"/"+timeM+"/"+timeD +" "+timeHour+":"+timeMinute+":"+timeSecond)

def do_connect():
    global addressIp
    try:
        import network
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False) #先将Wifi断开,方便模拟断网调试
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect('你的wifi名', '你的wifi密码')
            while not wlan.isconnected():#没有返回True将循环等待
                pass
        print('network config:', wlan.ifconfig())
        addressIp = str(wlan.ifconfig())
    except:
        pass
    
do_connect()#连接Wifi
port = 5001
#host = "127.0.0.1"

addressIp = addressIp.replace("(","")
addressIp = addressIp.replace(")","")
addressIp = addressIp.replace("'","")
addressIp = addressIp.split(",")

print("IP: "+addressIp[0]+ " 端口: "+ str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((addressIp[0], port))
s.listen(100)

def fbiOpenDoor():
    p22.value(0) #打开板载的小灯
    p19.value(1)
    time.sleep(1)
    p19.value(0)
    p22.value(1) #点亮1秒后关闭

while(True):
    try:
        print(getTime() + " 开始监听...")
        clientsocket, addr = s.accept()
        data = clientsocket.recv(1024)
        stringKey = data.decode("utf-8")
        print(getTime()+" 接收信息..."+ stringKey)
        if stringKey == "解锁大门":
            _thread.start_new_thread(fbiOpenDoor,())
            msg = "开门成功"
            clientsocket.send(msg.encode("utf-8"))
            print(getTime()+" 返回信息..."+ msg)
        clientsocket.close()
        time.sleep(0.1)
    except:
        print(getTime()+" 连接断开...")
        clientsocket.close()
        time.sleep(0.1)


