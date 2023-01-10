import numpy as np
import matplotlib.pyplot as plt
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

if __name__ == '__main__':
    dim = 3

    B: {np.ndarray: (3,)} = np.transpose([0.02, 0.0, 0.0])
    zeta_x = Er167_Y2SiO5.Perturbation_Zeta("x")
    zeta_y = Er167_Y2SiO5.Perturbation_Zeta("y")
    zeta_z = Er167_Y2SiO5.Perturbation_Zeta("z")

    for i in range(0, 20):
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

        # エネルギー計算（摂動行列、振動子強度、Gradient、Curvature）
        val, vec = eigh(RareEarthIon_DopedInCrystal.Hamiltonian_odd(PhysicalConstant_DB.beta_e,
                                                                    PhysicalConstant_DB.beta_n,
                                                                    Er167_Y2SiO5.gn(),
                                                                    B,
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

        # 1次元の場合
        if dim == 1:
            C = np.array([[energy_curvature_xx[0, 7], 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]])
            V = np.transpose([energy_gradient_x[0, 7], 0, 0])
            C = np.real(C)
            B = B - np.array([V[0] / C[0, 0], 0, 0])
        # 2次元の場合
        elif dim == 2:
            C = np.array([[energy_curvature_xx[0, 7], energy_curvature_xy[0, 7]],
                          [energy_curvature_yx[0, 7], energy_curvature_yy[0, 7]]])
            V = np.transpose([energy_gradient_x[0, 7], energy_gradient_y[0, 7]])
            C = np.real(C)
            B = B - 0.5 * np.append(np.dot(np.linalg.inv(C), V), 0)
        # 3次元の場合
        elif dim == 3:
            C = np.array([[energy_curvature_xx[0, 7], energy_curvature_xy[0, 7], energy_curvature_xz[0, 7]],
                          [energy_curvature_yx[0, 7], energy_curvature_yy[0, 7], energy_curvature_yz[0, 7]],
                          [energy_curvature_zx[0, 7], energy_curvature_zy[0, 7], energy_curvature_zz[0, 7]]])
            V = np.transpose([energy_gradient_x[0, 7], energy_gradient_y[0, 7], energy_gradient_z[0, 7]])
            C = np.real(C)
            B = B - 0.5 * np.dot(np.linalg.inv(C), V)
        else:
            V = 0
        V = np.abs(V)
        # print(str(C[0]) + ", " + str(C[1]) + ", ")  # + str(C[2]))
        print(str(V[0]) + ", " + str(V[1]) + ", " + str(V[2]))
        # print(str(B[0]) + ", " + str(B[1]) + ", " + str(B[2]))
