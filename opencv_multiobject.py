import serial
import time
import bt

init = False
port = '/dev/ttyACM0'

try:
  ser = serial.Serial(port, 9600)
  init = True
except:
  pass

if (init == False):
  print("WARNING: No Arduino Detected At " + port)

import cv2
import numpy as np

W = 128
H = W/16*9

IMAGE_FLIP_HORIZONTALLY = True
IMAGE_RESIZE = True

cap = cv2.VideoCapture(0)
if (IMAGE_RESIZE):
    cap.set(3, W)
    cap.set(4, H)
_, frame = cap.read()
frame = cv2.flip(frame, 0)
if (IMAGE_FLIP_HORIZONTALLY):
    frame = cv2.flip(frame, 1)
rows, cols, _ = frame.shape

low_red = np.array([161, 155, 84])
high_red = np.array([179, 255, 255])

low_green = np.array([40, 50, 20])
high_green = np.array([60, 255, 255])

low_blue = np.array([90, 155, 20])
high_blue = np.array([150, 255, 255])

low_gray = np.array([0, 0, 50])
high_gray = np.array([180, 20, 150])

ballX = 0
ballY = 0

debugging = True

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 0)
    if (IMAGE_FLIP_HORIZONTALLY):
        frame = cv2.flip(frame, 1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    red_contours = sorted(red_contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    green_contours = sorted(green_contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    blue_contours = sorted(blue_contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    gray_mask = cv2.inRange(hsv_frame, low_gray, high_gray)
    gray_contours, _ = cv2.findContours(gray_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    gray_contours = sorted(gray_contours, key=lambda x:cv2.contourArea(x), reverse=True)

    redX = W / 2
    redY = H / 2
    
    greenX = W / 2
    greenY = H / 2
    
    blueX = W / 2
    blueY = H / 2
    
    grayX = W / 2
    grayY = H / 2
    
    for cnt in red_contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        redX = int((x + x + w) / 2)
        redY = int((y + y + h) / 2)
        break
    
    for cnt in green_contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        greenX = int((x + x + w) / 2)
        greenY = int((y + y + h) / 2)
        break
    
    for cnt in blue_contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        blueX = int((x + x + w) / 2)
        blueY = int((y + y + h) / 2)
        break
      
    for cnt in gray_contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        grayX = int((x + x + w) / 2)
        grayY = int((y + y + h) / 2)
        break

    if(debugging):
      frame = cv2.line(frame, (int(redX), 0), (int(redX), int(H)*10), (0, 0, 255), 2)
      frame = cv2.line(frame, (0, int(redY)), (int(W)*10, int(redY)), (0, 0, 255), 2)
      
      frame = cv2.line(frame, (int(greenX), 0), (int(greenX), int(H)*10), (0, 255, 0), 2)
      frame = cv2.line(frame, (0, int(greenY)), (int(W)*10, int(greenY)), (0, 255, 0), 2)
      
      frame = cv2.line(frame, (int(blueX), 0), (int(blueX), int(H)*10), (255, 0, 0), 2)
      frame = cv2.line(frame, (0, int(blueY)), (int(W)*10, int(blueY)), (255, 0, 0), 2)
          
      frame = cv2.line(frame, (int(grayX), 0), (int(grayX), int(H)*10), (100, 100, 100), 2)
      frame = cv2.line(frame, (0, int(grayY)), (int(W)*10, int(grayY)), (100, 100, 100), 2)
    
      cv2.imshow("Frame", frame)
      
    key = cv2.waitKey(1)
    ser.write(b'\n')
    
    if key == 27:
        break
    
bt.sync()
    
ser.write(b'-2\n')
time.sleep(5)
    
cap.release()
cv2.destroyAllWindows()
