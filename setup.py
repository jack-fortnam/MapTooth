import socket
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
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
print("""
███╗   ███╗ █████╗ ██████╗ ████████╗ ██████╗  ██████╗ ████████╗██╗  ██╗
████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗╚══██╔══╝██║  ██║
██╔████╔██║███████║██████╔╝   ██║   ██║   ██║██║   ██║   ██║   ███████║
██║╚██╔╝██║██╔══██║██╔═══╝    ██║   ██║   ██║██║   ██║   ██║   ██╔══██║
██║ ╚═╝ ██║██║  ██║██║        ██║   ╚██████╔╝╚██████╔╝   ██║   ██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝    ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝""")
print(f"{bcolours.BOLD}Welcome to MapTooth!")
ip_choice = int(input("DHCP or Manual?\n[1] DHCP\n[2] Manual\n>>> "))
match ip_choice:
    case 1:
        print(f"{bcolours.OKGREEN}Setting server IP to {ip}")
    case 2:
        ip = input("Enter custom IP:\n>>> ") 
        