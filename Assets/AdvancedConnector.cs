using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class AdvancedConnector : MonoBehaviour
{
    private AdvancedNode origin;
    private Dictionary<AdvancedConnector, LineController> targets = new Dictionary<AdvancedConnector, LineController>();

    public Dictionary<AdvancedConnector, LineController> Targets { get => targets; }

    private LineController dynamicLine = null;

    private Vector3 mousePos;
    private Vector3 cameraPos;

    public void SetOrigin(AdvancedNode origin)
    {
        this.origin = origin;
    }

    public void Connect(AdvancedConnector other)
    {
        if (origin == other.origin) return;
        LineController lc;
        if (targets.TryGetValue(other, out lc))
        {
            lc.DeleteLine();
            origin.RemoveLine(lc);
            other.origin.RemoveLine(lc);
            targets.Remove(other);
        }
        else
        {
            lc = EditorFactory.CreateLine();
            lc.CreateLine(new Transform[] { transform, other.transform });
            origin.AddLine(lc);
            other.origin.AddLine(lc);
            targets.Add(other, lc);
        }
    }

    private Vector3 GetMousePos()
    {
        return Camera.main.WorldToScreenPoint(transform.position);
    }

    private void OnMouseDown()
    {
        print("MOUSE DOWN");
        dynamicLine = EditorFactory.CreateLine();
        if (Input.GetMouseButton(1))
        {
            foreach (AdvancedConnector ac in targets.Keys.ToArray())
            {
                Connect(ac);
            }
        }
    }

    private void OnMouseDrag()
    {
        if (dynamicLine != null) dynamicLine.StretchLine(transform, Camera.main.ScreenToWorldPoint(Input.mousePosition + new Vector3(0,0,GetMousePos().z)));
    }

    private void OnMouseUp()
    {
        print("MOUSE UP");
        dynamicLine.DeleteLine();
        dynamicLine = null;
        Vector3 pos = Camera.main.ScreenToWorldPoint(Input.mousePosition + new Vector3(0, 0, GetMousePos().z));

        Collider[] colliders;
        AdvancedConnector other;
        if ((colliders = Physics.OverlapSphere(pos, 1f /* Radius */)).Length > 1)
        {
            foreach (var collider in colliders)
            {
                var gObj = collider.gameObject; 
                if (gObj == gameObject) continue; 
                if (gObj.TryGetComponent<AdvancedConnector>(out other))
                {
                    Connect(other);
                    break;
                }

            }
        }
    }

    private void Awake()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
