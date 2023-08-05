# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime as dt
import numpy as np
import math

# 三相電力の計算


class Hioki:

    # 先頭列が時刻のCSVファイルをロード
    def load_csv(self, csv_path, skip_rows=None, rename_label=None):

        # CSVファイルのロード
        df_raw = pd.read_csv(csv_path, encoding="SHIFT-JIS")

        # 列数、行数の取得
        rows, columns = df_raw.shape

        if skip_rows == None:
            skip_rows = columns + 4

        # ある行数（列数+4）を読み飛ばしてデータフレームに格納
        df = pd.read_csv(csv_path, encoding="SHIFT-JIS", skiprows=skip_rows)

        # 時刻先頭の「'」を「20」に置換
        df['Time'] = df['Time'].str.replace("\'", "20")

        # ISO8601形式の時刻表記に変換
        df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%Ss')

        # インデックスに「Time」列を設定
        df.set_index('時間[s]', inplace=True)

        # カラム名の変更
        df.columns = rename_label

        # 経過時間[HH:MM:SS]の計算
        df2['Duration time[HH:MM:SS]'] = df2.index.to_series() - \
            pd.to_datetime(start_time)

        # 経過時間[sec]の計算
        df2['Duration time[sec]'] = df2['Duration time[HH:MM:SS]'].apply(
            lambda x: x / np.timedelta64(1, 's'))

        # 経過時間[min]の計算
        df2['Duration time[min]'] = df2['Duration time[HH:MM:SS]'].apply(
            lambda x: x / np.timedelta64(1, 'm'))

        return df2

    # 先頭列が時刻のCSVファイルをロード
    def load_csv2(self, csv_path, skip_rows=None, rename_label=None):

        # CSVファイルのロード
        df_raw = pd.read_csv(csv_path, encoding="SHIFT-JIS")

        # 列数、行数の取得
        rows, columns = df_raw.shape

        if skip_rows == None:
            skip_rows = columns + 4

        # ある行数（列数+4）を読み飛ばしてデータフレームに格納
        df = pd.read_csv(csv_path, encoding="SHIFT-JIS", skiprows=skip_rows)

        if rename_label != None:
            # カラム名の変更
            df.columns = rename_label
            df.set_index(rename_label[0], inplace=True)

        df.set_index("time", inplace=True)

        return df

    def show_graph(self, df2):
        # グラフ化
        df2.plot(x='Duration time[min]', y=df.columns)
        plt.legend(loc=4, fontsize=20)           # 凡例の表示（4：位置は第4象限）
        plt.title('Heating test', fontsize=20)   # グラフタイトル
        plt.xlabel('Duration time[min]', fontsize=20)            # x軸ラベル
        plt.ylabel('Temp.[℃] / Voltage[V]', fontsize=20)            # y軸ラベル
        plt.tick_params(labelsize=20)         # 軸ラベルの目盛りサイズ
        plt.tight_layout()                      # ラベルがきれいに収まるよう表示
        plt.grid()                              # グリッドの表示
        plt.show()                              # グラフ表示


def main():
    hioki = Hioki()

    # CSVファイルのパス
    csv_path = "C:\prog\python\\auto\\test.csv"

    # 抽出する時刻（最初の時刻、最後の時刻）
    #start_time = '2018-09-24 09:55:00'
    #end_time = '2018-09-24 10:55:10'

    # 新しいカラム名
    #rename_label = ['Motor1[℃]', 'Motor2[℃]', 'Motor3[℃]',
    #            'Battery1[V]', 'Battery2[V]', 'Battery3[V]', 'Battery4[V]']
    df = hioki.load_csv2(csv_path, skip_rows=0)
    print(df)
    #ac3.show_result(result12)


if __name__ == "__main__":
    main()
