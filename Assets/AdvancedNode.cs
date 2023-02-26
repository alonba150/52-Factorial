using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AdvancedNode : MonoBehaviour
{

    public static float planeScale = 10f;

    public System.Guid guid;

    private int inputsL = 3;
    private int outputsL = 3;
    private int triggersL = 1;
    private static int distance = 1;
    private static int thingSize = 5;
    public string code;
    public AdvancedConnector[] inputs;
    public AdvancedConnector[] outputs;
    public AdvancedConnector[] triggers;
    public AdvancedConnector trigger;

    public List<LineController> updateables = new List<LineController>();

    public void SetAttributes(int iL, int oL, int tL, string code)
    {
        inputsL = iL;
        inputs = new AdvancedConnector[inputsL];
        outputsL = oL;
        outputs = new AdvancedConnector[outputsL];
        triggersL = tL;
        triggers = new AdvancedConnector[triggersL];
        this.code = code;
        guid = System.Guid.NewGuid();
    }

    public void AddLine(LineController lc) { updateables.Add(lc); }
    public void RemoveLine(LineController lc) { updateables.Remove(lc); }

    float GetHeight()
    {
        return (distance + thingSize) * Mathf.Max(inputsL + 1, outputsL + triggersL) + distance;
    }

    void SetHeight() { this.transform.localScale = new Vector3(1, 1, (float)(GetHeight() / 30f)); }

    float GetConnectorSize() { return EditorFactory.Instance.advancedConnectorPrefab.transform.localScale.x * planeScale; }

    void PlaceConnectors()
    {

        Vector3 size = new Vector3(planeScale * transform.localScale.x, 0, planeScale * transform.localScale.z);

        Vector3 botLeft = -size / 2f;
        Vector3 topRight = size / 2f;
        Vector3 topLeft = Vector3.Scale(topRight, new Vector3(-1, 0, 1));

        Vector3 halfConnectorRight = new Vector3(GetConnectorSize() / 2f, 0, 0);
        Vector3 halfConnectorUp = new Vector3(0, 0, GetConnectorSize() / 2f);
        Vector3 distanceRight = new Vector3(distance, 0, 0);
        Vector3 distanceUp = new Vector3(0, 0, distance);

        Vector3 startingPos = topLeft + transform.position - distanceUp - halfConnectorUp + 
            distanceRight + halfConnectorRight + Vector3.up/100f;


        int i = 0;
        while (i < inputsL + 1 || i < triggersL + outputsL)
        {
            Vector3 currentPos = startingPos - (halfConnectorUp * 2 + distanceUp) * i;
            if (i == 0) trigger = EditorFactory.CreateConnector(currentPos, this, IO.TriggerIn, 0);
            else if (i < inputsL + 1) inputs[i-1] = EditorFactory.CreateConnector(currentPos, this, IO.Input, i - 1);
            currentPos = Vector3.Scale(currentPos - transform.position, new Vector3(-1, 1, 1)) + transform.position;
            print(i + " " + triggers.Length);
            if (i < triggersL) triggers[i] = EditorFactory.CreateConnector(currentPos, this, IO.TriggerOut, i);
            else if (i < outputsL + triggersL) outputs[i-triggersL] = EditorFactory.CreateConnector(currentPos, this, IO.Output,
                i - triggersL);
            i++;
        }
    }

    // Start is called before the first frame update
    void Start()
    {
        Draggable d = transform.gameObject.GetComponent<Draggable>();
        d.onDrag += UpdateLines;

        inputs = new AdvancedConnector[3];
        outputs = new AdvancedConnector[3];
        triggers = new AdvancedConnector[1];

        //SetHeight();
        PlaceConnectors();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private void UpdateLines()
    {
        foreach (LineController lc in updateables) { lc.UpdateLine(); }
    }

}
