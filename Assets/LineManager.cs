using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LineManager : MonoBehaviour
{

    #region Singleton

    private LineManager() { }
    private static LineManager instance = null;
    public static LineManager Instance
    {
        get
        {
            if (instance == null)
            {
                instance = new LineManager();
            }
            return instance;
        }
    }

    #endregion

    public GameObject LinePrefab;

    private void Awake()
    {
        instance = this;
    }

}
