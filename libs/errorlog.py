import colorama

# Make an error log
elog = []

def add(error: str) -> None:
    elog.append(error)


def fetch() -> list[str]:
    return elog


def show():
    if not elog:
        print(f"{colorama.Fore.GREEN}*** No errors found ***{colorama.Style.RESET_ALL}")
    else:
        print(f"{colorama.Fore.RED}")
        print("*** ERRORS WERE FOUND ***")
        print("")
        for error in elog:
            print(error)
        print(f"{colorama.Style.RESET_ALL}")
        