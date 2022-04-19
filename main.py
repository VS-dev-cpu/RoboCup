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

W = 320
H = 240

IMAGE_FLIP_VERTICALLY = True
IMAGE_FLIP_HORIZONTALLY = True
IMAGE_RESIZE = True

cap = cv2.VideoCapture(0)
if (IMAGE_RESIZE):
    cap.set(3, int(W))
    cap.set(4, int(H))
_, frame = cap.read()

# Flip the image
if (IMAGE_FLIP_VERTICALLY):
	frame = cv2.flip(frame, 0)
if (IMAGE_FLIP_HORIZONTALLY):
    frame = cv2.flip(frame, 1)
    
rows, cols, _ = frame.shape

#RED
low_acorn = np.array([161, 155, 84])
high_acorn = np.array([179, 255, 255])

W = cap.get(3)
H = cap.get(4)

acorn = False
acornX = 0
acornY = 0
acornSize = 0
acornDist = 0
gap = 2.5
minacornSize = 150

debugging = False

bt = bt.BT("basic")

#bt.sync()

ser.write(b'-1\n')
time.sleep(3)

#bt.sync()

while True:
	# Read image from the camera
    ret, frame = cap.read()
    
    if not ret:
    	print("ERROR: CAN NOT READ IMAGE FROM THE CAMERA")
    	exit()
    
    # Flip the image
    if (IMAGE_FLIP_VERTICALLY):
    	frame = cv2.flip(frame, 0)
    if (IMAGE_FLIP_HORIZONTALLY):
        frame = cv2.flip(frame, 1)
        
    #Create masks and find the objects
        
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    acorn_mask = cv2.inRange(hsv_frame, low_acorn, high_acorn)
    acorn_contours, _ = cv2.findContours(acorn_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    acorn_contours = sorted(acorn_contours, key=lambda x:cv2.contourArea(x), reverse=True)
   
    acornX = W / 2
    acornY = H / 2
    acornSize = 0
    acornDist = 0
    acorn = False
    
    for cnt in acorn_contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        acornX = int((x + x + w) / 2)
        acornY = int((y + y + h) / 2)
        acornSize = int((w + h) / 2)
        acornDist = int(-acornSize + w)
        acorn = True
        break
    
    # Move the robot
    
    if (acorn):
      wall = False
      if (acornX < (W/2 - W/gap)):
        ser.write(b'2')
      elif (acornX > (W/2 + W/gap)):
          ser.write(b'1')
      else:
          ser.write(b'3')
    else:
	ser.write(b'1')

    ser.write(b'\n')

    key = cv2.waitKey(1)
    
    # Exit, if needed
    
    if key == 27:
        break
    
    if (acorn and acornSize > minacornSize):
        break
    
ser.write(b'0\n')
bt.sync()
    
ser.write(b'-2\n')
time.sleep(5)
    
cap.release()
cv2.destroyAllWindows()
