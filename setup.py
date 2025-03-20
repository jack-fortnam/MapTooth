import hashlib,socket,random,utils
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
    
def out(message,state):
    if state == "ok":
        return f"{bcolours.OKGREEN}{message}{bcolours.ENDC}"
    elif state == "warn":
        return f"{bcolours.WARNING}{message}{bcolours.ENDC}"
    else:
        return f"{bcolours.FAIL}{message}{bcolours.ENDC}"
    
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
        print(out(f"Setting server IP to {ip}","ok"))
        break
    elif ip_choice == 2:
        ip = input("Enter custom IP:\n>>> ")
        if len(ip.split('.')) == 4:
            c = 0
            for x in ip.split('.'):
                if 0 <= int(x) <= 255:
                    c+= 1
            if c ==4:
                print(out(f"Setting server IP to {ip}","ok"))
                break
        print(out("Invalid choice! Please choose again","fail"))
    else:
        print(out("Invalid choice! Please choose again","fail"))

while True:
    port_choice = int(input("PORT\n[1] Default (6785)\n[2] Manual\n>>> "))
    if port_choice == 1:
        print(out("Setting PORT to 6785","ok"))
        break
    elif port_choice == 2:
        port = int(input("Enter custom PORT:\n>>> "))
        if port <= 1000 or port >= 65535:
            print(out("PORT out of range","fail"))
            continue
        print(out(f"Setting PORT to {port}","ok"))
        break
    else:
        print(out("Invalid choice! Please choose again","fail"))

root_user = input("What is the root username?\n>>> ")
while True:
    root_pass = input("What is the root password?\n>>> ")
    if len(root_pass) >= 8:
        print(out("Setting password","ok"))
        break
    else:
        print(out("password too short","fail"))
salt = str(random.randint(10000,999999))

root_pass = utils.encrypt(root_pass,salt)

with open('config.cfg','w') as f:
    config['CORE'] = {'server_ip':ip,'port':port}
    config['USERS'] = {"root":{"user":root_user,"password":root_pass,"salt":salt}}
    print("Writing to file")
    config.write(f)
        