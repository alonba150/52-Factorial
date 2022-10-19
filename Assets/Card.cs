using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using System;

public class Card : MonoBehaviour
{
    public static float xScale = 0.75f;
    public static float yScale = 0.005f;
    public static float zScale = 1f;

    public static readonly string[] ranks = new string[] { "ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king" };
    public static readonly string[] suits = new string[] { "spades", "hearts", "diamonds", "clubs" };
    public static readonly Dictionary<string, int> rankDic = new Dictionary<string, int>() {
        {"ace", 1},
        {"two", 2},
        {"three", 3},
        {"four", 4},
        {"five", 5},
        {"six", 6},
        {"seven", 7},
        {"eight", 8},
        {"nine", 9},
        {"ten", 10},
        {"jack", 11},
        {"queen", 12},
        {"king", 13}
    };

    [SerializeField]
    private int rank;
    [SerializeField]
    private string suit;

    public int Rank { get => rank; set => rank = value; }
    public string Suit { get => suit; set => suit = value; }

    public static Card Create(int rank, string suit)
    {
        Card c = Instantiate(BoardManagerController.Instance.cardPrefab).GetComponent<Card>();
        Destroy(c.gameObject);
        c.Rank = rank;
        c.Suit = suit;
        if (0 < rank && rank < 14 && suits.Any(s => s == suit))
            c.GetComponent<Renderer>().material.mainTexture = BoardManagerController.Instance.cardSprites[rank + 13 * Array.IndexOf(suits, suit)];
        return c;
    }

    private void Awake()
    {
        Debug.Log(string.Format("Hello, I am a card! ({0} of {1})", ranks[rank-1], suit));
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
