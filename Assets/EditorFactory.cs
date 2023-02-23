using System.Collections;
using System.Collections.Generic;
using UnityEngine;

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

    public static LineController CreateLine()
    {
        LineController c = Instantiate(LineManager.Instance.LinePrefab, LineManager.Instance.transform)
            .GetComponent<LineController>();
        return c;
    }

    public static AdvancedConnector CreateConnector(Vector3 pos, AdvancedNode parent)
    {
        AdvancedConnector c = Instantiate(Instance.advancedConnectorPrefab, pos, parent.transform.rotation, parent.transform)
            .GetComponent<AdvancedConnector>();
        c.SetOrigin(parent);
        return c;
    }
}
