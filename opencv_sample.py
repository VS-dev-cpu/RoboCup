import serial

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

cap = cv2.VideoCapture(0)
cap.set(3, W)
cap.set(4, H)
_, frame = cap.read()
rows, cols, _ = frame.shape

ballX = 0
ballY = 0
ballSize = 0
ballDist = 0

debugging = True

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

    ballX = W / 2
    ballY = H / 2
    ballSize = 0
    ballDist = 0

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        ballX = int((x + x + w) / 2)
        ballY = int((y + y + h) / 2)
        ballSize = int((w + h) / 2)
        ballDist = int(-ballSize + w)
        if (debugging):
          print(str(ballX) + ', ' + str(ballY) + ', ' + 
          str(ballSize) + ', ' + str(ballDist) + '\n')
        break

    if (init):
      ser.write(str(ballX) + ',' + str(ballY) + ',')
      ser.write(str(ballSize) + ',' + str(ballDist))
      ser.write(b'\n')
    
    if(debugging):
      cv2.line(frame, (ballX, 0), (ballX, W), (0, 255, 0), 2)
      cv2.line(frame, (ballY, 0), (ballY, H), (0, 255, 0), 2)
    
      cv2.imshow("Frame", frame)
      
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
