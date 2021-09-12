using System;
using System.Net;
using System.Text;
using System.Net.Sockets;
using System.Threading;
using System.Net.NetworkInformation;

namespace Core
{
    public static class OpenDoor
    {
    }
    public static class ClientSocket
    {
        private static Socket tcpClient;
        private static string serverIP = "这里填写你的域名";
        private static int serverPort = 5000;
        public static string serverStatic = "";
        private static IPAddress address = null;

        public static void InitServer()
        {
            IPHostEntry iPHostEntry = Dns.GetHostEntry(serverIP);
            address = iPHostEntry.AddressList[0];
        }
        public static void CreateSocket() {
            tcpClient = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        }
        public static void ConnectServer()
        {
            //建立连接
            try
            {
                IAsyncResult asyncResult = tcpClient.BeginConnect(address, serverPort, null, null);
                bool sucess = asyncResult.AsyncWaitHandle.WaitOne(TimeSpan.FromSeconds(0.2f));

                if (!sucess){

                    tcpClient.EndConnect(asyncResult);
                }
            }
            catch (Exception ex)
            {
                serverStatic = "连接服务器错误..."+ex.Message;
            }
        }
        public static string pingIP()
        {
            try
            {
                Ping ping = new Ping(); //测试网络质量
                PingReply pr = ping.Send(address, 1);
                return pr.RoundtripTime.ToString();
            }
            catch (Exception)
            {

                return "未连接";
            }
           
        }
        static void ReceiveCallback(IAsyncResult result)
        {
            result.AsyncWaitHandle.Close();
        }
        public static string SendMessage(string message)
        {
            try
            {
                byte[] buffer = new byte[1024];
                tcpClient.Send(Encoding.UTF8.GetBytes(message));
                IAsyncResult asyncReceive = tcpClient.BeginReceive(buffer, 0, buffer.Length, SocketFlags.None, new AsyncCallback(ReceiveCallback), tcpClient);
                bool sucessReceive = asyncReceive.AsyncWaitHandle.WaitOne(TimeSpan.FromSeconds(0.6f));
                string acceptString = "";

                if (sucessReceive){
                    acceptString = Encoding.UTF8.GetString(buffer, 0, buffer.Length).Replace("\0", "");
                }
                else{
                    acceptString = "接收服务器信息超时...";
                }
                return acceptString;
            }
            catch (Exception ex)
            {
                ConnectServer();
                return "连接错误: "+ex.Message;
                throw;
            }

        }
    }
}