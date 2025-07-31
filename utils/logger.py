from enum import Enum

class Color(Enum):
    GREEN = "92"
    RED = "91"
    YELLOW = "93"
    BLUE = "94"
    CYAN = "96"
    RESET = "0"

def printc(text: str, color: Color):
    print(f"\033[{color.value}m{text}\033[0m")