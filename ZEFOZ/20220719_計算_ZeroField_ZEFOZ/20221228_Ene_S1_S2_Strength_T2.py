import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.cm as cm
from scipy.linalg import eigh
from PhysicalConstant_DB import PhysicalConstant_DB
from RareEarthIon_DopedInCrystal import RareEarthIon_DopedInCrystal
from Er167_Y2SiO5 import Er167_Y2SiO5

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.top'] = True
plt.rcParams['xtick.major.size'] = 7
plt.rcParams['ytick.major.size'] = 7
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.style.use(["science", "nature"])
# 図示(色コード)
# デフォ
# plt.rcParams['axes.prop_cycle'] = cycler(color=['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747', '#9e9e9e'])
# クロ
# plt.rcParams['axes.prop_cycle'] = cycler(color=['#9e9e9e', '#9e9e9e', '#9e9e9e', '#9e9e9e', '#9e9e9e', '#9e9e9e', '#20D220', '#9e9e9e',
#                                                 '#FFAA00', '#9e9e9e', '#9e9e9e', '#9e9e9e', '#9e9e9e', '#9e9e9e', '#9e9e9e', '#9e9e9e'])
# カラフル
# plt.rcParams['axes.prop_cycle'] = cycler(color=['#D8D83D', '#FFC000', '#FF0000', '#009900', '#6FCF10', '#67E1E1', '#20D220', '#DADA46',
#                                                 '#FFAA00', '#FF0000', '#CC01A4', '#6700CC', '#0032CC', '#0088CC', '#00CCCC', '#009999'])

if __name__ == '__main__':
    """
    Bx0 float:
        グラフの左端

    Bx1 float:
        グラフの右端

    nB int:
        分割数（どれくらいの精度で計算するか）
    """
    Bx0 = -0.1
    Bx1 = 0.1
    nB = 1001
    # deltaB_x = (Bx1 - Bx0) / nB
    deltaB_x = 0
    deltaB_y = 0
    deltaB_z = 8e-06
    Bx: {np.ndarray: (nB,)} = np.linspace(Bx0, Bx1, nB)
    By: {np.ndarray: (nB,)} = np.zeros(nB)
    Bz: {np.ndarray: (nB,)} = np.zeros(nB)
    B: {np.ndarray: (nB, 3)} = np.transpose([Bx, By, Bz])

    zeta_x = Er167_Y2SiO5.Perturbation_Zeta("x")
    zeta_y = Er167_Y2SiO5.Perturbation_Zeta("y")
    zeta_z = Er167_Y2SiO5.Perturbation_Zeta("z")

    energy = []
    vectors: {np.ndarray: (16, 16, 601)} = []
    energy_gradient_x = []
    energy_gradient_y = []
    energy_gradient_z = []
    energy_curvature_xx = []
    energy_curvature_xy = []
    energy_curvature_xz = []
    energy_curvature_yx = []
    energy_curvature_yy = []
    energy_curvature_yz = []
    energy_curvature_zx = []
    energy_curvature_zy = []
    energy_curvature_zz = []
    transitionStrength_x = []
    transitionStrength_y = []
    transitionStrength_z = []

    Sx, Sy, Sz = Er167_Y2SiO5.S()
    Ix, Iy, Iz = Er167_Y2SiO5.I()

    # エネルギー計算（摂動行列、振動子強度、Gradient、Curvature）
    for Bj in B:
        # 固有値，固有ベクトル
        val, vec = eigh(RareEarthIon_DopedInCrystal.Hamiltonian_odd(PhysicalConstant_DB.beta_e,
                                                                    PhysicalConstant_DB.beta_n,
                                                                    Er167_Y2SiO5.gn(),
                                                                    Bj,
                                                                    Er167_Y2SiO5.A(1),
                                                                    Er167_Y2SiO5.g(1),
                                                                    Er167_Y2SiO5.Q(1),
                                                                    Er167_Y2SiO5.I()[0],
                                                                    Er167_Y2SiO5.I()[1],
                                                                    Er167_Y2SiO5.I()[2],
                                                                    Er167_Y2SiO5.S()[0],
                                                                    Er167_Y2SiO5.S()[1],
                                                                    Er167_Y2SiO5.S()[2]))
        energy.append(val)
        vectors.append(vec)

        perturbationMatrix_x = np.dot(np.conjugate(vec.T), np.dot(zeta_x, vec))
        perturbationMatrix_y = np.dot(np.conjugate(vec.T), np.dot(zeta_y, vec))
        perturbationMatrix_z = np.dot(np.conjugate(vec.T), np.dot(zeta_z, vec))

        transitionStrength_x.append(np.absolute(perturbationMatrix_x))
        transitionStrength_y.append(np.absolute(perturbationMatrix_y))
        transitionStrength_z.append(np.absolute(perturbationMatrix_z))

        energy_gradient_x.append(np.real(np.diag(perturbationMatrix_x)))
        energy_gradient_y.append(np.real(np.diag(perturbationMatrix_y)))
        energy_gradient_z.append(np.real(np.diag(perturbationMatrix_z)))

        _tempCurvature_xx = []
        _tempCurvature_xy = []
        _tempCurvature_xz = []
        _tempCurvature_yx = []
        _tempCurvature_yy = []
        _tempCurvature_yz = []
        _tempCurvature_zx = []
        _tempCurvature_zy = []
        _tempCurvature_zz = []
        for p in range(0, 16):
            _tempTempCurvature_xx = 0
            _tempTempCurvature_xy = 0
            _tempTempCurvature_xz = 0
            _tempTempCurvature_yx = 0
            _tempTempCurvature_yy = 0
            _tempTempCurvature_yz = 0
            _tempTempCurvature_zx = 0
            _tempTempCurvature_zy = 0
            _tempTempCurvature_zz = 0
            for q in range(0, 16):
                if p == q:
                    continue
                else:
                    _tempTempCurvature_xx += (perturbationMatrix_x[p, q] * perturbationMatrix_x[q, p]) / (val[p] - val[q]) * 2
                    _tempTempCurvature_xy += (perturbationMatrix_x[p, q] * perturbationMatrix_y[q, p]) / (val[p] - val[q]) * 2
                    _tempTempCurvature_xz += (perturbationMatrix_x[p, q] * perturbationMatrix_z[q, p]) / (val[p] - val[q]) * 2
                    _tempTempCurvature_yx += (perturbationMatrix_y[p, q] * perturbationMatrix_x[q, p]) / (val[p] - val[q]) * 2
                    _tempTempCurvature_yy += (perturbationMatrix_y[p, q] * perturbationMatrix_y[q, p]) / (val[p] - val[q]) * 2
                    _tempTempCurvature_yz += (perturbationMatrix_y[p, q] * perturbationMatrix_z[q, p]) / (val[p] - val[q]) * 2
                    _tempTempCurvature_zx += (perturbationMatrix_z[p, q] * perturbationMatrix_x[q, p]) / (val[p] - val[q]) * 2
                    _tempTempCurvature_zy += (perturbationMatrix_z[p, q] * perturbationMatrix_y[q, p]) / (val[p] - val[q]) * 2
                    _tempTempCurvature_zz += (perturbationMatrix_z[p, q] * perturbationMatrix_z[q, p]) / (val[p] - val[q]) * 2
            _tempCurvature_xx.append(_tempTempCurvature_xx)
            _tempCurvature_xy.append(_tempTempCurvature_xy)
            _tempCurvature_xz.append(_tempTempCurvature_xz)
            _tempCurvature_yx.append(_tempTempCurvature_yx)
            _tempCurvature_yy.append(_tempTempCurvature_yy)
            _tempCurvature_yz.append(_tempTempCurvature_yz)
            _tempCurvature_zx.append(_tempTempCurvature_zx)
            _tempCurvature_zy.append(_tempTempCurvature_zy)
            _tempCurvature_zz.append(_tempTempCurvature_zz)
        energy_curvature_xx.append(_tempCurvature_xx)
        energy_curvature_xy.append(_tempCurvature_xy)
        energy_curvature_xz.append(_tempCurvature_xz)
        energy_curvature_yx.append(_tempCurvature_yx)
        energy_curvature_yy.append(_tempCurvature_yy)
        energy_curvature_yz.append(_tempCurvature_yz)
        energy_curvature_zx.append(_tempCurvature_zx)
        energy_curvature_zy.append(_tempCurvature_zy)
        energy_curvature_zz.append(_tempCurvature_zz)

    energy = np.array(energy)
    vectors = np.array(vectors)
    energy_gradient_x = np.array(energy_gradient_x)
    energy_gradient_y = np.array(energy_gradient_y)
    energy_gradient_z = np.array(energy_gradient_z)
    energy_curvature_xx = np.array(energy_curvature_xx)
    energy_curvature_xy = np.array(energy_curvature_xy)
    energy_curvature_xz = np.array(energy_curvature_xz)
    energy_curvature_yx = np.array(energy_curvature_yx)
    energy_curvature_yy = np.array(energy_curvature_yy)
    energy_curvature_yz = np.array(energy_curvature_yz)
    energy_curvature_zx = np.array(energy_curvature_zx)
    energy_curvature_zy = np.array(energy_curvature_zy)
    energy_curvature_zz = np.array(energy_curvature_zz)
    transitionStrength_x = np.array(transitionStrength_x)
    transitionStrength_y = np.array(transitionStrength_y)
    transitionStrength_z = np.array(transitionStrength_z)

    # 差分処理（p-q）
    energy_pq = []
    energy_gradient_pq_x = []
    energy_gradient_pq_y = []
    energy_gradient_pq_z = []
    energy_curvature_pq_xx = []
    energy_curvature_pq_xy = []
    energy_curvature_pq_xz = []
    energy_curvature_pq_yx = []
    energy_curvature_pq_yy = []
    energy_curvature_pq_yz = []
    energy_curvature_pq_zx = []
    energy_curvature_pq_zy = []
    energy_curvature_pq_zz = []
    transitionStrength_pq_x = []
    transitionStrength_pq_y = []
    transitionStrength_pq_z = []
    t2_hyp = []
    for p in range(0, 16):
        for q in range(0, 16):
            if p > q:
                _tempEnergy_pq = energy[:, p] - energy[:, q]
                _tempGradient_pq_x = energy_gradient_x[:, p] - energy_gradient_x[:, q]
                _tempGradient_pq_y = energy_gradient_y[:, p] - energy_gradient_y[:, q]
                _tempGradient_pq_z = energy_gradient_z[:, p] - energy_gradient_z[:, q]
                _tempCurvature_pq_xx = energy_curvature_xx[:, p] - energy_curvature_xx[:, q]
                _tempCurvature_pq_xy = energy_curvature_xy[:, p] - energy_curvature_xy[:, q]
                _tempCurvature_pq_xz = energy_curvature_xz[:, p] - energy_curvature_xz[:, q]
                _tempCurvature_pq_yx = energy_curvature_yx[:, p] - energy_curvature_yx[:, q]
                _tempCurvature_pq_yy = energy_curvature_yy[:, p] - energy_curvature_yy[:, q]
                _tempCurvature_pq_yz = energy_curvature_yz[:, p] - energy_curvature_yz[:, q]
                _tempCurvature_pq_zx = energy_curvature_zx[:, p] - energy_curvature_zx[:, q]
                _tempCurvature_pq_zy = energy_curvature_zy[:, p] - energy_curvature_zy[:, q]
                _tempCurvature_pq_zz = energy_curvature_zz[:, p] - energy_curvature_zz[:, q]
                energy_pq.append(_tempEnergy_pq)
                energy_gradient_pq_x.append(_tempGradient_pq_x)
                energy_gradient_pq_y.append(_tempGradient_pq_y)
                energy_gradient_pq_z.append(_tempGradient_pq_z)
                energy_curvature_pq_xx.append(_tempCurvature_pq_xx)
                energy_curvature_pq_xy.append(_tempCurvature_pq_xy)
                energy_curvature_pq_xz.append(_tempCurvature_pq_xz)
                energy_curvature_pq_yx.append(_tempCurvature_pq_yx)
                energy_curvature_pq_yy.append(_tempCurvature_pq_yy)
                energy_curvature_pq_yz.append(_tempCurvature_pq_yz)
                energy_curvature_pq_zx.append(_tempCurvature_pq_zx)
                energy_curvature_pq_zy.append(_tempCurvature_pq_zy)
                energy_curvature_pq_zz.append(_tempCurvature_pq_zz)
                transitionStrength_pq_x.append(transitionStrength_x[:, p, q])
                transitionStrength_pq_y.append(transitionStrength_y[:, p, q])
                transitionStrength_pq_z.append(transitionStrength_z[:, p, q])

                _tempT2_hyp_x = deltaB_x * _tempCurvature_pq_xx * deltaB_x + deltaB_x * _tempCurvature_pq_xy * deltaB_y \
                                + deltaB_x * _tempCurvature_pq_xz * deltaB_z + _tempGradient_pq_x * deltaB_x
                _tempT2_hyp_y = deltaB_y * _tempCurvature_pq_yx * deltaB_x + deltaB_y * _tempCurvature_pq_yy * deltaB_y \
                                + deltaB_y * _tempCurvature_pq_yz * deltaB_z + _tempGradient_pq_y * deltaB_y
                _tempT2_hyp_z = deltaB_z * _tempCurvature_pq_zx * deltaB_x + deltaB_z * _tempCurvature_pq_zy * deltaB_y \
                                + deltaB_z * _tempCurvature_pq_zz * deltaB_z + _tempGradient_pq_z * deltaB_z
                t2_hyp.append(1 / (abs(_tempT2_hyp_x + _tempT2_hyp_y + _tempT2_hyp_z) * np.pi))

                text = str(p) + "-" + str(q) + ":" + "\n" \
                       + "Transition Frequency: " + str(_tempEnergy_pq[(nB - 1) // 2]) + "\n" \
                       + "T2hyp: " + str(1 / (abs(_tempT2_hyp_x[(nB - 1) // 2] + _tempT2_hyp_y[(nB - 1) // 2] + _tempT2_hyp_z[(nB - 1) // 2]) * np.pi)) + "\n" \
                       + "Transition Strength: " \
                       + str(transitionStrength_x[(nB - 1) // 2, p, q]) + ", " + str(transitionStrength_y[(nB - 1) // 2, p, q]) + ", " \
                       + str(transitionStrength_z[(nB - 1) // 2, p, q]) + "\n"
                print(text)
                with open("ene.txt", "a", encoding="utf_8") as f:
                    f.write(text)

    energy_pq = np.array(energy_pq)
    energy_gradient_pq_x = np.array(energy_gradient_pq_x)
    energy_gradient_pq_y = np.array(energy_gradient_pq_y)
    energy_gradient_pq_z = np.array(energy_gradient_pq_z)
    energy_curvature_pq_xx = np.array(energy_curvature_pq_xx)
    energy_curvature_pq_xy = np.array(energy_curvature_pq_xy)
    energy_curvature_pq_xz = np.array(energy_curvature_pq_xz)
    energy_curvature_pq_yx = np.array(energy_curvature_pq_yx)
    energy_curvature_pq_yy = np.array(energy_curvature_pq_yy)
    energy_curvature_pq_yz = np.array(energy_curvature_pq_yz)
    energy_curvature_pq_zx = np.array(energy_curvature_pq_zx)
    energy_curvature_pq_zy = np.array(energy_curvature_pq_zy)
    energy_curvature_pq_zz = np.array(energy_curvature_pq_zz)
    transitionStrength_pq_x = np.array(transitionStrength_pq_x)
    transitionStrength_pq_y = np.array(transitionStrength_pq_y)
    transitionStrength_pq_z = np.array(transitionStrength_pq_z)
    t2_hyp = np.array(t2_hyp)

    energy_curvature_pq_max = []
    for p in range(0, 120):
        energy_curvature_pq_max.append(np.max([
            np.abs(energy_curvature_pq_xx[p, (nB - 1) // 2]),
            np.abs(energy_curvature_pq_xy[p, (nB - 1) // 2]),
            np.abs(energy_curvature_pq_xz[p, (nB - 1) // 2]),
            np.abs(energy_curvature_pq_yx[p, (nB - 1) // 2]),
            np.abs(energy_curvature_pq_yy[p, (nB - 1) // 2]),
            np.abs(energy_curvature_pq_yz[p, (nB - 1) // 2]),
            np.abs(energy_curvature_pq_zx[p, (nB - 1) // 2]),
            np.abs(energy_curvature_pq_zy[p, (nB - 1) // 2]),
            np.abs(energy_curvature_pq_zz[p, (nB - 1) // 2])
        ]))
    energy_curvature_pq_max = np.array(energy_curvature_pq_max)

    # 図示
    fig = plt.figure()
    fig.patch.set_alpha(0)
    # 1つ目の図
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.patch.set_alpha(0)
    # ax1.set_xlabel(r'$\rm{Magnetic \, Field \, (mT)}$')
    # ax1.set_ylabel(r'$\rm{Frequency (GHz)}$')
    ax1.set_xlabel(r'$\rm{Transition \, Strength \, (MHz/mT)}$')
    ax1.set_ylabel(r'$\rm{T^{hyp}_2 \, (s)}$')
    ax1.set_xscale('linear')
    # ax1.set_yscale('linear')
    ax1.set_yscale('log')
    # プロット処理
    # ax1.plot(Bx * 1e+03, energy * 1e-09)
    # ax1.scatter(energy_pq[:, (nB - 1) // 2] * 1e-09, energy_curvature_pq_max * 1e-15)
    # ax1.scatter(energy_pq[:, (nB - 1) // 2] * 1e-09, transitionStrength_pq_z[:, (nB - 1) // 2] * 1e-12)
    sc = plt.scatter(transitionStrength_pq_z[:, (nB - 1) // 2] * 1e-09, t2_hyp[:, (nB - 1) // 2], vmin=0, vmax=6, c=energy_pq[:, (nB - 1) // 2] * 1e-09,
                     cmap=cm.seismic)
    plt.colorbar(sc)
    plt.show()
    fig.savefig('test.png', bbox_inches="tight", pad_inches=0.05, dpi=300)

    print("finished.")
