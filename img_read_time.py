#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 21:25:42 2018

@author: sumi
"""


import os
import glob
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from urllib.request  import urlopen
import cv2
import PIL
from matplotlib import pyplot as plt   
from PIL import Image
import requests
import io
from io import BytesIO
from urllib.parse import urlparse
from bs4 import BeautifulSoup, SoupStrainer
import requests
import datetime
from itertools import chain
import math



#this method will take start date, end date and url, return url with date
date1 = '2017-01-01 00:00:00'
date2 = '2017-12-31 23:59:00'
url = "https://sdo.gsfc.nasa.gov/assets/img/browse/"
wavelength = '0193'
resolution = '512'
#timespan = 20

#angle = 15

start_date = datetime.datetime.strptime(date1, '%Y-%m-%d %X')
#start_date = start_date.strftime('%Y/%m/%d')
end_date = datetime.datetime.strptime(date2, '%Y-%m-%d %X')
step = datetime.timedelta(days = 1)
#step = datetime.timedelta(minutes = 15)
url_dates=[]
while start_date <= end_date:
    #date = start_date.date()
    ##print (start_date.date())
    dt = start_date.date()
    dt_f = dt.strftime('%Y/%m/%d')
    url_d = url + dt_f + '/'
    #url_dates.append(url_d)
    #start_date += step


# this method will take the url with date, return the url with date and image file name (with wavelength)

#urls_dates_images = []
#for i in range(len(url_dates)):
#    page = requests.get(url_dates[i])    
    page = requests.get(url_d) 
    data = page.text
    soup = BeautifulSoup(data)
    # get the image file name
    img_files=[]    # image files with all info like wavelength, resolution, time
    for link in soup.find_all('a'):
        img_file = link.get('href')
        img_files.append(img_file)
        
    img_files_wr = []        # image files with all info like wavelength, resolution   
    for k in range(5, len(img_files)):
        splitting = re.split(r'[_.?=;/]+',img_files[k])
        if (splitting[3] == wavelength and splitting[2] == resolution):
            img_files_wr.append(img_files[k])

###       #select timespan        
    img_files_time = []     # image files with time
    for m in range(len(img_files_wr)):
    #for m in range(7, 8):
        #print(m)
        splitting = re.split(r'[_.?=;/]+',img_files_wr[m])
        #print('splitting', splitting)
        time_datetime = datetime.datetime.strptime(splitting[1], '%H%M%S').time()
        #print('time',time_datetime)
        
        start_date_hr = start_date + datetime.timedelta(hours = 1)    
        #print('start_date_hr',start_date_hr.time())
        while (start_date_hr.time() <= end_date.time()):  
            for sec in range(-366,367):
                start_date_range = start_date_hr + datetime.timedelta(seconds = sec)
                #print(start_date_range.time())
                if (time_datetime == start_date_range.time()):
                    img_files_time.append(img_files_wr[m])
                    #print('correct')
                    #print(start_date_hr.time())
                    start_date_hr += datetime.timedelta(hours = 1)
                    #print('after',start_date_hr.time()) 
                    break
            start_date_hr += datetime.timedelta(hours = 1)
            #print('up',start_date_hr.time())
           
            if dt != start_date_hr.date():
                #print('t')
                break 
    img_files_time.append(img_files_wr[len(img_files_wr)-1])
    start_date += step            
          
                       
    size = len(img_files_time)
    url_dates_imgs = []
    for j in range(size): #range(size)
        #url_ = url_dates[i] + img_files_time[j]
        url_ = url_d + img_files_time[j]
        url_dates_imgs.append(url_)
    #urls_dates_images.append(url_dates_imgs)
    url_dates.append(url_dates_imgs)

# converting a list of list to a list
#urls_dates_images = list(chain.from_iterable(urls_dates_images))  
urls_dates_images = list(chain.from_iterable(url_dates))      


# this method will take the url with date and image name, return the corresponding images 
img_all=[]
for i in range(len(urls_dates_images)):
#for i in range(5):
    response = requests.get(urls_dates_images[i])
    img = Image.open(BytesIO(response.content))
    img.save('/Users/sumi/python/research/solar_images_2017/'+str(i)+'.jpg')
    img = np.array(img) # img.shape: height x width x channel
    img = img/255        # scaling from [0,1]
    img = np.mean(img,axis=2) #take the mean of the R, G and B  
    img_all.append(img) 


######## to read .txt files   ################# 

path = '/Users/sumi/python/research/flux_2017/'

for filename in glob.glob(os.path.join(path, 'goes5min_2017_*.txt')):
    data1 = np.loadtxt(filename)
    #data1 =  np.loadtxt('/Users/sumi/python/research/goes5min_2017_12_31.txt')
    time_data1 = data1[:,3]
    short_data1 = data1[:,6]
    
    hour = 0
    flux = np.zeros(24)
    tot_short = short_data1[0]
            
    for i in range(1,data1.shape[0]):
    #for i in range(1, 13):
        
        if time_data1[i]%100 != 0:
            tot_short = tot_short + short_data1[i]
            #print("if",i, tot_short, short_data1[i])
        else:
            flux[hour] = tot_short/12
            hour += 1
            tot_short = short_data1[i]
            #print("else",i, tot_short, hour, flux[hour])
    flux[23] = tot_short/12
    #print(tot_short)
    
    os.chdir(path)
    file_name = str(data1[0][0].astype(int)) + '_' +  str(data1[0][1].astype(int)) + '_' + str(data1[0][2].astype(int))
    np.savetxt(file_name+'.txt', flux)

        
        
        #************************************#















 
