import numpy as np
import xlrd
from matplotlib import pyplot as plt

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
t_end = 373.0

def T_air(s):

    T1,T2,T3,T4 = 175,195,235,255
    if s <= L0+5 and s >= L0-5:
        return 25+(T1-25)*(s-L0+5)/10
    elif s>=L0+5 and s <= L1-5:
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
<<<<<<< HEAD
    elif s >= L4-5 and s <= L4+10:
        return T4+(25-T4)*(s-L4+5)/15.0
=======
    elif s >= L4 and s <= L4+5:
        return T4+(25-T4)*(s-L4)/(5)
>>>>>>> 3c4b6a53acd6e6961ff19b650cfde7d7b8091876
    else :return 25



Delta_t = 0.5
speed = 70/60.0
result_k = []
Tair=[]
for i in range(len(data_org)-1):
    distance = speed * time_org[i]
    k = -(data_org[i+1]-data_org[i])/(Delta_t * (data_org[i] - T_air(distance)))
    if abs(k)>=1:
        k = 0
    result_k.append(k)
    Tair.append(T_air(distance))
    print('%.4f'%k,'%.2f'%distance, time_org[i], T_air(distance))


result_k.append(0)
Tair.append(25)
fig = plt.figure()
#ax = fig.add_subplot(111)
##ax.set(ylim = [-0.03,1])
#ax.plot(time_org*speed, result_k)
plt.plot(time_org*speed, Tair)
plt.plot(time_org*speed, data_org)
plt.show()

#21.0 | (165.5,170.0) | (195,199.5) | (22
#t1 = L0/speed

k_best = 0.017
for k in np.arange(0.017, 0.021, 0.0001):
    j = 4
    T_now = data_org[j]
    error_tmp = 0
    for t in np.arange(21.5,169.5, Delta_t):
        T_next = T_now *(1 - k*Delta_t) + k * T_air(t*speed) * Delta_t
        j += 1
        error_tmp += (T_next-data_org[j])**2
        T_now = T_next
    if(k != 0.017):
        if(error_tmp < error):
            error = error_tmp
            k_best = k
    else: 
        error = error_tmp

#print(k_best,error)

def k_s(s):
    if s <= L0 or s >= L5:
        return result_k[0]
    if s >= L0 and s <= L1:
        return result_k[1]
    if s >= L1 and s <= L2:
        return result_k[2]
    if s >= L2 and s <= L3:
        return result_k[3]
    if s >= L3 and s <= L4:
        return result_k[4]

def u_cacl(s):
    T_cal = [25]
    i = 0
    for t in np.arange(0,t_end, 0.5):
        distance = t*speed
        k = k_s(distance)
        T_next = T_cal[i] *(1-k*Delta_t) + k * T_air(distance) * Delta_t
        T_cacl.append(T_next)
        i += 1
    return np.array(T_cal)


def chao(M,a,b):
    m0 = np.random.rand()
    m_list = [((b-a)*m0+a)]
    for i in range(M):
        m = 4*m0*(1-m0)
        m_list.append(((b-a)*m+a))
        m0 = m
    return m_list

print(chao(20,75,80))


