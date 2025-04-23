"""util"""

import pyautogui


def get_location(img_full_path: str, conf=0.9) -> pyautogui.Point | None:
    """True if image exists"""

    try:
        location = pyautogui.locateCenterOnScreen(img_full_path, confidence=conf)
        return location
    except (pyautogui.ImageNotFoundException, OSError):
        return None


def click_imgs(img_full_paths: list[str], conf=0.9) -> bool:
    """click images"""

    for img_full_path in img_full_paths:
        location = get_location(img_full_path, conf)
        if not location:
            continue

        x, y = location
        pyautogui.click(x, y)
        return True

    return False
