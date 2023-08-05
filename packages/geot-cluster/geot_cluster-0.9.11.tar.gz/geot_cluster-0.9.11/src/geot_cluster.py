#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy  as np
import markov_clustering as mc
import matplotlib.pyplot as plt
import math
import pytz
import folium
import os.path
import networkx as nx


from haversine       import haversine, Unit
from collections     import Counter
from datetime        import datetime
from timezonefinder  import TimezoneFinder
from IPython.display import clear_output


def dist_km(lat_1, lon_1, lat_2, lon_2):
    """
    Finds distance in kilometers between two coordinates
    
    :type lat_1: numeric
    :param lat_1: latitude of the 1 coordinate 
    
    :type lon_1: numeric
    :param lon_1: lontitude of the 1 coordinate 
    
    :type lat_2: numeric
    :param lat_2: latitude of the 2 coordinate
    
    :type lon_2: numeric
    :param lon_2: lontitude of the 2 coordinate 
    """
    var_1 = (lat_1, lon_1)
    var_2 = (lat_2, lon_2)
    return haversine(var_1, var_2, Unit.KILOMETERS)


def color_change(prob):
    """
    Is a utility function used for color change of the circle drawn on the map 
    
    :type prob: numeric
    :param prob: probability assigned to a circle
    """
    if(prob > 0.66):
        return('red')
    elif(0.33 <= prob <0.66):
        return('yellow')
    else:
        return('green')
    
   
def data_load(path):
    """
    Loads data of the specified type to work with
    
    :type path: string
    :param path: full path to the file with data
    """
    data = pd.read_csv(path).dropna()
    data = data.drop("Unnamed: 0", axis=1)
    Time = []
    Date = []
    for i in data['event_time']:
        date,time = i.split(' ')
        time = time.split('.')[0]
        Time.append(time)
        Date.append(date)
    data['Date'] = Date
    data['Time'] = Time
    data = data.sort_values(by = ['user_id','Date', 'Time'])
    data = data.reset_index().drop('index', axis=1)
    data = data.drop('event_time', axis=1)
    data.rename(columns={'latitude':'lat', 'longitude':'lon'}, inplace = True)
    data.drop('event_dt', axis=1, inplace=True)

    names = list(set(data['user_id']))
    
    return data, names

def skip(x,n):
    """
    Reduces precision of the numeric value
    
    :type x: floating point value
    :param x: number to reduce precision
    
    :type n: int
    :param n: number of values after dot

    """
    return int(x*(10**n))/10**n


def sigmoid_dt_(x,y, k = 4.5584, beta = 7.0910, step_osn = 2.0762, h_b=0.95, l_b=0.85):
    """
    Function for aging introduction, computation of alpha
    
    :type x: string
    :param x: date and time in the form "%H:%M:%S %Y-%m-%d"
    
    :type y: string
    :param y: date and time in the form "%H:%M:%S %Y-%m-%d"
    
    :type k: numeric
    :param k: base of the logarithm
    
    :type beta: numeric
    :param beta: beta from the formula
    
    :type step_osn: numeric
    :param step_osn: change of e in the sigmoid function
    
    :type h_b: numeric
    :param h_b: top bound of the result
    
    :type l_b: numeric
    :param l_b: low bound of the result
    """
    dist = minutes_between_high(y,x)
    res = 1 - 1.0/(1+step_osn**(-(math.log(dist+k)/math.log(k)-beta)))
    if(res>=h_b):
        return h_b
    if(res<=l_b):
        return l_b
    return res

def sigmoid_dt(x,y, k = 3.3, beta = 5.6):
    """
    Function for aging introduction, computation of alpha
    
    :type x: string
    :param x: date and time in the form "%H:%M:%S %Y-%m-%d"
    
    :type y: string
    :param y: date and time in the form "%H:%M:%S %Y-%m-%d"
    
    :type k: numeric
    :param k: base of the logarithm
    
    :type beta: numeric
    :param beta: beta from the formula
    """
    k = k
    b = beta
    dist = minutes_between_high(y,x)
    res = 1-1.0/(1+math.exp(-(math.log(dist+k,k)-b)))
    if(res>=0.95):
        return 0.95
    if(res<=0.5):
        return 0.5
    return res



def minutes_between_high(d1, d2):
    """
    Minutes beteen two dates
    
    :type d1: string
    :param d1: date and time in the form "%H:%M:%S %Y-%m-%d"
    
    :type d2: string
    :param d2: date and time in the form "%H:%M:%S %Y-%m-%d"
    
    """
    d1 = datetime.strptime(d1, "%H:%M:%S %Y-%m-%d")
    d2 = datetime.strptime(d2, "%H:%M:%S %Y-%m-%d")
    dif = abs(d2-d1)
    return (dif.days*24*60+dif.seconds//60)




def time_difference(lat,lon,param = 'utc'):
    """
    Time delta between timezone defined by lat and lot and param
    
    :type lat: numeric
    :param lat: latitude of the coordinate 
    
    :type lon: numeric
    :param lon: lontitude of the coordinate
    
    :type param: string
    :param param: name of the timezone
    """
    
    tf       = TimezoneFinder()
    try:
        tzz      = tf.timezone_at(lng=lon, lat=lat)
        timezone = pytz.timezone(tzz)
        dt       = datetime.now()
        utc_diff = timezone.utcoffset(dt)
    except BaseException:
        utc_diff = timedelta(seconds=10800)
    
    if(param=='utc'):
        return utc_diff
    elif(param=='msc'):
        msc_delta = timedelta(seconds=10800)
        return (utc_diff-msc_delta)
    

def dataFrame_localization(data, param='msc'):
    """
    Converting of date and time to local time from timezone specified by param
    
    :type data: pandas DataFrame
    :param data: data loaded with data_load function
    
    :type param: string
    :param param: name of the timezone in which all the data is given
    
    """
    
    i=0
    for lat,lon,time,date in zip(data['lat'], data['lon'], data['Time'], data['Date']):
        
        dt = datetime.strptime(time+' '+date, "%H:%M:%S %Y-%m-%d")
        dt+= time_difference(lat,lon, param=param)
        data.loc[i,'Time'], data.loc[i,'Date'] = str(dt.time()), str(dt.date())
        i+=1


def selection_2(person):
    """
    Adding part of the day and day of the week columns to the Series
    
    :type person: pandas Series
    :param person: slice from the dataframe with selected index
    
    """
    
    noch = [datetime.strptime("00:00:00", "%H:%M:%S"),datetime.strptime("04:00:00", "%H:%M:%S")]
    utro = [datetime.strptime("04:00:00", "%H:%M:%S"),datetime.strptime("09:00:00", "%H:%M:%S")]
    den  = [datetime.strptime("09:00:00", "%H:%M:%S"),datetime.strptime("17:00:00", "%H:%M:%S")]
    vecher_1 = [datetime.strptime("17:00:00", "%H:%M:%S"),datetime.strptime("20:30:00", "%H:%M:%S")]
    vecher_2 = [datetime.strptime("20:30:00", "%H:%M:%S"),datetime.strptime("00:00:00", "%H:%M:%S")]
    
    person = person.groupby(['Date', 'Time']).apply(pd.DataFrame.reset_index)
    person = person.iloc[:,[1,2,3,4,5]].reset_index(drop=True)
    lol = pd.to_datetime(person['Date']).dt.dayofweek
    oh = []
    for i in range(len(person)):
        tmp = datetime.strptime(person.loc[i]['Time'], "%H:%M:%S")
        if(noch[0]<=tmp<=noch[1]):
            oh.append(0)
        elif(utro[0]<=tmp<=utro[1]):
            oh.append(1)
        elif(den[0]<=tmp<=den[1]):
            oh.append(2)
        elif(vecher_1[0]<=tmp<=vecher_1[1]):
            oh.append(3)
        else:
            oh.append(4)
    person['Part_day'] = pd.Series(oh)
    person['Day_week'] = pd.to_datetime(person['Date']).dt.dayofweek
    return person




def l1_norm(x1,y1,x2,y2):
    """
    L1 norm in R2 space
    
    :type x1: numeric
    :param x1: first coordinate
    
    :type y1: numeric
    :param y1: first coordinate
    
    :type x2: numeric
    :param x2: first coordinate
    :type y2: numeric
    :param y2: first coordinate
    
    """
    return abs(x1-x2)+abs(y1-y2)



def l2_norm(x1,y1,x2,y2): 
    """
    L2 norm in R2 space
    
    :type x1: numeric
    :param x1: first coordinate
    
    :type y1: numeric
    :param y1: first coordinate
    
    :type x2: numeric
    :param x2: first coordinate
    :type y2: numeric
    :param y2: first coordinate
    
    """
    return dist_km(x1,y1,x2,y2)



def check_incl(s,x,y, val, norm = l1_norm, use_norm=True):
    """
    Checks wheather coordinate (x,y) is in circle with center s and radius val
    
    :type s: string
    :param s: coordinate of center of the circle
    
    :type x: numeric
    :param x: latitude to check
    
    :type y: numeric
    :param y: lontitude to check
    
    :type val: numeric
    :param val: radius of the circle
    
    :type norm: function
    :param norm: specified norm to measure distance between s and (x,y)
    
    :type use_norm: boolean
    :param use_norm: wheather to use norm or to measure distance in naturaly implied way with degrees
    """
    
    keki = s.split(' ')
    o = float(keki[0])
    h = float(keki[1])
    if(not use_norm):
        if((abs(o-x)<val) and (abs(h-y))<val*2):
            return True
        else:
            return False
    if(norm(o,h,x,y)<val):
        return True
    else:
        return False

def check_incl2(s,S, val, norm = l2_norm, use_norm=True):
    """
    Checks wheather coordinate (x,y) is in circle with center s and radius val
    
    :type s: string
    :param s: coordinate of center of the circle
    
    :type S: string
    :param S: coordinate in the string format
    
    :type val: numeric
    :param val: radius of the circle
    
    :type norm: function
    :param norm: specified norm to measure distance between s and (x,y)
    
    :type use_norm: boolean
    :param use_norm: wheather to use norm or to measure distance in naturaly implied way with degrees
    """
    
    
    keki = s.split(' ')
    o = float(keki[0])
    h = float(keki[1])
    keki2 = S.split(' ')
    x = float(keki2[0])
    y = float(keki2[1])
    if(not use_norm):
        if((abs(o-x)<val) and (abs(h-y))<val*2):
            return True
        else:
            return False
    if(norm(o,h,x,y)<val):
        return True
    else:
        return False

    
    

def re_count(s,x,y,mas,l1,l2, val, norm = l1_norm):
    """
    Recount of the circle center, based on the coordinates of the circles below
    
    :type s: string
    :param s: coordinate of center of the circle
    
    :type x: numeric
    :param x: latitude of the new transaction
    
    :type y: numeric
    :param y: lontitude of the new transaction
    
    :type mas: numeric array
    :param mas: array with centers of circles for the current map
    
    :type l1: int
    :param l1: number of the layer below
    
    :type l2: int
    :param l2: number of the layer below l1 (can be anything)
    
    :type val: numeric
    :param val: radius of the circle
    
    :type norm: function
    :param norm: norm function
    
    """
    
    l2 = l1+1
    s2 = s.split(' ')
    laats = []
    loons = []
    w1 = float(s2[0])
    w2 = float(s2[1])
    if(l1==(len(mas)-1)):
        w1 = str((w1+x)/2)
        w2 = str((w2+y)/2)
        return w1+' '+w2
    for op in range(len(mas[l2])):
        s2 = mas[l2][op].split(' ')
        if(norm(w1,w2,float(s2[0]), float(s2[1]))<val):
            laats.append(float(s2[0]))
            loons.append(float(s2[1]))
            
    w1 = str((sum(laats)+x)/(len(laats)+1))
    w2 = str((sum(loons)+y)/(len(loons)+1))
    return(w1+' '+w2)



def otbor_ver2(num, level, massive, mas):
    
    """
    Selection of circles with highest probabilities from the level
    
    :type num: int
    :param num: number of circles to select
    
    :type level: int
    :param level: circle level on which to select
    
    :type massive: numeric array
    :param massive: array with circle coordinates
    
    :type mas: numeric array
    :param mas: array with probabilities of circles
    
    """
    
    tmp_ver = np.array([-1.0]*num)
    tmp_idx = np.array([0]*num)
    for i in range(len(mas[level])):
        kek = mas[level][i]
        for j in range(num):
            if tmp_ver[j]<=kek:
                tmp_ver[j+1:]=tmp_ver[j:-1]
                tmp_idx[j+1:]=tmp_idx[j:-1]
                tmp_ver[j]=kek
                tmp_idx[j]=i
                break
    op = num
    for j in range(len(tmp_idx)):
        if(tmp_ver[-(j+1)]>-1):
            if(j==0):
                break
            op = num-j
            break
    coordinates = []
    probs = []
    for i in range(op):
        coordinates.append(massive[level][tmp_idx[i]])
        probs.append(mas[level][tmp_idx[i]])
    return coordinates, probs


def low_level_map(usr1,day, part_day,border=1):
    """
    Returns map for client for selected day of the week and part of the day with specified radius
    
    :type usr1: pandas Dataframe
    :param usr1: datframe slice with specified client
    
    :type day: int
    :param day: number corrensponing to the day of the week
    
    :type part_day: int
    :param part_day: number corrensponing to the part of the day
    
    :type border: numeric
    :param border: radius of the circle
    """
    
    
    border*=10 
    
    
    VALUE = 10.0
    NORM = l2_norm
    ss = usr1.loc[usr1['Day_week']==day]
    l = ss.shape[0]
        
    if(l>=2):                      
        sred_lat = ss['lat'].mean()
        sred_lon = ss['lon'].mean()
        su = 0.0
        for i,j in zip(ss['lat'], ss['lon']):
            su+=dist_km(i,j,sred_lat,sred_lon)
        border = su/l*100

    last_t=0
    tmp = (usr1.loc[(usr1['Part_day']==part_day) & (usr1['Day_week']==day)]).iloc[:,:-2]
    fl =True
    if(len(tmp!=0)):    
        gmassive = list(np.ndarray(shape=(1,1), dtype=object))
        gvalues = list(np.ndarray(shape=(1,1), dtype=float))
        gprobs = list(np.ndarray(shape=(1,1), dtype=float))
        for i in tmp.index:

            dt = ' '.join(tmp.loc[i,['Time','Date']].values)
            p  = tmp.loc[i,['lat','lon']].values

            if(fl):
                tok=True
                fl=False
            else:
                tok=False
            last_t, gmassive, gvalues, gprobs = update_mg(p, dt, last_t, gmassive, gvalues, gprobs,border,norm=l2_norm, tok=tok)
                    
    else:
        gmassive, gvalues, gprobs =  cluster2(usr1, border=border)
            
    return gmassive, gvalues, gprobs

def archivate_maps(data, names, base = "/home/lars/kek/",level  = 1,levels = 4,border = 100):
    """
    Makes an archive of maps for all users in the base folder
    
    :type data: pandas DataFrame
    :param data: DataFrame with all the data
    
    :type names: string list
    :param names: list with clients indecies
    
    :type base: string
    :param base: path to the folder for maps
    
    :type level: int
    :param level: level on which to store vizualiztion
    
    :type levels: int
    :param levels: number of levels for maps
    
    :type border: numeric
    :param border: largest radius, each of the folowing will be 10 times less
    
    """
    
    
    num=0
    end=len(names)
    for i in names:
        num+=1
        clear_output(wait=True)
        print("Map archivation",str(num/end*100),"%")

        usr1 = data[data['user_id']==i]
        usr1 = usr1.reset_index(drop=True)

        if(not usr1.isnull().values.any()):
            dataFrame_localization(usr1)
            usr1 = selection_2(usr1)
            _,massive, values, probs = cluster(data,i,level,levels=levels, border = border, aging=False,re_c=False)
            gm1,gv1,gp1 = global_map(usr1,border = border*(10**(-(levels-2))), 
                                     aging=False, sq=True, re_c=False)


            np.savez(base+i, massive, values, probs)

            for j in range(len(gm1)):
                np.savez(base+i+"g"+str(j),gm1[j],gv1[j],gp1[j])

        else:
            print("lol",i)
    

def load_maps(uid, base="/home/lars/kek/"):
    """
    Loads maps for the specified user id
    
    :type uid: string
    :param uid: user id
    
    :type base: string
    :param base: path to the folder with archivated maps
    """
    
    
    if(not path_check(uid, base=base)):
        return 0,0,0,0,0,0
    
    f = np.load(base+uid+".npz",allow_pickle = True)
    m,v,p = f['arr_0'],f['arr_1'],f['arr_2']
    
    gm, gv, gp = [],[],[]
    
    for j in range(35):
        f = np.load(base+uid+"g"+str(j)+".npz",allow_pickle = True)
        gm.append(f['arr_0'])
        gv.append(f['arr_1'])
        gp.append(f['arr_2'])
    
    return m,v,p,gm,gv,gp

def convert(m, l1=0.05,l2=0.10,l3=0.2):
    """
    Normalizing probabilities
    
    :type m: numeric list
    :param m: list with counted probabilities
    
    :type l1: numeric
    :param l1: normalizing value
    
    :type l2: numeric
    :param l2: normalizing value
    
    :type l3: numeric
    :param l3: normalizing value
    """
    assert l1+l2+l3<1
    assert l1<=l2 and l2<=l3
    
    print(m)
    
    return m[0]*l1+m[1]*l2+m[2]*l3, 1.0-l1-l2-l3


def convert_2(m, l1=0.15,l2=0.2):
    """
    Normalizing probabilities
    
    :type m: numeric list
    :param m: list with counted probabilities
    
    :type l1: numeric
    :param l1: normalizing value
    
    :type l2: numeric
    :param l2: normalizing value
    """
    
    assert l1+l2<1
    assert l1<=l2
    
    return m[0]*l1+m[1]*l2, 1.0-l1-l2


    
def znak(m1,p1, m2, p2,ran = [100,10,1,0.1], sq=True):
    """
    Probability of knowing each other for two clients
    
    :type m1: numeric list
    :param m1: list circles for client one
    
    :type p1: numeric list
    :param p1: list probabilities of circles for client one
    
    :type m2: numeric list
    :param m2: list circles for client two
    
    :type p2: numeric list
    :param p2: list probabilities of circles for client one
    
    :type ran: numeric list
    :param ran: list with radiuses specified for each circle
    
    :type sq: boolean
    :param sq: use square root during calculation
    
    """
    
    
    probs = []
    for i in range(len(m2)-1):
        p=0.0                                       
        for j in range(len(m1[i])):                  
            su=0.0                                   
            for z in range(len(m2[i+1])):           
                if(check_incl2(m1[i][j],m2[i+1][z],ran[i])):
                    su+=p2[i+1][z]
            if(sq):
                p+= np.sqrt(p1[i][j]*su)
            else:
                p+= p1[i][j]*su
        probs.append(p)
    if(len(m1)==3):
        return convert_2(probs)
    elif(len(m1)==4):
        return convert(probs)
    



def low_level_znakomstvo(usr1, usr2, pogr=100, local=True, aging=True, sq=True, re_c=True,
                        low_level_border =10, pairs=5):
    
    """
    Low level probability of knowing each other
    
    :type usr1: DataFrame
    :param usr1: DataFrame for client 1
    
    :type usr2: DataFrame
    :param usr2: DataFrame for client 2
    
    :type pogr: numeric
    :param pogr: special number to calculate when circle centers are the same
    
    :type local: boolean
    :param local: localize data or not
    
    :type aging: boolean
    :param aging: enable aging or not
    
    :type sq: boolean
    :param: use sqrt during calculation
    
    :type re_c: boolean
    :param re_c: recount centers of the circles or not
    
    :type low_level_border: numeric
    :param low_level_border: radius of circle
    
    :type pairs: int
    :param pairs: number of pairs of circles to select
    """
    
    if(local):
        
        dataFrame_localization(usr1)
        dataFrame_localization(usr2)
    
    usr1 = selection_2(usr1)
    usr2 = selection_2(usr2)
    
    
    
    dist = pd.DataFrame(columns=['idx','dist'])
    
    gm1,gv1,gp1 = global_map(usr1,border = low_level_border, aging=aging, sq=sq, re_c=re_c)
    gm2,gv2,gp2 = global_map(usr2,border = low_level_border, aging=aging, sq=sq, re_c=re_c)
    
    op=0
    
    for m1, m2, p1, p2 in zip(gm1, gm2, gp1, gp2):
        lats1 = np.array([])
        lons1 = np.array([])
        
        lats2 = np.array([])
        lons2 = np.array([])
        
        for i in m1[-2]:
            s1 = i.split(' ')
            lats1 = np.append(lats1,float(s1[0]))
            
            lons1 = np.append(lons1, float(s1[1]))
        
        
        for j in m2[-2]:
            s2 = j.split(' ')
            lats2 = np.append(lats2,float(s2[0]))
            lons2 = np.append(lons2, float(s2[1]))
            
        clt_1, cln_1 = np.dot(lats1,p1[-2]),np.dot(lons1,p1[-2])
        clt_2, cln_2 = np.dot(lats2,p2[-2]),np.dot(lons2,p2[-2])
        
        dist = dist.append({'idx':op,'dist':dist_km(clt_1,cln_1,clt_2, cln_2)}, ignore_index=True)
        op+=1
    dist = dist.sort_values(by='dist', ascending=False).reset_index(drop=True)
    idx = dist.loc[:pairs-1,'idx']
    
    total=0.0
    prob = 0.0
    
    for i in idx:
        
        coords1, p1  = otbor_ver2(4,-1,gm1[int(i)],gp1[int(i)])
        coords2, p2  = otbor_ver2(4,-1,gm2[int(i)],gp2[int(i)])
        
        lats1 = np.array([])
        lons1 = np.array([])
        
        lats2 = np.array([])
        lons2 = np.array([])
        
        for S1 in coords1:
            s1 = S1.split(' ')
            lats1 = np.append(lats1,float(s1[0]))
            
            lons1 = np.append(lons1,float(s1[1]))
            
        for S2 in coords2:
            s2 = S2.split(' ')
            lats2 = np.append(lats2,float(s2[0]))
            
            lons2 = np.append(lons2,float(s2[1]))
        
        pogr = 100
        
        for lt1, ln1,pr1 in zip(lats1, lons1, p1):
            k=0
            prob=0.0
            for lt2, ln2,pr2 in zip(lats2, lons2, p2):
            
                rng = l2_norm(lt1, ln1, lt2, ln2)
                k+=1
                if(rng<1):
                    if(rng<0.1):
                        prob+=np.sqrt(pr1*pr2)
                    else:
                        prob += np.sqrt(pr1*pr2)/(1.1)
                else:
                    prob += np.sqrt(pr1*pr2)/rng
            total += prob
    
    return total*1.0/len(idx)



def znakomstvo(data, uid1, uid2, low_level_border = 10,aging=True, sq=True, re_c=True, pairs=5, 
               debug = False, levels=4, border=100):
    
    """
    Union of low level and high level calculation of probabilities of knowing each other

    
    
    :type data: DataFrame
    :param data: DataFrame with all the data
    
    :type uid1: string
    :param uid1: id of the client 1
    
     :type uid2: string
    :param uid2: id of the client 1
    
    :type local: boolean
    :param local: localize data or not
    
    :type aging: boolean
    :param aging: enable aging or not
    
    :type sq: boolean
    :param: use sqrt during calculation
    
    :type re_c: boolean
    :param re_c: recount centers of the circles or not
    
    :type low_level_border: numeric
    :param low_level_border: radius of circle
    
    :type pairs: int
    :param pairs: number of pairs of circles to select
    
    :type levels: numeric
    :param levels: number of levels for maps making
    
    :type border: numeric
    :param border: radius of the biggest circle
    """
    
    
    ran = [100,10,1,0.1] 
    map1, m1, v1, p1 = cluster(data,uid1,level=0,levels=levels, border = border, aging=aging, re_c=re_c)
    map1, m2, v2, p2 = cluster(data,uid2,level=0,levels=levels, border = border, aging=aging, re_c=re_c)
    
    p1, l4 = znak(m1,p1,m2,p2, sq=sq)
    p1 = min(p1,1-l4)
    if(debug):
        print("p1", p1)
    
    usr1 = data.loc[data['user_id']==uid1]
    usr1 = usr1.groupby(['Date', 'Time']).apply(pd.DataFrame.reset_index)
    usr1 = usr1.iloc[:,[1,2,3,4,5]].reset_index(drop=True)


    usr2 = data.loc[data['user_id']==uid2]
    usr2 = usr2.groupby(['Date', 'Time']).apply(pd.DataFrame.reset_index)
    usr2 = usr2.iloc[:,[1,2,3,4,5]].reset_index(drop=True)

    p2 = min(l4*low_level_znakomstvo(usr1, usr2, local=False, low_level_border = low_level_border,
                                 aging=aging, sq=sq, re_c=re_c, pairs=pairs), l4)
    if(debug):
        print("p2", p2)
    return round((p1+p2),2)

def check_znak(m1,p1,m2,p2, treshold = 100):
    """
    Checks wheather we should check for people to know each other
    
    :type m1: numeric list
    :param m1: list with all circles for client 1
    
    :type p1: numeric list
    :param p1: list with probabilities of circles for client 1
    
    :type m2: numeric list
    :param m2: list with all circles for client 2
    
    :type p2: numeric list
    :param p2: list with probabilities of circles for client 2
    
    :type treshold: numeric
    :param treshold: critical distance between two centers of mass of two clients
    
    """
    lats1 = np.array([])
    lons1 = np.array([])
        
    lats2 = np.array([])
    lons2 = np.array([])
        
    for i in m1[-2]:
        s1 = i.split(' ')
        lats1 = np.append(lats1,float(s1[0]))
            
        lons1 = np.append(lons1, float(s1[1]))
        
        
    for j in m2[-2]:
        s2 = j.split(' ')
        lats2 = np.append(lats2,float(s2[0]))
        lons2 = np.append(lons2, float(s2[1]))
            
    clt_1, cln_1 = np.dot(lats1,p1[-2]),np.dot(lons1,p1[-2])
    clt_2, cln_2 = np.dot(lats2,p2[-2]),np.dot(lons2,p2[-2])
    
    if(dist_km(clt_1, cln_1, clt_2, cln_2)<treshold):
        return True
    return False

def graph_preparation(data, names, base):
    """
    Forming library of people knowing each other
    
    :type data: pandas dataframe
    :param data: data with all records for clients
    
    :type names: string list
    ;param names: list with ids
    
    :type base: string 
    :param base: path to folder with maps
    
    """
    names_pairs = [(i, j) for i in names for j in names if i<j]
    
    f = np.load("/home/lars/kek/"+names_pairs[0][0]+".npz",allow_pickle = True)
    
    last_u = names_pairs[0][0]
    
    library_znakomstv = {}
    
    u1m = f['arr_0']
    u1p = f['arr_2']
    
    tmp_mas = []
    
    num = 1.0
    end = len(names_pairs)
    
    for i in names_pairs:
        
        
        if(num%20000==0):
            clear_output(wait=True)
            print("Graph preparation",str(num/end*100),"%")
        
        num+=1
        u1, u2 = i[0], i[1]
        if(path_check(u1) and path_check(u2)):
            
            if(u1 != last_u):
                
                if(len(tmp_mas)>0):
                    library_znakomstv[last_u] = set(tmp_mas)
                tmp_mas = []
                
                f = np.load("/home/lars/kek/"+u1+".npz",allow_pickle = True)
                last_u = u1
                u1m = f['arr_0']
                u1p = f['arr_2']
                
            f = np.load("/home/lars/kek/"+u2+".npz",allow_pickle = True)
            u2m = f['arr_0']
            u2p = f['arr_2']
            
            if(check_znak(u1m,u1p,u2m,u2p)):
                tmp_mas.append(u2)
                
    return library_znakomstv

def graph_forming(lib, prob_lib, treshold=0.1):
    """
    Forming of graph
    
    :type lib: 
    :param lib:
    
    :type prob_lib:
    :param prob_lib:
    
    :type treshold: numeric
    :param treshold: treshold to set probability of zero 
    """
    
    list_lib_values = list(lib.values())
    
    total = []
    for i in list_lib_values:
        for j in i:
            total.append(j)
    total = set(total)
    keys = prob_lib.keys()
    
    c = set(total | set(list(keys)))
    c = sorted(list(c))
    
    graph = np.zeros(shape=(len(c),len(c)), dtype=float)
    
    for i in range(len(c)):
        key = c[i]
        if(key not in keys):
            continue
        for j in range(i+1, len(c)):
            value = c[j]
            if(value not in lib[key]):
                continue
            vals = list(lib[key])
            p = prob_lib[key][vals.index(value)]
            if(p>treshold):
                graph[i,j] = p
    graph = graph.T+graph
    
    return graph

def low_level_znakomstvo_lib(gm1,gp1,gm2,gp2, pairs=5):
    """
    Low level probability calculation from library
    
    :type gm1: numeric list
    :param gm1: massive with list of circles centers
    
    :type gp1: numeric list
    :param gp1: massive with list of probabilities of circles
    
    :type pairs: int
    :param pairs: number of pairs of circles to calculate probabilities
    
    """
    
    dist = pd.DataFrame(columns=['idx','dist'])
    op=0
    
    for m1, m2, p1, p2 in zip(gm1, gm2, gp1, gp2):
        lats1 = np.array([])
        lons1 = np.array([])
        
        lats2 = np.array([])
        lons2 = np.array([])
        
        for i in m1[-2]:
            s1 = i.split(' ')
            lats1 = np.append(lats1,float(s1[0]))
            
            lons1 = np.append(lons1, float(s1[1]))
        
        
        for j in m2[-2]:
            s2 = j.split(' ')
            lats2 = np.append(lats2,float(s2[0]))
            lons2 = np.append(lons2, float(s2[1]))
            
        clt_1, cln_1 = np.dot(lats1,p1[-2]),np.dot(lons1,p1[-2])
        clt_2, cln_2 = np.dot(lats2,p2[-2]),np.dot(lons2,p2[-2])
        
        dist = dist.append({'idx':op,'dist':dist_km(clt_1, cln_1,clt_2, cln_2)}, ignore_index=True)
        op+=1
    dist = dist.sort_values(by='dist', ascending=False).reset_index(drop=True)
    idx = dist.loc[:pairs-1,'idx']
    
    total=0.0
    prob = 0.0
    
    for i in idx:
        
        coords1, p1  = otbor_ver2(4,-1,gm1[int(i)],gp1[int(i)])
        coords2, p2  = otbor_ver2(4,-1,gm2[int(i)],gp2[int(i)])
        
        lats1 = np.array([])
        lons1 = np.array([])
        
        lats2 = np.array([])
        lons2 = np.array([])
        
        for S1 in coords1:
            s1 = S1.split(' ')
            lats1 = np.append(lats1,float(s1[0]))
            
            lons1 = np.append(lons1,float(s1[1]))
            
        for S2 in coords2:
            s2 = S2.split(' ')
            lats2 = np.append(lats2,float(s2[0]))
            
            lons2 = np.append(lons2,float(s2[1]))
        
        pogr = 100
        
        for lt1, ln1,pr1 in zip(lats1, lons1, p1):
            k=0
            prob=0.0
            for lt2, ln2,pr2 in zip(lats2, lons2, p2):
            
                rng = l2_norm(lt1, ln1, lt2, ln2)
                k+=1
                if(rng<1):
                    if(rng<0.1):
                        prob+=np.sqrt(pr1*pr2)
                    else:
                        prob += np.sqrt(pr1*pr2)/(1.1)
                else:
                    prob += np.sqrt(pr1*pr2)/rng
            total += prob
    
    return total*1.0/len(idx)

def znakomstvo_lib(data, uid1, uid2, base="/home/lars/kek/",low_level_border = 10,debug=False, aging=True, sq=True, re_c=True, pairs=5):
    """
    Union of low level and high level calculation of probabilities of knowing each other from libraries

    
    
    :type data: DataFrame
    :param data: DataFrame with all the data
    
    :type uid1: string
    :param uid1: id of the client 1
    
    :type uid2: string
    :param uid2: id of the client 1
    
    :type base: string
    :param base: path to folder with maps
    
    :type aging: boolean
    :param aging: enable aging or not
    
    :type sq: boolean
    :param: use sqrt during calculation
    
    :type re_c: boolean
    :param re_c: recount centers of the circles or not
    
    :type low_level_border: numeric
    :param low_level_border: radius of circle
    
    :type pairs: int
    :param pairs: number of pairs of circles to select

    """
    m1, _, p1, gm1, _, gp1 = load_maps(uid1,base=base) 
    m2, _, p2, gm2, _, gp2 = load_maps(uid2,base=base) 
    
    if(type(m1)==int or type(m2)==int):
        return 0
    
    p1, l4 = znak(m1,p1,m2,p2, sq=sq)
    p1 = min(p1,1-l4)
    
    if(debug):
        print("p1", p1)
    
    p2 = min(l4*low_level_znakomstvo_lib(gm1,gp1,gm2,gp2, pairs), l4)
    if(debug):
        print("p2", p2)
    return round((p1+p2),2)

def znakomstvo_by_lib(lib, data, aging=False, sq=True, re_c=False, pairs=5):
    """
    Calculating probabilities for people of knowing each other from pre-estimated library of meeting
    
    :type lib: dictionary
    :param lib: dictionary of pre-estimated people of knowing each other
    
    :type data: dataframe
    :param data: dataframe with all the records
    
    :type aging: boolean
    :param aging: enable aging or not
    
    :type sq: boolean
    :param: use sqrt during calculation
    
    :type re_c: boolean
    :param re_c: recount centers of the circles or not
    
    :type low_level_border: numeric
    :param low_level_border: radius of circle
    
    :type pairs: int
    :param pairs: number of pairs of circles to select
    
    """
    keys = list(lib.keys())
    
    prob_lib = {}
    
    num=1.0
    
    for k in keys:
        clear_output(wait=True)
        print("Znakomstvo by lib",str(num/len(keys)*100), "%")
        num+=1
        tmp = []
        for v in lib[k]:
            tmp.append(znakomstvo_lib(data, k, v, base="/home/lars/kek/",aging=aging, 
                                      sq=sq, re_c=re_c, pairs=pairs))
        prob_lib[k] = tmp[:]
        
        
    return prob_lib

def load_libs(base="/home/lars/kek"):
    """ Loading of libraries
    
    :type base: string
    :param base: path to folder with libraries
    
    
    """
    f = np.load(base+"/lib_keys"+".npz",allow_pickle = True)
    lib_keys = f['arr_0']
    f = np.load(base+"/lib_values"+".npz",allow_pickle = True)
    lib_values = f['arr_0']
    f = np.load(base+"/prob_lib_keys"+".npz",allow_pickle = True)
    prob_lib_keys = f['arr_0']
    f = np.load(base+"/prob_lib_values"+".npz",allow_pickle = True)
    prob_lib_values = f['arr_0']
    
    lib = {k:v for k,v in zip(lib_keys,lib_values)}
    prob_lib = {k:v for k,v in zip(prob_lib_keys,prob_lib_values)}
    
    return lib, prob_lib

def clusters_to_ids(lib, prob_lib, clusters, number):
    """
    Transformation of cluster to ids 
    
    :type lib: dataFrame
    :param lib:
    
    :type prob_lib:
    :param prob_lib:
    
    :type clusters: dictionary
    :param clusters: dictionary of clusters
    
    :type number: int
    :param number: number of cluster to convert ids
    
    """
    
    cluster1   = list(clusters[number])
    total = []
    for i in list(lib.values()):
        for j in i:
            total.append(j)
    total = set(total)
    
    keys = prob_lib.keys()

    c = set(total | set(list(keys)))
    
    dictionary = np.array(sorted(list(c)))
    
    return dictionary[cluster1]

def get_cluster_maps(data,clust, level = 2, levels = 3, border=100, aging=False, re_c=False):
    """
    Get maps for all clients in the specified cluster
    
    :type data: dataframe
    :param data: dataframe with all records
    
    :type clust: set
    :param clust: cluster with ids
    
    :type level: int
    :param level: level of map to visualize
    
    :type levels: int
    :param levels: levels to form maps
    
    :type border: numeric
    :param border: radius of the largest map
    
    :type aging: boolean
    :param aging: enable aging or not
    
    :type re_c: boolean
    :param re_c: recount centers of the circles or not
    
    """
    maps = []
    for i in clust:
        mapy, _, _, _ = cluster(data,i,level,levels=levels, border = border, aging=False, re_c=False)
        maps.append(mapy)
    return maps   


def update_mg(pay, time, last_t, m, v, p, value,norm=l1_norm, tok=False, aging=True, re_c=True):
    """
    Update of maps from new transaction
    
    :type pay: numeric array
    :param pay: [latitude, lontitude] of the new transaction
    
    :type time: string
    :param time: date and time of th transaction
    
    :type last_t: string
    :param last_t: date and time of the latest transaction
    
    :type m: string list
    :param m: list with centers of circles
    
    :type v: numeric list
    :param v: list with values, corresponding to already existing circles
    
    :type p: numeric list
    :param p: list with probabilities corresponding to the existing circles
    
    :type value: numeric
    :param value: value, corresponding to the transaction
    
    :type norm: function
    :param norm: distance function
    
    :type tok: boolean
    :param tok: first iteration flag
    
    :type aging: boolean
    :param aging: enable aging or not
    
    :type re_c: boolean
    :param re_c: recount centers of the circles or not
    
    """
    
    massive, values_massive, probs_massive = list(m), list(v), list(p)
    
    i=pay[0]
    j=pay[1]
    f=False
    
    if(tok):
        for o in range(len(massive)):
            massive[o][0]=' '.join([str(i),str(j)])
            values_massive[o][0]=10.0
            probs_massive[o][0]=1.0
            last_t=time
    else:
        if(aging):
            alpha = sigmoid_dt_(last_t,time)
        else:
            alpha=1
        last_t=time
        for o in range(len(massive)):
            idx = []
            la = i
            lo = j
            val = value*(0.1**(o))
            if(val==0):
                val=0.1
            gigy=0
            is_in=False
            for samp in massive[o]:
                if(check_incl(samp, la, lo, val, norm=norm)):
                    is_in=True
                    if(re_c):
                        massive[o][gigy]=re_count(s = samp,x = la, y = lo,mas = massive,val= val,l1=o,l2=o+1, norm=norm)
                    idx.append(gigy)
                gigy+=1
                
            if(not is_in):
                f=True
                for k in range(o,len(massive)):
                    massive[k] = np.append(massive[k],' '.join([str(i),str(j)]))
                    values_massive[k]*=alpha
                    values_massive[k] = np.append(values_massive[k], 10.0)
                    
                    probs_massive[k] = np.append(probs_massive[k], 0.0)
                
            else:
                values_massive[o]*alpha
                for z in idx:
                    pass
                    values_massive[o][z]+=10.0
                    
            if(f):
                probs_massive = update_pg(values_massive, probs_massive)
                break
    return last_t, np.array(massive), np.array(values_massive), np.array(probs_massive)


def  update_pg(mas_v,probs_massive):
    """
    Probabilities update after new transaction
    
    :type mas_v: numeric list
    :param mas_v: list with values of circles
    
    :type probs_massive: numeric list
    :param probs_massive: list with probabilities to update afer new transaction
    """
    
    for i in range(len(mas_v)):
        for j in range(len(mas_v[i])):
            probs_massive[i][j]=(mas_v[i][j]*1.0/sum(mas_v[i]))
    return probs_massive


def global_map(usr1, levels=2, border=100, re_c=True, aging=True, sq=True): 
    """
    Builds local maps< if no activity encountered dring the period it will be replaced by global map
    
    :type usr1: pandas DataFrame
    :param usr1: dataframe with data of the specified client
    
    :type levels: int
    :param levels: number of levels on the local map
    
    :type aging: boolean
    :param aging: enable aging or not
    
    :type sq: boolean
    :param: use sqrt during calculation
    
    :type re_c: boolean
    :param re_c: recount centers of the circles or not
    
    """
    
    gm,gl,gp = None, None, None
    glob = False
    
    gmassive = list(np.ndarray(shape=(35,levels,1), dtype=object))
    gvalues = list(np.ndarray(shape=(35,levels,1), dtype=float))
    gprobs = list(np.ndarray(shape=(35,levels,1), dtype=float))
    
    VALUE = 10.0
    NORM = l2_norm
    opp = 0
    
    for day in range(1,8):
        
        ss = usr1.loc[usr1['Day_week']==day]
        l = ss.shape[0]
            
        for part_day in range(5):
            
            last_t=0
            tmp = (usr1.loc[(usr1['Part_day']==part_day) & (usr1['Day_week']==day)]).iloc[:,:-2]
            fl =True
            
            if(len(tmp)!=0):
                for i in tmp.index:

                    dt = ' '.join(tmp.loc[i,['Time','Date']].values)
                    p  = tmp.loc[i,['lat','lon']].values

                    if(fl):
                        tok=True
                        fl=False
                    else:
                        tok=False
                    last_t, gmassive[opp], gvalues[opp], gprobs[opp] = update_mg(p, dt, last_t, gmassive[opp], 
                                                                                 gvalues[opp], 
                                                                                 gprobs[opp],
                                                                                 border,
                                                                                 norm=l2_norm, 
                                                                                 tok=tok,
                                                                                re_c=re_c, aging=aging)
            else:
                if(not glob):
                    glob=True
                    gm,gv,gp = cluster3(usr1,levels,border,re_c=re_c, aging=aging, sq=sq)
                gmassive[opp], gvalues[opp], gprobs[opp] = gm, gv, gp
                    
                
            opp+=1
            
    return gmassive, gvalues, gprobs


def cluster(data, uid, level, levels = 4, border = 100, aging=True, local=True, re_c=True):
    
    """
    Builds global mapfor the client with specified uid
    
    :type data: pandas dataFrame
    :param data: dataframe with all data
    
    :type uid: string
    :param uid: index of the client
    
    :type level: int
    :param level: number of level on which to visualize map
    
    :type levels: int
    :param levels: number of levels on the global map
    
    :type border: numeric
    :param border: radius of the largest circle
    
    :type aging: boolean
    :param aging: enable aging or not
    
    :type local: boolean
    :param local: to localize time or not
    
    :type re_c: boolean
    :param re_c: recount centers of the circles or not
    
    """
    
    usr1 = data.loc[data['user_id']==uid]
    usr1 = usr1.groupby(['Date', 'Time']).apply(pd.DataFrame.reset_index)
    usr1 = usr1.iloc[:,[1,2,3,4,5]].reset_index(drop=True)
    
    if(local):
        dataFrame_localization(usr1)
    
    last_t=0
    
    massive = np.ndarray(shape=(levels,1), dtype=object)
    values = np.ndarray(shape=(levels,1), dtype=float)
    probs = np.ndarray(shape=(levels,1), dtype=float)
    
    VALUE = 10.0
    BORDER_VALUE = border
    NORM = l2_norm
    
    for i in range(usr1.shape[0]):
                dt = ' '.join(usr1.loc[i,['Time','Date']].values)
                p  = usr1.loc[i,['lat','lon']].values
                if(i==0):
                    tok=True
                else:
                    tok=False
                last_t, massive, values, probs = update_mg(p, dt, last_t, massive, values, probs,
                                                              BORDER_VALUE,
                                                              norm=l2_norm,
                                                              tok=tok, aging=aging, re_c = re_c)


    lat = usr1['lat']
    lon = usr1['lon']

    VALUE = 10.0
    BORDER_VALUE*= 1000


    map3 = folium.Map(location=[lat.values[0],lon.values[0]], zoom_start = 12)

    level=level 
    if level>(levels-1) or level<0:
        level=(levels-1)
    t=level-levels
    val = BORDER_VALUE*(0.1**(level))

    s=1
    for i in zip(lat,lon):
        folium.Marker(location=i, 
                      radius = 10,
                      popup=usr1.loc[s-1,'Time']+' '+usr1.loc[s-1,'Date'],
                      icon=folium.Icon(color = 'green')).add_to(map3)
        s+=1
        
    idx = 0
    for i in massive[level]:
        ss = i.split(' ')
        la = float(ss[0])
        lo = float(ss[1])
        folium.vector_layers.Circle([la,lo], 
                                    val,
                                    popup=None,
                                    color=color_change(probs[t][idx]),
                                       opacity=probs[t][idx],
                                    fill_color=color_change(probs[t][idx]),
                                    fill_opacity=probs[t][idx]).add_to(map3)
        idx+=1
        
    map3.save("map3.html")
    return map3, massive, values, probs

def cluster2(usr1, border = 10, level=-1):
    """
    Builds global mapfor the client with specified client on the specified layer
    
    :type usr1: pandas dataFrame
    :param usr1: dataframe slice with client's data
    
    :type level: int
    :param level: number of level on which to build map
    
    :type border: numeric
    :param border: radius of the circle
    """
    
    

    massive = np.ndarray(shape=(1,1), dtype=object)
    values = np.ndarray(shape=(1,1), dtype=float)
    probs = np.ndarray(shape=(1,1), dtype=float)
    
    last_t=0.0
    VALUE = 10.0
    BORDER_VALUE = border*10
    NORM = l2_norm
    
    for i in range(usr1.shape[0]):
                dt = ' '.join(usr1.loc[i,['Time','Date']].values)
                p  = usr1.loc[i,['lat','lon']].values
                if(i==0):
                    tok=True
                else:
                    tok=False
                last_t, massive, values, probs = update_mg(p, dt, last_t, massive, values, probs,
                                                              BORDER_VALUE,
                                                              norm=l2_norm,
                                                              tok=tok)
   
    return massive[level], values[level], probs[level]

def cluster3(usr1, levels, border, re_c=True, aging=True, sq=True):
    """
    Builds global map for the client with specified client
    
    :type usr1: pandas dataFrame
    :param usr1: dataframe slice with client's data
    
    :type levels: int
    :param levels: number of levels on the map
    
    :type border: numeric
    :param border: radius of the largest circle
    
    :type aging: boolean
    :param aging: enable aging or not
    
    :type aging: boolean
    :param aging: to enable aging or not
    
    :type re_c: boolean
    :param re_c: recount centers of the circles or not
    
    """
    
    last_t=0

    massive = np.ndarray(shape=(levels,1), dtype=object)
    values = np.ndarray(shape=(levels,1), dtype=float)
    probs = np.ndarray(shape=(levels,1), dtype=float)
    
    VALUE = 10.0
    BORDER_VALUE = border
    NORM = l2_norm
    
    for i in range(usr1.shape[0]):
                dt = ' '.join(usr1.loc[i,['Time','Date']].values)
                p  = usr1.loc[i,['lat','lon']].values
                if(i==0):
                    tok=True
                else:
                    tok=False
                last_t, massive, values, probs = update_mg(p, dt, last_t, massive, values, probs,
                                                              BORDER_VALUE,
                                                              norm=l2_norm,
                                                              tok=tok,
                                                              re_c=re_c, aging=aging)

    return massive, values, probs


def low_level_transaction(lat,lon, mp, pbs, pogr=100):
    """
    low level check of validity of the transaction based on history
    
    :type lat: numeric
    :param lat: latitude of the transaction
    
    :type lon: numeric
    :param lon: lontitude of the transaction
    
    :type mp: string list
    :param mp: list with centers of circles of the selected level
    
    :type pbs: numeric list
    :param pbs: list with probabilities corresponding to the circles
    
    :type pogr: numeric
    :param pogr:value used to count probability
    
    """
    
    prob = 0.0
    for i,j in zip(mp,pbs):
        s = i.split(' ')
        lt,ln = float(s[0]),float(s[1])
        rng = l2_norm(lat, lon, lt, ln)
        
        if(rng<1):
            prob += j/np.log2(pogr)
        else:
            prob += j/rng
            
    print(prob)
            
    return prob

def transaction(data, lat,lon,time, date, uid, local=False):
    """
    Checks full legitimicy of the transaction
    
    :type data: pandas dataFrame
    :param data: dataFrame withall the data
    
    :type lat: numeric
    :param lat: latitude of the transaction
    
    :type lon: numeric
    :param lon: lontitude of the transaction
    
    :type time: string
    :param time: time of the transaction
    
    :type date: string
    :param date: date of the transaction
    
    :type uid: string
    :param uid: index of the client
    
    :type local: boolean
    :param local: wheather to localize user's history or not
    
    """
    levels = 4
    border = 10**(levels-1)
    
    usr1 = data.loc[data['user_id']==uid]
    usr1 = usr1.groupby(['Date', 'Time']).apply(pd.DataFrame.reset_index)
    usr1 = usr1.iloc[:,[1,2,3,4,5]].reset_index(drop=True)
    
    if(local):
        for i in range(usr1.shape[0]):
                usr1.loc[i,'Time'], usr1.loc[i,'Date']  = correction_time(usr1.loc[i,'lat'],
                                                                         usr1.loc[i,'lon'],
                                                                          usr1.loc[i,'Time']+' '+usr1.loc[i,"Date"])  
    usr1 = selection_2(usr1)
    gm, gv, gp = cluster3(usr1, levels, 100)
    
    print(gp)
    
    probs = np.ndarray(shape=(1,levels-1))
    coefs = np.array([0.1,0.2,0.3])
    
    for i in range(levels-1):
        for s,p in zip(gm[i],gp[i]):
            if(check_incl(s,lat,lon,border, l2_norm)):
                probs[0][i]+=p
                
    assert len(probs[0])==len(coefs)
    
    print("Probs",probs)
    
    p1 = np.dot(probs[0],coefs)
    
    tmp = datetime.strptime(time, "%H:%M:%S")
    
    if(noch[0]<=tmp<=noch[1]):
        oh=0
    elif(utro[0]<=tmp<=utro[1]):
        oh=1
    elif(den[0]<=tmp<=den[1]):
        oh=2
    elif(vecher_1[0]<=tmp<=vecher_1[1]):
        oh=3
    else:
        oh=4
        
    week_day = datetime.strptime(date, "%Y-%m-%d").weekday()
    m, v, p = low_level_map(usr1,week_day, oh,border=border*(10**(-levels)))
    
    l4 = 1.0-sum(coefs)
    
    print(m,p)
    p2=0
    if(type(m[0])==str):
        p2 = low_level_transaction(lat,lon,m,p)*l4
    else:
        p2 = low_level_transaction(lat,lon,m[0],p[0])*l4
    print(p1,p2)
    
    print('\n',"Легальность транзакции",(p1+p2)*100,"%")

