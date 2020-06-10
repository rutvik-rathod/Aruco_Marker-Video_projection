"""
Author:- Rutvik Manoj Rathod
"""
import cv2
import cv2.aruco as aruco
import numpy as np
import math
import time
import requests

#if you want to takein feed from web cam uncomment the below line
cap = cv2.VideoCapture(0)

#If use of IP_WEBCAM_SERVER comment ahe above line and uncomment the below line
#url = "http://[2401:4900:1977:ddd9::9]:8080/shot.jpg"

#These are all the parameters responsible for video wrting

#change the filename to video file location
filename = '//home//debz//Desktop//Work//Open CV learning//hello.mp4'
codec = cv2.VideoWriter_fourcc('X','V','I','D')
framerate = 25
resolution = (960,720)
VideoFileOutput = cv2.VideoWriter(filename,codec,framerate,resolution)

#Video file Read
video_address = '//home//debz//Desktop//video_project.mp4'
video = cv2.VideoCapture(video_address)


#while using the webcam uncomment the below line and comment the line below
while(cap.isOpened()):
    ret,image = cap.read()
    if not ret:
        break

    #if you are using IP_WEBCAM uncomment the while loop below and comment the above present while loop
    """while(True):
        img_req = requests.get(url)
        img_arr = np.array(bytearray(img_req.content),dtype = np.uint8)
        image = cv2.imdecode(img_arr,-1)
    """   
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)
    parameters = aruco.DetectorParameters_create()
    corners,ids,_=aruco.detectMarkers(image,aruco_dict,parameters=parameters)
    im_src = cv2.imread('//home//debz//Desktop//Work//Open CV learning//ss5.png')
       
    

    if np.all(ids != None):
        
        flag,im_src = video.read()
        if not flag:
            video = cv2.VideoCapture(video_address)
            flag,im_src = video.read()
        x1 = [corners[0][0][0][0],corners[0][0][0][1]]
        x2 = [corners[0][0][1][0],corners[0][0][1][1]]
        x3 = [corners[0][0][2][0],corners[0][0][2][1]]
        x4 = [corners[0][0][3][0],corners[0][0][3][1]]

        im_dst = image
        # im_src = cv2.imread('ss1.jpg')

        size = im_src.shape

        pts_dst = np.array([x1,x2,x3,x4])
        pts_src = np.array([[0,0],
                            [size[1]-1,0],
                            [size[1]-1,size[0]-1],
                            [0,size[0]-1]], dtype = float);

        h,status = cv2.findHomography(pts_src,pts_dst)
        temp = cv2.warpPerspective(im_src,h,(im_dst.shape[1],im_dst.shape[0]))
        cv2.fillConvexPoly(im_dst,pts_dst.astype(int),0,16);
        image = im_dst+temp        
    
    image = cv2.resize(image,(960,720))
    VideoFileOutput.write(image)
    cv2.imshow('frame',image)
    k = cv2.waitKey(10)
    if(k==27):
        VideoFileOutput.release()
        break