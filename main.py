# from cubeline import OutText
# from utils import *
import pytesseract
import pyautogui
import time
import keyboard
import cv2
import numpy as np
from PIL import Image
import os
import winsound

# Constants
ER = 'exp Rate: +25%'
IED = 'ignores 50%'
IED_2 = 'igneres 50%'
OP = 'overpower: +50%'
ATT = 'att: +40%'
MATT = 'magic att: +40%'
path = 'in.png'
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

start = time.time()
count = 0
text = None

def detectColor(img):
    # imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # #cv2.imshow("hsv", imgHSV)
    # lower = np.array([0, 0, 0])
    # upper = np.array([255, 255, 255])
    # mask = cv2.inRange(imgHSV, lower, upper)
    # imgResult = cv2.bitwise_and(img, img, mask=mask)
    # # resize
    # imgResult = cv2.resize(imgResult, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # # grayscale:yy
    # imgResult = cv2.cvtColor(imgResult, cv2.COLOR_BGR2GRAY)
    height, width, channels = img.shape
    img = cv2.resize(img, ( width*3, height*3))
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## Gen lower mask (0-5) and upper mask (175-180) of RED
    mask1 = cv2.inRange(img_hsv, (0,50,20), (5,255,255))
    mask2 = cv2.inRange(img_hsv, (175,50,20), (180,255,255))

    ## Merge the mask and crop the red regions
    mask = cv2.bitwise_or(mask1, mask2 )
    croped = cv2.bitwise_and(img, img, mask=mask)

    
    # # grayscale:
    grey = cv2.cvtColor(croped, cv2.COLOR_BGR2GRAY)
    
    ## Display
    # cv2.imshow("mask", mask)
    # cv2.imshow("croped", croped)
    # cv2.imshow("grey", grey)
    # cv2.waitKey()
    
    return grey

while keyboard.is_pressed("q") == False:
    if text :
        pyautogui.keyDown("y")
        time.sleep(0.2) 
    
    # read image    
    myScreenshot = pyautogui.screenshot('in.png',region=(0,500, 350, 130))
    img = cv2.imread(path)
    # detect red text
    imgResult = detectColor(img)
    
    cv2.imwrite('out.png', imgResult)

    text = pytesseract.image_to_string(Image.open('out.png'))        
    
    start = text.find('-') +2
    end = text.find('%') +1

    OutText = text[start:end].lower()
    
    print(OutText)
    
    # Change what to cube here
    if OutText in [IED,MATT,IED_2]: 
        end = time.time()
        print(round(end-start,2))
        os.remove("out.png")
        winsound.Beep(440, 1000)
        break
    
    # myScreenshot = pyautogui.screenshot(path)
