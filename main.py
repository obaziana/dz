from colorama import init, Fore, Back, Style
init()

a = input(Fore.YELLOW + "a:")

try:
    print(Fore.BLUE + f'{int(a)}')
except ValueError as ve:
    print(Fore.RED + "Неможливо конвертувати в число")
