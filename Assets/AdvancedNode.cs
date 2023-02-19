using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AdvancedNode : MonoBehaviour
{

    private int inputsL = 3;
    private int outputsL = 3;
    private int triggersL = 1;
    private static int distance = 1;
    private static int thingSize = 5;
    public string code;
    public Dictionary<AdvancedNode, LineController> inputs;
    public Dictionary<AdvancedNode, LineController> outputs;
    public Dictionary<AdvancedNode, LineController> triggers;

    float GetHeight()
    {
        return (distance + thingSize) * Mathf.Max(inputsL + 1, outputsL + triggersL) + distance;
    }

    void Connect(AdvancedNode other)
    {

    }

    // Start is called before the first frame update
    void Start()
    {
        this.transform.localScale = new Vector3(1, 1, (float)(GetHeight()/30f));
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
