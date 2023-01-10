import numpy as np
import RareEarthIon_DopedInCrystal
from Quantum import Quantum
from PhysicalConstant_DB import PhysicalConstant_DB


class Er167_Y2SiO5:

    @staticmethod
    def g(site: int) -> np.array:
        """
        siteを与えると電子のgテンソル（行列）gを返却します   \n
        :param site: Y2SiO5結晶におけるYの置換位置。1 or 2。
        :return: np.array
        """
        # Legacy g1
        g1 = np.array([[2.90, -2.95, -3.56],
                       [-2.95, 8.90, 5.57],
                       [-3.56, 5.57, 5.12]])

        # New g1(Rakonjac)
        # g1 = np.array([[2.85, -2.98, -3.63],
        #                [-2.98, 9.00, 5.51],
        #                [-3.63, 5.51, 5.19]])

        # g1 for Optical
        # g1 = np.array([[2.38, -2.66, -3.63],
        #                [-2.66, 4.83, 5.22],
        #                [-3.63, 5.22, 7.68]])

        # Legacy g2
        g2 = np.array([[14.37, -1.77, 2.40],
                       [-1.77, 1.93, -0.43],
                       [2.40, -0.43, 1.44]])
        return g1 if site == 1 else g2

    @staticmethod
    def A(site: int) -> np.array:
        """
        siteを与えると超微細結合テンソル（行列）Aを返却します   \n
        :param site: Y2SiO5結晶におけるYの置換位置。1 or 2。
        :return: np.array
        """
        # Legacy A1
        A1 = np.array([[274.3, -202.5, -350.8],
                       [-202.5, 827.5, 635.2],
                       [-350.8, 635.2, 706.1]]) * 1e+06

        # New A1(Rakonjac)
        # A1 = np.array([[304.8, -252.8, -307.6],
        #                [-252.8, 778.0, 710.2],
        #                [-307.6, 710.2, 616.2]]) * 1e+06

        # A1 for Optical
        # A1 = np.array([[307.9, -327.5, -464.8],
        #                [-327.5, 607.8, 676.7],
        #                [-464.8, 676.7, 980.5]]) * 1e+06

        # Legacy A2
        A2 = np.array([[-1565.3, 219.0, -124.4],
                       [219.0, - 15.3, -  0.7],
                       [- 124.4, -  0.7, 127.8]]) * 1e+06
        return A1 if site == 1 else A2

    @staticmethod
    def Q(site: int) -> np.array:
        """
        siteを与えると核四重極テンソル（行列）Qを返却します   \n
        :param site: Y2SiO5結晶におけるYの置換位置。1 or 2。
        :return: np.array
        """
        # Legacy Q1
        Q1 = np.array([[10.4, - 9.1, -10.0],
                       [- 9.1, - 6.0, -14.3],
                       [-10.0, -14.3, - 4.4]]) * 1e+06

        # New Q1(Rakonjac)
        # Q1 = np.array([[10.1, -10.1, -14.0],
        #                [-10.1, -6.3, -15.6],
        #                [-14.0, -15.6, -3.8]]) * 1e+06

        # Q1 for Optical
        # Q1 = np.array([[56.0, 1.66, 5.80],
        #                [1.66, -53.2, -10.3],
        #                [5.80, -10.3, 46.4]]) * 1e+06

        # Legacy Q2
        Q2 = np.array([[-10.5, -22.8, - 3.1],
                       [-22.8, -19.5, -17.7],
                       [- 3.1, -17.7, 30.0]]) * 1e+06
        return Q1 if site == 1 else Q2

    @staticmethod
    def gn() -> float:
        """
        核のg因子   \n
        :return: float
        """
        return -0.1618

    @staticmethod
    def S() -> {np.ndarray: (2, 2)}:
        """
        電子のスピンハミルトニアンS（パウリ行列）x3   \n
        ※タプル型、３個   \n
        :return: np.array
        """
        return Quantum.spin_matrix(1 / 2)

    @staticmethod
    def I() -> {np.ndarray: (8, 8, 3)}:
        """
        核のスピンハミルトニアンIx3   \n
        ※タプル型、３個   \n
        :return: np.array
        """
        return Quantum.spin_matrix(7 / 2)

    @staticmethod
    def Perturbation_Zeta(direction: str) -> {np.ndarray: (16, 16)}:
        """
        摂動の中央項 ζij。     \n
        例えば、i=xのとき：     \n
        ζx = βe・gxx・Sx + βe・gxy・Sy + βe・gxz・Sz - βn・gn・Ix   \n
        :param direction: 摂動方向（i=x,y,z）。"x" or "y" or "z"。
        :return: np.array
        """
        beta_e = PhysicalConstant_DB.beta_e
        beta_n = PhysicalConstant_DB.beta_n
        gn = Er167_Y2SiO5.gn()
        Sx = np.kron(np.eye(8), Er167_Y2SiO5.S()[0])
        Sy = np.kron(np.eye(8), Er167_Y2SiO5.S()[1])
        Sz = np.kron(np.eye(8), Er167_Y2SiO5.S()[2])
        gxx = Er167_Y2SiO5.g(1)[0, 0]
        gxy = Er167_Y2SiO5.g(1)[0, 1]
        gxz = Er167_Y2SiO5.g(1)[0, 2]
        gyx = Er167_Y2SiO5.g(1)[1, 0]
        gyy = Er167_Y2SiO5.g(1)[1, 1]
        gyz = Er167_Y2SiO5.g(1)[1, 2]
        gzx = Er167_Y2SiO5.g(1)[2, 0]
        gzy = Er167_Y2SiO5.g(1)[2, 1]
        gzz = Er167_Y2SiO5.g(1)[2, 2]
        Ix = np.kron(Er167_Y2SiO5.I()[0], np.eye(2))
        Iy = np.kron(Er167_Y2SiO5.I()[1], np.eye(2))
        Iz = np.kron(Er167_Y2SiO5.I()[2], np.eye(2))

        zeta_x = beta_e * (gxx * Sx + gxy * Sy + gxz * Sz) + beta_n * gn * Ix
        zeta_y = beta_e * (gyx * Sx + gyy * Sy + gyz * Sz) + beta_n * gn * Iy
        zeta_z = beta_e * (gzx * Sx + gzy * Sy + gzz * Sz) + beta_n * gn * Iz

        if direction == "x":
            return zeta_x
        elif direction == "y":
            return zeta_y
        elif direction == "z":
            return zeta_z
        else:
            raise Exception(
                'Argument Exception: Argument "direction" is invalid. Use "x", "y", "z".\nSee docstring for detail.')
