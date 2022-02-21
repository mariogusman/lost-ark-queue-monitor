from PIL import Image

import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'D:\\Tesseract\\tesseract.exe'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'


def image_converter(image_path):
    """
    This function tries to convert an image to text and times out after 2 seconds.
    """
    try:
        text = pytesseract.image_to_string(
            Image.open(image_path), lang='eng', timeout=2)
        return text
    except Exception as e:
        print(e)
        return None


def numbers_only(text):
    """
    This function returns only the numbers from the text, and prints the result.
    """
    return ''.join(filter(str.isdigit, text))


print(numbers_only(image_converter(
    'C:\\Users\\mario\\Documents\\GitHub\\lost-ark-queue-monitor\\screenshots\\teste1.jpg')))
