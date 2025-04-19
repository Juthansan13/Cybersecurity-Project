import requests
from concurrent.futures import ThreadPoolExecutor

# Banner
def banner():
    print(r"""
_______________________________________________________________
|   ____        _     _                         _              |
|  / ___| _   _| |__ | | ___  _ __ ___   ___   (_) ___  _ __   |
|  \___ \| | | | '_ \| |/ _ \| '_ ` _ \ / _ \  | |/ _ \| '_ \  |
|   ___) | |_| | |_) | | (_) | | | | | |  __/  | | (_) | | | | |
|  |____/ \__,_|_.__/|_|\___/|_| |_| |_|\___| _/ |\___/|_| |_| |
|                                             |__/             |
|______________________________________________________________|
  
  [+] Tool: Fast Subdomain Finder
    """)

# Subdomain checking function
def check_subdomain(domain, subdomain):
    url = f"http://{subdomain}.{domain}"
    try:
        response = requests.get(url, timeout=1)
        return url
    except requests.RequestException:
        return None

# Main function
def main():
    banner()
    domain = input("Enter target domain (e.g., example.com): ").strip()

    wordlist = [
        "www", "mail", "ftp", "dev", "api", "blog", "admin", "shop", "webmail", "cpanel",
        "test", "beta", "secure", "vpn", "portal", "staging", "dashboard", "upload"
    ]

    found = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(check_subdomain, domain, sub) for sub in wordlist]

        for future in futures:
            result = future.result()
            if result:
                print(f"[+] Found: {result}")
                found.append(result)

    print(f"\n[✓] Scan Complete! {len(found)} subdomains found.")

if __name__ == "__main__":
    main()