import pytesseract
import pyautogui
import pydirectinput
import time
import cv2
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def detectColor(img):

    # Resize image
    height, width, channels = img.shape
    img = cv2.resize(img, (width*3, height*3))
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return grey


if __name__ == '__main__':
    myScreenshot = pyautogui.screenshot('in.png', region=(1700, 520, 220, 80))
    img = cv2.imread('in.png')
    # detect red text
    imgResult = detectColor(img)

    cv2.imwrite('out.png', imgResult)

    text = pytesseract.image_to_string(Image.open('out.png'))

    start = text.find(':') + 2
    end = text.find('\n')  # + 1

    OutText = text[start:end].lower()
    print(OutText)
    try:
        print(int(OutText))
        time.sleep(0.5)
        for i in OutText:
            print(i)
            pyautogui.press(i)
            # time.sleep(0.1)
        pyautogui.press('enter')
        os.remove('out.png')
    except ValueError:
        print("not number, shutting down")
        pydirectinput.keyDown("ctrl")
        pydirectinput.keyDown("q")
        pydirectinput.keyUp("ctrl")
        pydirectinput.keyUp("q")