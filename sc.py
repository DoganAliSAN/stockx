import cv2
import numpy as np
import mss
import pyautogui
import time

def click_with_image(template_path, threshold=0.8, timeout=10):
    print(f"Looking for image: {template_path}")
    start_time = time.time()

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]

    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Fullscreen

        while time.time() - start_time < timeout:
            screenshot = np.array(sct.grab(monitor))
            gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

            res = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val >= threshold:
                print(f"Match found at {max_loc} with confidence {max_val}")
                x, y = max_loc[0] + w // 2, max_loc[1] + h // 2
                pyautogui.moveTo(x, y, duration=0.2)
                pyautogui.mouseDown()
                time.sleep(4)
                pyautogui.mouseUp()
                return True
            else:
                print(f"No match (confidence={max_val:.2f})")
            time.sleep(0.5)

    print("Image not found within timeout.")
    return False

click_with_image("presshold.png")