import pyautogui
import keyboard

# Left: 1730, Top: 381, Width: 110, Height: 12
# Left: 1730, Top: 397, Width: 111, Height: 12
LIFE_REGION = (1767,308,91,4)
MANA_REGION = (1767, 318,91,4)



LIFE_COLOR = (231,90,90)
MANA_COLOR = (94,91,230)

WIDTH = 91

def calculate_width(percent):
    return int(WIDTH * percent/100)

# def check_color(region, percent):
#     result_percent = calculate_width(percent)
#     x = region[0] + result_percent
#     y = region[1] + region[3]
#     print(pyautogui.pixel(x,y))

# keyboard.wait('h')
# check_color(MANA_REGION, 80)

def pixel_matches_color(region, percent, color):
    result = calculate_width(percent)
    x = region[0] + result
    y = region[1] + region[3]
    actual_color = pyautogui.pixel(int(x), int(y))
    print(f"Checking pixel at ({x}, {y}), actual color: {actual_color}, expected color: {color}")
    return pyautogui.pixelMatchesColor(int(x), int(y), color, 40)

def manager_suplies(event):
    while not event.is_set():
        if not pixel_matches_color(LIFE_REGION, 65, LIFE_COLOR):
            pyautogui.press('3')
            print(LIFE_COLOR, LIFE_REGION)
        if event.is_set():
             return
        else:
             if not pixel_matches_color(LIFE_REGION, 90, LIFE_COLOR):
                 pyautogui.press('1')
             if not pixel_matches_color(MANA_REGION, 90, MANA_COLOR):
                pyautogui.press('2')    
             if event.is_set():
                return