
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


def write(text, *args, style=Style.INFORM):
    adapter = Colors.CYAN
    for i, value in enumerate(args):
        old = '<<' + str(i) + '>>'
        new = f'{adapter}{args[i]}{Colors.ENDC}'
        text = text.replace(old, new)
    print(text)


def color_print(text, color=None):
    if color:
        print(color + text + Colors.ENDC)
    else:
        print(text)


def alert(text):
    color_print(text, color=Colors.FAIL)


def warn(text):
    color_print(text, color=Colors.WARNING)


def success(text):
    color_print(text, color=Colors.OKGREEN)


def inform(text):
    color_print(text, color=Colors.OKBLUE)
