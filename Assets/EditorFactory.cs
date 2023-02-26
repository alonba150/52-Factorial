using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class EditorFactory : MonoBehaviour
{

    #region Singleton

    private EditorFactory() { }
    private static EditorFactory instance = null;
    public static EditorFactory Instance
    {
        get
        {
            if (instance == null)
            {
                instance = new EditorFactory();
            }
            return instance;
        }
    }

    #endregion

    private void Awake()
    {
        instance = this;
    }

    public GameObject advancedConnectorPrefab;
    public GameObject advancedNodePrefab;

    private List<AdvancedNode> nodes = new List<AdvancedNode>();

    public static LineController CreateLine()
    {
        LineController c = Instantiate(LineManager.Instance.LinePrefab, LineManager.Instance.transform)
            .GetComponent<LineController>();
        return c;
    }

    public static AdvancedConnector CreateConnector(Vector3 pos, AdvancedNode parent, IO type, int index)
    {
        AdvancedConnector c = Instantiate(Instance.advancedConnectorPrefab, pos, parent.transform.rotation, parent.transform)
            .GetComponent<AdvancedConnector>();
        c.SetAttributes(parent, type, index);
        return c;
    }

    public static AdvancedNode CreateNode(Vector3 pos, string code="")
    {
        pos.y = 0.1f;
        AdvancedNode n = Instantiate(Instance.advancedNodePrefab, pos, Quaternion.identity).GetComponent<AdvancedNode>();
        Instance.nodes.Add(n);
        n.SetAttributes(2, 1, 1, "B000");
        return n;
    }

    public void CreateNode()
    {
        CreateNode(Vector3.zero);
    }

    public string GetNodes()
    {
        string res = "";
        foreach (AdvancedNode node in Instance.nodes)
        {
            res += $"{node.guid.ToString().Substring(0, 3)}: [";
            res += node.code;
            res += '*';
            foreach (AdvancedConnector input in node.inputs)
            {
                //input.
            }
            res += '*';
            if (node.outputs.Any(t => t != null)) {
                List<string> toAdd = new List<string>();
                foreach (AdvancedConnector output in node.outputs)
                {
                    if (output != null && output.Targets.Keys.Count > 0)
                        toAdd.Add($"({string.Join('/', output.Targets.Keys.Select(t => t.origin.guid.ToString().Substring(0, 3)).ToList())})");
                }
                if (toAdd.Count > 0)
                {
                    res += "{";
                    res += string.Join("//", toAdd);
                    res += "}";
                }
            }
            res += '*';
            if (node.triggers.Any(t => t != null))
            {
                List<string> toAdd = new List<string>();
                foreach (AdvancedConnector trigger in node.triggers) 
                {
                    if (trigger != null && trigger.Targets.Keys.Count > 0)
                        toAdd.Add($"({string.Join('/', trigger.Targets.Keys.Select(t => t.origin.guid.ToString().Substring(0, 3)).ToList())})");
                }
                if (toAdd.Count > 0)
                {
                    res += "{";
                    res += string.Join("//", toAdd);
                    res += "}";
                }
            }

            res += "]///";
        }
        return res;
    }

    public void PrintNodeString()
    {
        print(GetNodes());
    }
}
