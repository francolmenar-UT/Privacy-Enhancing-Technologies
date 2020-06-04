class bcolors:
    OK = '\033[92m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    yellow = '\033[93m'
    WARN = '\033[93m'
    ERR = '\033[31m'
    UNDERLINE = '\033[4m'
    ITALIC = '\x1B[3m'
    BOLD = '\033[1m'
    LIGHT_BLUE = '\033[34m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    lightcyan = '\033[96m'
    orange = '\033[33m'
    lightred = '\033[91m'

    HEADER = '\033[95m' + BOLD
    PASS = OK + BOLD
    FAIL = ERR + BOLD

    OKMSG = BOLD + OK + u'\u2705' + "  "
    ERRMSG = BOLD + FAIL + u"\u274C" + "  "
    WAITMSG = BOLD + WARN + u'\u231b' + "  "

    HELP = WARN
    BITALIC = BOLD + ITALIC
    BLUEIC = BITALIC + OK
    END = ENDC