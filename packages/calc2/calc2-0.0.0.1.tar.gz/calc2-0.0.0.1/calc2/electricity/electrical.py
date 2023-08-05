# -*- coding: utf-8 -*-
import math

# 三相電力の計算
class AC:
    dst = {}
    
    # 線間電圧、消費電力、力率を入力（Δ結線）
    def phase3(self, El=None, P3p=None, Cos=None, Rp=None, Il=None, Zp=None, Xp=None, cmd="El_P3p_delta"):

        dst = {}

        if(cmd == "El_P3p_delta"):
            dst["El"] = El
            dst["P3p"] = P3p
            dst["Cos"] = Cos
            dst["Pp"] = Pp = P3p / 3
            dst["Ep"] = Ep = El
            dst["Il"] = Il = P3p / (math.sqrt(3) * El * Cos)
            dst["Ip"] = Ip = Il / math.sqrt(3)
            dst["Zp"] = Zp = Ep / Ip
            dst["Rp"] = Rp = Zp * Cos
            dst["Xp"] = Xp = math.sqrt(Zp**2 - Rp**2)
            return dst

        # 線間電圧、抵抗、リアクタンスを入力（Δ結線）
        if(cmd == "El_Rp_Xp_delta"):
            dst["El"] = El
            dst["Rp"] = Rp
            dst["Xp"] = Xp
            dst["Ep"] = Ep = El
            dst["Zp"] = Zp = math.sqrt(Rp**2 + Xp**2)
            dst["Cos"] = Cos = Rp/ float(Zp)
            dst["Pp"] = Pp = (Ep**2) / Rp
            dst["P3p"] = P3p = Pp * 3
            dst["Il"] = Il = P3p / (math.sqrt(3) * El * Cos)
            dst["Ip"] = Ip = Il / math.sqrt(3)

            return dst

        # 線電流、インピーダンス、力率を入力（Δ結線）
        if(cmd == "Il_Zp_delta"):
            dst["Il"] = Il
            dst["Zp"] = Zp
            dst["Cos"] = Cos
            dst["Rp"] = Rp = Zp * Cos
            dst["Xp"] = Xp = math.sqrt(Zp**2 - Rp**2)
            dst["Ip"] = Ip = Il / math.sqrt(3)   
            dst["Ep"] = Ep = Zp * Ip
            dst["El"] = El = Ep
            dst["Pp"] = Pp = Ep * Ip  * Cos
            dst["P3p"] = P3p = Pp * 3

            return dst            

        # 線電流、抵抗、リアクタンスを入力（Δ結線）
        if(cmd == "Il_Rp_Xp_delta"):
            dst["Il"] = Il
            dst["Rp"] = Rp
            dst["Xp"] = Xp
            dst["Zp"] = Zp = math.sqrt(Rp**2 + Xp**2) 
            dst["Ip"] = Ip = Il / math.sqrt(3)
            dst["Pp"] = Pp = Rp * Ip**2
            dst["P3p"] = P3p = Pp * 3
            dst["Cos"] = Cos = Rp / Zp
            dst["Ep"] = Ep = Zp * Ip
            dst["El"] = El = Ep
            return dst

        # 線電流、線電圧を入力（Δ結線）
        if(cmd == "Il_El_delta"):
            dst["Il"] = Il
            dst["El"] = El
            dst["Cos"] = Cos
            dst["Ep"] = Ep = El
            dst["Ip"] = Ip = Il / math.sqrt(3) 
            dst["Zp"] = Zp = Ep / Ip
            dst["Rp"] = Rp = Zp * Cos
            dst["Pp"] = Pp = Rp * Ip**2
            dst["Xp"] = Xp = math.sqrt(Zp**2 - Rp**2)   
            dst["P3p"] = P3p = Pp * 3
            return dst

        # 線間電圧、消費電力、力率を入力（Δ結線）
        if(cmd == "Il_P3p_delta"):
            dst["Il"] = Il
            dst["P3p"] = P3p
            dst["Cos"] = Cos
            dst["Pp"] = Pp = P3p / 3
            dst["Ip"] = Ip = Il / math.sqrt(3)
            dst["Zp"] = Zp = P3p /(3 * Ip**2 * Cos)
            dst["Ep"] = Ep = Zp * Ip
            dst["El"] = El = Ep
            dst["Rp"] = Rp = Zp * Cos
            dst["Xp"] = Xp = math.sqrt(Zp**2 - Rp**2)
            return dst


    def show_result(self, dst, cmds):
        if(cmds == "three_phase"):
            print("Il[A] = ",     dst["Il"])
            print("El[V] = ",     dst["El"])
            print("P3p（W） = ",     dst["P3p"])
            print("Pp（W） = ",     dst["Pp"])
            print("Cosθ[rad] = ",     dst["Cos"])
            print("Ep[V] = ",     dst["Ep"])
            print("Ip[A] = ",     dst["Ip"])
            print("Zp[Ω] = ",     dst["Zp"])
            print("Rp[Ω] = ",     dst["Rp"])
            print("Xp[Ω] = ",     dst["Xp"])

def main():
    print("test")