using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ConnectionType
{
    public enum IO {
        Input,
        Output,
    }

    public enum Signal
    {
        Pulse,
        Information
    }

    public IO io;
    public Signal signal;
    public object information;

    public ConnectionType(IO io, Signal signal, object information)
    {
        this.io = io;
        this.signal = signal;
        this.information = information;
    }

    public bool Match(ConnectionType other)
    {
        return (this.io != other.io) && (this.signal == other.signal) && (this.information.GetType().Equals(other.information.GetType()));
    }

}
