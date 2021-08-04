from matplotlib import pyplot as plt

#温度场
def T_air(s, T_air_list):

    L0 = 25
    L1 = 30.5*5 + 5*4+25 
    L2 = 30.5*6 + 5*5+25 
    L3 = 30.5*7 + 5*6+25  
    L4 = 30.5*9 + 5*8+25  
    L5 = 30.5*11 + 5*10+25 

    T1 = T_air_list[0]
    T2 = T_air_list[1]
    T3 = T_air_list[2]
    T4 = T_air_list[3]
    
    if s <= L0+18 and s >= L0-15:
        return 25+(T1-25)*(s-L0+15)/33.0

    elif s>=L0+18 and s <= L1:
        return T1

    elif s >= L1 and s<= L1+5:
        return T1+(T2-T1)*(s-L1)/5.0

    elif s >= L1+5 and s<= L2:
        return T2

    elif s >= L2 and s<= L2+5:
        return T2+(T3-T2)*(s-L2)/5.0

    elif s>= L2+5 and s<= L3:
        return T3

    elif s >= L3 and s<= L3+5:
        return T3+(T4-T3)*(s-L3)/5.0

    elif s >= L3+5 and s<= L4:
        return T4
    
    elif s >= L4 and s <= L4+50:
        return T4+(90-T4)*(s-L4)/50.0

    elif s >= L4+50:
        return 90+(25-90)*(s-L4-50)/250

    else:
        return 25

#根据距离返回k
def k_s(s):
    L1 = 30.5*5 + 5*4+25 
    L2 = 30.5*6 + 5*5+25 
    L3 = 30.5*7 + 5*6+25  
    L4 = 30.5*9 + 5*8+25  
    L5 = 30.5*11 + 5*10+25 

    if s <= L1:
        return 0.0194

    if s >= L1 and s <= L2:
        return 0.0142
    if s >= L2 and s <= L3:
        return 0.0213
    if s >= L3 and s <= L4:
        return 0.0211
    if s >= L4:
        return 0.0168


