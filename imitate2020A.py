import numpy as np
import xlrd
from matplotlib import pyplot as plt
import math
from sklearn.linear_model import LinearRegression

data = xlrd.open_workbook('D:\\Python data\\imitate2020A\\imitate2020A\\data.xls')
table = data.sheet_by_name(u'Sheet1')

data_org = np.array(table.col_values(1)[1:])
time_org = np.array(table.col_values(0)[1:])


L0 = 25
L1 = 30.5*5 + 5*4+25 #193.5
L2 = 30.5*6 + 5*5+25 #228.0
L3 = 30.5*7 + 5*6+25  #262.5
L4 = 30.5*9 + 5*8+25  #331.5
L5 = 30.5*11 + 5*10+25 #400.5

def T_air(s):

    T1,T2,T3,T4 = 175,195,235,255
    if s <= L0+25 and s >= L0-5:
        return max(4.61*s-22.3,175)
    elif s>=L0+25 and s <= L1-5:
        return T1
    elif s >= L1-5 and s<= L1+10:
        return T1+(T2-T1)*(s-L1+5)/15.0

    elif s >= L1+10 and s<= L2-5:
        return T2
    elif s >= L2-5 and s<= L2+10:
        return T2+(T3-T2)*(s-L2+5)/15.0

    elif s>= L2+10 and s<= L3-5:
        return T3
    elif s >= L3-5 and s<= L3+10:
        return T3+(T4-T3)*(s-L3+5)/15.0

    elif s >= L3+10 and s<= L4-5:
        return T4
    elif s >= L4-5 and s <= L4+10:
        return T4+(25-T4)*(s-L4+5)/15.0
    else:
        return 25



Delta_t = 0.5
speed = 70/60.0
result_k = []
Tair=[]
for i in range(len(data_org)-1):
    distance = speed * time_org[i]
    k = -(data_org[i+1]-data_org[i])/(Delta_t * (data_org[i] - T_air(distance)))
    if (i<=4):
        tair_calc = data_org[i] + (data_org[i+1]-data_org[i])/(0.018*Delta_t)
        print([distance,tair_calc,T_air(distance)])
        Tair.append(tair_calc)
    else:
        Tair.append(T_air(distance))
    result_k.append(k)
    #print('%.4f'%k,'%.2f'%distance, time_org[i], T_air(distance))


#result_k.append(0)
#Tair.append(25)
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.set(ylim = [-0.03,0.03])
#ax.plot(time_org*speed, result_k)
#plt.show()

def painter(y):
    plt.figure()
    plt.plot(time_org*speed,y)
    plt.plot(time_org*speed,data_org)
    plt.show()


#0.02 | 0.018 | 0.025 | 0.021 | 0.01
#4 291 351 412 534


def search_k(start, end, k_predict):
    k_best = k_predict
    flag = False

    for k in np.arange(k_predict - 0.006 , k_predict + 0.006 , 0.0001):
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

print(search_k(0,291,0.017))
print(search_k(292,351,0.018))
print(search_k(352,412,0.025))
print(search_k(413,534,0.021))
print(search_k(534,708,0.01))

cal_klist = [0.185, 0.142, 0.213, 0.211, 0.0061]
def k_s(s):
    if s <= L1:
        return cal_klist[0]
    if s >= L1 and s <= L2:
        return cal_klist[1]
    if s >= L2 and s <= L3:
        return cal_klist[2]
    if s >= L3 and s <= L4:
        return cal_klist[3]
    if s >= L4:
        return cal_klist[4]

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

painter(u_cacl())

def chao(M,a,b):
    m0 = np.random.rand()
    m_list = [((b-a)*m0+a)]
    for i in range(M):
        m = 4*m0*(1-m0)
        m_list.append(((b-a)*m+a))
        m0 = m
    return m_list

#print(chao(20,75,80))
