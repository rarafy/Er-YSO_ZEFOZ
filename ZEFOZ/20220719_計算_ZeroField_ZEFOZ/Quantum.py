import numpy as np


class Quantum:
    @staticmethod
    def spin_matrix(nuclearSpin: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        核スピンIの大きさを与えるとスピン行列（電子の場合はパウリ行列）を返却します

        使用例 :
        a = Quantum.spin_matrix(1 / 2)
        Jx = a[:, :, 0]
        Jy = a[:, :, 1]
        Jz = a[:, :, 2]

        :param nuclearSpin: 核スピンI, 例：電子→1/2, Er原子核→7/2
        :return: np.ndarray:(2I+1, 2I+1, 3)
        """
        dim: int = int(nuclearSpin * 2 + 1)
        I = nuclearSpin
        # I ～ -I 【終端含む】の範囲で公差-1の行列を生成
        mz = np.linspace(I, -I, int(2 * I) + 1, endpoint=True)
        LdrUp = np.sqrt((I - mz) * (I + mz + 1)) * np.eye(dim, k=1)
        LdrDw = np.sqrt((I + mz) * (I - mz + 1)) * np.eye(dim, k=-1)
        Jx = (LdrUp + LdrDw) / 2.
        Jy = (LdrUp - LdrDw) / 2.j
        Jz = mz * np.eye(dim)
        return Jx, Jy, Jz


if __name__ == '__main__':
    print(Quantum.spin_matrix(7 / 2))
    Jx, Jy, Jz = Quantum.spin_matrix(7 / 2)
