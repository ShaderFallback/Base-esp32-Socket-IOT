using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace iotServer
{
    class Program
    {
        static Socket socketServer;
        static Socket clientSocket;

        private static string serverIP = "";
        private static int serverPort = 5000;

        private static Socket iotClient;
        private static int iotPort = 5001;
        private static IPAddress iotAddress = IPAddress.Parse("192.168.3.92");

        static void Main(string[] args)
        {
            string hostName = Dns.GetHostName();//本机名   
            String ipIndex = "";
            IPAddress[] addressList = Dns.GetHostAddresses(hostName);//会返回所有地址，包括IPv4和IPv6   
            for (int i = 0; i < addressList.Length; i++)
            {
                Console.WriteLine("["+i+"] "+ addressList[i]);
            }
            Console.WriteLine("选择IP: ");
            ipIndex = Console.ReadLine();
            serverIP = addressList[Convert.ToInt64(ipIndex)].ToString();

            Console.WriteLine("当前服务器IP: "+ serverIP);

            IPAddress address = IPAddress.Parse(serverIP);
            EndPoint localEP = new IPEndPoint(address, serverPort);
            socketServer = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            socketServer.Bind(localEP);

            while (true)
            {
                try
                {
                    ListenServer();
                    byte[] buffer = new byte[1024];
                    IAsyncResult asyncReceive = clientSocket.BeginReceive(buffer, 0, buffer.Length, SocketFlags.None, new AsyncCallback(ReceiveCallback), clientSocket);
                    bool sucessReceive = asyncReceive.AsyncWaitHandle.WaitOne(TimeSpan.FromSeconds(0.2f));
                    string acceptString = "";
                    if (sucessReceive){
                        acceptString = Encoding.UTF8.GetString(buffer, 0, buffer.Length);
                    }
                    else{
                        acceptString = "接收客户端信息超时...";
                    }
                    acceptString = acceptString.Replace("\0", "");
                    Console.WriteLine(DateTime.Now + " 接收客户端信息: " + acceptString);
                    if (acceptString == "解锁大门"){
                        SendMessage(iotConnected(acceptString));
                    }
                    else{
                        SendMessage("授权失败!");
                    }
                }
                catch (Exception ex)
                {
                    clientSocket = null;
                    Console.WriteLine(DateTime.Now + " 客户端断开连接...." + ex.Message);
                    ListenServer();
                }
            }
        }
        static void ReceiveCallback(IAsyncResult result)
        {
            result.AsyncWaitHandle.Close();
        }
        static string iotConnected(string message)
        {
            try
            {
                iotClient = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                IAsyncResult asyncConnect = iotClient.BeginConnect(iotAddress, iotPort, null, null);
                bool sucessConnect = asyncConnect.AsyncWaitHandle.WaitOne(TimeSpan.FromSeconds(0.2f));
                string getMessage = "";
                if (sucessConnect)
                {
                    Console.WriteLine(DateTime.Now + " 转发客户端请求: " + message);
                    iotClient.Send(Encoding.UTF8.GetBytes(message));
                    byte[] buffer = new byte[1024];
                    IAsyncResult asyncReceive = iotClient.BeginReceive(buffer, 0, buffer.Length, SocketFlags.None, new AsyncCallback(ReceiveCallback), iotClient);
                    bool sucessReceive = asyncReceive.AsyncWaitHandle.WaitOne(TimeSpan.FromSeconds(0.2f));

                    if (sucessReceive)
                    {
                        getMessage = Encoding.UTF8.GetString(buffer, 0, buffer.Length).Replace("\0", "");
                        Console.WriteLine(DateTime.Now + " 接收终端返回信息:  " + getMessage);
                    }
                    else{
                        getMessage =  "接收信息超时...";
                    }
                }
                else{
                    getMessage = "连接开发板超时...";
                }
                iotClient.Close();
                return getMessage;

            }
            catch (Exception ex)
            {
                return "连接开发板错误!" + ex.Message;
            }
        }

        static void ListenServer()
        {
            socketServer.Listen(100);
            if (clientSocket == null)
            {
                Console.WriteLine(DateTime.Now +" 服务器开始监听...");
                clientSocket = socketServer.Accept(); //等待客户端链接
            }
        }

        static void SendMessage(string message)
        {
            byte[] byteskey = Encoding.UTF8.GetBytes(message);
            clientSocket.Send(byteskey);
            Console.WriteLine(DateTime.Now + " 回复客户端请求: " + message);
            clientSocket.Close();
        }
    }
}
