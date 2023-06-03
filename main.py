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


def getFullname(text, lang="UZ"):
    pattern = r'ISMI\s*/\s*(?:.+)\n(.+)'
    match = re.search(pattern, text)
    if match:
        name = match.group(1)
        words = name.split()
        name = max(words, key=len)
    else:
        name = ""
    
    pattern = r'FAMILI.+\/ SUR.+\s*(.+)'
    match2 = re.search(pattern, text, re.IGNORECASE)
    if match2:
        surname = match2.group(1)
        surwords = surname.split()
        surname = max(surwords, key=len)
    else:
        surname = ""
    
    pattern = r'\s*.*TASI.+\s*(.+)'
    match3 = re.search(pattern, text, re.IGNORECASE)
    if match3:
        lastname = match3.group(1)
        surwords = lastname.split()
        lastname = max(surwords, key=len)
    else:
        lastname = ""

    fullname = surname + " " + name + " " + lastname

    return fullname

def getDataBirth(text, lang="UZ"):
    pattern = r'\s*.*LGAN.+\s*(.+)'
    match2 = re.search(pattern, text, re.IGNORECASE)
    if match2:
        
        Birthday = match2.group(1)
        surwords = Birthday.split()
        data = [item for item in surwords if item.isdigit()]
    else:
        data = ['01','01','1900']
        
    return data


def transliterate_text(text):
    mapping = {
        'A': 'А', 'B': 'Б', 'C': 'Ц', 'D': 'Д', 'E': 'Е', 'F': 'Ф', 'G': 'Г', 'H': 'Х', 'I': 'И',
        'J': 'Й', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'Q': 'К', 'R': 'Р',
        'S': 'С', 'T': 'Т', 'U': 'У', 'V': 'В', 'W': 'В', 'X': 'КС', 'Y': 'Ы', 'Z': 'З',
        'a': 'а', 'b': 'б', 'c': 'ц', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и',
        'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'q': 'к', 'r': 'р',
        's': 'с', 't': 'т', 'u': 'у', 'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'ы', 'z': 'з'
    }

    transliterated_text = ""
    for char in text:
        if char in mapping:
            transliterated_text += mapping[char]
        else:
            transliterated_text += char

    return transliterated_text

def capitalize_text(text):
    words = text.split()
    capitalized_words = [word.capitalize() for word in words]
    capitalized_text = ' '.join(capitalized_words)
    return capitalized_text


russian_text = transliterate_text(getFullname(text))
capitalized_russian_text = capitalize_text(russian_text)
print(capitalized_russian_text)


