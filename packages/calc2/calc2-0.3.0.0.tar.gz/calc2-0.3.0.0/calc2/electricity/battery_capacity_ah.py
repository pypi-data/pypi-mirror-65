# -*- coding: uTf-8 -*-
"""
@brief Analyzes battery capacity measurement data(in Ah).電池の容量測定データ（Ah単位）を解析します。
"""
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

class BatteryCapacityAh():
    ##
    # @fn calc
    # @brief Analyzes battery capacity measurement data(in Ah).電池の容量測定データ（Ah単位）を解析します。
    # @param time times-series.Series形式の時間。
    # @param sampling_time sampling time sec(default:).サンプリング時間。
    # @param save_dir_path save directry path.保存先のディレクトリパス。
    # @param stop_charge_current stop charge Ah(default:0.0).充電停止時の出力電流。
    # @param stop_discharge_current stop discharge Ah(default:0.0).放電停止時の出力電流。
    # @param graph_time_unit graph time unit(default:h).グラフの時間軸の単位。
    # @param pre_discharge_start_time pre discharge start time(float, default:None).捨て放電開始時間。
    # @param pre_discharge_end_time pre discharge end time(float, ddefault:None).捨て放電終了時間。
    # @param charge_start_time charge start time(float, default:None).充電開始時間。
    # @param charge_end_time charge end time(float, ddefault:None).充電終了時間。
    # @param discharge_start_time discharge start time(float, ddefault:None).放電開始時間。
    # @param discharge_end_time discharge end time(float, ddefault:None).放電終了時間。
    # @retval param Ah_max, Ah_min, pre_discharge_Ah_sum, pre_discharge_time, charge_Ah_sum, charge_time, discharge_Ah_sum, discharge_time.出力の最大値・最小値、捨て放電時間、捨て放電の電力量、充電の電力量、放電の電力量。
    # @retval df dataframe.電力量を追加したデータフレーム。
    # @retval dst dictionary.辞書型。
    def calc(self,
             time,
             currents,
             sampling_time=1,
             save_dir_path=None,
             stop_charge_current=0.0,
             stop_discharge_current=0.0,
             graph_time_unit="h",
             charge_positive = True,
             pre_discharge_start_time=None,
             pre_discharge_end_time=None,
             charge_start_time=None,
             charge_end_time=None,
             discharge_start_time=None,
             discharge_end_time=None,
             ):
        # 保存先のディレクトリパスが存在しなければ作成
        save_dir_path = os.path.dirname(save_dir_path)
        if not os.path.exists(save_dir_path):
            os.mkdir(save_dir_path)

        if graph_time_unit == "h":
            time_unit = 3600.0
            time_label = "Time[h]"
        elif graph_time_unit == "m":
            time_unit = 60.0
            time_label = "Time[m]"
        elif graph_time_unit == "s":
            time_unit = 1.0
            time_label = "Time[s]"

        dst = {}
        param = {}

        # サンプリング時間[sec]を計算
        if sampling_time == 1:
            sampling_time = time[1] - time[0]

        df = pd.DataFrame(currents)

        # Ahの最大値、最小値を計算
        max_current = currents.max()
        min_current = currents.min()

        # AhをAhに変換し、カラムに追加
        Ah = currents * sampling_time / 3600.0

        # Ahの累積和を計算し、カラムに追加
        Ah_cumsum = Ah.cumsum()

        df["Ah"] = Ah
        df["Ah_cumsum"] = Ah_cumsum

        # 捨て放電の開始時間が指定されなければ捨て放電の開始時間を自動取得
        if pre_discharge_start_time == None:
            # 充電電流が正なら
            if charge_positive == True:
                pre_discharge_start_time = time[currents < 0].min()
            # 充電電流が負なら
            else:
                pre_discharge_start_time = time[currents > 0].min()
        print(pre_discharge_start_time)
        # 捨て放電の終了時間が指定されなければ捨て放電の終了時間を取得
        if pre_discharge_end_time == None:
            # 充電電流が正なら
            if charge_positive == True:
                temp_time = time[currents >= stop_discharge_current]
            # 充電電流が負なら
            else:
                temp_time = time[currents <= stop_discharge_current]
            
            pre_discharge_end_time = temp_time[temp_time >
                                               pre_discharge_start_time].min() - sampling_time

        # 充電開始時間が指定されなければ充電の開始時間を取得
        if charge_start_time == None:
            # 充電電流が正なら
            if charge_positive == True:
                temp_time = time[currents > stop_charge_current]
            else:
                # 充電の開始時間を取得
                temp_time = time[currents < stop_charge_current]

            charge_start_time = temp_time[temp_time >
                                          pre_discharge_end_time].min()

        # 充電開始時間が指定されなければ充電の終了時間を取得
        if charge_end_time == None:
            # 充電電流が正なら
            if charge_positive == True:
                temp_time = time[currents <= stop_charge_current]
            # 充電電流が負なら
            else:
                temp_time = time[currents >= stop_charge_current]

            charge_end_time = temp_time[temp_time >
                                        charge_start_time].min() - sampling_time

        # 充電開始時間が指定されなければ電の開始時間を取得
        if discharge_start_time == None:
            # 充電電流が正なら
            if charge_positive == True:
                temp_time = time[currents < stop_discharge_current]
                # 充電電流が負なら
            else:
                temp_time = time[currents > stop_discharge_current]
            discharge_start_time = temp_time[temp_time >
                                             charge_end_time].min()

        # 充電終了時間が指定されなければ電の終了時間を取得
        if discharge_end_time == None:
            # 充電電流が正なら
            if charge_positive == True:
                temp_time = time[currents >= stop_discharge_current]
            else:
                temp_time = time[currents <= stop_discharge_current]
            discharge_end_time = temp_time[temp_time >
                                           discharge_start_time].min() - sampling_time
        print(discharge_end_time)

        # 捨て放電の電力量積算、電力量累積和、所要時間を計算
        pre_discharge_Ah_sum = df.loc[
            pre_discharge_start_time:pre_discharge_end_time, "Ah"].sum()
        pre_discharge_Ah_cumsum = df.loc[pre_discharge_start_time:
                                          pre_discharge_end_time, "Ah_cumsum"]

        pre_discharge_time = pre_discharge_end_time - pre_discharge_start_time
        df_pre_discharge = df.loc[pre_discharge_start_time:pre_discharge_end_time, :]

        # 充電の電力量積算、電力量累積和、所要時間を計算し、データフレームをCSV出力
        charge_Ah_sum = df.loc[charge_start_time:charge_end_time, "Ah"].sum()
        charge_Ah_cumsum = df.loc[charge_start_time:
                                   charge_end_time, "Ah_cumsum"]
        charge_time = charge_end_time - charge_start_time
        df_charge = df.loc[charge_start_time:charge_end_time, :]

        # 放電の電力量積算、電力量累積和、所要時間を計算し、データフレームをCSV出力
        discharge_Ah_sum = df.loc[discharge_start_time:discharge_end_time, "Ah"].sum()
        discharge_Ah_cumsum = df.loc[discharge_start_time:
                                      discharge_end_time, "Ah_cumsum"]
        discharge_time = discharge_end_time - discharge_start_time
        df_discharge = df.loc[discharge_start_time:discharge_end_time, :]

        # 充電の電力量、電力量積算、累積和、所要時間を計算
        charge_Ah = Ah.loc[charge_start_time:charge_end_time]
        df_charge_Ah = pd.DataFrame(charge_Ah)
        charge_Ah_sum = charge_Ah.sum()
        charge_Ah_cumsum = charge_Ah.cumsum()
        charge_time = charge_end_time - charge_start_time

        # 放電の電力量、電力量積算、累積和、所要時間を計算
        discharge_Ah = Ah.loc[discharge_start_time:discharge_end_time]
        df_discharge_Ah = pd.DataFrame(discharge_Ah)
        discharge_Ah_sum = discharge_Ah.sum()
        discharge_Ah_cumsum = discharge_Ah.cumsum()
        discharge_time = discharge_end_time - discharge_start_time

        param["max_current"] = max_current
        param["min_current"] = min_current
        param["pre_discharge_time"] = pre_discharge_time
        param["charge_time"] = charge_time
        param["discharge_time"] = discharge_time
        param["pre_discharge_Ah_sum"] = pre_discharge_Ah_sum
        param["charge_Ah_sum"] = charge_Ah_sum
        param["discharge_Ah_sum"] = discharge_Ah_sum
        param["pre_discharge_start_time"] = pre_discharge_start_time
        param["pre_discharge_end_time"] = pre_discharge_end_time
        param["charge_start_time"] = charge_start_time
        param["charge_end_time"] = charge_end_time
        param["discharge_start_time"] = discharge_start_time
        param["discharge_end_time"] = discharge_end_time
        df_param = pd.Series(param)
        df_param = df_param.T

        # データフレームをCSVファイルに書き込む
        df_pre_discharge.to_csv(save_dir_path + "/pre-discharge.csv")
        df_charge.to_csv(save_dir_path + "/charge.csv")
        df_discharge.to_csv(save_dir_path + "/discharge.csv")
        df_param.to_csv(save_dir_path + "/param.csv", header=False)

        dst["pre_discharge_start_time"] = pre_discharge_start_time
        dst["pre_discharge_end_time"] = pre_discharge_end_time
        dst["charge_start_time"] = charge_start_time
        dst["charge_end_time"] = charge_end_time
        dst["discharge_start_time"] = discharge_start_time
        dst["discharge_end_time"] = discharge_end_time
        dst["pre_discharge"] = df_pre_discharge
        dst["charge"] = df_charge
        dst["discharge"] = df_discharge
        dst["charge_Ah"] = df_charge_Ah
        dst["charge_Ah_cumsum"] = charge_Ah_cumsum
        dst["discharge_Ah"] = df_discharge_Ah = pd.DataFrame(discharge_Ah)
        dst["discharge_Ah_cumsum"] = discharge_Ah_cumsum

        # グラフ表示
        fig = plt.figure(figsize=(15.0, 8.0))
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 12

        # 時間信号（元）
        plt.subplot(221)
        plt.plot(time/time_unit, Ah_cumsum, label='All time')
        plt.xlabel(time_label, fontsize=12)
        plt.ylabel("Cumulative sum[Ah]", fontsize=12)
        plt.grid()

        plt.subplot(222)
        plt.plot(df_pre_discharge.index/time_unit,
                 df_pre_discharge["Ah"], label='All time')
        plt.xlabel(time_label, fontsize=14)
        plt.ylabel("Pre discharge[Ah]", fontsize=14)
        plt.grid()
        # leg = plt.legend(loc=1, fontsize=15)
        # leg.get_frame().set_alpha(1)

        # 充電のグラフ化
        plt.subplot(223)
        plt.plot(df_charge.index/time_unit, df_charge["Ah"], label='All time')
        plt.xlabel(time_label, fontsize=14)
        plt.ylabel("Charge[Ah]", fontsize=14)
        plt.grid()
        # leg = plt.legend(loc=1, fontsize=15)
        # leg.get_frame().set_alpha(1)

        # 放電のグラフ化
        plt.subplot(224)
        plt.plot(df_discharge.index/time_unit,
                 df_discharge["Ah"], label='All time')
        plt.xlabel(time_label, fontsize=14)
        plt.ylabel("Discharge[Ah]", fontsize=14)
        plt.grid()

        plt.savefig(save_dir_path + "/graph.png")
        plt.close()
        return param, dst, df

def main():
    # 読み込むCSVファイルのパス
    CSV_PATH = "C:/github/libs/python/calc2/examples/battery_capacity_ah/datasets/battery_capacity_measurement_ah.csv"

    # 保存先のディレクトリパス
    SAVE_DIR_PATH = "C:/github/libs/python/calc2/examples/battery_capacity_ah/result/"

    bck = BatteryCapacityAh()

    # 空のデータフレームを作成
    df = pd.DataFrame({})

    # CSVファイルのロードし、データフレームへ格納
    df = pd.read_csv(CSV_PATH, encoding="UTF-8", skiprows=0)

    # 時刻の列データを取り出し
    date = df.loc[:, "時刻"]
    df["date"] = pd.to_datetime(date, format='%Y年%m月%d日%H時%M分%S秒')

    # 経過時間[sec]を計算し、カラムに追加
    df["time"] = time = df["date"] - df.loc[0, "date"]
    df["time"] = df['time'].dt.total_seconds()

    # 重複した経過時間があれば、重複行を削除
    df = df[~df["time"].duplicated()]

    # 経過時間をインデックスラベルに設定
    df.set_index("time", inplace=True)

    # ラベル名のリネーム
    df = df.rename(columns={'電流': 'current'})

    # 蓄電池の容量測定（Ah単位）
    param, dst, df = bck.calc(
        time=df.index,
        currents=df["current"],
        save_dir_path=SAVE_DIR_PATH,
        graph_time_unit="h",
        charge_positive=False,
        pre_discharge_start_time=None,
        pre_discharge_end_time=None,
        charge_start_time=None,
        charge_end_time=None,
        discharge_start_time=None,
        discharge_end_time=None,)


if __name__ == "__main__":
    main()
