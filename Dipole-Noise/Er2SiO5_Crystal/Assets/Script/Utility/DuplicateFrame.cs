using System.Collections;
using System.Collections.Generic;
using Sirenix.OdinInspector;
using UnityEngine;

public class DuplicateFrame : MonoBehaviour
{
    [SerializeField] private Transform _frame;
    [SerializeField] private float a;
    [SerializeField] private float b;
    [SerializeField] private float c;
    [SerializeField] private float Beta;

    [Button(ButtonSizes.Medium)]
    void Duplicate()
    {
        for (var j = -1; j <= 1; j++)
        {
            for (var k = -1; k <= 1; k++)
            {
                for (var l = -1; l <= 1; l++)
                {
                    var offset = new Vector3(
                        (a * Mathf.Cos((Beta - 90) * Mathf.PI / 180)),
                        (b),
                        (c * l - a * Mathf.Sin((Beta - 90) * Mathf.PI / 180) * -j)
                    );
                    offset = Vector3.Scale(offset, new Vector3(j, k, 1));

                    var instantiatedTransform = Instantiate(_frame, _frame.localPosition + offset, _frame.rotation);

                    instantiatedTransform.parent = _frame.parent;
                }
            }
        }
    }
}
