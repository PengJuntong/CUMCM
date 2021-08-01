import numpy as np
import xlrd
from matplotlib import pyplot as plt
import math
import matplotlib
import pandas as pd
from sklearn.linear_model import LinearRegression

data = xlrd.open_workbook('data.xls')
table = data.sheet_by_name(u'Sheet1')

data_org = np.array(table.col_values(1)[1:])
time_org = np.array(table.col_values(0)[1:])
Delta_t = 0.5
speed = 70/60.0
result_k = []
Tair=[]

L0 = 25
L1 = 30.5*5 + 5*4+25 #193.5
L2 = 30.5*6 + 5*5+25 #228.0
L3 = 30.5*7 + 5*6+25  #262.5
L4 = 30.5*9 + 5*8+25  #339.5
L5 = 30.5*11 + 5*10+25 #400.5
#初始的温区设定
T1,T2,T3,T4 = 175,195,235,255
###
##温度场的确定
###
#############################################################################################################
def T_air(s):

    
    if s <= L0+18 and s >= L0-15:
        #return min(4.61*s-22.3,175)
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

#画空气温度曲线
#for time in time_org:
#    distance = speed * time
#    Tair.append(T_air(distance))
#painter(Tair)

###
###
#############################################################################################################


#温度场的合理性检验

#for i in range(len(data_org)-1):
#    distance = speed * time_org[i]
#    k = -(data_org[i+1]-data_org[i])/(Delta_t * (data_org[i] - T_air(distance)))
#    Tair.append(T_air(distance))
#    result_k.append(k)
#    #print('%.4f'%k,'%.2f'%distance, time_org[i], T_air(distance))
#result_k.append(0)
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.set(ylim = [-0.03,0.03])
#ax.plot(time_org*speed, result_k)
#plt.show(）






#找最优k
#############################################################################################################
def search_k(start, end, k_predict):
    k_best = k_predict
    flag = False

    for k in np.arange(k_predict - 0.006 , k_predict + 0.008 , 0.0001):
        T_now = data_org[start]
        error_tmp = 0
        for t in range(start, end):
            T_next = T_now *(1 - k*Delta_t) + k * T_air(time_org[t]*speed) * Delta_t
            error_tmp += (T_next-data_org[t+1])**2
            T_now = T_next
        if flag:
            if(error_tmp < error):
               error = error_tmp
               k_best = k
        else: 
            error = error_tmp
            flag = True

    return [k_best, error]

k1=search_k(0,291,0.017)
print(k1)
k2=search_k(292,351,0.018)
print(k2)
k3=search_k(352,412,0.025)
print(k3)
k4=search_k(413,534,0.021)
print(k4)
k5=search_k(534,708,0.02)
print(k5)
kerror=[k1,k2,k3,k4,k5]
cal_klist = [k1[0], k2[0], k3[0], k4[0],k5[0]] #每段最优k
data_df=pd.DataFrame(kerror)
data_df.columns =["k","error"]
data_df.index = ["k1","k2","k3","k4","k5"]
writer = pd.ExcelWriter('klist.xls')  
data_df.to_excel(writer,float_format='%.7f')  
writer.save()


#根据距离返回k
def k_s(s):
    if s <= L1:
        return cal_klist[0]
    #if s >= L1 and s <= L1+5:
    #    return cal_klist[0]+(cal_klist[1]-cal_klist[0])*(s-L1)/5.0
    if s >= L1 and s <= L2:
        return cal_klist[1]
    #if s>=L2 and s<=L2+5:
    #    return cal_klist[1]+(cal_klist[2]-cal_klist[1])*(s-L2)/5.0
    if s >= L2 and s <= L3:
        return cal_klist[2]
    if s >= L3 and s <= L4:
        return cal_klist[3]
    if s >= L4:
        return cal_klist[4]
#############################################################################################################



#根据初值生成炉温曲线
def u_cacl():
    T_cacl = [30.03]
    i = 0
    for t in np.arange(19.0,373.0, 0.5):
        distance = t*speed
        k = k_s(distance)
        T_next = T_cacl[i] *(1-k*Delta_t) + k * T_air(distance) * Delta_t
        T_cacl.append(T_next)
        i += 1
    return np.array(T_cacl)

#画算出来的炉温曲线
#画图函数，横坐标距离
def painter1(y):
    #plt.figure()
    plt.rcParams['font.family']=['Microsoft Yahei']
    plt.title("生成炉温曲线与原始炉温曲线的比较")
    plt.xlabel("时间(s)")
    plt.ylabel("温度(℃)")
    plt.plot(time_org,y)
    plt.plot(time_org,data_org)
    plt.savefig('生成炉温曲线与原始炉温曲线的比较.png')
    plt.show()
painter1(u_cacl())



#更新温区温度设置,以下两幅图为问题1的答案
T1,T2,T3,T4=182,203,237,254

prob1=u_cacl()
def painter2(y):
    
    plt.rcParams['font.family']=['Microsoft Yahei']
    plt.title("新炉温曲线与原始炉温曲线的比较")
    plt.xlabel("时间(s)")
    plt.ylabel("温度(℃)")
    plt.plot(time_org,y)
    plt.plot(time_org,data_org)
    plt.savefig('新炉温曲线与原始炉温曲线的比较.png')
    plt.show()
  


def painter3(y):
    
    plt.rcParams['font.family']=['Microsoft Yahei']
    plt.title("新炉温曲线")
    plt.xlabel("时间(s)")
    plt.ylabel("温度(℃)")
    plt.plot(time_org,y)
  
    plt.savefig('新炉温曲线.png')
    plt.show()

painter2(prob1)
painter3(prob1)
#混沌序列
def chao(M,a,b):
    m0 = np.random.rand()
    m_list = [((b-a)*m0+a)]
    for i in range(M):
        m = 4*m0*(1-m0)
        m_list.append(((b-a)*m+a))
        m0 = m
    return m_list

#print(chao(20,75,80))

