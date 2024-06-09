"""util"""

import pyautogui


def get_location(img_full_path: str, conf=0.9) -> pyautogui.Point | None:
    """True if image exists"""

    try:
        location = pyautogui.locateCenterOnScreen(img_full_path, confidence=conf)
        return location
    except pyautogui.ImageNotFoundException:
        return None


def click_img(img_full_path, conf=0.9):
    """click image"""
    location = get_location(img_full_path, conf)
    if not location:
        return False
    x, y = location
    pyautogui.click(x, y)
    return True
