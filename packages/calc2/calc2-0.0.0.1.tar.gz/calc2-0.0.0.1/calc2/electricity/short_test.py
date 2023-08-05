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
    TARGET_CURRENT = 5000  # 目標電流値[A]
    TARGET_VOLTAGE = 600  # 目標電圧値[V]
    TEST_RESISTANCE = 0  # 試験体の抵抗[mΩ]
    OTHER_RESISTANCE = 0  # その他の抵抗値（端子台など）
    LINE_RESISTANCE = 7  # 配線抵抗[mΩ]
    POWER_MODULE_RESISTANCE = 22  # 電源1つ(1直1並)あたりの内部抵抗[mΩ]
    POWER_MODULE_NUM = 8  # 電源の最大個数
    POWER_MODULE_MIN_VOLTAGE = 70.4  # 電源1つ(1直1並)あたりの最小電圧[V]
    POWER_MODULE_MAX_VOLTAGE = 121.6  # 電源1つ(1直1並)あたりの最大電圧[V]
    # 外部短絡装置の可変抵抗組み合わせパターン(昇順に並べる)
    EXTERNAL_RESISTANCES = [1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23, 29, 30, 31, 32, 33, 34, 35, 36, 45, 46, 47, 48, 49, 50, 51,
                            52, 53, 54, 55, 56, 57, 67, 68, 69, 70, 71, 72, 73, 79, 80, 81, 82, 83, 84, 85, 86, 95, 96, 97, 98, 99, 100, 101, 102]
    # 計算結果の保存先パス
    PATH = "C:/github/libs/python/electrical-python/tests/short_test/"
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
Pattern                   5s1p-ext7         5s1p-ext7
Min current[A]              2933.33           2933.33
Max current[A]              5066.67           5066.67
Min voltage[V]                  608               608
Max voltage[V]                  352               352
Current[A](600V)               5000              5000
Voltage[V](5000A)               600               600
Current error           9.09495e-13       9.09495e-13
Voltage error           1.13687e-13       1.13687e-13
----------------------------------------
●List of pattern match test conditions
             Pattern  Min current[A]  ...  Current error  Voltage error
5s1p-ext1  5s1p-ext1         3087.72  ...         263.16           30.0
5s1p-ext2  5s1p-ext2         3060.87  ...         217.39           25.0
5s1p-ext3  5s1p-ext3         3034.48  ...         172.41           20.0
5s1p-ext4  5s1p-ext4         3008.55  ...         128.21           15.0
5s1p-ext5  5s1p-ext5         2983.05  ...          84.75           10.0
5s1p-ext6  5s1p-ext6         2957.98  ...          42.02            5.0
5s1p-ext7  5s1p-ext7         2933.33  ...           0.00            0.0
6s1p-ext1  6s1p-ext1         3105.88  ...         588.24           80.0
6s1p-ext2  6s1p-ext2         3083.21  ...         620.44           85.0
6s1p-ext3  6s1p-ext3         3060.87  ...         652.17           90.0
6s1p-ext4  6s1p-ext4         3038.85  ...         683.45           95.0
6s1p-ext5  6s1p-ext5         3017.14  ...         714.29          100.0
6s1p-ext6  6s1p-ext6         2995.74  ...         744.68          105.0
6s1p-ext7  6s1p-ext7         2974.65  ...         774.65          110.0
7s1p-ext1  7s1p-ext1         3118.99  ...        1202.53          190.0
7s1p-ext2  7s1p-ext2         3099.37  ...        1226.42          195.0
7s1p-ext3  7s1p-ext3         3080.00  ...        1250.00          200.0
7s1p-ext4  7s1p-ext4         3060.87  ...        1273.29          205.0
7s1p-ext5  7s1p-ext5         3041.98  ...        1296.30          210.0
7s1p-ext6  7s1p-ext6         3023.31  ...        1319.02          215.0
7s1p-ext7  7s1p-ext7         3004.88  ...        1341.46          220.0
8s1p-ext1  8s1p-ext1         3128.89  ...        1666.67          300.0
8s1p-ext2  8s1p-ext2         3111.60  ...        1685.08          305.0
8s1p-ext3  8s1p-ext3         3094.51  ...        1703.30          310.0
8s1p-ext4  8s1p-ext4         3077.60  ...        1721.31          315.0
8s1p-ext5  8s1p-ext5         3060.87  ...        1739.13          320.0
8s1p-ext6  8s1p-ext6         3044.32  ...        1756.76          325.0
8s1p-ext7  8s1p-ext7         3027.96  ...        1774.19          330.0

[28 rows x 9 columns]
"""
