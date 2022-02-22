from lib2to3.pytree import convert
from random import gammavariate
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
import sys


# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'D:\\Tesseract\\tesseract.exe'
# Example tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

screenshot_area = (773, 458, 1148, 626)
game_version = "LOST ARK (64-bit, DX11) V.2.0.1.2"
telegram_message = ""


def check_game_open():
    """
    This function checks if the game window is open and returns true if it is.
    """
    try:
        win32gui.GetWindowText(win32gui.GetForegroundWindow())
        print('Game is open. Proceeding...')
        return True
    except:
        print('Game is not open. Please open the game and try again. Exiting the program for now.')
        send_telegram_message(
            'Game is not open. Please open the game and try again. Exiting the program for now.')
        exit()


def take_screenshot():
    """
    This function tries to focus the game by getting the window handle and setting it as foreground.
    Returns warning if not possible.
    This function takes a screenshot and saves it to a file in the screenshots folder.
    """
    try:
        # try to get the window handle of the game and focus the game before taking the screenshot
        win32gui.SetForegroundWindow(win32gui.FindWindow(
            None, game_version))
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
        print('Could not focus game. I\'ll try again in the next round.')
        send_telegram_message(
            'Could not focus the game window. I\'ll try again in the next round.')


def image_converter(filename):
    """
    This function tries to convert an image to text and times out after 2 seconds.
    """
    if filename is not None:
        try:
            print('Converting image to text...')
            converted_text = pytesseract.image_to_string(
                Image.open(filename), lang='eng', timeout=2)
            print('Successfully converted image to text.')
            return converted_text
        except Exception as e:
            print(e)
            return None


def check_valid_text(converted_text):
    """
    This function checks if the text contains the string "Your queue number" and returns a positive result.
    Else if text contains "Cannot connect to the server" returns an error message.
    Else if none of the above are true, returns an error saying "Not in the queue or unable to verify" and stops the application.
    """
    if "Your queue number" in converted_text:
        print('Checking converted text... Looks like you are in the queue.')
        return True
    elif "Cannot connect to the server" in converted_text:
        print("You got disconnected from the server. Please try again.")
        send_telegram_message(
            "You got disconnected from the server. Please try again.")
        return False
    else:
        print("Not in the queue or unable to verify.")
        send_telegram_message("Not in the queue or unable to verify.")
        return False


def numbers_only(converted_text):
    """
    This function checks if check_valid_text() is True, and returns only the numbers from the text.
    """
    if check_valid_text(converted_text):
        telegram_message = 'Your position in the queue is:'.join(
            filter(str.isdigit, converted_text))
        print('Extracted numbers from text.')
        return telegram_message


def send_telegram_message(telegram_message):
    token = keys.token
    id = keys.id

    requests.post(
        f'https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={telegram_message}')


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


# run the program every X minutes
run(0.25)
