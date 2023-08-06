import os
import platform
import ctypes
from caos._third_party.ansi189.ansicon import DLLs

_architecture = platform.architecture()[0]
_dlls_path: str = os.path.dirname(DLLs.__file__)
_32bit_dll: str = os.path.abspath(_dlls_path + "/" + "ANSI32.dll")
_64bit_dll: str = os.path.abspath(_dlls_path + "/" + "ANSI64.dll")


_dll_to_use = None
if _architecture == "32bit":
    _dll_to_use = _32bit_dll

elif _architecture == "64bit":
    _dll_to_use = _64bit_dll


def load():
    try:
        ctypes.WinDLL(_dll_to_use, use_last_error=True)
    except:
        return False
    return True
