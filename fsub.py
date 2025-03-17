import os
import sys
import requests
import time
import urllib3
import logo
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Define colors for convenience
class colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    WHITEY = "\033[1;37m"
    PINK = "\033[38;5;213m"
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL

version = 0.3

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description="Fsub: A tool to discover subdomains using crt.sh"
    )
    parser.add_argument(
        '-d', '--domain', 
        type=str, 
        required=True, 
        help='Target Domain (e.g., example.com)'
    )
    parser.add_argument(
        '-o', '--output', 
        type=str, 
        required=False, 
        help='Output file to store subdomains'
    )
    return parser.parse_args()

def banner():
    logo.root()
    global version
    print(f"{colors.CYAN}Name: Fsub")
    print(f"{colors.WHITEY}Version: {version}")
    print(f"{colors.WHITEY}Dev: losesec(lose_sec)")
    print(f"{colors.PINK}[✨]Do you wanna buy me a coffee☕? > https://ko-fi.com/lose_sec")
    print("Here We Go🚀")
    time.sleep(1)

def parser_url(url):
    try:
        host = urllib3.util.parse_url(url).host
    except Exception as a:
        print(f"{colors.RED}[*] Invalid domain, try again..")
        sys.exit(1)
    return host

def write_subs_to_file(subdomain, output_file):
    with open(output_file, 'a') as fp:
        fp.write(subdomain + '\n')

def main():
    banner()
    subdomains = []

    args = parse_args()
    target = parser_url(args.domain)
    output = args.output

    req = requests.get(f'https://crt.sh/?q=%.{target}&output=json')
    
    if req.status_code != 200:
        print(f"{colors.RED}[*] Information not available!")
        sys.exit(1)

    for value in req.json():
        subdomains.extend(value["name_value"].split("\n"))
    
    print(f"\n{colors.GREEN}[*] *********** TARGET: {target} ************\n")

    subs = sorted(set(subdomains))

    for s in subs:
        print(f"{colors.YELLOW}[*] {s}{colors.RESET}")
        if output:
            write_subs_to_file(s, output)

    print(f"\n\n{colors.GREEN}[**] Fsub is complete, all subdomains have been found.{colors.RESET}")

if __name__ == '__main__':
    main()
