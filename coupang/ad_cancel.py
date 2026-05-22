"""cancel ad"""

from util import move_mouse_parabolic
from pyscreeze import Box
import pyautogui
import pyperclip
import time
import random
import os
import subprocess
import cv2
import numpy as np
import logging
from dotenv import load_dotenv

# Load env credentials
load_dotenv()

# Configure pyautogui safety features
pyautogui.FAILSAFE = True  # Move mouse to far top-left corner of screen to abort script
pyautogui.PAUSE = 0.1  # Small pause between basic pyautogui actions


def human_click(target_x, target_y):
    """
    Simulates physical mouse clicks: presses down, holds, and releases.
    """

    pyautogui.moveTo(target_x, target_y)
    time.sleep(random.uniform(0.1, 0.2))
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.06, 0.08))  # physical click speed
    pyautogui.mouseUp()
    time.sleep(random.uniform(0.3, 0.3))


def human_click_element(image_name, confidence=0.85, region=None):
    """
    Finds a target PNG screenshot on screen and performs a human click on it.
    """
    logging.debug(f"finding {image_name}...")
    pos = human_locate_center(image_name, confidence, region)
    if pos:
        logging.debug(f"found {image_name} at {pos}. Clicking...")
        move_mouse_parabolic(x_to=pos[0], y_to=pos[1], height=100, duration=0.5)
        human_click(pos[0], pos[1])
        return True

    raise ValueError(f"Could not find '{image_name}' icon.")


def locate_unicode_image(image_path, **kwargs) -> Box | None:
    # Load the image from a path that may contain Unicode characters
    # np.fromfile reads the file as a byte array, bypassing OpenCV's path limitations
    img_array = np.fromfile(image_path, np.uint8)

    # Decode the byte array into an OpenCV image object
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Could not load image at {image_path}. Check file integrity.")

    try:
        return pyautogui.locateOnScreen(img, **kwargs)
    except pyautogui.ImageNotFoundException:
        return None


def locate_image(
    image_name: str, confidence: float = 0.85, region: None = None
) -> Box | None:
    """
    Locates a target image on screen using OpenCV template matching and returns its box.
    """
    image_path = os.path.join(
        os.path.join(os.path.dirname(__file__), "images"), f"{image_name}.PNG"
    )
    if not os.path.exists(image_path):
        raise FileExistsError(f"Image path does not exist: {image_path}")

    return locate_unicode_image(image_path, confidence=confidence, region=region)


def human_locate_center(image_name: str, confidence: float = 0.85, region: None = None):
    """
    Locates an image on screen and returns its human-like coordinates.
    """
    box = locate_image(image_name, confidence, region)
    if box:
        return pyautogui.center(box) + (random.randint(-5, 5), random.randint(-5, 5))
    return None


def do_for_popups():
    """
    - if "동의철회" shows, click "동의철회"
    - if "확인" shows, click "확인"
    """
    # Check for "동의철회" button popup
    btn_withdraw = human_locate_center("동의철회")
    if btn_withdraw:
        logging.debug("🔔 Detected '동의철회' popup on screen! Clicking...")
        human_click(*btn_withdraw)
        time.sleep(1.0)

    # Check for "확인" button popup
    btn_confirm = human_locate_center("확인")
    if btn_confirm:
        logging.debug("🔔 Detected '확인' popup on screen! Clicking...")
        human_click(*btn_confirm)
        time.sleep(1.0)


def paste_text(text):
    """
    Copies input strings to your system clipboard and pastes it via Ctrl+V shortcut.
    Bypasses secure virtual keyboards and input layout language issues.
    """
    pyperclip.copy(text)
    time.sleep(0.1)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.2)


def wait_for_image(image_name: str, timeout: int = 15):
    """
    Monitors the screen to find an image.
    """

    logging.debug(f"waiting for {image_name}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        if locate_image(image_name):
            time.sleep(random.uniform(0.1, 0.5))
            return True
        time.sleep(0.1)
    return False


def wait_for_all_images(image_names: list[str], timeout=15):
    """
    Monitors the screen to find an image.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        not_found = False
        for image_name in image_names:
            if not wait_for_image(image_name, timeout):
                not_found = True
                break

        if not not_found:
            return True

    return False


def login_from_main_page():
    """login"""

    if not wait_for_image("로그인_링크", timeout=3):
        raise RuntimeError("Could not find '로그인_링크' icon.")
    human_click_element("로그인_링크")

    if not wait_for_image("로그인_실행", timeout=3):
        raise RuntimeError("Could not find '로그인_실행' icon.")
    human_click_element("로그인_실행")

    if not wait_for_image("로그아웃", timeout=3):
        raise RuntimeError("Could not find '로그아웃' icon.")


def set_logger():
    """write both screen and file"""

    logger = logging.getLogger()
    if not logger.handlers:
        path = os.path.join(os.path.dirname(__file__), "ad_cancel.log")
        logging.basicConfig(
            level=logging.DEBUG,  # show both INFO and DEBUG messages
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(path, encoding="utf-8"),  # file handler
                logging.StreamHandler(),  # screen handler
            ],
        )


def main():
    set_logger()

    coupang_password = os.getenv("COUPANG_PASSWORD")
    if not coupang_password:
        raise ValueError("COUPANG_PASSWORD is not set in the .env file.")

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        raise FileNotFoundError(f"Google Chrome was not found at '{chrome_path}'")

    # Open Chrome directly targeting coupang
    subprocess.Popen([chrome_path, "https://www.coupang.com"])

    if not wait_for_image("로그아웃", timeout=3):
        login_from_main_page()

    if not wait_for_all_images(["로그아웃", "마이쿠팡"], timeout=3):
        raise RuntimeError("Could not find '로그아웃' or '마이쿠팡' icon.")
    human_click_element("마이쿠팡")

    if not wait_for_image("개인정보확인수정", timeout=3):
        raise RuntimeError("Could not find '개인정보확인수정' icon.")
    human_click_element("개인정보확인수정")

    if wait_for_all_images(["인증방법선택", "비밀번호_링크"], timeout=3):
        human_click_element("비밀번호_링크")

        if not wait_for_all_images(["비밀번호입력", "비밀번호_입력"], timeout=3):
            raise RuntimeError("Could not find '비밀번호입력' or '비밀번호_입력' icon.")

        human_click_element("비밀번호_입력")
        paste_text(coupang_password)
        human_click_element("계속하기")

    if not wait_for_image("회원정보수정", timeout=3):
        raise RuntimeError("Could not find '회원정보수정' icon.")

    text1_box = locate_image("마케팅목적의개인정보수집및이용동의함")
    if text1_box:
        left, top, width, height = text1_box
        # Scan in a local bounding box to its left
        region1 = (int(left - 75), int(top - 10), 80, int(height + 20))
        checked1 = locate_image("체크됨", region=region1)
        if checked1:
            cx, cy = pyautogui.center(checked1)
            human_click(cx, cy)
            time.sleep(1.0)
            do_for_popups()

    text2_box = locate_image("광고성정보수신동의함")
    if text2_box:
        left, top, width, height = text2_box
        region2 = (int(left - 75), int(top - 10), 80, int(height + 20))
        checked2 = locate_image("체크됨", region=region2)
        if checked2:
            cx, cy = pyautogui.center(checked2)
            human_click(cx, cy)
            time.sleep(1.0)
            do_for_popups()

    pyautogui.hotkey("ctrl", "w")
    time.sleep(1.0)
    logging.debug("done")


main()
