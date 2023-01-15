using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class Bundle : MonoBehaviour
{
    public enum Formation
    {
        ROW = 0,
        COLUMN = 1,
        STACK = 2
    }

    [SerializeField]
    private List<Card> cards = new List<Card>();
    public Card[] Cards { get => cards.ToArray(); }

    public bool trigger = false;
    public bool remove_card = false;

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

    public float x;
    public float z;

    public float rotation;

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

    public void ReverseCardOrder()
    {
        this.cards.Reverse();
    }
    #endregion

    #region Display Functions
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
        for (int i = 0; i < Count; i++) { cards[i].gameObject.SetActive(false); cards[i].transform.position = this.transform.position; }
        if (Count < 1 || !displayActive) return;
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
    #endregion

    public static Bundle Create(Formation f, float spaceX, float spaceZ, float x, float z, float rotation)
    {
        Bundle b = Instantiate(BoardManagerController.Instance.bundlePrefab).GetComponent<Bundle>();
        Destroy(b.gameObject);
        b.display = f;
        b.spaceX = spaceX;
        b.spaceZ = spaceZ;
        b.rotation = rotation;
        b.x = x;
        b.z = z;
        return b;
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

    public Bundle Enable(float x, float z, float rotation, Quaternion quat)
    {
        this.x = x;
        this.z = z;
        Bundle b = Instantiate(this, new Vector3(this.x, 0.5f, this.z), quat);
        b.transform.Rotate(new Vector3(0, rotation, 0), Space.World);
        b.name = "Bundle";
        b.enabled = true;
        b.gameObject.SetActive(true);
        b.SetDisplay(true);
        return b;
    }

    public Bundle Enable(Quaternion quat)
    {
        Bundle b = Instantiate(this, new Vector3(this.x, 0.5f, this.z), quat);
        b.transform.Rotate(new Vector3(0, this.rotation, 0), Space.World);
        b.name = "Bundle";
        b.enabled = true;
        b.gameObject.SetActive(true);
        b.SetDisplay(true);
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
        if (trigger)
        {
            this.Display();
            trigger = false;
        }
        if (remove_card) {
            this.Remove(1);
            remove_card = false;
        }
    }
}
