import PIL
from PIL import ImageGrab  # to get the image from the screen
from PIL import Image
import pytesseract  # to ocr the image
import time  # to create filename
import win32gui  # to get the window handle of the game


# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'D:\\Tesseract\\tesseract.exe'
# Example tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'


def take_screenshot():
    """
    This function tries to focus the game by getting the window handle and setting it as foreground.
    Returns warning if not possible.
    This function takes a screenshot and saves it to a file in the screenshots folder.
    """
    try:
        win32gui.SetForegroundWindow(win32gui.FindWindow(
            None, 'LOST ARK (64-bit, DX11) v.2.0.1.2'))
        print('Game focused.')
        # sleeps for 1 second before continuing
        time.sleep(1)
        print('Taking screenshot...')

        filename = f'screenshots\\{time.strftime("%Y-%m-%d_%H-%M-%S")}.png'
        ImageGrab.grab().save(filename)
        print(f'Screenshot saved to {filename}')
    except:
        print('Could not focus game.')


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


take_screenshot()
