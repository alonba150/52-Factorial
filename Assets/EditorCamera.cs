using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EditorCamera : MonoBehaviour
{

    public int rate;
    public int speed;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        float mouseScroll = Input.GetAxis("Mouse ScrollWheel");
        if (mouseScroll != 0)
        {
            this.transform.Translate(new Vector3(0, 0, mouseScroll * speed * Time.deltaTime * Mathf.Abs(this.transform.position.y - 5) * Mathf.Pow(rate, mouseScroll)));
        }
    }
}
