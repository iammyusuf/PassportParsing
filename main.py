import cv2  # Импортируем библиотеку OpenCV для обработки изображений
import pytesseract  # Импортируем библиотеку pytesseract для использования Tesseract OCR
import re  # Импортируем модуль re для работы с регулярными выражениями
import string  # Импортируем модуль string для работы со строками

# Указываем путь к изображению
filename = "image/3.jpeg"

# Загружаем изображение
image = cv2.imread(filename)

# Применяем морфологическую операцию закрытия для улучшения изображения
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

# Преобразуем изображение в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применяем пороговую обработку для получения черно-белого изображения
(thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 127
im_bw = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]

# Указываем путь к исполняемому файлу Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Устанавливаем конфигурацию для Tesseract OCR
config = r'--oem 3 --psm 6'

# Извлекаем текст из изображения с помощью Tesseract OCR
text = pytesseract.image_to_string(im_bw, config=config, lang='uzb')

# Функция для извлечения пола
def getGender(text, lang="UZ"):
    # Паттерн для поиска информации о поле
    pattern = r'\s*.*SEX.+\s*(.+)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        # Извлекаем найденную информацию о поле
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

# Функция для извлечения полного имени
def getFullname(text, lang="UZ"):
    # Паттерн для поиска полного имени
    pattern = r'ISMI\s*/\s*(?:.+)\n(.+)'
    match = re.search(pattern, text)
    if match:
        # Извлекаем найденное полное имя
        name = match.group(1)
        words = name.split()
        name = max(words, key=len)
    else:
        name = ""
    
     # Паттерн для поиска фамилии
    pattern = r'FAMILI.+\/ SUR.+\s*(.+)'
    match2 = re.search(pattern, text, re.IGNORECASE)
    if match2:
        # Извлекаем найденную фамилию
        surname = match2.group(1)
        surwords = surname.split()
        surname = max(surwords, key=len)
    else:
        surname = ""
    
    # Паттерн для поиска отчества
    pattern = r'\s*.*TASI.+\s*(.+)'
    match3 = re.search(pattern, text, re.IGNORECASE)
    if match3:
        # Извлекаем найденное отчество
        lastname = match3.group(1)
        surwords = lastname.split()
        lastname = max(surwords, key=len)
    else:
        lastname = ""

    # Соединяем фамилию, имя и отчество в одну строку
    fullname = surname + " " + name + " " + lastname

    return fullname

# Функция для извлечения даты рождения
def getDataBirth(text, lang="UZ"):
    # Паттерн для поиска даты рождения
    pattern = r'\s*.*LGAN.+\s*(.+)'
    match2 = re.search(pattern, text, re.IGNORECASE)
    if match2:
        # Извлекаем найденную дату рождения
        Birthday = match2.group(1)
        surwords = Birthday.split()
        data = [item for item in surwords if item.isdigit()]
    else:
        # Устанавливаем значение по умолчанию, если дата рождения не найдена
        data = ['01', '01', '1900']
        
    return data

# Функция для транслитерации текста
def transliterate_text(text):
    # Словарь с соответствием латинских и кириллических символов
    mapping = {
        'A': 'А', 'B': 'Б', 'C': 'Ц', 'D': 'Д', 'E': 'Е', 'F': 'Ф', 'G': 'Г', 'H': 'Х', 'I': 'И',
        'J': 'Й', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'Q': 'К', 'R': 'Р',
        'S': 'С', 'T': 'Т', 'U': 'У', 'V': 'В', 'W': 'В', 'X': 'КС', 'Y': 'Ы', 'Z': 'З',
        'a': 'а', 'b': 'б', 'c': 'ц', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и',
        'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'q': 'к', 'r': 'р',
        's': 'с', 't': 'т', 'u': 'у', 'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'ы', 'z': 'з'
    }

    # Транслитерируем текст, заменяя латинские символы на соответствующие кириллические
    transliterated_text = ""
    for char in text:
        if char in mapping:
            transliterated_text += mapping[char]
        else:
            transliterated_text += char

    return transliterated_text


# Функция для приведения текста к заглавным буквам
def capitalize_text(text):
    # Разбиваем текст на слова
    words = text.split()
    
    # Приводим каждое слово к заглавным буквам
    capitalized_words = [word.capitalize() for word in words]
    
    # Соединяем слова в одну строку
    capitalized_text = ' '.join(capitalized_words)
    
    return capitalized_text

# Транслитерируем текст полного имени на русский язык
russian_text = transliterate_text(getFullname(text))

# Приводим текст полного имени на русском языке к заглавным буквам
capitalized_russian_text = capitalize_text(russian_text)

# Выводим приведенный к заглавным буквам текст полного имени на русском языке

def getPassportNumber(text):
    # Функция для извлечения номера заграничного паспорта Узбекистана из текста
    
    # Шаблон для поиска номера паспорта
    pattern = r'[A-Z]{2}\d{8}'
    
    # Поиск совпадения по шаблону в тексте
    match = re.search(pattern, text)
    
    if match:
        # Если найдено совпадение, извлекаем номер паспорта из группы совпадения
        passport_number = match.group(0)
        return passport_number
    else:
        # Если совпадение не найдено, возвращаем пустую строку
        return ""

# Извлекаем номер паспорта
passport_number = getPassportNumber(text)

# Извлекаем пол
gender = getGender(text)

# Извлекаем полное имя
fullname = getFullname(text)

# Извлекаем дату рождения
birth_data = getDataBirth(text)

# Транслитерируем текст полного имени на русский язык
russian_text = transliterate_text(fullname)

# Приводим текст полного имени на русском языке к заглавным буквам
capitalized_russian_text = capitalize_text(russian_text)

# Выводим результаты
print("Номер паспорта:", passport_number)
print("Пол:", gender)
print("Полное имя на кириллице:", fullname)
print("Транслитерированное полное имя на русском языке:", capitalized_russian_text)
print("Дата рождения:", '/'.join(birth_data))