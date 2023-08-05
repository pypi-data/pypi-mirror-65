# -*- coding: utf-8 -*-
import math

# 三相電力の計算
class AcPhase3:
    dst = {}
    
    # 入力が（線間電圧、消費電力、力率）の場合
    def El_P3p_Cos(self, El, P3p, Cos, wire):

        dst = {}
        dst["El"] = El
        dst["P3p"] = P3p
        dst["Cos"] = Cos
        dst["Pp"] = Pp = P3p / 3
        
        # delta
        if(wire == "delta"):
            dst["Ep"] = Ep = El
            dst["Il"] = Il = P3p / (math.sqrt(3) * El * Cos)
            dst["Ip"] = Ip = Il / math.sqrt(3)
  
         # star結線
        if(wire == "star"):
            dst["Ep"] = Ep = El / math.sqrt(3)
            dst["Il"] = Il = P3p / (math.sqrt(3) * El * Cos)
            dst["Ip"] = Ip = Il
            
        dst["Zp"] = Zp = Ep / Ip
        dst["Rp"] = Rp = Zp * Cos
        dst["Xp"] = Xp = math.sqrt(Zp**2 - Rp**2)
        
        return dst
        
    # 入力が（線間電圧、抵抗、リアクタンス）の場合
    def El_Rp_Xp(self, El, Rp, Xp, wire):

        dst = {}
        dst["El"] = El
        dst["Rp"] = Rp
        dst["Xp"] = Xp
               
        # Δ結線
        if(wire == "delta"):
            dst["Ep"] = Ep = El

        # star結線
        if(wire == "star"):
            dst["Ep"] = Ep = El / math.sqrt(3)
            
        dst["Zp"] = Zp = math.sqrt(Rp**2 + Xp**2)
        dst["Cos"] = Cos = Rp/ float(Zp)
        dst["Pp"] = Pp = (Ep**2) / Rp
        dst["P3p"] = P3p = Pp * 3
        dst["Il"] = Il = P3p / (math.sqrt(3) * El * Cos)
        dst["Ip"] = Ip = Il

        return dst
  
    # 入力が（線電流、インピーダンス、力率）の場合
    def Il_Zp_Cos(self, Il, Zp, Cos, wire):     

        dst = {}
        dst["Il"] = Il
        dst["Zp"] = Zp
        dst["Cos"] = Cos
        dst["Rp"] = Rp = Zp * Cos
        dst["Xp"] = Xp = math.sqrt(Zp**2 - Rp**2)              

        # Δ結線        
        if(wire == "delta"):
            dst["Ip"] = Ip = Il / math.sqrt(3)   
            dst["Ep"] = Ep = Zp * Ip
            dst["El"] = El = Ep
            
        # star結線
        if(wire == "star"):
            dst["Ip"] = Ip = Il 
            dst["Ep"] = Ep = Zp * Ip
            dst["El"] = El = Ep * math.sqrt(3)  
            
        dst["Pp"] = Pp = Ep * Ip  * Cos
        dst["P3p"] = P3p = Pp * 3

        return dst            

    # 入力が（線電流、抵抗、リアクタンス）の場合
    def Il_Rp_Xp(self, Il, Rp, Xp, wire):    

        dst = {}
        dst["Il"] = Il
        dst["Rp"] = Rp
        dst["Xp"] = Xp
        dst["Zp"] = Zp = math.sqrt(Rp**2 + Xp**2) 
            
        # Δ結線
        if(wire == "delta"):
            dst["Ip"] = Ip = Il / math.sqrt(3)
            dst["Ep"] = Ep = Zp * Ip
            dst["El"] = El = Ep

        # star結線
        if(wire == "star"):
            dst["Ip"] = Ip = Il
            dst["Ep"] = Ep = Zp * Ip
            dst["El"] = El = Ep * math.sqrt(3)
            
        dst["Pp"] = Pp = Rp * Ip**2
        dst["P3p"] = P3p = Pp * 3
        dst["Cos"] = Cos = Rp / Zp

        return dst

    # 入力が（線間電圧、線電流、力率）の場合
    def El_Il_Cos(self, El, Il, Cos, wire):

        dst = {}
        dst["Il"] = Il
        dst["El"] = El
        dst["Cos"] = Cos      
        
        # Δ結線
        if(wire == "delta"):
            dst["Ep"] = Ep = El
            dst["Ip"] = Ip = Il / math.sqrt(3) 

        # star結線
        if(wire == "star"):
            dst["Ep"] = Ep = El / math.sqrt(3)
            dst["Ip"] = Ip = Il
            
        dst["Zp"] = Zp = Ep / Ip
        dst["Rp"] = Rp = Zp * Cos
        dst["Pp"] = Pp = Rp * Ip**2
        dst["Xp"] = Xp = math.sqrt(Zp**2 - Rp**2)   
        dst["P3p"] = P3p = Pp * 3
        
        return dst

    # 入力が（線間電圧、消費電力、力率）の場合
    def Il_P3p_Cos(self, Il, P3p, Cos, wire):

        dst = {}
        dst["Il"] = Il
        dst["P3p"] = P3p
        dst["Cos"] = Cos
        dst["Pp"] = Pp = P3p / 3
              
        # Δ結線
        if(wire == "delta"):
            dst["Ip"] = Ip = Il / math.sqrt(3)
            dst["Zp"] = Zp = P3p /(3 * Ip**2 * Cos)
            dst["Ep"] = Ep = Zp * Ip
            dst["El"] = El = Ep

        # star結線
        if(wire == "star"):
            dst["Ip"] = Ip = Il
            dst["Zp"] = Zp = P3p /(3 * Ip**2 * Cos)
            dst["Ep"] = Ep = Zp * Ip
            dst["El"] = El = Ep *  math.sqrt(3)
        
        dst["Rp"] = Rp = Zp * Cos
        dst["Xp"] = Xp = math.sqrt(Zp**2 - Rp**2)
        
        return dst

    def show_result(self, dst):
        print("Il[A] = ", dst["Il"])
        print("El[V] = ", dst["El"])
        print("P3p（W） = ", dst["P3p"])
        print("Pp（W） = ", dst["Pp"])
        print("Cosθ[rad] = ", dst["Cos"])
        print("Ep[V] = ", dst["Ep"])
        print("Ip[A] = ", dst["Ip"])
        print("Zp[Ω] = ", dst["Zp"])
        print("Rp[Ω] = ", dst["Rp"])
        print("Xp[Ω] = ", dst["Xp"])
        print("------------------------------------")

def main():
    ac3 = AcPhase3()

    print("■Input...El, P3p, Cos, delta or star wire")
    result1 = ac3.El_P3p_Cos(El=480., P3p=2000000., Cos=1., wire="delta")
    ac3.show_result(result1)

    result2 = ac3.El_P3p_Cos(El=480., P3p=2000000., Cos=1., wire="star")
    ac3.show_result(result2)
    
    print("■Input...El, Rp, Xp, delta or star wire")
    result3 = ac3.El_Rp_Xp(El=480., Rp=0.345, Xp=0., wire="delta")
    ac3.show_result(result3)

    result4 = ac3.El_Rp_Xp(El=480., Rp=0.1152, Xp=0., wire="star")
    ac3.show_result(result4)

    print("■Input...Il, Zp, Cos, delta or star wire")
    result5 = ac3.Il_Zp_Cos(Il=2405.3, Zp=0.346, Cos=1., wire="delta")
    ac3.show_result(result5)

    result6 = ac3.Il_Zp_Cos(Il=2405.3, Zp=0.1152, Cos=1., wire="star")
    ac3.show_result(result6)
 
    print("■Input...Il, Rp, Xp, delta or star wire")
    result7 = ac3.Il_Rp_Xp(Il=2405.5, Rp=0.3456, Xp=0., wire="delta")
    ac3.show_result(result7)

    result8 = ac3.Il_Rp_Xp(Il=2405.5, Rp=0.1152, Xp=0., wire="star")
    ac3.show_result(result8)
    
    
    print("■Input...Il, El, Cos, delta or star wire")
    result9 = ac3.El_Il_Cos(Il=2405.6, El=480., Cos=1., wire="delta")
    ac3.show_result(result9)

    result10 = ac3.El_Il_Cos(Il=2405.6, El=480., Cos=1., wire="star")
    ac3.show_result(result10)
    
    print("■Input...Il, P3p, Cos, delta or star wire")
    result11 = ac3.Il_P3p_Cos(Il=2405.6, P3p=2000000., Cos=1., wire="delta")
    ac3.show_result(result11)
    
    result12 = ac3.Il_P3p_Cos(Il=2405.6, P3p=2000000., Cos=1., wire="star")
    ac3.show_result(result12)

if __name__ == "__main__":
    main()