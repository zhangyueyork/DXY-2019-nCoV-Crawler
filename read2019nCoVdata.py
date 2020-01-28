#!/usr/bin/env python3.7
#
import requests
import time
print("-"*10,"import end0","-"*10)
from datetime import datetime
import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
#plt.style.use(["classic", "myself"])
print("-"*10,"import end","-"*10)
########


def printdict(inputdict):
    print('v'*50)
    for keyi in inputdict.keys():
        print(keyi, '-->', inputdict[keyi])
    print('^'*50)
   #^^^^^^^END


def timechange(timetime):
#    if len(str(timetime)) > 10:
#        timetime = float(str(timetime)[:10] + '.'+str(timetime)[10:])
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timetime))
    return t
   #^^^^^^^END


def getdata(url):
    response = requests.get(url)
    return response.json()
   #^^^^^^^END


def selectkeydata(listdict, keyword, keyvalue):
    # 仅留下列表中，keyword==keyvalue的字典
    newlist = []
    for dicti in listdict:
        if dicti[keyword] == keyvalue:
            newlist.append(dicti)
    return newlist
   #^^^^^^^END


def selecttimedata(listdict, keyword, t1, t2):
    # 仅留下某个时间段内的字典
    newlist = []
    for dicti in listdict:
        if t1 < dicti[keyword] <= t2:
            newlist.append(dicti)
    return newlist
   #^^^^^^^END


def listvalue(listdict, keyword):
    # 留下列表内，时间最新的字典
    timelst = []
    for dicti in listdict:
        timelst.append(dicti[keyword])
    ########
    timelst.sort()
    latestdict = {}
    for dicti in listdict:
        if dicti[keyword] == timelst[-1]:
            latestdict = dicti
            break
    return latestdict
   #^^^^^^^END


def timeseries(t0, deltaT=60*60*24):
    tnow = int(time.time())
    tlst0 = np.arange(t0, tnow, deltaT)
    tlst0 = [int(ti) for ti in tlst0]
    tlst1 = list(tlst0[0::1])
    tlst2 = list(tlst0[1::1]) + [tnow]
    return tlst1, tlst2


def evolution(listdict, tlst1, tlst2, timekeyword, valuekeyword):
    tlst = []
    valuelst = []
    valuei = 0
    for i1, tA in enumerate(tlst1):
        tB = tlst2[i1]
        rangelistdictI = selecttimedata(listdict, timekeyword, tA, tB)
        if len(rangelistdictI) != 0:
            valuedict = listvalue(rangelistdictI, timekeyword)
            valuei = valuedict[valuekeyword]
        valuelst.append(valuei)
        ########
        tlst.append(tB)
    return tlst, valuelst
   #^^^^^^^END


def province_evolution(province, countkeyword, listdict, tAlst, tBlst):
#    listdict = selectkeydata(listdict, 'country', '中国')
    province_data = selectkeydata(listdict, 'provinceName', province)
#    print(len(listdict))
#    print(len(province_data))
    ######## dataset1
    count1 = []
    tlst1 = []
    for listi in province_data:
        count1.append(listi[countkeyword])
        tlst1.append(listi['updateTime'])
    ######## dataset2
    tlst2, count2 = evolution(province_data, tAlst, tBlst, 
            'updateTime', countkeyword)
    ########
    return tlst1, count1, tlst2, count2
   #^^^^^^^END


def nationalevolution(allprovince, countkeyword, listdict, tAlst, tBlst):
    countall = np.zeros(len(tBlst))
    for pi in allprovince:
        tlst1, count1, tlst2, count2 \
                = province_evolution(pi, countkeyword, listdict, tAlst, tBlst)
        countall += np.array(count2)
    return tBlst, countall
   #^^^^^^^END




###############################################################################
url0 = 'http://lab.isaaclin.cn/nCoV'
url1 = url0 + '/api/overall'
url2 = url0 + '/api/provinceName'
url3 = url0 + '/api/province'
url4 = url0 + '/api/area'
###############################################################################
# 时间零点从2020-1-20 00:00:01 开始，
t0 = 1579449601
print('t0---->', time.asctime(time.localtime(t0)))
########################
if __name__ == '__main__':
    r1 = getdata(url1)
    r2 = getdata(url2)
    printdict(r1['results'][0])
    allprovince = r2['results']
    print(allprovince)
    ########
#    r = getdata(url4)
    ff = open('123.txt', 'r')
#    print(r, file=ff)
    lst = [i1.replace('\n', '') for i1 in ff]
    ff.close()
    r = eval(lst[0])
    print(r['results'][0])
    ########################
    t1, t2 = timeseries(t0, 60*60*12)
    t1 = [ti*1e3 for ti in t1]
    t2 = [ti*1e3 for ti in t2]
    ########################
#    tlst, countall = nationalevolution(allprovince, 
#            'confirmedCount', r['results'], t1, t2)
    tlst1, count1, tlst2, count2 = province_evolution('北京市', 
            'confirmedCount', r['results'], t1, t2)
    tlst1 = [(ti*1e-3-t0)/3600/24 for ti in tlst1]
    tlst2 = [(ti*1e-3-t0)/3600/24 for ti in tlst2]
    ########################
    print(tlst2)
    print(count2)
#    print(countall[-1])
    plt.figure()
    plt.plot(tlst1, count1, '.-')
    plt.plot(tlst2, count2, '.-')
#    plt.yscale('log')
    plt.show()
    ########################
#    tlst2x = [datetime.strptime(timechange(ti), "%Y-%m-%d %H:%M:%S").date() 
#            for ti in tlst2]
#    tlst1x = [datetime.strptime(timechange(ti), "%Y-%m-%d %H:%M:%S").date() 
#            for ti in tlst1]
#    print([timechange(ti) for ti in tlst2])
    #tc2 = [ti.split()[0].replace('2020-', '') for ti in tc]
    ########
#    plt.setp(plt.gca(), xticklabels=tc2)
#    pl.xticks(rotation=90)

