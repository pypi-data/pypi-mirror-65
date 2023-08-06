import os
import re
import sys
from caos._internal.utils.os import is_posix_os, is_win_os
from caos._third_party.ansi189 import ansicon


def supports_color() -> bool:
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    supported_platform = is_posix_os() or os.environ.get('ANSICON') or (is_win_os() and ansicon.load())
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() # isatty is not always present
    return supported_platform and is_a_tty


def escape_ansi(line) -> str:
    """
    Returns a string without ansi color codes
    """
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)



