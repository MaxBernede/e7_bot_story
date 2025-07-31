import ctypes
import win32gui
import win32ui
import win32con
import numpy as np
import cv2

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

PrintWindow = user32.PrintWindow  # get function from user32.dll

def screenshot_window(title="Epic Seven") -> np.ndarray:
    hwnd = win32gui.FindWindow(None, title)
    if not hwnd:
        print("❌ Fenêtre non trouvée.")
        return None

    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    width, height = right - left, bottom - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)

    # Call PrintWindow via ctypes
    result = PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    if result != 1:
        print("❌ PrintWindow a échoué.")
        return None

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    img = np.frombuffer(bmpstr, dtype='uint8')
    img.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return img
