"""main"""

import pyautogui
import time

from util import click_imgs


def main():
    """main"""

    # config
    pyautogui.PAUSE = 0.5

    img_dir = "./images/"

    while True:
        time.sleep(0.5)

        full_paths = [f"{img_dir}youtube_skip.png", f"{img_dir}youtube_skip_poll.png"]
        ret = click_imgs(full_paths)
        if not ret:
            continue

        print(full_paths)


main()

# python main.py
