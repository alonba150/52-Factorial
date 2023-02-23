using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EditorCamera : MonoBehaviour
{

    public int rate;
    public int speed;

    private Vector3 difference;
    private Vector3 origin;
    private bool drag;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void LateUpdate()
    {
        float mouseScroll = Input.GetAxis("Mouse ScrollWheel");
        if (mouseScroll != 0)
        {
            this.transform.Translate(new Vector3(0, 0, mouseScroll * speed * Time.deltaTime * Mathf.Abs(this.transform.position.y - 5) * Mathf.Pow(rate, mouseScroll)));
        }

        if (Input.GetMouseButton(2))
        {
            Vector3 additive = new Vector3(0, 0, this.transform.position.y);
            difference = Camera.main.ScreenToWorldPoint(Input.mousePosition + additive) - Camera.main.transform.position;
            if (drag == false)
            {
                drag = true;
                origin = Camera.main.ScreenToWorldPoint(Input.mousePosition + additive);
            }
        }
        else drag = false;

        if (drag)
        {
            this.transform.position = origin - difference;
        }
    }
}
