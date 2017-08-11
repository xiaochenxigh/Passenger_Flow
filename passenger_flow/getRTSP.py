

import numpy as np
import cv2
import json
import time
import urllib2

def post_to_http(http,centers,otherStyleTime):
    data={"getwayId":"192.168.1.168:80",
            "getwayType":"0",
            "deviceId":"1",
            "deviceType":"VIVE",
            "pointSets":centers,
            "createTime":otherStyleTime
        }
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=http, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)


def findcontours_x(fgmask,otherStyleTime):
    im2,contours,hecichy= cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 200: 
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        if w>10 and h>20:
            a=(x+w/2,y+h/2,otherStyleTime)
            return a

def findcontours_x_2(fgmask,otherStyleTime):
    im2,contours,hecichy= cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    xxxa=[]
    for c in contours:
        if cv2.contourArea(c) < 200: 
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        if w>10 and h>20:
            a=(x+w/2,y+h/2)
            ccc=(a,1)
            xxxa.append(a)
    if len(xxxa)>0:
        b=(xxxa,otherStyleTime)
        print b
        return b


#[([(473, 194)], '2017-07-21 15:25:56'), ([(438, 183)], '2017-07-21 15:25:57'), ([(411, 203)], '2017-07-21 15:25:58'), ([(456, 185)], '2017-07-21 15:25:58'), ([(494, 195)], '2017-07-21 15:25:59'), ([(496, 200)], '2017-07-21 15:26:00')]
def findcontours_x_1(fgmask,otherStyleTime):
    im2,contours,hecichy= cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    a=[]
    for c in contours:
        if cv2.contourArea(c) < 200: 
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        if w>5 and h>10:
            #a=(x+w/2,y+h/2,otherStyleTime)
            xxx1=(x+w/2,y+h/2)
            a.append(xxx1)

    if len(a)>0:
        return a
        #return b
'''        if w>5 and h>10:
            xx1=(x+w/2,y+h/2)
            a.append(xx1)
        if len(a)>0:
            t=(a,otherStyleTime)
            b.append(t)
    if len(b)>0: 
        return b
'''
#----
def bgSubstract(filename):
    capture=cv2.VideoCapture(filename)
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    http="http://192.168.1.248:9010/viso_collect/point"

    frameNum=0
    centers=[]
    ctflags=0
    xtime0=0

    while(1):
        if ctflags==0:
            centers=[]
            ctflags=1
        ret,frame=capture.read()
        if frame is None:
            break
        #----getframe/20--------------- 
        frameNum=frameNum+1
        if frameNum%20!=0:
            continue

        #----apply back ground substract---------------------
        imgrsz=cv2.resize(frame,(0,0),fx=0.3,fy=0.3)
        fgmask=fgbg.apply(imgrsz)
        
        #----get localtime------------
        now=int(time.time())
        timeArray=time.localtime(now)
        otherStyleTime=time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        
        aaa=findcontours_x_2(fgmask,otherStyleTime)
        if aaa is not None:
            centers.append(aaa)
        
        #----send to http------------------------
        #print timeArray,timeArray[4]
        Xtime1=timeArray[5]
        if len(centers)>0 and Xtime1%5==0 and Xtime1!=xtime0:
            print otherStyleTime,centers
            post_to_http(http,centers,otherStyleTime)
            xtime0=Xtime1
            ctflags=0
        #cv2.imshow('img', imgrsz)
        #if cv2.waitKey(1)==27:
        #    break
    capture.release()
    #cv2.destroyAllWindows()


rtsp='rtsp://192.168.1.168:80/0'
bgSubstract(rtsp)
