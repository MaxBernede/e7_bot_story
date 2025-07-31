import win32api
import win32con
import win32gui
import time

def click_in_window(window_title, x, y):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        print("❌ Fenêtre non trouvée.")
        return False

    # Convert client coords to screen coords
    point = win32gui.ClientToScreen(hwnd, (x, y))

    win32api.SetCursorPos(point)
    time.sleep(0.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, point[0], point[1], 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, point[0], point[1], 0, 0)
    return True


# import win32gui
# import win32con
# import win32api

# def click_in_window_invisible(window_title, x, y):
#     hwnd = win32gui.FindWindow(None, window_title)
#     if not hwnd:
#         print("❌ Fenêtre non trouvée.")
#         return False

#     # PAS de ClientToScreen ici
#     lParam = win32api.MAKELONG(x, y)
#     rect = win32gui.GetClientRect(hwnd)
#     print(f"🖼️ Client rect: {rect}")
#     print(f"🎯 Click coords: ({x}, {y})")
#     win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
#     win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
#     return True