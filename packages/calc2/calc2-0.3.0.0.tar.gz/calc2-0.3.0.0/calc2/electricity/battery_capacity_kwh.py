# -*- coding: uTf-8 -*-
"""
@brief Analyzes battery capacity measurement data(in kw).電池の容量測定データ（kw単位）を解析します。
"""
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

class BatteryCapacityKwh():
    ##
    # @fn calc
    # @brief Analyzes battery capacity measurement data(in kw).電池の容量測定データ（kw単位）を解析します。
    # @param time times-series.Series形式の時間。
    # @param sampling_time sampling time sec(default:).サンプリング時間。
    # @param save_dir_path save directry path.保存先のディレクトリパス。
    # @param stop_charge_kw stop charge kw(default:0.0).充電停止時の出力電力。
    # @param stop_discharge_kw stop discharge kw(default:0.0).放電停止時の出力電力。
    # @param graph_time_unit graph time unit(default:h).グラフの時間軸の単位。
    # @param pre_discharge_start_time pre discharge start time(float, default:None).捨て放電開始時間。
    # @param pre_discharge_end_time pre discharge end time(float, ddefault:None).捨て放電終了時間。
    # @param charge_start_time charge start time(float, default:None).充電開始時間。
    # @param charge_end_time charge end time(float, ddefault:None).充電終了時間。
    # @param discharge_start_time discharge start time(float, ddefault:None).放電開始時間。
    # @param discharge_end_time discharge end time(float, ddefault:None).放電終了時間。
    # @retval param kw_max, kw_min, pre_discharge_kwh_sum, pre_discharge_time, charge_kwh_sum, charge_time, discharge_kwh_sum, discharge_time.出力の最大値・最小値、捨て放電時間、捨て放電の電力量、充電の電力量、放電の電力量。
    # @retval df dataframe.電力量を追加したデータフレーム。
    # @retval dst dictionary.辞書型。
    def calc(self,
             time,
             kw,
             sampling_time=1,
             save_dir_path=None,
             stop_charge_kw=0.0,
             stop_discharge_kw=0.0,
             graph_time_unit="h",
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

        df = pd.DataFrame(kw)

        # kwの最大値、最小値を計算
        kw_max = kw.max()
        kw_min = kw.min()

        # kwをkwhに変換し、カラムに追加
        kwh = kw * sampling_time / 3600.0

        # kwhの累積和を計算し、カラムに追加
        kwh_cumsum = kwh.cumsum()

        df["kwh"] = kwh
        df["kwh_cumsum"] = kwh_cumsum

        # 捨て放電の開始時間が指定されなければ
        if pre_discharge_start_time == None:
            # 捨て放電の開始時間を自動取得
            pre_discharge_start_time = time[kw > 0].min()

        # 捨て放電の終了時間が指定されなければ
        if pre_discharge_end_time == None:
            # 捨て放電の終了時間を取得
            temp_time = time[kw <= stop_discharge_kw]
            pre_discharge_end_time = temp_time[temp_time >
                                               pre_discharge_start_time].min() - sampling_time

        # 充電開始時間が指定されなければ
        if charge_start_time == None:
            # 充電の開始時間を取得
            temp_time = time[kw < stop_charge_kw]
            charge_start_time = temp_time[temp_time >
                                          pre_discharge_end_time].min()

        # 充電開始時間が指定されなければ
        if charge_end_time == None:
            # 充電の終了時間を取得
            temp_time = time[kw >= stop_charge_kw]
            charge_end_time = temp_time[temp_time >
                                        charge_start_time].min() - sampling_time

        # 充電開始時間が指定されなければ
        if discharge_start_time == None:
            # 放電の開始時間を取得
            temp_time = time[kw > stop_discharge_kw]
            discharge_start_time = temp_time[temp_time >
                                             charge_end_time].min()

        # 充電終了時間が指定されなければ
        if discharge_end_time == None:
            # 充電の終了時間を取得
            temp_time = time[kw <= stop_discharge_kw]
            discharge_end_time = temp_time[temp_time >
                                           discharge_start_time].min() - sampling_time

        # 捨て放電の電力量積算、電力量累積和、所要時間を計算
        pre_discharge_kwh_sum = df.loc[
            pre_discharge_start_time:pre_discharge_end_time, "kwh"].sum()
        pre_discharge_kwh_cumsum = df.loc[pre_discharge_start_time:
                                          pre_discharge_end_time, "kwh_cumsum"]

        pre_discharge_time = pre_discharge_end_time - pre_discharge_start_time
        df_pre_discharge = df.loc[pre_discharge_start_time:pre_discharge_end_time, :]

        # 充電の電力量積算、電力量累積和、所要時間を計算し、データフレームをCSV出力
        charge_kwh_sum = df.loc[charge_start_time:charge_end_time, "kwh"].sum()
        charge_kwh_cumsum = df.loc[charge_start_time:
                                   charge_end_time, "kwh_cumsum"]
        charge_time = charge_end_time - charge_start_time
        df_charge = df.loc[charge_start_time:charge_end_time, :]

        # 放電の電力量積算、電力量累積和、所要時間を計算し、データフレームをCSV出力
        discharge_kwh_sum = df.loc[discharge_start_time:discharge_end_time, "kwh"].sum(
        )
        discharge_kwh_cumsum = df.loc[discharge_start_time:
                                      discharge_end_time, "kwh_cumsum"]
        discharge_time = discharge_end_time - discharge_start_time
        df_discharge = df.loc[discharge_start_time:discharge_end_time, :]

        # 充電の電力量、電力量積算、累積和、所要時間を計算
        charge_kwh = kwh.loc[charge_start_time:charge_end_time]
        df_charge_kwh = pd.DataFrame(charge_kwh)
        charge_kwh_sum = charge_kwh.sum()
        charge_kwh_cumsum = charge_kwh.cumsum()
        charge_time = charge_end_time - charge_start_time

        # 放電の電力量、電力量積算、累積和、所要時間を計算
        discharge_kwh = kwh.loc[discharge_start_time:discharge_end_time]
        df_discharge_kwh = pd.DataFrame(discharge_kwh)
        discharge_kwh_sum = discharge_kwh.sum()
        discharge_kwh_cumsum = discharge_kwh.cumsum()
        discharge_time = discharge_end_time - discharge_start_time

        param["kw_max"] = kw_max
        param["kw_min"] = kw_min
        param["pre_discharge_time"] = pre_discharge_time
        param["charge_time"] = charge_time
        param["discharge_time"] = discharge_time
        param["pre_discharge_kwh_sum"] = pre_discharge_kwh_sum
        param["charge_kwh_sum"] = charge_kwh_sum
        param["discharge_kwh_sum"] = discharge_kwh_sum
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
        dst["charge_kwh"] = df_charge_kwh
        dst["charge_kwh_cumsum"] = charge_kwh_cumsum
        dst["discharge_kwh"] = df_discharge_kwh = pd.DataFrame(discharge_kwh)
        dst["discharge_kwh_cumsum"] = discharge_kwh_cumsum

        # グラフ表示
        fig = plt.figure(figsize=(15.0, 8.0))
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 12

        # 時間信号（元）
        plt.subplot(221)
        plt.plot(time/time_unit, kwh_cumsum, label='All time')
        plt.xlabel(time_label, fontsize=12)
        plt.ylabel("Cumulative sum[kwh]", fontsize=12)
        plt.grid()

        plt.subplot(222)
        plt.plot(df_pre_discharge.index/time_unit,
                 df_pre_discharge["kwh"], label='All time')
        plt.xlabel(time_label, fontsize=14)
        plt.ylabel("Pre discharge[kwh]", fontsize=14)
        plt.grid()
        # leg = plt.legend(loc=1, fontsize=15)
        # leg.get_frame().set_alpha(1)

        # 充電のグラフ化
        plt.subplot(223)
        plt.plot(df_charge.index/time_unit, df_charge["kwh"], label='All time')
        plt.xlabel(time_label, fontsize=14)
        plt.ylabel("Charge[kwh]", fontsize=14)
        plt.grid()
        # leg = plt.legend(loc=1, fontsize=15)
        # leg.get_frame().set_alpha(1)

        # 放電のグラフ化
        plt.subplot(224)
        plt.plot(df_discharge.index/time_unit,
                 df_discharge["kwh"], label='All time')
        plt.xlabel(time_label, fontsize=14)
        plt.ylabel("Discharge[kwh]", fontsize=14)
        plt.grid()

        plt.savefig(save_dir_path + "/graph.png")
        plt.close()
        return param, dst, df

def main():
    # 読み込むCSVファイルのパス
    CSV_PATH = "C:/github/libs/python/calc2/examples/battery_test/datasets/battery_capacity_measurement.csv"

    # 保存先のディレクトリパス
    SAVE_DIR_PATH = "C:/github/libs/python/calc2/examples/battery_test/result/"

    bck = BatteryCapacityKwh()

    # 空のデータフレームを作成
    df = pd.DataFrame({})

    # CSVファイルのロードし、データフレームへ格納
    df = pd.read_csv(CSV_PATH, encoding="SHIFT-JIS", skiprows=0)

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
    df = df.rename(columns={'電力': 'kw'})

    # 蓄電池の容量測定（kwh単位）
    param, dst, df = bck.calc(
        time=df.index,
        kw=df["kw"],
        save_dir_path=SAVE_DIR_PATH,
        graph_time_unit="h",
        pre_discharge_start_time=None,
        pre_discharge_end_time=None,
        charge_start_time=None,
        charge_end_time=None,
        discharge_start_time=None,
        discharge_end_time=None,)


if __name__ == "__main__":
    main()
