import time
import threading
import tkinter as tk
from utils import *
from utils.config import GAME_WINDOW_NAME

stop_event = threading.Event()

def bot_loop(max_minutes):
    start_time = time.time()
    try:
        if not is_window_running(GAME_WINDOW_NAME):
            print(f"{GAME_WINDOW_NAME} window not detected, please try again using the Strove application")
            return
        resize_window(GAME_WINDOW_NAME, 800, 450)
        preload_images("imgs")

        while not stop_event.is_set():
            elapsed_minutes = (time.time() - start_time) / 60
            if max_minutes > 0 and elapsed_minutes >= max_minutes:
                print("⏰ Temps max atteint, arrêt du bot.")
                break

            verify_images_folder('imgs/story')
            time.sleep(3)
    except Exception as e:
        print(f"🛑 Program stopped: {e}")

def start_bot():
    stop_event.clear()
    try:
        max_minutes = float(delay_entry.get())
    except ValueError:
        max_minutes = 0  # Pas de limite si invalide ou vide
    threading.Thread(target=bot_loop, args=(max_minutes,), daemon=True).start()
    print("Bot started")

def stop_bot():
    stop_event.set()
    print("Bot stopped manually")

root = tk.Tk()
root.title("Epic Seven Bot")

tk.Label(root, text="Temps max (minutes, 0 = infini) :").pack(padx=10, pady=(10,0))
delay_entry = tk.Entry(root)
delay_entry.insert(0, "0")
delay_entry.pack(padx=10, pady=5)

start_button = tk.Button(root, text="Start Bot", command=start_bot)
start_button.pack(padx=10, pady=5)

stop_button = tk.Button(root, text="Stop Bot", command=stop_bot)
stop_button.pack(padx=10, pady=5)

root.mainloop()