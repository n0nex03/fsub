import os
import sys
import requests
import time
import urllib3
import logo  # Ensure this is correctly defined elsewhere
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Define colors for convenience
class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    WHITEY = "\033[1;37m"
    PINK = "\033[38;5;213m"
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL

VERSION = 0.5

# List of country-specific TLDs to exclude
EXCLUDED_TLDS = {
    ".af", ".ag", ".ai", ".ar", ".au", ".bd", ".bh", ".bn", ".bo", ".br", ".by",
    ".bz", ".cn", ".co", ".cu", ".cy", ".do", ".ec", ".eg", ".et", ".fj", ".ge",
    ".gh", ".gi", ".gr", ".gt", ".hk", ".iq", ".jm", ".jo", ".kh", ".kw", ".lb",
    ".ly", ".mm", ".mt", ".mx", ".my", ".na", ".nf", ".ng", ".ni", ".np", ".nr",
    ".om", ".pa", ".pe", ".pg", ".ph", ".pk", ".pl", ".pr", ".py", ".qa", ".ru",
    ".sa", ".sb", ".sg", ".sl", ".sv", ".tj", ".tn", ".tr", ".tw", ".ua", ".uy",
    ".vc", ".ve", ".vn"
}

def parse_args():
    """Parse command-line arguments."""
    import argparse
    parser = argparse.ArgumentParser(description="Fsub: A tool to discover subdomains using crt.sh")
    parser.add_argument(
        '-d', '--domain', 
        type=str, 
        required=True, 
        help='Target Domain (e.g., example.com)'
    )
    parser.add_argument(
        '-o', '--output', 
        type=str, 
        help='Output file to store subdomains'
    )
    return parser.parse_args()

def banner():
    """Display the banner information."""
    logo.root()  # Ensure your logo function is correctly defined
    print(f"{Colors.CYAN}Name: Fsub")
    print(f"{Colors.WHITEY}Version: {VERSION}")
    print(f"{Colors.WHITEY}Dev: lose(n0nex03)")
    print(f"{Colors.PINK}[✨] Do you wanna buy me a ₿itcoin? > '3Fa938teyhMwyRMGwaiaBwEkL1EJiTJAPJ'")
    time.sleep(1)

def parse_url(url):
    """Extract the host from the given URL."""
    try:
        return urllib3.util.parse_url(url).host
    except Exception:
        print(f"{Colors.RED}[*] Invalid domain, please try again..")
        sys.exit(1)

def write_subdomains_to_file(subdomains, output_file):
    """Write subdomains to an output file."""
    try:
        with open(output_file, 'a') as file:
            file.writelines([f"{sub}\n" for sub in subdomains])
    except Exception as e:
        print(f"{Colors.RED}[*] Error writing to file: {e}")

def filter_subdomains(subdomains):
    """Filter out subdomains with excluded TLDs."""
    filtered_subdomains = []
    for sub in subdomains:
        # Check if the subdomain has an excluded TLD
        if not any(sub.endswith(tld) for tld in EXCLUDED_TLDS):
            filtered_subdomains.append(sub)
    return filtered_subdomains

def main():
    """Main execution logic."""
    banner()
    subdomains = set()  # Using a set to store unique subdomains

    args = parse_args()
    target = parse_url(args.domain)
    output_file = args.output

    try:
        req = requests.get(f'https://crt.sh/?q=%.{target}&output=json')
        req.raise_for_status()  # Will raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}[*] Request failed: {e}")
        sys.exit(1)

    # Parse the JSON response and extract subdomains
    try:
        subdomains_data = req.json()
        for entry in subdomains_data:
            subdomains.update(entry["name_value"].split("\n"))
    except ValueError:
        print(f"{Colors.RED}[*] Error parsing JSON response.")
        sys.exit(1)

    print(f"\n{Colors.GREEN}[*] *********** TARGET: {target} ************\n")

    # Filter subdomains based on TLD
    filtered_subdomains = filter_subdomains(sorted(subdomains))

    # Print and write filtered subdomains
    for subdomain in filtered_subdomains:
        print(f"{Colors.YELLOW}[*] https://{subdomain}{Colors.RESET}")
        if output_file:
            write_subdomains_to_file([subdomain], output_file)

    print(f"\n\n{Colors.GREEN}[**] Fsub is complete, all subdomains have been found.{Colors.RESET}")

if __name__ == '__main__':
    main()
