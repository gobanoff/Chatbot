from colorama import Back,Fore,Style

with open("example.txt", "w") as file:
    file.write("Hello, Python!")


with open("example.txt", "r") as file:
    content = file.read()

    
    print(content)
    print(Fore.RED + content + Style.BRIGHT)
    print(Fore.YELLOW + content + Style.RESET_ALL)
    print(Fore.GREEN + content + Style.RESET_ALL)
    print(Fore.BLUE + content + Style.RESET_ALL)
    print(Fore.MAGENTA + content + Style.RESET_ALL)
    print(Back.WHITE + Fore.BLACK + content + Style.RESET_ALL)
    print(Back.YELLOW + Fore.RED + content + Style.RESET_ALL)
    print(Back.MAGENTA + Fore.WHITE + content + Style.RESET_ALL)