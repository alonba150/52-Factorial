using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LineController : MonoBehaviour
{
    private LineRenderer lr;
    private RectTransform[] points;
    public bool isLineCreated = false;

    private void Awake()
    {
        lr = GetComponent<LineRenderer>();
    }

    public void StretchLine(RectTransform origin, Vector2 pointer)
    {
        lr.positionCount = 2;
        lr.SetPosition(0, origin.position);
        lr.SetPosition(1, new Vector3(pointer.x, pointer.y, origin.position.z));
        isLineCreated = false;
    }

    public void CreateLine(RectTransform[] points)
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
            lr.SetPosition(i, points[i].position);
        }
    }

    public void DeleteLine()
    {
        lr.positionCount = 0;
        this.points = null;
        isLineCreated = false;
    }

}
