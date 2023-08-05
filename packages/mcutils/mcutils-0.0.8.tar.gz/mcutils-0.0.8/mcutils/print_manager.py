import colorama, sys

class Color_Settings:
    is_dev=False
    print_color=True

class Color:
    BLUE = colorama.Fore.BLUE
    RED = colorama.Fore.RED
    GREEN = colorama.Fore.GREEN
    CYAN = colorama.Fore.CYAN
    BLACK = colorama.Fore.BLACK
    YELLOW = colorama.Fore.YELLOW
    MAGENTA = colorama.Fore.MAGENTA
    WHITE = colorama.Fore.WHITE
    RESET = colorama.Fore.RESET

def mcprint(text="", format="", color=None, end="\n"):
    if not Color_Settings.is_dev:
        colorama.init(convert=True)

    text = "{}{}".format(format, text)
    if color and Color_Settings.print_color==True:
        text = "{}{}{}".format(color, text, colorama.Fore.RESET)
    print(text, end=end)


def progress_bar(current_index, total, text="", length=100, symbol_a="+", symbol_b="-"):
    percentage = 0
    if isinstance(total, range) or isinstance(total, list) or isinstance(total, tuple):
        percentage = (current_index + 1)/len(total)
    elif isinstance(total, int):
        percentage = (current_index + 1)/(total)
    else:
        raise TypeError("Type: {} is not permited".format(type(total)))

    print("\r", end="")

    n_ok = int(length*(int(percentage*100)/100.0))
    n_nok = length - n_ok


    progress = "{}{}{}".format(Color.GREEN, symbol_a*n_ok, Color.RESET) + "{}{}{}".format(Color.RED, symbol_b*n_nok, Color.RESET)
    print("[{:>5}%]".format("{:01.1f}".format(percentage*100))+" {}\t[{}]".format(text, progress), end="")