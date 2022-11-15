using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class Node : MonoBehaviour, IPointerDownHandler, IPointerUpHandler, IBeginDragHandler, IEndDragHandler, IDragHandler
{
    private Node next = null;

    [SerializeField] private Canvas canvas;
    [SerializeField] private LineController lc;

    private RectTransform rectTransform;
    private CanvasGroup canvasGroup;
    private Canvas thisCanvas;

    private void Awake()
    {
        rectTransform = GetComponent<RectTransform>();
        canvasGroup = GetComponent<CanvasGroup>();
        thisCanvas = GetComponent<Canvas>();
    }

    public void OnBeginDrag(PointerEventData eventData)
    {
        lc.UpdateLine();
    }

    public void OnDrag(PointerEventData eventData)
    {
        rectTransform.anchoredPosition += eventData.delta / canvas.scaleFactor;
        lc.UpdateLine();
    }

    public void OnEndDrag(PointerEventData eventData)
    {
        lc.UpdateLine();
    }

    public void OnPointerDown(PointerEventData eventData)
    {
        thisCanvas.sortingOrder = 10;
        rectTransform.localScale = new Vector3(1.1f, 1.1f, 1);
        canvasGroup.blocksRaycasts = false;
        lc.UpdateLine();
    }

    public void OnPointerUp(PointerEventData eventData)
    {
        thisCanvas.sortingOrder = 0;
        rectTransform.localScale = new Vector3(1, 1, 1);
        canvasGroup.blocksRaycasts = true;
        lc.UpdateLine();
    }

    void UpdateLines()
    {
        //GetComponentsInChildren<>
    }
    
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

}
