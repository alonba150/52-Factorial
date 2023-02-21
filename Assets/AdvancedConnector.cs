using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AdvancedConnector : MonoBehaviour
{
    private AdvancedNode origin;
    private Dictionary<AdvancedNode, LineController> targets;

    public Dictionary<AdvancedNode, LineController> Targets { get => targets; }

    private LineController dynamicLine = null;

    public void Connect(AdvancedNode other)
    {
        //targets.Add(other, EditorFactory.CreateLine())
    }

    private Vector3 GetMousePos()
    {
        return Camera.main.WorldToScreenPoint(transform.position);
    }

    private void OnMouseDown()
    {
        dynamicLine = EditorFactory.CreateLine();
        dynamicLine.StretchLine(transform, Input.mousePosition);
    }

    private void OnMouseDrag()
    {
        if (dynamicLine != null) dynamicLine.StretchLine(transform, Input.mousePosition);
    }

    private void OnMouseUp()
    {
        dynamicLine.DeleteLine();
        Destroy(dynamicLine);
        dynamicLine = null;
        //if (Input.mousePosition.TryGetComponent<Connector>(out Connector connector))
        //{
        //    if (!ct.Match(connector.ct)) { Debug.Log("FAILED TO CONNECT"); return; }
        //    if (connector.next.Contains(this))
        //    {
        //        connector.next.Remove(this);
        //        connector.DeleteLine();
        //        Debug.Log("DELETED");
        //    }
        //    else
        //    {
        //        connector.next.Add(this);
        //        connector.ConnectLine(new RectTransform[] { rectTransform, connector.rectTransform });
        //        Debug.Log("ADDED");
        //    }
        //}
    }

    private void Awake()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
