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
    public List<AdvancedNode>[] inputs;
    public AdvancedConnector[] outputs;
    public AdvancedConnector[] triggers;

    float GetHeight()
    {
        return (distance + thingSize) * Mathf.Max(inputsL + 1, outputsL + triggersL) + distance;
    }

    void SetHeight() { this.transform.localScale = new Vector3(1, 1, (float)(GetHeight() / 30f)); }

    void PlaceConnectors()
    {
        Vector3 topLeft = transform.TransformVector(0, 0, 0);
        topLeft.y = 0;
        Vector3 botRight = transform.TransformVector(1, 0, 1);
        float w = Mathf.Abs(topLeft.x - botRight.x);
        float h = Mathf.Abs(topLeft.z - botRight.z);

        EditorFactory.CreateConnector(topLeft - new Vector3(distance + thingSize / 2f, 0, distance + thingSize / 2f),
            gameObject);
    }

    // Start is called before the first frame update
    void Start()
    {
        SetHeight();
        PlaceConnectors();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

}
