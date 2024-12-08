# import pynput
# import pyautogui
# import threading
# import random
# from vida_mana import manager_suplies

# pyautogui.ImageNotFoundException(False)


# def get_loot():
#     random.shuffle(LIST_POSITION_LOOT)
#     pyautogui.PAUSE= 0.045
#     for position in LIST_POSITION_LOOT:
#         pyautogui.moveTo(position)
#         pyautogui.click(button="right")

#     pyautogui.PAUSE= 0.1

# REGION_BATTLE = (1572, 25, 156, 44)

# def rotate_skills():
#     while not event_rotate_skills.is_set():
#         for attack in LIST_HOTKEYS_ATTACKS:
#             if event_rotate_skills.is_set():
#                 return 
#             pyautogui.screenshot('debug_region.png', region=REGION_BATTLE)
#             # if pyautogui.locateOnScreen('battle.png', confidence=0.5, region=REGION_BATTLE):
#             #     continue
#             pyautogui.press('space')
#             pyautogui.press(attack["hotkey"])
#             pyautogui.sleep(attack["delay"])

# def execute_hotkey(hotkey):
#     pyautogui.press(hotkey)

# LIST_POSITION_LOOT  = [
#     (938, 384),
#     (993, 378),
#     (996, 425),
#     (999, 476),
#     (934, 489),
#     (894, 498),
#     (892, 436),
#     (885, 376)
# ]

# LIST_HOTKEYS_ATTACKS = [{"hotkey":'v', "delay": 1}, {"hotkey":'4', "delay": 1}, {"hotkey":'5', "delay": 1}, {"hotkey":'6', "delay": 1}]
# FULL_DEFENSIVE_HOTKEY = '-'
# FULL_OFFENSIVE_HOTKEY = '='
# USE_RING_HOTKEY = 'F10'
# list_hotkey_before = [FULL_OFFENSIVE_HOTKEY, USE_RING_HOTKEY  ]
# list_hotkey_after = [FULL_DEFENSIVE_HOTKEY, USE_RING_HOTKEY  ]


# running = False
# def key_code(key):
#     global running
#     if key == pynput.keyboard.Key.delete:
#         return False
#     if hasattr(key, 'char') and key.char == 'f':
#         if running == False:
#            running = True 
#            global th_rotate_skills, event_rotate_skills, th_suplies, event_suplies
#            event_suplies = threading.Event()
#            th_suplies = threading.Thread(target= manager_suplies, args=(event_suplies, ))
#            event_rotate_skills=threading.Event()
#            th_rotate_skills = threading.Thread(target=rotate_skills)
#            print('Iniciamos a rotação de skills')
#            for hotkey in list_hotkey_before:
#             execute_hotkey(hotkey)
#            th_rotate_skills.start()
#            print('iniciamos o life helper')
#            th_suplies.start()
           
           
#         else:
#             running = False
#             event_rotate_skills.set()
#             event_suplies.set()
#             th_rotate_skills.join()
#             th_suplies.join()
#             print('Parando rotação de skills')
#             execute_hotkey(FULL_DEFENSIVE_HOTKEY)
#             execute_hotkey(USE_RING_HOTKEY)

#     if hasattr(key, 'char') and key.char == 'r':
#         print('coletando loot')
#         get_loot()

# with pynput.keyboard.Listener(on_press=key_code) as listener:    listener.join()
import logging
from pynput import keyboard
import pyautogui
import threading
import time
from vida_mana import manager_suplies

logging.basicConfig(level=logging.INFO)

LOOT_POSITIONS = [
    (938, 384), (993, 378), (996, 425), (999, 476),
    (934, 489), (894, 498), (892, 436), (885, 376)
]

ORDERED_HOTKEYS = [
    {"hotkey": '4', "delay": 1.4},
    {"hotkey": '5', "delay": 1.4},
    {"hotkey": 'r', "delay": 1.4},
    {"hotkey": '4', "delay": 1.4},
    {"hotkey": '5', "delay": 1.4},
    {"hotkey": 'g', "delay": 1.4}
]

class GameManager:
    def __init__(self):
        self.running = False
        self.event_rotate_skills = threading.Event()
        self.event_suplies = threading.Event()
        self.thread_rotate_skills = None
        self.thread_suplies = None

    def start(self):
        """Start skill rotation and supplies management."""
        self.running = True
        # self.event_rotate_skills.clear()
        self.event_suplies.clear()
        # self.thread_rotate_skills = threading.Thread(target=self.rotate_skills)
        self.thread_suplies = threading.Thread(target=manager_suplies, args=(self.event_suplies,))
        # self.thread_rotate_skills.start()
        self.thread_suplies.start()
        logging.info("Started threads.")

    def stop(self):
        """Stop skill rotation and supplies management."""
        self.running = False
        self.event_rotate_skills.set()
        self.event_suplies.set()
        if self.thread_rotate_skills:
            self.thread_rotate_skills.join()
        if self.thread_suplies:
            self.thread_suplies.join()
        logging.info("Stopped threads.")

    def rotate_skills(self):
        """Rotate through attack hotkeys in a fixed order."""
        next_cast_time = time.monotonic()  # Inicializa o tempo para o primeiro cast

        for hotkey in ORDERED_HOTKEYS:
            hotkey["next_time"] = next_cast_time  # Configura o próximo uso para cada hotkey

        while not self.event_rotate_skills.is_set():
            now = time.monotonic()  # Tempo atual
            for hotkey in ORDERED_HOTKEYS:
                if now >= hotkey["next_time"]:  # Verifica se já está no tempo certo para usar a magia
                    pyautogui.press(hotkey["hotkey"])
                    logging.info(f"Casted {hotkey['hotkey']} at {now:.2f}")
                    hotkey["next_time"] = now + hotkey["delay"]  # Atualiza o tempo do próximo uso
                    break  # Sai do loop e verifica novamente no próximo intervalo

            time.sleep(0.01)  # Pequeno intervalo para evitar sobrecarga da CPU

    def get_loot(self):
        """Simulate loot collection."""
        pyautogui.PAUSE = 0.045
        for position in LOOT_POSITIONS:
            pyautogui.moveTo(position)
            pyautogui.click(button="right")
        pyautogui.PAUSE = 0.1


def key_code(key, game_manager):
    """Handle keyboard events."""
    if key == keyboard.Key.delete:
        return False
    if hasattr(key, 'char') and key.char == 'h':
        if not game_manager.running:
            game_manager.start()
        else:
            game_manager.stop()
    if hasattr(key, 'char') and key.char == 'u':
        logging.info("Collecting loot...")
        game_manager.get_loot()


if __name__ == "__main__":
    game_manager = GameManager()
    with keyboard.Listener(on_press=lambda key: key_code(key, game_manager)) as listener:
        listener.join()
