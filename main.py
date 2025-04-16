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

        full_paths = [
            f"{img_dir}youtube_skip.png",
            f"{img_dir}youtube_skip_poll.png",
            f"{img_dir}youtube_skip_transparent_dark_background.png",
            f"{img_dir}youtube_skip_no_arrow_dark_background.png",
            f"{img_dir}youtube_no_thanks.png",
            f"{img_dir}youtube_no_thanks_2.png",
            # f"{img_dir}youtube_dot_3.png",
        ]
        ret = click_imgs(full_paths)
        if not ret:
            continue

        pyautogui.moveTo(0, 0)
        print(ret)


main()

# python main.py
