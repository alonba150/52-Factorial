using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class BoardManagerController : MonoBehaviour
{
    private static BoardManagerController instance = null;
    public static BoardManagerController Instance
    {
        get
        {
            if (instance == null)
            {
                instance = new BoardManagerController();
            }
            return instance;
        }
    }

    public GameObject cardPrefab;
    public GameObject bundlePrefab;

    public List<Bundle> bundles = new List<Bundle>();

    public Hand hand1;
    public Hand hand2;
    public Hand hand3;
    public Hand hand4;

    public Texture[] cardSprites;

    public bool one_to_two;
    public bool two_to_one;
    public bool add_to_all;
    public bool remove_from_all;
    public bool connect;
    public bool play;

    private Socket server;

    private void Awake()
    {
        instance = this;
    }

    private void Start()
    {
        //
        // Read Starter File
        //
        //string[] lines = File.ReadAllLines("C:\\Users\\u101040.DESHALIT\\Desktop\\Haproyekt shel ran\\52-Factorial\\Cards.txt");
        //string[] hands = lines[0].Split(',');
        Hand[] _hands = new Hand[] { hand1, hand2, hand3, hand4 };
        bundles.Add(hand1);
        bundles.Add(hand2);
        bundles.Add(hand3);
        bundles.Add(hand4);
        //for (int i = 0; i < hands.Length; i++)
        //{
        //    if (i >= 4) break;
        //    foreach (string c in hands[i].Split(':'))
        //    {
        //        string[] options = c.Split('.');
        //        _hands[i].Add(Card.Create(int.Parse(options[0]), options[1]));
        //    }
        //}
        //for (int i = 1; i < lines.Length; i++)
        //{
        //    string[] bundle = lines[i].Split(',');
        //    string[] coords = bundle[0].Split(':');
        //    string[] bSettings = bundle[1].Split(':');
        //    Bundle b = Bundle.Create(Bundle.Formation.Parse<Bundle.Formation>(bSettings[0]), float.Parse(bSettings[1]), float.Parse(bSettings[2]));
        //    bundles.Add(b);
        //    foreach (string c in bundle[2].Split(':'))
        //    {
        //        string[] options = c.Split('.');
        //        b.Add(Card.Create(int.Parse(options[0]), options[1]));
        //    }
        //    Debug.Log("INSTANT");
        //    b = b.Enable(float.Parse(coords[0]), float.Parse(coords[1]), Quaternion.identity);
        //}
        //
        // Start Connection with server
        //
        IPHostEntry host = Dns.GetHostEntry(Dns.GetHostName());
        IPAddress ipAddress = host.AddressList[4];
        foreach (IPAddress ip in host.AddressList)
        {
            Debug.Log(ip);
        }
        IPEndPoint localEndPoint = new IPEndPoint(ipAddress, 55555);

        try
        {

            server = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            Debug.Log(string.Format("Waiting for a connection from ({0}, {1})...", ipAddress, "55555"));
            server.Connect(localEndPoint);
            Debug.Log("Connected");
        }
        catch (Exception e)
        {
            Debug.Log(e.ToString());
        }

    }

    // Update is called once per frame
    void Update()
    {
        //
        // Server Connection
        //

        if (server != null && server.IsBound && server.Available > 0)
        {
            string data = null;
            byte[] bytes = null;
            bytes = new byte[Math.Min(server.Available, 1024)];
            int bytesRec = server.Receive(bytes);
            data += Encoding.ASCII.GetString(bytes, 0, bytesRec);
            if (data.IndexOf("<EOF>") > -1)
            {
                server.Disconnect(true);
            }
            HandleData1(data.Substring(8));
        }
   
        //
        // Tests
        //
        if (one_to_two)
        {
            hand1.MoveCard(hand1.Get(0), hand2);
            one_to_two = false;
        }
        if (two_to_one)
        {
            hand2.MoveCard(hand2.Get(0), hand1);
            two_to_one = false;
        }
        if (add_to_all)
        {
            hand1.Add(Card.Create(1, "spades"));
            hand2.Add(Card.Create(1, "spades"));
            hand3.Add(Card.Create(1, "spades"));
            hand4.Add(Card.Create(1, "spades"));
            add_to_all = false;
        }
        if (remove_from_all)
        {
            hand1.Remove(hand1.Get(hand1.Count-1));
            hand2.Remove(hand2.Get(hand2.Count-1));
            hand3.Remove(hand3.Get(hand3.Count-1));
            hand4.Remove(hand4.Get(hand4.Count-1));
            remove_from_all = false;
        }
        if (connect)
        {
            if (server != null)
            {
                server.Send(Encoding.ASCII.GetBytes("00000007connect"));
            }
            connect = false;
        }
        if (play)
        {
            if (server != null)
            {
                server.Send(Encoding.ASCII.GetBytes("00000004play"));
            }
            play = false;
        }
    }

    void OnMouseClick()
    {
        RaycastHit raycastHit;
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        if (Physics.Raycast(ray, out raycastHit, 100f))
        {
            if (raycastHit.transform != null)
            {
                Debug.Log(raycastHit.transform.gameObject.name);
            }
        }
    }

    private void HandleData(string data)
    {
        if (!data.Contains('(') || !data.Contains(')')) return;
        string content = data.Split('(')[1];
        content = content.Remove(content.Length - 1);
        string[] args = content.Split(',');
        int bundleId;
        switch (data.Split('(')[0])
        {
            case "AddCard":
                bundleId = int.Parse(args[0]);
                int cRank = int.Parse(args[1]);
                int cSuit = int.Parse(args[2]);
                bundles[bundleId].Add(Card.Create(cRank, Card.suits[cSuit]));
                break;
            case "RemoveCard":
                bundleId = int.Parse(args[0]);
                int cardId = int.Parse(args[1]);
                bundles[bundleId].Remove(cardId);
                break;
            case "AddBundle":
                int f = int.Parse(args[0]);
                float bx = float.Parse(args[1]);
                float bz = float.Parse(args[2]);
                bundles.Add(Bundle.Create((Bundle.Formation)f, 0.5f, 0.3f).Enable(bx, bz, 0, Quaternion.identity));
                break;
            case "RemoveBundle":
                bundleId = int.Parse(args[0]);
                Bundle b = bundles[bundleId];
                Destroy(b.gameObject);
                bundles.Remove(b);
                break;
            case "MoveCard":
                bundleId = int.Parse(args[0]);
                int otherBundleId = int.Parse(args[1]);
                cardId = int.Parse(args[2]);
                bundles[bundleId].MoveCard(cardId, bundles[otherBundleId]);
                break;
            default:
                Debug.Log("Unknown Command: " + data);
                break;
        }
    }

    private void HandleData1(string data)
    {
        print(data);
        foreach (Bundle b in bundles)
        {
            Destroy(b.gameObject);
        }
        bundles.Clear();
        data = data.Substring(1, data.Length - 2);
        string[] spl = data.Split("Bundle ");
        foreach (string _bundle in spl)
        {
            if (_bundle == "") continue;
            print(_bundle);
            string b = _bundle.Substring(0, _bundle.Length - 2);
            b = b.Split(": ")[1];
            b = b.Substring(1, b.Length - 2);
            string[] temp = b.Split(" + ");
            string[] cards = temp[0].Substring(1, temp[0].Length - 2).Split(", ");
            string[] position = temp[1].Substring(1, temp[1].Length - 2).Split(", ");
            print(temp[1]);
            Bundle n = Bundle.Create(Bundle.Formation.STACK, 0, 0, float.Parse(position[0]), float.Parse(position[1]), float.Parse(position[2]));
            foreach (string card in cards)
            {
                if (card == "" || card.Trim() == "") continue;
                print(card);
                string[] c = card.Substring(1, card.Length - 2).Split(" - ");
                print(c[0] + " " + c[1]);
                n.Add(Card.Create(int.Parse(c[1]) + 1, Card.suits[int.Parse(c[0])]));
            }
            n.ReverseCardOrder();
            bundles.Add(n);
        }
        List<Bundle> templ = new List<Bundle>();
        foreach (Bundle b in bundles)
        {
            templ.Add(b.Enable(Quaternion.identity));
        }
        bundles = templ;

    }
}
