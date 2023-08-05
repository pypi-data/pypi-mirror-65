# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class ShortTest():
    # 合成抵抗の計算
    def calc_resistance(self, resistance, series_num, parallel_num):
        # 直列分の計算
        resistance_series = np.repeat(resistance * series_num, parallel_num)

        # 並列分の計算
        return 1. / np.sum(1. / resistance_series)

    ##
    # @fn make_table
    # @brief Create an impedance pattern table(インピーダンスのパターン表を作成します)
    # @param power_module_num Maximum number of power supplies[電源モジュールの最大個数]
    # @param power_module_resistance Internal resistance per power supply[電源モジュールの内部抵抗]
    # @param test_resistance Test resistance[試験体の抵抗mΩ]
    # @param external_resistances External short-circuit resistance[外部短絡抵抗のパターンmΩ]
    # @param line_resistance Wiring resistance[配線抵抗mΩ]
    # @param power_module_max_voltage Max voltage)[電源のモジュール最大電圧V]
    # @param power_module_min_voltage Min voltage[電源のモジュール最小電圧V]
    # @retval df Dataframe of impidance table constant[Dataframe:インピーダンスのパターン表]
    def make_table(self,
                   power_module_num,
                   power_module_resistance,
                   test_resistance,
                   external_resistances,
                   line_resistance,
                   power_module_max_voltage,
                   power_module_min_voltage):
        # 電源の内部抵抗を計算（直並列のパターンごと）
        power_module_resistances = {}
        # 直並列数のパターンを列に追加
        series_nums = []
        parallel_nums = []
        self.external_resistances = external_resistances

        for j in range(power_module_num):
            list_r = []
            for i in range(power_module_num):
                if((j+1) * (i+1) < power_module_num + 1):
                    # 合成抵抗の計算
                    power_module_resistances[str(j+1)+"s" + str(i+1) +
                                             "p"] = self.calc_resistance(power_module_resistance, j+1, i+1)
                    # 直列数を記録
                    series_nums.append(j + 1)
                    # 並列数を記録
                    parallel_nums.append(i + 1)

        # データフレームを作成し、電源の内部抵抗を追加
        df = pd.DataFrame(
            pd.Series(data=power_module_resistances, name="power_module_resistance"))
        df.index.name = "Pattern"

        # データフレームに直並列数を追加
        df["Series_num"] = series_nums
        df["Parallel_num"] = parallel_nums

        # 直列数に応じて電源の総電圧（最大値、最小値）を計算して追加
        df["max_voltage"] = df["Series_num"] * power_module_max_voltage
        df["min_voltage"] = df["Series_num"] * power_module_min_voltage

        # 外部抵抗値に応じて回路全体の抵抗、電流（最大値、最小値）を計算
        for external_resistance in external_resistances:
            # 回路全体の抵抗を計算（電源の内部抵抗 + 外部短絡装置の抵抗 + 配線抵抗）を計算し、列に追加
            df["external_resistance" + str(external_resistance)] = df["power_module_resistance"] + \
                external_resistance + line_resistance + test_resistance

            # 電流の最大値を計算（電源の組合せパターン毎）
            df["max_current_ext" + str(external_resistance)] = df["max_voltage"] / \
                df["external_resistance" + str(external_resistance)] * 1000

            # 電流の最小値を計算（電源の組合せパターン毎）
            df["min_current_ext" + str(external_resistance)] = df["min_voltage"] / \
                df["external_resistance" + str(external_resistance)] * 1000

        self.df = df

        return df

    ##
    # @fn search_pattern
    # @brief Search for a combination of power supply and external short-circuit resistance that satisfies the target current (output the result as a mask)目標電流を満たす電源・外部短絡抵抗の組合せを検索（結果をマスクで出力）
    # @param target_current Current of target[目標電流]
    # @param target_voltage Voltage of target[目標電圧]
    # @param round_num round number(default:0)[小数点の桁数]
    # @retval df_result List of equipment configuration that satisfies the test conditions[試験条件を満たす装置構成一覧（ 電源を○直○並で接続し、外部短絡抵抗を○mΩにするか）]
    # @retval ss_min_current_error When the output current of the power supply is matched with the test conditions, the device configuration when the output current of the power supply is closest to the target current.[電源の出力電圧を試験条件と一致させた場合、電源の出力電流が目標電流に最も近いときの装置構成（ 電源を○直○並で接続し、外部短絡抵抗を○mΩにするか）]
    # @retval ss_min_voltage_error When the output voltage of the power supply is matched with the test conditions, the device configuration when the output current of the power supply is closest to the target current.（ 電源を○直○並で接続し、外部短絡抵抗を○mΩにするか）]
    def search_pattern(self, target_current, target_voltage, round_num=0):
        df_min_current = self.df.loc[:, 'min_current_ext' +
                                     str(self.external_resistances[0]):'min_current_ext' + str(self.external_resistances[-1])]
        df_max_current = self.df.loc[:, 'max_current_ext' +
                                     str(self.external_resistances[0]):'max_current_ext' + str(self.external_resistances[-1])]
        df_min_current_mask = (df_min_current <= target_current)
        df_max_current_mask = (target_current <= df_max_current)

        # 目標電圧を満たす電源・外部短絡抵抗の組合せを検索（結果をマスクで出力）
        df_min_voltage = self.df.loc[:, 'min_voltage']
        df_max_voltage = self.df.loc[:, 'max_voltage']
        df_min_voltage_mask = (df_min_voltage <= target_voltage)
        df_max_voltage_mask = (target_voltage <= df_max_voltage)

        # 目標値用のデータフレーム作成
        df_target = df_min_current.copy()

        # 目標電圧・電流を満たす電源と外部短絡抵抗を検索（結果をマスクで出力）
        for external_resistance in self.external_resistances:
            df_target['ext' + str(external_resistance)] = df_min_current_mask['min_current_ext' + str(
                external_resistance)] & df_max_current_mask['max_current_ext' + str(external_resistance)] & df_min_voltage_mask & df_max_voltage_mask

        # 外部短絡抵抗値
        df_target = df_target.loc[:, "ext" +
                                  str(self.external_resistances[0]):"ext" + str(self.external_resistances[-1])]
        patterns = df_target.index.tolist()

        # データフレームを転置
        df_target = df_target.transpose()

        result_ext_dict = {}

        # 目標電圧・目標電流を電源・両方満たす外部短絡抵抗の組合せを取得
        for pattern in patterns:
            result = df_target[df_target[pattern] == True].index.tolist()
            if result:
                result_ext_dict[pattern] = df_target[df_target[pattern]
                                                     == True].index.tolist()

        df_result = pd.DataFrame(columns=[
                                 'Pattern',
                                 'Min current[A]',
                                 'Max current[A]',
                                 'Min voltage[V]',
                                 'Max voltage[V]',
                                 'Current[A](' + str(target_voltage) + 'V)',
                                 'Voltage[V](' + str(target_current) + 'A)'])

        self.target_voltage = target_voltage
        self.target_current = target_current

        for key, value in result_ext_dict.items():
            for i in range(len(value)):

                # 試験条件を満たす電流、電圧の最小値、最大値
                min_current = self.df.loc[key, "min_current_" + value[i]]
                max_current = self.df.loc[key, "max_current_" + value[i]]
                max_voltage = self.df.loc[key, "max_voltage"]
                min_voltage = self.df.loc[key, "min_voltage"]
                # 電源電圧を目標電圧に固定したときの電流値を計算
                current = max_current - (max_current - min_current) * \
                    ((max_voltage - target_voltage) / (max_voltage - min_voltage))

                # 電源電流を目標電流に固定したときの電圧を計算
                voltage = max_voltage - (max_voltage - min_voltage) * \
                    ((max_current - target_current) / (max_current - min_current))

                # データフレームに追加
                df_result.loc[key + "-" +
                              str(value[i])] = [key + "-" + str(value[i]), min_current, max_current, max_voltage, min_voltage, current, voltage]

        # 目標電流値と理論電流値との絶対誤差を計算（電源電圧を目標値に固定した場合）
        df_result["Current error"] = (
            df_result['Current[A](' + str(target_voltage) + 'V)'] - target_current).abs()

        # 目標電圧値と電源電圧値との絶対誤差を計算（電源電流を目標値に固定した場合）
        df_result["Voltage error"] = (
            df_result['Voltage[V](' + str(target_current) + 'A)'] - target_voltage).abs()

        # データフレームが空の場合（試験条件を満たす構成が無い）
        if df_result.empty:
            print("試験条件を満たす構成は存在しません。")
            return - 1

       # 目標電流値と理論電流値との絶対誤差が最小になるときの装置構成を取得
        self.ss_min_current_error = df_result.loc[df_result['Current error'].idxmin(
        )]
        self.ss_min_voltage_error = df_result.loc[df_result['Voltage error'].idxmin(
        )]
        df_error_min_result = pd.concat(
            [self.ss_min_current_error, self.ss_min_voltage_error], axis=1)
        df_error_min_result.columns = [
            'Min current error', 'Min voltage error']

        self.df_result = df_result
        if round_num != 0:
            self.df_result = df_result.round(round_num)
            self.df_error_min_result = df_error_min_result.round(round_num)

        print('\n----------------------------------------')
        print('●Error between the target current or voltage and the theoretical current is minimum')
        print(self.df_error_min_result)

        # 試験条件を満たす装置構成を一覧表示
        print('----------------------------------------')
        print('●List of pattern match test conditions')
        print(self.df_result)

    def save_csv(self, path):
        # 結果をCSVファイルに出力
        self.df_result.to_csv(path + '/result.csv')
        self.ss_min_current_error.to_csv(
            path + '/result_min_current_error.csv', header=False)
        self.ss_min_voltage_error.to_csv(
            path + '/result_min_voltage_error.csv', header=False)
        self.df.to_csv(path + '/table.csv')

        return 0

    def save_excel(self, path):
        # 結果をCSVファイルに出力
        with pd.ExcelWriter(path + '/result.xlsx') as writer:
            self.df_result.to_excel(writer, sheet_name='result')
            self.ss_min_current_error.to_excel(
                writer, header=False, sheet_name='min_current_error')
            self.ss_min_voltage_error.to_excel(
                writer, header=False, sheet_name='min_voltage_error')
            self.df.to_excel(writer, sheet_name='table')

    def save_graph(self,
                   save_file_path,
                   fig_size_x,
                   fig_size_y,
                   lim_font_size,
                   loc="upper left",
                   x_lim=None,
                   y_lim=None,
                   bbox_to_anchor=(-1, 0),
                   borderaxespad=0):
        # グラフ設定
        plt.figure(figsize=(fig_size_x, fig_size_y))
        ax = plt.axes()
        plt.rcParams['font.family'] = 'Times New Roman'  # 全体のフォント
        plt.rcParams['font.size'] = lim_font_size  # 全体のフォント
        plt.rcParams['axes.linewidth'] = 1.0    # 軸の太さ

        max_voltages = self.df["max_voltage"]
        min_voltages = self.df["min_voltage"]
        
        # 電流の最大値（外部短絡抵抗が最小）
        max_currents = self.df["max_current_ext" +
                               str(self.external_resistances[0])]

        # 電流の最小値（外部短絡抵抗が最小）
        min_voltage_max_currents = self.df["min_current_ext" +
                               str(self.external_resistances[0])]

        print("min_voltage_max_currents:", min_voltage_max_currents)
        print("-----------")
        max_voltages_min_currents = self.df["max_current_ext" +
                               str(self.external_resistances[-1])]

        print("max_voltages_min_currents:", max_voltages_min_currents)
        print("-----------")
        min_voltages_min_currents = self.df["min_current_ext" +
                               str(self.external_resistances[-1])]
        print("min_voltages_min_ccurrents:", min_voltages_min_currents)
        print("-----------")
        # patterns = 1s1p, 1s2p ....
        patterns = self.df.index

        plt.scatter(self.target_current,
                    self.target_voltage, s=300, marker="o", color="r")
 
        # patterns = 1s1p, 1s2p ....
        for i in range(len(patterns)):
            x = [min_voltages_min_currents[i], min_voltage_max_currents[i], max_currents[i],
                 max_voltages_min_currents[i], min_voltages_min_currents[i]]
            y = [min_voltages[i], min_voltages[i], max_voltages[i],
                 max_voltages[i], min_voltages[i]]
            plt.plot(x, y, lw=2, alpha=0.7, ms=2, label=patterns[i])

        plt.legend(loc=loc,
                   bbox_to_anchor=bbox_to_anchor,
                   borderaxespad=borderaxespad)           # 凡例の表示（2：位置は第二象限）
        plt.title('I-V Area', fontsize=lim_font_size)   # グラフタイトル
        plt.xlabel('Output Current[A]',
                   fontsize=lim_font_size)            # x軸ラベル
        plt.ylabel('Output Voltage[V]',
                   fontsize=lim_font_size)            # y軸ラベル

        if x_lim != None:
            (x_min, x_max, x_dim) = x_lim
            (y_min, y_max, y_dim) = y_lim
            # x軸の目盛りを引く場所を指定（無ければ自動で決まる）
            plt.xticks(np.arange(x_min, x_max, x_dim))
            # y軸の目盛りを引く場所を指定（無ければ自動で決まる）
            plt.yticks(np.arange(y_min, y_max, y_dim))

        plt.tick_params(labelsize=lim_font_size)
        plt.grid()                              # グリッドの表示
        # plt.show()
        plt.savefig(save_file_path)
        plt.close() # バッファ解放

        return 0


def main():
    # 試験条件
    TARGET_CURRENT = 2500  # 目標電流値[A]
    TARGET_VOLTAGE = 40  # 目標電圧値[V]
    TEST_RESISTANCE = 0  # 試験体の抵抗[mΩ]
    OTHER_RESISTANCE = 0  # その他の抵抗値（端子台など）
    LINE_RESISTANCE = 5  # 配線抵抗[mΩ]
    POWER_MODULE_RESISTANCE = 3  # 電源1つ(1直1並)あたりの内部抵抗[mΩ]
    POWER_MODULE_NUM = 4  # 電源の最大個数
    POWER_MODULE_MIN_VOLTAGE = 10.4  # 電源1つ(1直1並)あたりの最小電圧[V]
    POWER_MODULE_MAX_VOLTAGE = 21.6  # 電源1つ(1直1並)あたりの最大電圧[V]
    # 外部短絡装置の可変抵抗組み合わせパターン(昇順に並べる)
    EXTERNAL_RESISTANCES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # 計算結果の保存先パス
    PATH = "C:/github/libs/python/calc2/examples/short_test/"
    ROUND_NUM = 2  # 小数点の桁数
    st = ShortTest()

    # 一覧表を作成・保存
    st.make_table(power_module_num=POWER_MODULE_NUM,
                  power_module_resistance=POWER_MODULE_RESISTANCE,
                  test_resistance=TEST_RESISTANCE + OTHER_RESISTANCE,
                  external_resistances=EXTERNAL_RESISTANCES,
                  line_resistance=LINE_RESISTANCE,
                  power_module_max_voltage=POWER_MODULE_MAX_VOLTAGE,
                  power_module_min_voltage=POWER_MODULE_MIN_VOLTAGE)

    # 試験条件を満たす電源・外部短絡抵抗の組合せを探索
    search_result = st.search_pattern(
        TARGET_CURRENT,  TARGET_VOLTAGE, round_num=ROUND_NUM)
    if search_result == -1:
        print("試験条件を満たす構成は存在しません。")

    else:
        print("試験条件を満たす構成は存在したので記録します")
        # 結果保存
        st.save_excel(PATH)

    # I-V領域グラフをプロット
    st.save_graph(save_file_path = PATH + "graph.png",
                  #x_lim=(0, 20000, 1000),
                  #y_lim=(0, 1000, 100),
                  fig_size_x=30,
                  fig_size_y=15,
                  lim_font_size=30,
                  loc=1,
                  bbox_to_anchor=(1.05, 1),
                  borderaxespad=0)


if __name__ == "__main__":
    main()

"""
----------------------------------------
●Error between the target current or voltage and the theoretical current is minimum     
                  Min current error Min voltage error
Pattern                   2s1p-ext5         2s1p-ext5
Min current[A]                 1300              1300
Max current[A]                 2700              2700
Min voltage[V]                 43.2              43.2
Max voltage[V]                 20.8              20.8
Current[A](40V)                2500              2500
Voltage[V](2500A)                40                40
Current error                     0                 0
Voltage error                     0                 0
----------------------------------------
●List of pattern match test conditions
               Pattern  Min current[A]  ...  Current error  Voltage error
2s1p-ext1    2s1p-ext1         1733.33  ...         833.33           10.0
2s1p-ext2    2s1p-ext2         1600.00  ...         576.92            7.5
2s1p-ext3    2s1p-ext3         1485.71  ...         357.14            5.0
2s1p-ext4    2s1p-ext4         1386.67  ...         166.67            2.5
2s1p-ext5    2s1p-ext5         1300.00  ...           0.00            0.0
2s1p-ext6    2s1p-ext6         1223.53  ...         147.06            2.5
2s2p-ext1    2s2p-ext1         2311.11  ...        1944.44           17.5
2s2p-ext2    2s2p-ext2         2080.00  ...        1500.00           15.0
2s2p-ext3    2s2p-ext3         1890.91  ...        1136.36           12.5
2s2p-ext4    2s2p-ext4         1733.33  ...         833.33           10.0
2s2p-ext5    2s2p-ext5         1600.00  ...         576.92            7.5
2s2p-ext6    2s2p-ext6         1485.71  ...         357.14            5.0
2s2p-ext7    2s2p-ext7         1386.67  ...         166.67            2.5
2s2p-ext8    2s2p-ext8         1300.00  ...           0.00            0.0
2s2p-ext9    2s2p-ext9         1223.53  ...         147.06            2.5
3s1p-ext1    3s1p-ext1         2080.00  ...         166.67            2.5
3s1p-ext2    3s1p-ext2         1950.00  ...           0.00            0.0
3s1p-ext3    3s1p-ext3         1835.29  ...         147.06            2.5
3s1p-ext4    3s1p-ext4         1733.33  ...         277.78            5.0
3s1p-ext5    3s1p-ext5         1642.11  ...         394.74            7.5
3s1p-ext6    3s1p-ext6         1560.00  ...         500.00           10.0
3s1p-ext7    3s1p-ext7         1485.71  ...         595.24           12.5
3s1p-ext8    3s1p-ext8         1418.18  ...         681.82           15.0
3s1p-ext9    3s1p-ext9         1356.52  ...         760.87           17.5
3s1p-ext10  3s1p-ext10         1300.00  ...         833.33           20.0

[25 rows x 9 columns]
試験条件を満たす構成は存在したので記録します
min_voltage_max_currents: Pattern
1s1p    1155.555556
1s2p    1386.666667
1s3p    1485.714286
1s4p    1540.740741
2s1p    1733.333333
2s2p    2311.111111
3s1p    2080.000000
4s1p    2311.111111
Name: min_current_ext1, dtype: float64
-----------
max_voltages_min_currents: Pattern
1s1p    1200.000000
1s2p    1309.090909
1s3p    1350.000000
1s4p    1371.428571
2s1p    2057.142857
2s2p    2400.000000
3s1p    2700.000000
4s1p    3200.000000
Name: max_current_ext10, dtype: float64
-----------
min_voltages_min_ccurrents: Pattern
1s1p     577.777778
1s2p     630.303030
1s3p     650.000000
1s4p     660.317460
2s1p     990.476190
2s2p    1155.555556
3s1p    1300.000000
4s1p    1540.740741
Name: min_current_ext10, dtype: float64
-----------
"""