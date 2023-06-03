import cv2
import pytesseract
import re
import string


filename = "image/1.jpeg"
image = cv2.imread(filename)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
(thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 127
im_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(im_bw, config=config, lang='uzb')

# GET GENDER FUNCTION 
def getGender(text,lang="UZ"):
    pattern = r'\s*.*SEX.+\s*(.+)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        gendertext = match.group(1)
        gendertext = ''.join(char for char in gendertext if char.isalpha() and char not in string.ascii_lowercase)
        gendertext = gendertext[:3]
        if "F" in gendertext:
            gen = "F"
        elif "M" in gendertext:
            gen = "M"
        else: 
            gen = "NOT"
    else:
        return 0         
    return gen
