using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Draggable : MonoBehaviour
{
    Vector3 mousePos;


    private Vector3 GetMousePos()
    {
        return Camera.main.WorldToScreenPoint(transform.position);
    }

    private void OnMouseDown()
    {
        mousePos = Input.mousePosition - GetMousePos();
        transform.position = new Vector3(transform.position.x, transform.position.y + 1, transform.position.z);
    }

    private void OnMouseDrag()
    {
        Vector3 pos = Camera.main.ScreenToWorldPoint(Input.mousePosition - mousePos);
        transform.position = new Vector3(pos.x, transform.position.y, pos.z);
    }

    private void OnMouseUp()
    {
        transform.position = new Vector3(transform.position.x, transform.position.y - 1, transform.position.z);
    }
}
