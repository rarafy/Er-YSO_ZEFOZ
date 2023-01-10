path = "test.txt"

if __name__ == '__main__':
    print(path)

    with open(path) as f:
        s: {list: 1003688} = f.readlines()

        # 最初列と最終列
        print(s[0])
        print(s[len(s) - 1])

        for i in range(0, len(s) - 1, 4):
            # データ例：
            # 9-10:
            # V: 5.53131103515625e-05, 0.00012969970703125, 9.775161743164062e-05
            # B: 0.5276705604947777, -0.0681123562629626, 0.45210884371543936
            # Starts From B: 0.1, 0.1, -0.03

            # 加工後：
            # _level1 = 9
            # _level2 = 10
            # Bx = 0.5276705604947777
            # By = -0.0681123562629626
            # Bz = 0.45210884371543936

            # テスト用
            # print(s[i])
            # print(s[i + 1])
            # print(s[i + 2])
            # print(s[i + 3])

            _level1, _level2 = map(int, s[i].replace(":\n", "").split("-"))
            _Bx, _By, _Bz = map(float, s[i + 2].replace("\n", "").replace("B:", "").replace(" ", "").split(","))
