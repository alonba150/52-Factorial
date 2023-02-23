using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LineController : MonoBehaviour
{
    private LineRenderer lr;
    private Transform[] points;
    public bool isLineCreated = false;

    private void Awake()
    {
        lr = GetComponent<LineRenderer>();
    }

    public void StretchLine(Transform origin, Vector3 pointer)
    {
        
        lr.positionCount = 2;
        lr.SetPosition(0, origin.position + Vector3.up/100f);
        lr.SetPosition(1, new Vector3(pointer.x, origin.position.y, pointer.z) + Vector3.up/100f);
        isLineCreated = false;
    }

    public void CreateLine(Transform[] points)
    {
        lr.positionCount = points.Length;
        this.points = points;
        UpdateLine();
        isLineCreated = true;
    }

    public void UpdateLine()
    {
        if (this.points == null) return;
        for (int i = 0; i < points.Length; i++)
        {
            lr.SetPosition(i, points[i].position + Vector3.up/100f);
        }
    }

    public void DeleteLine()
    {
        Destroy(this.gameObject);
        //lr.positionCount = 0;
        //this.points = null;
        //isLineCreated = false;
    }

}
