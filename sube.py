import concurrent.futures
import requests
import argparse
import sys
from termcolor import colored
from pyfiglet import Figlet

def check_subdomain(subdomain):
    protocols = ["http://", "https://"]
    for protocol in protocols:
        try:
            response = requests.get(protocol + subdomain, timeout=3)
            if response.status_code == 200:
                print(colored("[+] Found: " + protocol + subdomain, "green"))
                break
        except:
            pass

def enumerate_subdomains(domain, wordlist):
    subdomains = []
    with open(wordlist, "r") as wordlist_file:
        for line in wordlist_file:
            subdomain = line.strip() + "." + domain
            subdomains.append(subdomain)

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_subdomain = {executor.submit(check_subdomain, subdomain): subdomain for subdomain in subdomains}
        for future in concurrent.futures.as_completed(future_to_subdomain):
            subdomain = future_to_subdomain[future]
            try:
                future.result()
            except Exception as exc:
                print(colored("[-] Exception: %s" % exc, "red"))

if __name__ == "__main__":
    custom_fig = Figlet(font='block')
    print(colored(custom_fig.renderText('SUBFUzZ'), "yellow"))

    parser = argparse.ArgumentParser(description="Subdomain enumeration tool")
    parser.add_argument("-d", "--domain", type=str, help="Target domain name", required=True)
    parser.add_argument("-w", "--wordlist", type=str, help="Wordlist file", required=True)
    args = parser.parse_args()

    domain = args.domain
    wordlist = args.wordlist

    enumerate_subdomains(domain, wordlist)

