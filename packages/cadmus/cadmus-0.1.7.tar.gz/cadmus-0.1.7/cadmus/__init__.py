
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    CYAN = '\033[96m'
    DARK_CYAN = '\033[36m'
    BLACK = '\033[97m'


class Style:
    INFORM = 0
    WARN = 1
    ALERT = 2
    SUCCESS = 3


def color_print(text, color=None):
    if color:
        print(f'{color}{text}{Colors.ENDC}')
    else:
        print(text)


def alert(text):
    if alert._show:
        color_print(text, color=Colors.FAIL)


def warn(text):
    if alert._show:
        color_print(text, color=Colors.WARNING)


def success(text):
    if alert._show:
        color_print(text, color=Colors.OKGREEN)


def inform(text):
    if inform._show:
        color_print(text, color=Colors.OKBLUE)


def hide_everything():
    alert._show = False
    inform._show = False
    success._show = False
    warn._show = False


def show(types=None):
    if types is None:
        types = ['alert', 'inform', 'success', 'warn']

    alert._show = 'alert' in types
    inform._show = 'inform' in types
    success._show = 'success' in types
    warn._show = 'warn' in types


def hide(types=None):
    if types is None:
        types = ['alert', 'inform', 'success', 'warn']

    alert._show = 'alert' not in types
    inform._show = 'inform' not in types
    success._show = 'success' not in types
    warn._show = 'warn' not in types


show()
