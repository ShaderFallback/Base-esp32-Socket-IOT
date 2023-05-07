import sys
import os
import socketserver
import socket
import threading
import time
import asyncio
import websockets
 
def GetTime():
    return(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"   ")

def GetHostIp():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        return ip
    except:
        return "127.0.0.1"

async def handler(websocket, path):
    try:
        data = await websocket.recv()
        strData = str(data)
        print(GetTime() + "Received messages: "+ strData)
        if strData  == "hello":
            tcpClientSocket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpClientSocket.connect(('192.168.3.92', 5001))
            time.sleep(0.5)
            tcpClientSocket.send("UnlockDoor".encode('utf-8'))
            tcpClientSocket.close()
            print(GetTime()+ "Successes!")
        else:
            print(GetTime() + "Error:"+str(data))
    except:
        print(GetTime() + "websocketError...")


ip = GetHostIp()
print(GetTime()+ "WebSocketServerStart IP: " + str(ip))
start_server = websockets.serve(handler, ip, 9001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
