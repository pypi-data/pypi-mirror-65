# -*- coding: uTf-8 -*-
"""
@brief Analyzes various parameters of pulse signals.
@details Analyzes various parameters of pulse signals.
"""
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math


class Pulse():

    ##
    # @fn calc_time
    # @brief Calculate the rise time, fall time, and the time between HIGH of the pulse signal.[波形の各種時間（立上り、下がり、ONなど]を計算)
    # @param ts times array[時間データのnumpy配列]
    # @param ts amplitude array[立ち上がり開始時間]
    # @param ts times array[立ち上がり開始時間]
    # @param Ymax max of amplitude(default:None)[振幅の最大値]
    # @param Ymin min of amplitude(default:None)[振幅の最小値]
    # @param upper_threshold upper threshold of amplitude(default:0.9)[振幅の上限]
    # @param lower_threshold lower threshold of amplitude(default:0.1)[振幅の下限]
    # @param Tr_start_min Tr start min (default:None)[立ち上がり開始時間の最小値]
    # @param Tr_start Tr start (default:None)[立ち上がり開始時間]
    # @param Ton_min Ton min (default:None)[ONしている時間の最小値]
    # @retval dist["Ymax"] max of amplitude[振幅の最大値]
    # @retval dist["Ymin"] min of amplitude[振幅の最小値]
    # @retval dist["Yamp"] amplitude[振幅]
    # @retval dist["upper"] upper threshold of amplitude[振幅の上限]
    # @retval dist["lower"] lower threshold of amplitude[振幅の下限]
    # @retval dist["Tr_start"] Start of rise time[立ち上がり開始時間]
    # @retval dist["Tr_end"] End of rise time[立ち上がり終了時間]
    # @retval dist["Tr"] rise time[立ち上がり時間]
    # @retval dist["Tf_start"] Start of rise time[立ち下がり開始時間]
    # @retval dist["Tf_end"] Start of rise time[立ち下がり終了時間]
    # @retval dist["Ton"] on time[ON中の時間]
    # @retval dist["Tf"] fall time[立ち下がり時間]
    # @retval dist["Tau"] Time constant[時定数]
    def calc_time(self, ts, ys, Ymax=None, Ymin=None, upper_threshold=0.9, lower_threshold=0.1, Tr_start_min=None, Tr_start=None, Ton_min=None):

        dst = {}

        # 最小時間が指定されていなければ、最も小さい時間をセット
        if Tr_start_min == None:
            Tr_start_min = ts.min()

        # 最小時間が指定されていなければ、最も小さい時間をセット
        if Ton_min == None:
            Ton_min = 0

        if Ymax == None:
            Ymax = ys.max()

        if Ymin == None:
            Ymin = ys.min()

        dst["Ymax"] = Ymax
        dst["Ymin"] = Ymin
        dst["Yamp"] = Yamp = Ymax - Ymin

        dst["upper"] = upper_threshold
        dst["lower"] = lower_threshold

        # 立上り開始時間（信号がしきい値と最小値を超えた直後の時間）を取得
        if Tr_start == None:
            Trs_start = ts[ys > Yamp * lower_threshold]
            dst["Tr_start"] = Tr_start = Trs_start[Trs_start > Tr_start_min].min()
        # 立上り開始時間が指定されているときは、指定値をセット
        else:
            dst["Tr_start"] = Tr_start

        # 立上り終了時間を取得
        Trs_end = ts[ys > Yamp * upper_threshold]
        dst["Tr_end"] = Tr_end = Trs_end[Trs_end > Tr_start].min()

        # 立上り時間を計算
        dst["Tr"] = Tr = Tr_end - Tr_start

        # 立下り開始時間を取得( ＞ 立上り終了時間 + ON最小時間)
        try:
            Tfs_start = ts[ys < Yamp * upper_threshold]
            dst["Tf_start"] = Tf_start = Tfs_start[Tfs_start >
                                                   Tr_end + Ton_min].min()
        except:
            dst["Tf_start"] = Tf_start = ts[-1]

        # 立下り終了時間を取得
        try:
            Tfs_end = ts[ys < Yamp * 0.1]
            dst["Tf_end"] = Tf_end = Tfs_end[Tfs_end > Tf_start].min()
        except:
            dst["Tf_end"] = Tf_end = ts[-1]

        if math.isnan(Tf_start):
            dst["Tf_start"] = Tf_start = ts[-1]

        if math.isnan(Tf_end):
            dst["Tf_end"] = Tf_end = ts[-1]

        # ONの時間を計算(立上り終了時間～立下り開始時間)
        dst["Ton"] = Ton = Tf_start - Tr_end

        # 立下り時間を計算
        dst["Tf"] = Tf = Tf_end - Tf_start

        # 時定数を計算
        Taus = ts[ys >= Yamp * 0.632]
        dst["Tau"] = Tau = Taus[Taus > Tr_start_min].min() - Tr_start
        self.pulse_times = dst

        return dst

    ##
    # @fn show_time
    # @brief Show the rise time, fall time, and the time between HIGH of the pulse signal.[波形の各種時間（立上り、下がり、ONなど]を表示)
    def show_time(self):
        dst = {}
        Tr_start = self.pulse_times["Tr_start"]
        Tr_end = self.pulse_times["Tr_end"]
        Tr = self.pulse_times["Tr"]
        Ton = self.pulse_times["Ton"]
        Tf_start = self.pulse_times["Tf_start"]
        Tf_end = self.pulse_times["Tf_end"]
        Tf = self.pulse_times["Tf"]
        Tau = self.pulse_times["Tau"]
        Ymax = self.pulse_times["Ymax"]
        Ymin = self.pulse_times["Ymin"]
        Yamp = self.pulse_times["Yamp"]

        print("Tr start:", Tr_start)
        print("Tr end:", Tr_end)
        print("Tr:", Tr)
        print("Ton:", Ton)
        print("Tf start:", Tf_start)
        print("Tr end:", Tf_end)
        print("Tf:", Tf)
        print("Tau:", Tau)

    def save_graph(self, x, y, xlabel, ylabel, save_path, label_name="Y"):
        Tr_start = self.pulse_times["Tr_start"]
        Tr_end = self.pulse_times["Tr_end"]
        Tr = self.pulse_times["Tr"]
        Ton = self.pulse_times["Ton"]
        Tf_start = self.pulse_times["Tf_start"]
        Tf_end = self.pulse_times["Tf_end"]
        Tf = self.pulse_times["Tf"]
        Tau = self.pulse_times["Tau"]
        Ymax = self.pulse_times["Ymax"]
        Ymin = self.pulse_times["Ymin"]
        Yamp = self.pulse_times["Yamp"]
        upper_threshold = self.pulse_times["upper"]
        lower_threshold = self.pulse_times["lower"]

        # 保存先のディレクトリパスが存在しなければ作成
        dir_path = os.path.dirname(save_path)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        # グラフ化
        ax = plt.axes()
        plt.rcParams['font.family'] = 'Times New Roman'  # 全体のフォント
        plt.rcParams['axes.linewidth'] = 1.0  # 軸の太さ

        # 電流値をプロット
        plt.plot(x, y, lw=1, c="r", alpha=0.7, ms=2, label=label_name)

        # 立上り・下りの開始、終了時間、時定数に垂線をプロット
        plt.vlines(Tr_start, min(y), max(y), ls='--',
                   color="b", lw=1, label="Tr start")
        plt.vlines(Tr_end, min(y), max(y), ls='--',
                   color="g", lw=1, label="Tr end")
        plt.vlines(Tf_start, min(y), max(y),
                   ls='--', lw=1, label="Tf start")
        plt.vlines(Tf_end, min(y), max(y), ls='--',
                   color="m", lw=1, label="Tf end")
        plt.vlines(Tau, min(y), max(y), ls='-', lw=1, label="Tau")

        # 電流最大値の10%、90%に水平線をプロット
        plt.hlines(Yamp * 0.9, min(x), max(x), ls='--',
                   color="r", lw=1, label="Amp " + sTr(upper_threshold*100)+"%")
        plt.hlines(Yamp * 0.1, min(x), max(x), ls='--',
                   color="y", lw=1, label="Amp " + sTr(lower_threshold*100)+"%")

        # グラフの保存
        plt.legend(loc="best")     # 凡例の表示（2：位置は第二象限）
        plt.xlabel('Time[msec]', fontsize=12)  # x軸ラベル
        plt.ylabel('Current[A]', fontsize=12)  # y軸ラベル
        plt.grid()  # グリッドの表示
        plt.legend(loc="best")  # 凡例の表示
        plt.savefig(save_path)
        plt.clf()

    # 実効値の計算
    def calc_rms(self, y):
        return np.sqrt(np.square(y).mean())  # 実効値の計算


def main():
    pulse = Pulse()

    # 読み込むCSVファイルのパス
    csv_path = "C:/prog/python/auto/current.csv"
    save_path = "C:/prog/python/auto/"

    # 空のデータフレームを作成
    df = pd.DataFrame({})

    # CSVファイルのロードし、データフレームへ格納
    df = pd.read_csv(csv_path, encoding="UTf-8", skiprows=0)

    # 電流値の列データを取り出し
    Its = df.loc[:, "current"]

    # 経過時間の列データを取り出し
    ts = df.loc[:, "time"]

    # 各種時間を計算（上限90%、下限10%）
    pulse.calc_time(ts, Its, Ymin=0, Ton_min=50)
    times = pulse.show_time()
    pulse.save_graph(
        ts, Its, xlabel="Time[msec]", ylabel="Current[A]", save_path=save_path+"a.png", label_name="I(t)")

    """
        Tr start: 8.4
        Tr end: 328.2
        Tr: 319.8
        Ton: 278.8
        Tf start: 607.0
        Tr end: 620.8
        Tf: 13.799999999999955
        Tau: 114.39999999999999
        RMS: 249.061976770524
    """
    print("RMS:", pulse.calc_rms(Its))


if __name__ == "__main__":
    main()
