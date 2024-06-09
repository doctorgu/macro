"""main"""

import pyautogui
import time

from util import click_img


def main():
    """main"""

    # config
    pyautogui.PAUSE = 0.5

    img_dir = "./images/"

    while True:
        time.sleep(0.5)

        full_path = f"{img_dir}youtube_skip.png"
        ret = click_img(full_path)
        if not ret:
            continue

        print(full_path)


main()

# python main.py
