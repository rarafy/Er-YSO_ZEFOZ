using System.Collections.Generic;
using System.Dynamic;
using Sirenix.OdinInspector;
using UnityEngine;

public class Er2SiO5_UnitCell : SerializedMonoBehaviour, IUnitCell
{
    [SerializeField] private float _a = 14.56434f;
    public float a => _a;
    [SerializeField] private float _b = 6.83539f;
    public float b => _b;
    [SerializeField] private float _c = 10.55697f;
    public float c => _c;

    [SerializeField] private float _Alpha = 90.0000f;
    public float Alpha => _Alpha;
    [SerializeField] private float _Beta = 122.1320f;
    public float Beta => _Beta;
    [SerializeField] private float _Gamma = 90.0000f;
    public float Gamma => _Gamma;

    [SerializeField]
    private List<Vector3> Y = new List<Vector3>();
    [SerializeField]
    private List<Vector3> Si = new List<Vector3>();
    [SerializeField]
    private List<Vector3> O = new List<Vector3>();


    public Dictionary<string, List<Vector3>> Atoms = new Dictionary<string, List<Vector3>>();

    private void Reset()
    {
        for (int i = 0; i < 16; i++)
        {
            var y = GetType().GetField(nameof(Y) + i,
                System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            Y.Add((Vector3)y.GetValue(this));
        }
        for (int j = 16; j < 24; j++)
        {
            var si = GetType().GetField(nameof(Si) + j,
                System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            Si.Add((Vector3)si.GetValue(this));
        }
        for (int k = 24; k < 64; k++)
        {
            var o = GetType().GetField(nameof(O) + k,
                System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            O.Add((Vector3)o.GetValue(this));
        }

        Atoms = new Dictionary<string, List<Vector3>>();
        Atoms.Add(nameof(Y), Y);
        Atoms.Add(nameof(Si), Si);
        Atoms.Add(nameof(O), O);
    }

    private Vector3 Y0 = new Vector3(0.96304f, 0.25571f, 0.03240f);
    private Vector3 Y1 = new Vector3(0.03696f, 0.25571f, 0.46760f);
    private Vector3 Y2 = new Vector3(0.03696f, 0.74429f, 0.96760f);
    private Vector3 Y3 = new Vector3(0.96304f, 0.74429f, 0.53240f);
    private Vector3 Y4 = new Vector3(0.14264f, 0.61805f, 0.33749f);
    private Vector3 Y5 = new Vector3(0.85736f, 0.61805f, 0.16251f);
    private Vector3 Y6 = new Vector3(0.85736f, 0.38195f, 0.66251f);
    private Vector3 Y7 = new Vector3(0.14264f, 0.38195f, 0.83749f);
    private Vector3 Y8 = new Vector3(0.46304f, 0.75571f, 0.03240f);
    private Vector3 Y9 = new Vector3(0.53696f, 0.75571f, 0.46760f);
    private Vector3 Y10 = new Vector3(0.53696f, 0.24429f, 0.96760f);
    private Vector3 Y11 = new Vector3(0.46304f, 0.24429f, 0.53240f);
    private Vector3 Y12 = new Vector3(0.64264f, 0.11805f, 0.33749f);
    private Vector3 Y13 = new Vector3(0.35736f, 0.11805f, 0.16251f);
    private Vector3 Y14 = new Vector3(0.35736f, 0.88195f, 0.66251f);
    private Vector3 Y15 = new Vector3(0.64264f, 0.88195f, 0.83749f);
    private Vector3 Si16 = new Vector3(0.68177f, 0.59011f, 0.30568f);
    private Vector3 Si17 = new Vector3(0.81823f, 0.09011f, 0.19432f);
    private Vector3 Si18 = new Vector3(0.31822f, 0.40989f, 0.69432f);
    private Vector3 Si19 = new Vector3(0.18178f, 0.90989f, 0.80568f);
    private Vector3 Si20 = new Vector3(0.18178f, 0.09011f, 0.30568f);
    private Vector3 Si21 = new Vector3(0.31822f, 0.59011f, 0.19432f);
    private Vector3 Si22 = new Vector3(0.81823f, 0.90989f, 0.69432f);
    private Vector3 Si23 = new Vector3(0.68177f, 0.40989f, 0.80568f);
    private Vector3 O24 = new Vector3(0.98334f, 0.59379f, 0.10422f);
    private Vector3 O25 = new Vector3(0.01667f, 0.59379f, 0.39578f);
    private Vector3 O26 = new Vector3(0.01667f, 0.40621f, 0.89578f);
    private Vector3 O27 = new Vector3(0.98334f, 0.40621f, 0.60422f);
    private Vector3 O28 = new Vector3(0.20118f, 0.92701f, 0.43196f);
    private Vector3 O29 = new Vector3(0.79882f, 0.92701f, 0.06804f);
    private Vector3 O30 = new Vector3(0.79882f, 0.07299f, 0.56804f);
    private Vector3 O31 = new Vector3(0.20118f, 0.07299f, 0.93196f);
    private Vector3 O32 = new Vector3(0.79703f, 0.64803f, 0.32369f);
    private Vector3 O33 = new Vector3(0.70297f, 0.14803f, 0.17631f);
    private Vector3 O34 = new Vector3(0.20297f, 0.35197f, 0.67631f);
    private Vector3 O35 = new Vector3(0.29703f, 0.85197f, 0.82369f);
    private Vector3 O36 = new Vector3(0.12060f, 0.71645f, 0.82423f);
    private Vector3 O37 = new Vector3(0.87940f, 0.71645f, 0.67577f);
    private Vector3 O38 = new Vector3(0.87940f, 0.28355f, 0.17578f);
    private Vector3 O39 = new Vector3(0.12060f, 0.28355f, 0.32423f);
    private Vector3 O40 = new Vector3(0.09070f, 0.99086f, 0.63757f);
    private Vector3 O41 = new Vector3(0.40930f, 0.49086f, 0.86243f);
    private Vector3 O42 = new Vector3(0.90930f, 0.00914f, 0.36244f);
    private Vector3 O43 = new Vector3(0.59070f, 0.50914f, 0.13757f);
    private Vector3 O44 = new Vector3(0.48333f, 0.09379f, 0.10422f);
    private Vector3 O45 = new Vector3(0.51666f, 0.09379f, 0.39578f);
    private Vector3 O46 = new Vector3(0.51666f, 0.90621f, 0.89578f);
    private Vector3 O47 = new Vector3(0.48333f, 0.90621f, 0.60422f);
    private Vector3 O48 = new Vector3(0.70118f, 0.42701f, 0.43196f);
    private Vector3 O49 = new Vector3(0.29882f, 0.42701f, 0.06804f);
    private Vector3 O50 = new Vector3(0.29882f, 0.57299f, 0.56804f);
    private Vector3 O51 = new Vector3(0.70118f, 0.57299f, 0.93196f);
    private Vector3 O52 = new Vector3(0.29703f, 0.14803f, 0.32369f);
    private Vector3 O53 = new Vector3(0.20297f, 0.64803f, 0.17631f);
    private Vector3 O54 = new Vector3(0.70297f, 0.85197f, 0.67631f);
    private Vector3 O55 = new Vector3(0.79703f, 0.35197f, 0.82369f);
    private Vector3 O56 = new Vector3(0.62060f, 0.21645f, 0.82423f);
    private Vector3 O57 = new Vector3(0.37940f, 0.21645f, 0.67577f);
    private Vector3 O58 = new Vector3(0.37940f, 0.78355f, 0.17578f);
    private Vector3 O59 = new Vector3(0.62060f, 0.78355f, 0.32423f);
    private Vector3 O60 = new Vector3(0.59070f, 0.49086f, 0.63757f);
    private Vector3 O61 = new Vector3(0.90930f, 0.99086f, 0.86243f);
    private Vector3 O62 = new Vector3(0.40930f, 0.50914f, 0.36244f);
    private Vector3 O63 = new Vector3(0.09070f, 0.00914f, 0.13757f);
}
