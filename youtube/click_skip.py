"""main"""

from datetime import datetime
import time
import pyautogui
import os
from util import click_imgs


def main():
    """main"""

    # config
    pyautogui.PAUSE = 0.5

    img_dir = os.path.join(os.path.dirname(__file__), "images")

    while True:
        time.sleep(0.5)

        full_paths = [
            os.path.join(img_dir, "youtube_skip.png"),
            os.path.join(img_dir, "youtube_skip_poll.png"),
            os.path.join(img_dir, "youtube_skip_transparent_dark_background.png"),
            os.path.join(img_dir, "youtube_skip_no_arrow_dark_background.png"),
            os.path.join(img_dir, "youtube_no_thanks.png"),
            os.path.join(img_dir, "youtube_no_thanks_2.png"),
            # f"{img_dir}youtube_dot_3.png",
        ]
        ret = click_imgs(full_paths)
        if not ret:
            continue

        pyautogui.moveTo(640, 640)
        print(datetime.now(), ret)


main()
