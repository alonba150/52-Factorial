using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class Bundle : MonoBehaviour
{
    public enum Formation
    {
        ROW,
        COLUMN,
        STACK
    }

    [SerializeField]
    private List<Card> cards = new List<Card>();
    public Card[] Cards { get => cards.ToArray(); }

    public bool trigger = false;

    /* Test
    public List<string[]> Cards {
        get => (List <string[]>)cards.Select(x => new string[] { x.Rank.ToString(), x.Suit });
        set => cards = (List<Card>)value.Select(x => Card.Create(int.Parse(x[0]), x[1]));
    }
    */

    public int Count { get => cards.Count; }

    public Formation display;

    public float spaceX;
    public float spaceZ;

    private bool displayActive = false;

    #region Basic Functions
    public Card Get(int i) {
        return cards[i];
    }

    public int Index(Card c)
    {
        return cards.Contains(c)? cards.IndexOf(c) : -1;
    }

    public void Add(Card c) {
        cards.Add(c);
        cards[Count - 1] = Instantiate(cards[Count - 1], this.gameObject.transform);
        cards[Count - 1].name = "Card";
        UpdateCards();
    }

    public void Add(Card c, int i)
    {
        cards.Insert(i, c);
        cards[i] = Instantiate(cards[i], this.gameObject.transform);
        cards[i].name = "Card";
        UpdateCards();
    }

    public void Remove(Card c) {
        cards.Remove(c);
        Destroy(c.gameObject);
        UpdateCards();
    }

    public void Remove(int i) {
        Destroy(cards[i].gameObject);
        cards.RemoveAt(i);
        UpdateCards();
    }

    public void MoveCard(Card c, Bundle b) {
        this.Remove(c);
        b.Add(c);
    }

    public void MoveCard(int i, Bundle b)
    {
        b.Add(cards[i]);
        this.Remove(i);
    }
    #endregion

    public void UpdateCards() {
        Display();
    }

    public void SetDisplay(bool active)
    {
        displayActive = active;
        Display();
    }

    public void Display()
    {
        if (Count < 1 || !displayActive) return;
        //this.gameObject.transform.localScale = new Vector3(Card.xScale, Card.yScale, Card.zScale);
        for (int i = 0; i < Count; i++) { cards[i].gameObject.SetActive(false); cards[i].transform.position = this.transform.position; }
        switch (display)
        {
            case Formation.COLUMN:
                float tColumnWidth = (Card.xScale+ spaceX) * Count - spaceX;
                for (int i = 0; i < Count; i++)
                {
                    float xToTranslate = -tColumnWidth / 2 + i * (spaceX + Card.xScale) + Card.xScale / 2;
                    cards[i].gameObject.transform.Translate(xToTranslate*transform.localScale.x, 0, 0);
                    cards[i].gameObject.SetActive(true);
                }
                break;
            case Formation.ROW:
                float tRowWidth = (Card.zScale + spaceZ) * Count - spaceZ;
                for (int i = 0; i < Count; i++)
                {
                    float zToTranslate = -tRowWidth / 2 + i * (spaceZ + Card.zScale) + Card.zScale / 2;
                    cards[i].gameObject.transform.Translate(0, 0, zToTranslate*transform.localScale.z);
                    cards[i].gameObject.SetActive(true);
                }
                break;
            case Formation.STACK:
                //float tHeight = Card.yScale * Count;
                //this.gameObject.transform.localScale = new Vector3(Card.xScale, tHeight, Card.zScale);
                for (int i = 0; i < Count; i++)
                {
                    cards[i].gameObject.transform.Translate(0, i*(Card.yScale)*transform.localScale.y, 0);
                    cards[i].gameObject.SetActive(true);
                }
                break;
            default:
                break;
        }
    }

    public static Bundle Create(Formation f, float spaceX, float spaceZ)
    {
        Bundle b = Instantiate(BoardManagerController.Instance.bundlePrefab).GetComponent<Bundle>();
        Destroy(b.gameObject);
        b.display = f;
        b.spaceX = spaceX;
        b.spaceZ = spaceZ;
        return b;
    }

    private void Awake()
    {
        Debug.Log("Hello, I am a bundle!");
    }

    void Start()
    {
        //Add(Card.Create(1, "diamonds"));
        //Add(Card.Create(7, "clubs"));
        //Add(Card.Create(5, "spades"));
        //Add(Card.Create(13, "hearts"));
        SetDisplay(true);
    }

    // Update is called once per frame
    void Update()
    {
        if (trigger) {
            this.Remove(1);
            trigger = false;
        }
    }
}
