import ctypes
import time
from pynput import keyboard
import threading

# Constants
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000  


# Globals
enabled = False
running = True

# Structures
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class _INPUTunion(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT)]

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("union", _INPUTunion)]

# Mouse movement function
def send_mouse_movement(dx, dy):
    extra = ctypes.c_ulong(0)
    flags = MOUSEEVENTF_MOVE | MOUSEEVENTF_MOVE_NOCOALESCE | MOUSEEVENTF_VIRTUALDESK
    mi = MOUSEINPUT(dx, dy, 0, flags, 0, ctypes.pointer(extra))
    inp_union = _INPUTunion(mi)
    inp = INPUT(ctypes.c_ulong(INPUT_MOUSE), inp_union)
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

# Recoil loop
def recoil_loop():
    global enabled, running
    while running:
        if enabled:
            send_mouse_movement(0, 3)  # Try 5 if it's too weak
            time.sleep(0.01)
        else:
            time.sleep(0.05)

# Key press handling
def on_key_press(key):
    global enabled, running
    try:
        if key.char == 'h':
            enabled = not enabled
            print(f"[Anti-Recoil] {'ENABLED' if enabled else 'DISABLED'}")
        elif key.char == 'q':
            print("[Anti-Recoil] Exiting...")
            running = False
            return False
    except AttributeError:
        pass

# Start everything
threading.Thread(target=recoil_loop, daemon=True).start()
keyboard.Listener(on_press=on_key_press).run()
