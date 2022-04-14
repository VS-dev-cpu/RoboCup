import serial
import time

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

ballX = 0
ballY = 0
ballSize = 0
ballDist = 0

debugging = True

ser.write(b'-1\n')
time.sleep(2)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 0)
    if (IMAGE_FLIP_HORIZONTALLY):
        frame = cv2.flip(frame, 1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    ballX = W / 2
    ballY = H / 2
    ballSize = 0
    ballDist = 0
    
    ball = False

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        ballX = int((x + x + w) / 2)
        ballY = int((y + y + h) / 2)
        ballSize = int((w + h) / 2)
        ballDist = int(-ballSize + w)
        ball = True
        if (debugging):
          print(str(ballX) + ', ' + str(ballY) + ', ' + 
          str(ballSize) + ', ' + str(ballDist) + '\n')
        break

    if (ball):
      if (ballX < (W/2 - W/2)):
        ser.write(b'2')
      elif (ballX > (W/2 + W/2)):
          ser.write(b'1')
      else:
          ser.write(b'3')
    else:
        ser.write(b'2')
    
    if(debugging):
      frame = cv2.line(frame, (int(ballX), 0), (int(ballX), int(H)*10), (0, 255, 0), 2)
      frame = cv2.line(frame, (0, int(ballY)), (int(W)*10, int(ballY)), (0, 255, 0), 2)
    
      cv2.imshow("Frame", frame)
      
    key = cv2.waitKey(1)
    ser.write(b'\n')
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
