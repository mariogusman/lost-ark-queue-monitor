import PIL
from PIL import ImageGrab  # to get the image from the screen
from PIL import Image
import pytesseract  # to ocr the image
import time  # to create filename
import win32gui  # to get the window handle of the game
import keys  # used for telegram API keys, token, etc
import requests
import os


# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'D:\\Tesseract\\tesseract.exe'
# Example tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

screenshot_area = (773, 458, 1148, 626)
game_version = "LOST ARK (64-bit, DX11) V.2.0.1.2"
telegram_message = ""
screenshot_name = None
last_three_numbers = []
cooldown = 1  # how many minutes to wait between each check


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
    if check_game_open():
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
            screenshot_name = f'screenshots\\{time.strftime("%Y-%m-%d_%H-%M-%S")}.png'
            ImageGrab.grab(bbox=screenshot_area).save(screenshot_name)
            print(f'Screenshot saved to {screenshot_name}')
            return screenshot_name

        except:
            # if the game is not focused, or if the screenshot cannot be taken, print a warning
            print('Could not focus game. I\'ll try again in the next round.')
            time.sleep(cooldown*60)
            send_telegram_message(
                'Could not focus the game window. I\'ll try again in the next round.')


def image_converter(screenshot_name):
    """
    This function tries to convert an image to text and times out after 2 seconds.
    """
    if screenshot_name is not None:
        try:
            print('Converting image to text...')
            converted_text = pytesseract.image_to_string(
                Image.open(screenshot_name), lang='eng', timeout=2)
            print('Successfully converted image to text.')
            check_valid_text(converted_text)
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
        numbers_only(converted_text)
    elif "Cannot connect to the server" in converted_text:
        print("You got disconnected from the server. Please try again.")
        send_telegram_message(
            "You got disconnected from the server. Please try again.")
    else:
        print("Not in the queue or unable to verify.")
        send_telegram_message("Not in the queue or unable to verify.")


def numbers_only(converted_text):
    """
    This function checks if check_valid_text() is True, and returns only the numbers from the text.
    """
    queue_number = ''.join(
        filter(str.isdigit, converted_text))
    print('Extracted numbers from text.')

    last_three_numbers.append(int(queue_number))
    if len(last_three_numbers) > 3:
        last_three_numbers.pop(0)

    elif len(last_three_numbers) == 3:
        first_interval = int(
            last_three_numbers[0]) - int(last_three_numbers[1])
        second_interval = int(
            last_three_numbers[1]) - int(last_three_numbers[2])
        interval_average = int((first_interval + second_interval) / 2)
        queue_speed = int(interval_average / cooldown)
        minutes_to_zero = str(last_three_numbers[2] / queue_speed)

        # strips minutes_to_zero to only show the digits before the "."
        stripped_minutes_to_zero = minutes_to_zero.split(".")[0]

        print(f'Estimated time to zero: {stripped_minutes_to_zero} minutes')
        send_telegram_message('Your position in the queue is: ' + queue_number +
                              '. Your estimated time to login is in ' + stripped_minutes_to_zero + ' minutes.')
    else:
        print('Not enough numbers to calculate. Trying again in the next round.')
        send_telegram_message('Your position in the queue is: ' + queue_number +
                              '. Calculating the estimated queue duration. Give me more time.')


def send_telegram_message(telegram_message):
    token = keys.token
    id = keys.id
    requests.post(
        f'https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={telegram_message}')


def delete_screenshot(screenshot_name):
    """
    This function deletes the screenshot after it has been used.
    """
    if screenshot_name is not None:
        try:
            os.remove(screenshot_name)
            print(f'{screenshot_name} deleted.')
        except Exception as e:
            print(e)


def run(cooldown):
    while True:
        minutes = cooldown * 60
        main()
        time.sleep(minutes)


def main():
    check_game_open()
    take_screenshot()
    image_converter(take_screenshot())
    delete_screenshot(take_screenshot())


# run the program every X minutes
run(cooldown)
