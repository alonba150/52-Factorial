using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.EventSystems;
using System.Linq;

public class Connector : MonoBehaviour, IPointerDownHandler, IBeginDragHandler, IEndDragHandler, IDragHandler, IDropHandler
{
    [SerializeField] private Canvas canvas;
    [SerializeField] private LineController lc;

    private RectTransform rectTransform;
    private Vector2 canvasSize;
    private List<Connector> next = new List<Connector>();

    public ConnectionType ct;
    public ConnectionType.IO io;
    public ConnectionType.Signal signal;

    private void Awake()
    {
        rectTransform = GetComponent<RectTransform>();
        ct = new ConnectionType(io, signal, 0);
        canvasSize = canvas.GetComponent<RectTransform>().sizeDelta;
    }

    public void OnBeginDrag(PointerEventData eventData)
    {
    }

    public void OnDrag(PointerEventData eventData)
    {
        lc.StretchLine(rectTransform, (eventData.position - new Vector2(0.5f, 0.5f)*canvasSize)/45.5f);
    }

    public void OnEndDrag(PointerEventData eventData)
    {
        if (!lc.isLineCreated) DeleteLine();
    }

    public void OnPointerDown(PointerEventData eventData)
    {
        
    }

    public void OnDrop(PointerEventData eventData)
    {
        Debug.Log($"Dropped {ct.io}");
        if (eventData.pointerDrag == null) return;
        if (ct.io == ConnectionType.IO.Output) return;
        if (eventData.pointerDrag.TryGetComponent<Connector>(out Connector connector))
        {
            if (!ct.Match(connector.ct)) { Debug.Log("FAILED TO CONNECT"); return; }
            if (connector.next.Contains(this))
            {
                connector.next.Remove(this);
                connector.DeleteLine();
                Debug.Log("DELETED");
            }
            else{
                connector.next.Add(this);
                connector.ConnectLine(new RectTransform[] { rectTransform, connector.rectTransform });
                Debug.Log("ADDED");
            }
        }
    }

    public void ConnectLine(RectTransform[] rt) { lc.CreateLine(rt); }

    public void DeleteLine() { lc.DeleteLine(); }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

}
