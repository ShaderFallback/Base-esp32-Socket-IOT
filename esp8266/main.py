from machine import Pin
import time
import socket

# 初始化引脚
p22 = Pin(2, Pin.OUT)   # D4（板载 LED）
p19 = Pin(5, Pin.OUT)   # D1
p19.value(0)
p22.value(1)

addressIp = ""

def getTime():
    t = time.gmtime()
    return "{}/{}/{} {}:{}:{}".format(t[0], t[1], t[2], t[3], t[4], t[5])

def do_connect():
    global addressIp
    try:
        import network
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)  # 先断开，方便调试
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect('your_wifi_name', 'your_wifi_password')
            while not wlan.isconnected():
                pass
        print('network config:', wlan.ifconfig())
        addressIp = str(wlan.ifconfig())
    except Exception as e:
        print("wifi error:", e)
        pass

do_connect()  # 连接 Wifi
port = 5001

# 处理 IP
addressIp = addressIp.replace("(", "").replace(")", "").replace("'", "").split(",")
print("IP: " + addressIp[0] + " Port: " + str(port))

# 创建 socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((addressIp[0], port))
s.listen(5)  # 修改监听队列为 5，避免过多连接

def fbiOpenDoor():
    p22.value(0)  # 点亮 LED
    p19.value(1)
    time.sleep(1)  # 阻塞 1 秒
    p19.value(0)
    p22.value(1)  # 恢复

# 主循环（阻塞版）
while True:
    try:
        print(getTime() + " Listening...")
        clientsocket, addr = s.accept()  # 阻塞，等待客户端连接
        data = clientsocket.recv(1024)  # 接收数据
        stringKey = data.decode("utf-8")
        print(getTime() + " Received messages..." + stringKey)
        
        if stringKey == "UnlockDoor":
            fbiOpenDoor()  # 直接调用，阻塞执行
            msg = "Success!"
            clientsocket.send(msg.encode("utf-8"))
            print(getTime() + " Sent message..." + msg)
        
        clientsocket.close()
        time.sleep(0.1)  # 等待 100ms，避免 CPU 占用过高
    
    except Exception as e:
        print(getTime() + " Disconnect... Error: " + str(e))
        try:
            clientsocket.close()
        except:
            pass
        time.sleep(0.1)  # 断开连接后，稍作休眠
