import numpy as np
import xlrd
from matplotlib import pyplot as plt

data = xlrd.open_workbook("C:\\Users\\junto\\Desktop\\mathematical modelling\\CUMCM\\附件.xls")
table = data.sheet_by_name(u'Sheet1')

data_org = np.array(table.col_values(1)[1:])
time_org = np.array(table.col_values(0)[1:])

def T_air(s):
    T1,T2,T3,T4 = 175,195,235,255
    L0 = 25
    L1 = 30.5*5 + 5*4+25 #193.5
    L2 = 30.5*6 + 5*5+25 #228.0
    L3 = 30.5*7 + 5*6+25  #262.5
    L4 = 30.5*9 + 5*8+25  #331.5
    L5 = 30.5*11 + 5*10 #400.5

    if s <= L0:
        return 25+(T1-25)*s/L0

    elif s >= L0 and s <= L1:
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
    elif s >= L4 and s <= L4+5:
        return T4+(25-T4)*(s-L4)/(5)
    else :return 25



Delta_t = 0.5
speed = 70/60.0
result_k = []
for i in range(len(data_org)-1):
   distance = speed * time_org[i]
   k = -(data_org[i+1]-data_org[i])/(Delta_t * (data_org[i] - T_air(distance)))
   if abs(k)>=1:
       k = 0
   result_k.append(k)
   print('%.4f'%k,'%.2f'%distance, time_org[i], T_air(distance))

tairdata=[]
for i in range(len(time_org)-1):
    distance=speed * time_org[i]
    tairdata.append(T_air(distance))

tairdata.append(0)

result_k.append(0)
fig1 = plt.figure()
#ax = fig.add_subplot(111)
#ax.set(ylim = [-0.03,0.03])
#ax.plot(time_org*speed, result_k)
plt.plot(time_org,result_k)
# plt.plot(time_org,data_org)
# plt.plot(time_org,tairdata)
plt.show()




#21.0 | (165.5,170.0) | (195,199.5) | (22
#t1 = L0/speed

# k_best1 = 0.017
# for k in np.arange(0.017, 0.021, 0.0001):
#     j = 4
#     T_now = data_org[j]
#     error_tmp = 0
#     for t in np.arange(21.0,165.0, Delta_t):
#         T_next = T_now *(1 - k*Delta_t) + k * T_air(t*speed) * Delta_t
#         j += 1
#         error_tmp += abs(T_next-data_org[j])
#         T_now = T_next
#     if(k != 0.017):
#         if(error_tmp < error):
#             error = error_tmp
#             k_best1 = k
#     else:
#         error = error_tmp
#
# print('温区1'，k_best1,error)
# k_best1 = 0.017
# for k in np.arange(0.017, 0.021, 0.0001):
#     j = 4
#     T_now = data_org[j]
#     error_tmp = 0
#     for t in np.arange(21.0,165.0, Delta_t):
#         T_next = T_now *(1 - k*Delta_t) + k * T_air(t*speed) * Delta_t
#         j += 1
#         error_tmp += abs(T_next-data_org[j])
#         T_now = T_next
#     if(k != 0.017):
#         if(error_tmp < error):
#             error = error_tmp
#             k_best1 = k
#     else:
#         error = error_tmp
#
# print('温区1'，k_best1,error)

#T_cal = [data_org[4]]

#now_i = 0
#for t in np.arange(21.0,165.0, 0.5):
#    T_next = T_cal[now_i] *(1-k*Delta_t) - T_air(t*speed)*Delta_t
#    T_cal.append(T_next)
#    i += 1


