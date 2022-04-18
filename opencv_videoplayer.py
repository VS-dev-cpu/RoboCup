import cv2
import numpy as np
import os

from datetime import datetime
import calendar

def get_unix():
    d = datetime.utcnow()
    return calendar.timegm(d.utctimetuple())

cap = cv2.VideoCapture("info.mp4")
current = ""
cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

def load(name):
    current = name
    cap = cv2.VideoCapture(str(name) + '.mp4')
    
def playsound(path):
    os.system("kill 2")
    os.system("mpg123 " +  str(path) + " &")
    
def play(name):
    load(name)
    playsound(str(name) + '.mp3')
    ret = True
    while(ret):
        ret, frame = cap.read()
        if ret == True:
          cv2.imshow('window', frame)

def playForTime(name, secs):
    start = get_unix()
    load(name)
    playsound(str(name) + '.mp3')
    ret = True
    while (ret):
        ret, frame = cap.read()
        if ret == True:
          cv2.imshow('window', frame)
        if (get_unix() - start >= secs):
            ret = False

playForTime("info", 226)

playForTime("sunrise", 19)

play(fractal)

playForTime("dance", 10)
    

cv2.destroyAllWindows()
