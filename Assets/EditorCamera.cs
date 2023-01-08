using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EditorCamera : MonoBehaviour
{

    public int speed;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        float mouseScroll = Input.GetAxis("Mouse ScrollWheel") * Time.deltaTime;
        this.transform.Translate(new Vector3(0, 0, mouseScroll * speed));
    }
}
