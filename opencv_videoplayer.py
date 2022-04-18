import cv2
import numpy as np
import os

from datetime import datetime
import calendar

def get_unix():
    d = datetime.utcnow()
    return calendar.timegm(d.utctimetuple())

current = ""
cap = cv2.VideoCapture("")
cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

def load(name):
    current = name
    cap.release()
    cap = cv2.VideoCapture(str(name) + '.mkv')
    
def playsound(path):
    os.system("mpg123 " +  str(path) + " &")
      
def play():
    playsound(str(current) + '.mp3')
    ret = True
    while(ret):
        ret, frame = cap.read()
        if ret == True:
          cv2.imshow('window', frame)
        
def playForTime(secs):
    start = get_unix()
    playsound(str(current) + '.mp3')
    ret = True
    while (ret):
        ret, frame = cap.read()
        if ret == True:
          cv2.imshow('window', frame)
        if (get_unix() - start >= secs)
            ret = False
            
load("info")
playForTime(226)
    
load("sunrise")
playForTime(19)

load("searching")
play()

load("dance")
playForTime()
    

cv2.destroyAllWindows()
