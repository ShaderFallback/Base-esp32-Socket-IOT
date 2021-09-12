using System;
using System.Collections.Generic;
using System.Net.NetworkInformation;
using System.Threading;
using Android.App;
using Android.OS;
using Android.Runtime;
using Android.Widget;
using AndroidX.AppCompat.App;

namespace App2
{
    [Activity(Label = "@string/app_name", Theme = "@style/AppTheme", MainLauncher = true)]
    public class MainActivity : AppCompatActivity
    {
        List<string> messagesString = new List<string>();
        TextView translatedPhoneWord;
        TextView translatedPhoneWord2;
        TextView translatedPhoneWord3;


        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            Xamarin.Essentials.Platform.Init(this, savedInstanceState);
            SetContentView(Resource.Layout.activity_main);

            translatedPhoneWord = FindViewById<TextView>(Resource.Id.textView1);
            translatedPhoneWord2 = FindViewById<TextView>(Resource.Id.textView2);
            translatedPhoneWord3 = FindViewById<TextView>(Resource.Id.textView3);

            Button translateButton = FindViewById<Button>(Resource.Id.button1);
            translatedPhoneWord.Text = "";
            translatedPhoneWord2.Text = "";
            translatedPhoneWord3.Text = "ping:0";

            Core.ClientSocket.InitServer();
            Thread _thread = new Thread(pingValue);
            _thread.Start();

            int count = 0;
            translateButton.Click += (sender, e) =>
            {
                Core.ClientSocket.CreateSocket();
                Core.ClientSocket.ConnectServer();
                string getString = Core.ClientSocket.SendMessage("解锁大门");
                translatedPhoneWord.Text = getString;
                Thread textDisplay = new Thread(TextDisplay);
                textDisplay.Start();
                count += 1;
                messagesString.Add(count.ToString() + getString);
                translatedPhoneWord2.Text = MessageList();
            };
            
        }
        private void pingValue()
        {
            while (true)
            {
                string pingValue = "Ping: " + Core.ClientSocket.pingIP();
                translatedPhoneWord3.Text = pingValue;
                Thread.Sleep(1000);
            }
            
        }
        private void TextDisplay()
        {
            Thread.Sleep(800);
            translatedPhoneWord.Text = "";
        }
        private string MessageList()
        {
            if (messagesString.Count > 6 )
            {
                messagesString.RemoveAt(0);
            }
            string comString = "";
            for (int i = 0; i < messagesString.Count; i++)
            {
                comString += messagesString[i] + "\n";
            }
            return comString;
        }
        public override void OnRequestPermissionsResult(int requestCode, string[] permissions, [GeneratedEnum] Android.Content.PM.Permission[] grantResults)
        {
            Xamarin.Essentials.Platform.OnRequestPermissionsResult(requestCode, permissions, grantResults);

            base.OnRequestPermissionsResult(requestCode, permissions, grantResults);
        }
    }
}