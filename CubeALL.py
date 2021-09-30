# from cubeline import OutText
# from utils import *
import pytesseract
import pyautogui
import pydirectinput
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


def detectColor(img):
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
    
    return grey

def GameCommands(nthLine, nthItem):
    pyautogui.press("n")
    time.sleep(1)
    pydirectinput.press("y")
    time.sleep(1)
    print(nthItem)
    for i in range(nthItem):
        pydirectinput.press("down")
        time.sleep(0.3)
    pydirectinput.press("y")
    time.sleep(0.3)
    
    # NumDown starts from 0
    LineCount = 0
    
    while LineCount < nthLine:
        pyautogui.press("down")
        time.sleep(0.2)
        LineCount+=1
    
    pydirectinput.press("y")

# Main start here
if __name__ == '__main__':
    startT = time.time()
    # Change this for Line
    nthLine = 0
    text = None
    counter = 0
    nthItem = 0
    # Change this for Item
    endItem = 1
    
    while nthItem < endItem:
        while nthLine < 5:
            # if nthLine == 1: continue
            # In game commands
            print(nthItem,"nth Item", nthLine,"nth Line")
            time.sleep(0.2)
            GameCommands(nthLine,nthItem)
            
            while keyboard.is_pressed("q") == False:
                if text :
                    pyautogui.press("y")
                    time.sleep(0.2) 
                
                # read image    
                myScreenshot = pyautogui.screenshot('in.png',region=(0,460, 350, 200))
                img = cv2.imread(path)
                # detect red text
                imgResult = detectColor(img)
                
                cv2.imwrite('out.png', imgResult)

                text = pytesseract.image_to_string(Image.open('out.png'))        
                
                start = text.find('-') +2
                end = text.find('%') +1

                OutText = text[start:end].lower()
                
                print(OutText)
                counter+=1
                # Change what to cube here
                if OutText in [IED,IED_2]: 
                    os.remove("out.png")
                    # winsound.Beep(220, 500)
                    break
            
                
            # count up to 5 times
            nthLine +=1
        # print(nthItem)
        nthItem+=1
        nthLine=0
        
        
    end = time.time()
    print("Time took: ",round((end-startT)/60,2),"m")
    print("Total cube times: ", counter)
    print("Total hearts used: ", counter*5)
    winsound.Beep(440, 1000)