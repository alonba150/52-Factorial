using System.Collections;
using System.Collections.Generic;
using System.IO;
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

    public Hand hand1;
    public Hand hand2;
    public Hand hand3;
    public Hand hand4;

    public Texture[] cardSprites;

    public bool one_to_two;
    public bool two_to_one;
    public bool add_to_all;
    public bool remove_from_all;
    private void Awake()
    {
        instance = this;
    }

    private void Start()
    {
        string[] lines = File.ReadAllLines("C:\\52-Factorial\\Cards.txt");
        string[] hands = lines[0].Split(',');
        Hand[] _hands = new Hand[] { hand1, hand2, hand3, hand4 };
        for (int i = 0; i < hands.Length; i++)
        {
            if (i >= 4) break;
            foreach (string c in hands[i].Split(':'))
            {
                string[] options = c.Split('.');
                _hands[i].Add(Card.Create(int.Parse(options[0]), options[1]));
            }
        }
        for (int i = 1; i < lines.Length; i++)
        {
            string[] bundle = lines[i].Split(',');
            string[] coords = bundle[0].Split(':');
            string[] bSettings = bundle[1].Split(':');
            Bundle b = Bundle.Create(Bundle.Formation.Parse<Bundle.Formation>(bSettings[0]), float.Parse(bSettings[1]), float.Parse(bSettings[2]));
            foreach (string c in bundle[2].Split(':'))
            {
                string[] options = c.Split('.');
                b.Add(Card.Create(int.Parse(options[0]), options[1]));
            }
            Debug.Log("INSTANT");
            b = Instantiate(b, new Vector3(float.Parse(coords[0]), 0.5f, float.Parse(coords[1])), Quaternion.identity);
            b.name = "Bundle";
            b.enabled = true;
            b.gameObject.SetActive(true);
            b.SetDisplay(true);
        }
    }

    // Update is called once per frame
    void Update()
    {
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
    }
}
