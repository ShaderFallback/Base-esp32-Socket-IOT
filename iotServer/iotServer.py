import sys
import os
import socket
import time
import asyncio
import websockets
import json

runDirectory = ""
#判断通过Python解释器运行还是exe打包
if 'python.exe' in sys.executable:
    #Get .py path 获取运行脚本目录
    runDirectory = sys.path[0]
else:
    #Get .exe path 获取exe运行目录
    runDirectory = os.path.dirname(os.path.realpath(sys.executable))

def load_config():
    config_path = os.path.join(runDirectory, "config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError("config.json not found")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()

def GetTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "   "

async def handler(websocket, path):
    try:
        data = await websocket.recv()
        strData = str(data)
        print(GetTime() + "Received messages: " + strData, flush=True)

        if strData == config["keyStr"]:
            tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpClientSocket.connect((config["tcp_target_ip"], config["tcp_target_port"]))
            time.sleep(0.5)
            tcpClientSocket.send(config["keyStr"].encode("utf-8"))
            tcpClientSocket.close()
            print(GetTime() + "Successes!", flush=True)
        else:
            print(GetTime() + "Authorization Fail: " + strData, flush=True)
    except Exception as e:
        print(GetTime() + "Error " + str(e), flush=True)


ip = config["websocket_ip"]
printStr = "WebSocketServerStart IP: " + str(ip)
print(GetTime() + printStr, flush=True)

start_server = websockets.serve(handler, ip, 9001)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
