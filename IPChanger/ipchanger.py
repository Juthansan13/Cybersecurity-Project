import os
import subprocess
import platform
import time
import random
import re

BLUE = '\033[94m'
RESET = '\033[0m'

# Clear screen
os.system("clear")

# Banner
print(f"""{BLUE}
    ______________________________________________________________
  |  ___ ____        ____ _   _    _    _   _  ____ _____ ____   |
  | |_ _|  _ \      / ___| | | |  / \  | \ | |/ ___| ____|  _ \  |
  |  | || |_) |____| |   | |_| | / _ \ |  \| | |  _|  _| | |_) | |
  |  | ||  __/_____| |___|  _  |/ ___ \| |\  | |_| | |___|  _ <  |
  | |___|_|         \____|_| |_/_/   \_\_| \_|\____|_____|_| \_\ |
  |______________________________________________________________|
                                                                                                       
{RESET}""")


def install_packages():
    try:
        with open("/etc/os-release") as f:
            content = f.read()
            match = re.search(r'NAME="(.+?)"', content)
            distro = match.group(1) if match else "Unknown"
    except Exception:
        print("Could not determine Linux distribution.")
        return

    if any(name in distro for name in ["Ubuntu", "Debian", "Kali"]):
        subprocess.run(["apt-get", "update"])
        subprocess.run(["apt-get", "install", "-y", "curl", "tor"])
    elif any(name in distro for name in ["Fedora", "CentOS", "Red Hat", "Amazon Linux"]):
        subprocess.run(["yum", "update"])
        subprocess.run(["yum", "install", "-y", "curl", "tor"])
    elif "Arch" in distro:
        subprocess.run(["pacman", "-S", "--noconfirm", "curl", "tor"])
    else:
        print(f"Unsupported distro: {distro}")
        exit(1)


def is_installed(command):
    return subprocess.call(["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


# Install curl and tor if not available
if not is_installed("curl") or not is_installed("tor"):
    print("Installing curl and tor...")
    install_packages()

# Start tor service if not running
status = subprocess.run(["systemctl", "--quiet", "is-active", "tor.service"])
if status.returncode != 0:
    print("Starting tor service...")
    subprocess.run(["systemctl", "start", "tor.service"])


def get_ip():
    try:
        result = subprocess.run(["curl", "-s", "-x", "socks5h://127.0.0.1:9050", "https://checkip.amazonaws.com"],
                                capture_output=True, text=True)
        ip_match = re.search(r"\d+\.\d+\.\d+\.\d+", result.stdout)
        return ip_match.group() if ip_match else "Unknown"
    except Exception:
        return "Error retrieving IP"


def change_ip():
    print("Reloading tor service...")
    subprocess.run(["systemctl", "reload", "tor.service"])
    print(f"{BLUE}New IP address: {get_ip()}{RESET}")


# User input
try:
    interval = int(input(f"{BLUE}Enter time interval in seconds (type 0 for random): {RESET}"))
    times = int(input(f"{BLUE}Enter number of times to change IP address (type 0 for infinite): {RESET}"))
except ValueError:
    print("Invalid input.")
    exit(1)

print()

# Run loop
if interval == 0 or times == 0:
    print("Starting infinite IP changes...")
    while True:
        change_ip()
        sleep_time = random.randint(10, 20)
        time.sleep(sleep_time)
else:
    for _ in range(times):
        change_ip()
        time.sleep(interval)
