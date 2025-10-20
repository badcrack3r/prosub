#!/usr/bin/env python3
import argparse
import requests
import json
import os
import re
import sys
import time
import random

print("\033[1;36m" + "═" * 55)
print("   🧩  prosub  |  simple CLI tool for Profundis subdomains")
print("        created by \033[1;35mbadcracker\033[1;36m")
print("═" * 55 + "\033[0m\n")

DOMAIN_RE = re.compile(r'^[\.a-z\-\d]+\.[a-z]+$')

def get_api_key():
    key = os.getenv("PROFUNDIS_API_KEY")
    if not key:
        print("\033[1;31m[!] Environment variable PROFUNDIS_API_KEY not set.\033[0m")
        print("Set it using:\nexport PROFUNDIS_API_KEY=your_api_key")
        sys.exit(1)
    return key.strip()

def validate_domain(domain: str) -> str:
    domain = domain.lower().strip()
    if not DOMAIN_RE.fullmatch(domain):
        print(f"\033[1;31m[!] Domain validation failed: {domain}\033[0m")
        return None
    return domain

def fetch_subdomains(key, domain):
    url = "https://api.profundis.io/api/v2/common/data/subdomains"
    headers = {
        "X-API-KEY": key,
        "Accept": "text/event-stream"
    }
    data = {"domain": domain}

    print(f"\033[1;34m[*] Fetching subdomains for {domain}...\033[0m\n")

    try:
        r = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
        if r.status_code != 200:
            print(f"\033[1;31m[!] Error {r.status_code}:\033[0m {r.text}")
            return

        for line in r.iter_lines():
            if line:
                print(line.decode())
    except Exception as e:
        print(f"\033[1;31m[!] Request failed for {domain}:\033[0m {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", action="append", help="Domain to scan (can be used multiple times)")
    parser.add_argument("-f", "--file", help="Path to a file with one domain per line")
    args = parser.parse_args()

    domains = []

    if args.domain:
        domains.extend(args.domain)

    if args.file:
        if not os.path.exists(args.file):
            print(f"\033[1;31m[!] File not found: {args.file}\033[0m")
            sys.exit(1)
        with open(args.file, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    domains.append(line)

    if not domains:
        print("\033[1;33m[!] No domains provided. Use -d or -f.\033[0m")
        sys.exit(1)

    key = get_api_key()

    for i, domain in enumerate(domains, start=1):
        valid_domain = validate_domain(domain)
        if valid_domain:
            fetch_subdomains(key, valid_domain)
            if i < len(domains):
                wait_time = random.uniform(2, 3)
                time.sleep(wait_time)
        else:
            print(f"\033[1;33m[!] Skipping invalid domain: {domain}\033[0m\n")

if __name__ == "__main__":
    main()
