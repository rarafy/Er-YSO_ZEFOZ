using System.Collections.Generic;
using System.Linq;
using Sirenix.OdinInspector;
using UnityEngine;

public class Display_Crystal : SerializedMonoBehaviour
{
    [SerializeField] private Er2SiO5_UnitCell crystal;
    [SerializeField] private Transform _parent;

    [SerializeField] private Material yMaterial;
    [SerializeField] private Material siMaterial;
    [SerializeField] private Material oMaterial;

    private List<GameObject> _generatedAtomObject = new List<GameObject>();


    private void Start()
    {
        var i = 0;
        _generatedAtomObject.ForEach(Destroy);
        _generatedAtomObject = new List<GameObject>();

        foreach (var collection in crystal.Atoms.Keys)
        {
            crystal.Atoms.TryGetValue(collection, out var atoms);

            foreach (var atom in atoms!)
            {
                for (var j = -1; j <= 1; j++)
                {
                    for (var k = -1; k <= 1; k++)
                    {
                        for (var l = -1; l <= 1; l++)
                        {
                            var offset = new Vector3(
                                        (crystal.a * Mathf.Cos((crystal.Beta - 90) * Mathf.PI / 180)),
                                        (crystal.b),
                                        (crystal.c * l - crystal.a * Mathf.Sin((crystal.Beta - 90) * Mathf.PI / 180) * -j)
                                        );


                            // x, z‚ª‹t‚Ì’l‚É‚È‚Á‚Ä‚¢‚é‚Ì‚Í‰EŽèŒn‚Æ¶ŽèŒn‚ð•ÏŠ·‚·‚é‚½‚ß
                            var atomPosition = new Vector3(
                                -(crystal.a * atom.x * Mathf.Cos((crystal.Beta - 90) * Mathf.PI / 180)),
                                -(crystal.b * atom.y),
                                (crystal.c * atom.z - crystal.a * atom.x * Mathf.Sin((crystal.Beta - 90) * Mathf.PI / 180))
                                );
                            atomPosition = atomPosition + Vector3.Scale(offset, new Vector3(j, k, 1));
                            var atomObject = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                            atomObject.transform.parent = _parent;
                            atomObject.transform.localPosition = atomPosition;
                            atomObject.transform.localScale = 0.3f * Vector3.one;
                            atomObject.name = collection + i;
                            i++;
                            switch (collection)
                            {
                                case "Y":
                                    atomObject.GetComponent<MeshRenderer>().material = yMaterial;
                                    break;
                                case "Si":
                                    atomObject.GetComponent<MeshRenderer>().material = siMaterial;
                                    Destroy(atomObject);
                                    continue;
                                    break;
                                case "O":
                                    atomObject.GetComponent<MeshRenderer>().material = oMaterial;
                                    Destroy(atomObject);
                                    continue;
                                    break;
                                default:
                                    atomObject.GetComponent<MeshRenderer>().material =
                                        atomObject.GetComponent<MeshRenderer>().material;
                                    break;
                            }

                            atomObject.AddComponent<Atom>();
                            _generatedAtomObject.Add(atomObject);
                        }
                    }
                }
            }
        }
    }

    [Button(ButtonSizes.Medium)]
    private void ExportAtomPositions()
    {
        var resultListVector4 = (from obj in _generatedAtomObject
                                 select obj.transform.position
                                            into pos
                                 let r = pos.magnitude
                                 select new Vector4(pos.x, pos.y, pos.z, r)).ToList();

        resultListVector4 = new List<Vector4>(resultListVector4.OrderBy(vec => vec.w));
        var result = resultListVector4.Aggregate("", (currentResult, vector4) => currentResult + vector4.ToString("F5") + "\n");

        Debug.Log(result);
        GUIUtility.systemCopyBuffer = result;
    }


}
