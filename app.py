import PIL
from PIL import ImageGrab  # to get the image from the screen
from PIL import Image
from black import re_compile_maybe_verbose
from httpx import delete
import pytesseract  # to ocr the image
import time  # to create filename
import win32gui  # to get the window handle of the game
import keys  # used for telegram API keys, token, etc
import requests
import os
import threading


# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'D:\\Tesseract\\tesseract.exe'
# Example tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

screenshot_area = (773, 458, 1148, 626)


def take_screenshot():
    """
    This function tries to focus the game by getting the window handle and setting it as foreground.
    Returns warning if not possible.
    This function takes a screenshot and saves it to a file in the screenshots folder.
    """
    try:
        # try to get the window handle of the game and focus the game before taking the screenshot
        win32gui.SetForegroundWindow(win32gui.FindWindow(
            None, 'LOST ARK (64-bit, DX11) v.2.0.1.2'))
        print('Game focused.')

        # sleeps for 1 second before continuing to give enough time for the game to focus
        time.sleep(1)
        print('Taking screenshot...')

        # takes the screenshot and saves it to the screenshots folder
        # screenshot_area is the area of the screenshot defined at the top of the file
        filename = f'screenshots\\{time.strftime("%Y-%m-%d_%H-%M-%S")}.png'
        ImageGrab.grab(bbox=screenshot_area).save(filename)
        print(f'Screenshot saved to {filename}')
        return filename

    except:
        # if the game is not focused, or if the screenshot cannot be taken, print a warning
        print('Could not focus game.')


def image_converter(filename):
    """
    This function tries to convert an image to text and times out after 2 seconds.
    """
    try:
        converted_text = pytesseract.image_to_string(
            Image.open(filename), lang='eng', timeout=2)
        return converted_text
    except Exception as e:
        print(e)
        return None


def numbers_only(converted_text):
    """
    This function returns only the numbers from the text, and prints the result.
    """
    queue_position = ''.join(filter(str.isdigit, converted_text))
    return queue_position


def send_telegram_message(converted_text):
    token = keys.token
    id = keys.id

    requests.post(
        f'https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text=Your Position in the Queue is: {converted_text}')


def delete_screenshot(filename):
    """
    This function deletes the screenshot after it has been used.
    """
    try:
        os.remove(filename)
        print(f'{filename} deleted.')
    except:
        pass


def run(cooldown):
    while True:
        minutes = cooldown * 60
        main()
        time.sleep(minutes)


def main():
    """
    This function calls take_screenshot, image_converter, and numbers_only.
    """
    filename = take_screenshot()
    converted_text = image_converter(filename)
    if converted_text is not None:
        converted_text = numbers_only(converted_text)
        print(f'Your position in the queue is: {converted_text}')
        # sending the message to telegram
        send_telegram_message(converted_text)
        delete_screenshot(filename)

    else:
        print('Could not convert image to text.')


# run the program every 5 minutes
run(5)
