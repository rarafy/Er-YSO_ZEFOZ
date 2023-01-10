using Sirenix.OdinInspector;
using UnityEngine;

public class Atom : MonoBehaviour
{
    [SerializeField, ReadOnly]
    private Vector3 _globalPosition;
    private Vector3 globalPosition
    {
        get => _globalPosition;
        set
        {
            if (_globalPosition == value) return;
            _globalPosition = value;
            distanceFromZero = globalPosition.magnitude;
        }
    }
    [SerializeField, ReadOnly] private float distanceFromZero;

    private void Update()
    {
        globalPosition = this.transform.position;
    }

    [Button(ButtonSizes.Medium, ButtonStyle.Box)]
    private void Centerize()
    {
        var _parent = this.transform.parent;
        _parent.transform.position = -this.transform.localPosition;
    }
}
