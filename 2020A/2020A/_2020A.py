

import numpy as np
import xlrd
from matplotlib import pyplot as plt
import matplotlib
import pandas as pd
from function import *

import time
import openpyxl

gy1_1 = [173,198,230,257]

answer_p1 = u_cacl(78/60.0,gy1_1)

painter(answer_p1,
        '新炉温曲线与原始炉温曲线的比较',True)

painter(answer_p1,
        '新炉温曲线',False)

#写入答案
ans = [time_org,answer_p1]
ans = np.transpose(ans)
np.savetxt("result.csv",ans, delimiter = ',')



###p2
#更新小温区温度
gy2 = [182,203,237,254]

#斜率检验函数
def properrate(y):
    flag=True
    for i in range (len(y)-1):
        rate=y[i+1]-y[i]
        if abs(rate) > 1.5:
            flag=False
            break
        else:
            continue
    return flag

#峰值温度检验函数
def propermax(y):
    if max(y) > 240 and max(y) < 250:
        return True
    else:
        return False

#找高于217时间点
def highT_time(y):

    init_i=0
    final_i=len(y)-1

    for i in range (len(y)):
        if y[i]>217:
            init_i=i
            break
        else:
            continue
    for i in range(len(y)-1, 0, -1): #range(,,-1)反向遍历
        if y[i]>217:
            final_i = i
            break
        else :
            continue
    deltai=final_i-init_i
    if deltai>80 and deltai<180:
        flag=True
    else:flag=False

    return [init_i, final_i,flag]


#高于217的时间检验函数
def hightemtime(y):
    i = highT_time(y)
    deltai = i[1] - i[0]

    if(deltai>80 and deltai<180):
        return True
    else:
        return False

#温度区间持续时间检验函数
def sptime(y):

    init_i=0
    final_i=len(y)-1

    for i in range (len(y)):
        if y[i]>150:
            init_i=i
            break
        else:
            continue
    for i in range (init_i,len(y)-1):
        if y[i]>190:
            final_i=i
            break
        else:
            continue
    deltai = final_i - init_i

    if(deltai>120 and deltai<240):
        return True
    else:
        return False


#递归用生成函数
def u_cacl2(v):
    return u_cacl(v,gy2)

lowerbound = 0.5
upperbound = 4
 
step=0.1

def recurf1(x):
    global step
    if step<pow(0.1,5):
        return x

    temp=u_cacl(x,gy2)
    if not propermax(temp):
        x=x-step
        return recurf1(x)
    if propermax(temp):
        x=x+step
        step=step/2.0
        return recurf1(x)

def recurf(x, algorithm):
    global step
    global upperbound
    if algorithm(u_cacl(upperbound,gy2)): return upperbound
    if step<pow(0.1,5):
        return x

    temp=u_cacl2(x)
    if not algorithm(temp):
        x=x-step
        return recurf(x)
    if algorithm(temp):
        x=x+step
        step=step/2.0
        return recurf(x)

upperbound=recurf1(upperbound)
step=0.1
upperbound=recurf(upperbound, properrate)
step=0.1
upperbound=recurf(upperbound, hightemtime)
step=0.1
upperbound=recurf(upperbound, sptime)


print("问题2中的速度最大值为：")
print(upperbound)
np.savetxt("prob2.csv",[upperbound], delimiter = ',')
answer_p2 = u_cacl2(upperbound)

painter(answer_p2,
        '问题2炉温曲线',False)


###p3、p4

def chao(M,a,b):

    m0 = np.random.rand()
    m_list = [((b-a)*m0+a)]
    for i in range(M-1):
        m = 4*m0*(1-m0)
        m_list.append(((b-a)*m+a))
        m0 = m
    return m_list


#判断温度序列是否满足制程界限
def goodSetting(u_list):
    if properrate(u_list):
        if sptime(u_list):
            if propermax(u_list):
                if hightemtime:
                    return True
    else:
        return False

#算面积
def highT_area(u_list):

    max_time = u_list.index(max(u_list))
    i = highT_time(u_list)[0]
    area = 0
    for time in range(i,max_time):
        area += u_list[time]*Delta_t

    return area-((max_time-i)*u_list[i]*Delta_t)

#算镜像误差
def mirror_error(u_list):
    max_time = u_list.index(max(u_list))
    i = highT_time(u_list)[1]
    error = 0
    for j in range(i,max_time,-1):
        error += (u_list[2*max_time-j]-u_list[j])**2
    return error


cycletimes = 3000
counter = 62
while True :
    tempre_pre = chao(cycletimes,165,185)
    tempre_stable1 = chao(cycletimes,185,205)
    tempre_stable2 = chao(cycletimes,225,245)
    tempre_back = chao(cycletimes,245,265)
    v_search = chao(cycletimes,65/60.0,100/60.0)
    P_mark = [False]*cycletimes #标记该设定是否满足制程界限

    #将5个混沌序列并排后转置，变成一行一组设定
    data_list = np.array([v_search, P_mark, tempre_pre, tempre_stable1, tempre_stable2, tempre_back])
    data_list = data_list.transpose()

    flag = False
    S_min = 0
    S_max = 0
    error_max = 0
    error_min = 0
    answer_p3 = np.zeros(5)

    #遍历求最小面积，顺便求最大面积和误差
    for u in data_list:
        u_list = u_cacl(u[0],u[2:])

        if goodSetting(u_list):
            u[1] = True #将符合制程界限的设定标记变成True

            S = highT_area(u_list) 
            error = mirror_error(u_list)
            print(S,error)

            if flag:                
                if S <= S_min:
                    S_min = S
                    answer_p3 = u
                if S >= S_max:
                    S_max = S
                if error <= error_min:
                    error_min = error
                if error >= error_max:
                    error_max = error
            else:
                S_min = S
                S_max = S
                error_min = error
                error_max = error
                flag = True

    flag = False
    P_best = 0
    answer_p4 = np.zeros(5)
    

    #遍历求综合指标
    for u in data_list:
        if u[1]:#只对标记为True的遍历，不再重复调用判断函数

            u_list = u_cacl(u[0],u[2:])
            S = highT_area(u_list) 
            error = mirror_error(u_list)
            P = (S-S_min)/(S_max-S_min) + (error-error_min)/(error_max-error_min)
            print(P)

            if flag:                
                if P <= P_best:
                    P_best = P
                    answer_p4 = u
            else:
                P_best = P
                flag = True

    print("以下为答案\n:")
    print(answer_p3)
    print(S_min)
    print(answer_p4)
    print(P_best)
    x=time.strftime("%H%M%S")
    wb= openpyxl.load_workbook("prob3.xlsx")
    sheet=wb['Sheet1']
    answer_p3=np.append(answer_p3,S_min)
    for j in range (7):
        sheet.cell(row=counter+1,column=j+1,value=answer_p3[j])
    wb.save("prob3.xlsx")
    #answer_p3=np.append(answer_p3,S_min)
    #answer_p4=answer_p4.transpose()
    #dataoutput3=pd.DataFrame(answer_p3)
    ##dataoutput3.index=["速度","T1","T2","T3","T4"]
    #dataoutput3.to_csv(r"C:\Users\junto\Desktop\mathematical modelling\CUMCM\CUMCM2020A\CUMCM2020A\p3\%s.csv"%x)
    ##dataoutput4=pd.DataFrame(answer_p3)
    ##dataoutput3.index=["速度","T1","T2","T3","T4"]
    ##dataoutput4.to_excel("\\p4\\%s.xlsx"%x)
    
    counter=counter+1
