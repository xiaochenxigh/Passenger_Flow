#%%
'''
@author by xiaochenxi------------------
at datetime:20170811
'''

# !/usr/bin/env python-----------
# coding:utf-8-------------------

'''
target: opencv videocapture to get rtsp stream
param1: rtsp
return: video
'''
def get_video_rtsp(rtsp):
    '''
    excample:
        >>> rtsp="rtsp://192.168.1.168:80/0"
        >>> get_vedeo_rtsp(rtsp)
    '''
    import cv2
    capture=cv2.videocapture(filename)
    while(1):
        ret,frame=capture.read()
        if frame is None:
            break
        cv2.imshow('img',frame)
        if cv2.waitKey(1) == 27:
            break
    capture.release()
    cv2.destroyAllWindows()

'''
target: every frame step to 5
param1: rtsp
return: video
'''
def get_video_rtsp_5_f(rtsp):
    '''
    excample:
        >>> rtsp="rtsp://192.168.1.168:80/0"
        >>> get_video_rtsp_5_f(rtsp)
    '''
    import cv2
    capture=cv2.videocapture(filename)
    while(1):
        ret,frame=capture.read()
        if frame is None:
            break
        if frameNum%5 ==0:
			setframe=frame

        cv2.imshow('img',setframe)
        if cv2.waitKey(1) == 27:
            break
    capture.release()
    cv2.destroyAllWindows()


'''
target: split fontground with background 
param1: video
param2: model(knn/Mog/Mog2)
'''
def bg_substract(capture,model):
    import cv2
    fgbg_knn=cv2.createBackgroundSubtractorKNN()
    fgbg_mog2=cv2.createBackgroundSubtractorMOG2()
    fgbg_mog=cv2.bgsegm.createBackgroundSubtractorMOG()
    if model==0:
        fgbg=fgbg_knn
    elif model==1:
        fgbg=fgbg_mog
    else:
        fgbg=fgbg_mog2

    while(1):
        ret,frame = capture.read()
        imgrsz=cv2.resize(setframe, (0,0), fx=0.2,fy=0.2)
		fgmask=fgbg.apply(imgrsz)
        cv2.imshow('img', fgmask)
		if (cv2.waitKey(1) & 0xff) == 27:
			break
	capture.release()
	cv2.destroyAllWindows()

'''
target: read system time
param1:
return: time.format
'''
def read_sys_time():
    '''
    excample:
        >>> time_f=read_sys_time()
    '''
    import time
    now=int(time.time())
    timeArray=time.localtime(now)
    otherStyleTime=time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


"""
target: post message with http
param1: http
param2: data
return: state
"""
def post_http(http,data):
    '''
    excample:
        >>> http="http://192.168.1.248:9010/viso_collect/point"
        >>> post_http(http,data)
    '''
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=http, headers=headers, data=json.dumps(data))
    response = urllib2.urlopen(request)