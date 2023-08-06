
class bcolors:
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


def write(text, *args):
    adapter = bcolors.CYAN
    for i, value in enumerate(args):
        old = '<<' + str(i) + '>>'
        new = f'{adapter}{args[i]}{bcolors.ENDC}'
        text = text.replace(old, new)
    print(text)
