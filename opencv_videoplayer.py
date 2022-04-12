import cv2
import numpy as np
from playsound import playsound

current = ""
cap = cv2.VideoCapture("")
cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

def load(name):
    current = name
    cap.release()
    cap = cv2.VideoCapture(str(name) + '.mkv')
    if (cap.isOpened()== False):
        cap = cv2.VideoCapture(str(name) + '_backup.mkv')
      
def play():
    playsound(str(current) + '.wav')
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
          cv2.imshow('window', frame)
    
load("sunrise")
play()

load("searching")
play()

load("dance")
play()
    

cv2.destroyAllWindows()
