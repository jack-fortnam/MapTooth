import socket
from configparser import ConfigParser
ip = socket.gethostbyname(socket.gethostname())
port = 6785
class bcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
with open('config.cfg','w') as f:
    pass
config = ConfigParser()
print("""
███╗   ███╗ █████╗ ██████╗ ████████╗ ██████╗  ██████╗ ████████╗██╗  ██╗
████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗╚══██╔══╝██║  ██║
██╔████╔██║███████║██████╔╝   ██║   ██║   ██║██║   ██║   ██║   ███████║
██║╚██╔╝██║██╔══██║██╔═══╝    ██║   ██║   ██║██║   ██║   ██║   ██╔══██║
██║ ╚═╝ ██║██║  ██║██║        ██║   ╚██████╔╝╚██████╔╝   ██║   ██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝    ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝""")
print(f"{bcolours.BOLD}Welcome to MapTooth!")
while True:
    ip_choice = int(input("IP address\n[1] DHCP\n[2] Manual\n>>> "))
    if ip_choice == 1:
        print(f"{bcolours.OKGREEN}Setting server IP to {ip}{bcolours.ENDC}")
        break
    elif ip_choice == 2:
        ip = input("Enter custom IP:\n>>> ")
        print(f"{bcolours.OKGREEN}Setting server IP to {ip}{bcolours.ENDC}")
    else:
        print(f"{bcolours.FAIL}Invalid choice! Please choose again{bcolours.ENDC}")

while True:
    port_choice = int(input("PORT\n[1] Default (6785)\n[2] Manual\n>>> "))
    if port_choice == 1:
        print(f"{bcolours.OKGREEN}Setting PORT to 6785{bcolours.ENDC}")
        break
    elif port_choice == 2:
        port = int(input("Enter custom PORT:\n>>> "))
        if port <= 1000 or port >= 65535:
            print(f"{bcolours.FAIL}PORT out of range{bcolours.ENDC}")
            continue
        print(f"{bcolours.OKGREEN}Setting PORT to {port}{bcolours.ENDC}")
        break
    else:
        print(f"{bcolours.FAIL}Invalid choice! Please choose again{bcolours.ENDC}")  
        