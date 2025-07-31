def is_window_running(title):
    def enum_handler(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            if title.lower() in win32gui.GetWindowText(hwnd).lower():
                result.append(hwnd)
    result = []
    win32gui.EnumWindows(enum_handler, result)
    return len(result) > 0

import win32gui

def resize_window(title, width, height):
    hwnd = win32gui.FindWindow(None, title)
    if not hwnd:
        print("❌ Fenêtre non trouvée.")
        return False
    win32gui.MoveWindow(hwnd, 0, 0, width, height, True)
    return True
