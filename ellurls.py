# Enhanced URL Gathering Tool (Python)

import subprocess
import os
import re
import argparse
import requests
import time
from colorama import init
from termcolor import colored
from threading import Thread
from itertools import cycle

# Loader animation
def loader_animation(message="Processing..."):
    animation = cycle(["|", "/", "-", "\\"])
    while not stop_loader:
        print(f"\r{message} {next(animation)}", end="")
        time.sleep(0.1)
    print("\r" + " " * len(message) + "\r", end="")  # Clear the line


import sys
from pyfiglet import Figlet

def animated_print(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_ascii_art():
    f = Figlet(font='slant')  # You can choose other fonts too
    ascii_art_lines = f.renderText('ELL URLS').split('\n')
    
    # Animate line by line
    for line in ascii_art_lines:
        print(line)
        time.sleep(0.2)
    
    # Print subtitle normally
    subtitle = "Most Powerful URLS Gathering Tool"
    animated_print(subtitle, delay=0.05)

print_ascii_art()


# Load extensions from file
def load_extensions_from_file(file_path='extensions.txt'):
    try:
        with open(file_path, 'r') as f:
            extensions = [line.strip() for line in f.readlines() if line.strip()]
        return extensions
    except FileNotFoundError:
        print(colored(f"{file_path} not found. Proceeding with no extensions.", "red"))
        return []

# Load domains from file
def load_domains_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            domains = [line.strip() for line in f.readlines() if line.strip()]
        return domains
    except FileNotFoundError:
        print(colored(f"{file_path} not found. Exiting.", "red"))
        exit()

# Fetch URLs using The Wayback Machine API with streaming and backoff
def fetch_urls(target, file_extensions):
    print(f"\nFetching URLs from The Time Machine Lite for {target}...")
    archive_url = f'https://web.archive.org/cdx/search/cdx?url=*.{target}/*&output=txt&fl=original&collapse=urlkey&page=/'

    global stop_loader
    stop_loader = False
    loader_thread = Thread(target=loader_animation, args=("Fetching URLs...",))
    loader_thread.start()

    max_retries = 3
    retry_delay = 5
    attempt = 0

    while attempt < max_retries:
        try:
            with requests.get(archive_url, stream=True, timeout=60) as response:
                response.raise_for_status()
                print(colored("\nStreaming response from archive...", "green"))

                url_list = []
                total_lines = 0
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        url_list.append(line)
                        total_lines += 1
                        if total_lines % 1000 == 0:
                            print(f"\rFetched {total_lines} URLs...", end="")

                print(colored(f"\nFetched {total_lines} URLs from archive.", "green"))
                stop_loader = True
                loader_thread.join()
                return {ext: [url for url in url_list if url.lower().endswith(ext.lower())] for ext in file_extensions}
        except requests.exceptions.RequestException as e:
            attempt += 1
            if attempt < max_retries:
                print(colored(f"\nAttempt {attempt} failed: {e}. Retrying in {retry_delay} seconds...", "yellow"))
                time.sleep(retry_delay)
            else:
                print(colored(f"\nError fetching URLs after {max_retries} attempts: {e}", "red"))
                print(colored("The server may be rate-limiting or refusing connections.", "yellow"))
                print(colored("Pausing for 5 minutes before continuing...", "yellow"))
                time.sleep(300)
                print(colored("Resuming...", "green"))
                return {}

# Check for archived snapshots
#def check_wayback_snapshot(url):
    #wayback_url = f'https://archive.org/wayback/available?url={url}'
    #try:
        #response = requests.get(wayback_url, timeout=5)
        #response.raise_for_status()
        #data = response.json()
        #if "archived_snapshots" in data and "closest" in data["archived_snapshots"]:
            #snapshot_url = data["archived_snapshots"]["closest"].get("url")
            #if snapshot_url:
                #print(f"[+] Found possible backup: {colored(snapshot_url, 'green')}")
        #else:
            #print(f"[-] No archived snapshot found for {url}.")
    #except Exception as e:
        #print(f"[?] Error checking Wayback snapshot for {url}: {e}")

# Save filtered URLs
def save_urls(target, extension_stats, file_suffix="_filtered_urls.txt"):
    folder = f"content/{target}"
    os.makedirs(folder, exist_ok=True)
    all_filtered_urls = []
    for ext, urls in extension_stats.items():
        if urls:
            file_path = os.path.join(folder, f"{target}_{ext.strip('.')}{file_suffix}")
            with open(file_path, 'w') as file:
                file.write("\n".join(urls))
            all_filtered_urls.extend(urls)
            print(f"Filtered URLs for {ext} saved to: {colored(file_path, 'green')}")
    return all_filtered_urls

# Process domain
def process_domain(target, file_extensions):
    extension_stats = fetch_urls(target, file_extensions)
    if not extension_stats:
        print(colored(f"No URLs fetched for {target}. Skipping...", "yellow"))
        return
    all_filtered_urls = save_urls(target, extension_stats)
    for url in all_filtered_urls:
        check_wayback_snapshot(url)

# Run external URL tools
def run_command(name, command, temp_file, url_set):
    print(f"[+] Running {name}...")
    try:
        subprocess.run(command, shell=True, check=True)
        with open(temp_file, "r") as f:
            for line in f:
                line = line.strip()
                if re.match(r"https?://", line):
                    url_set.add(line)
    except subprocess.CalledProcessError:
        print(f"[!] {name} failed or not installed. Skipping.")
    except FileNotFoundError:
        print(f"[!] Output file for {name} not found. Skipping.")

# Enhanced mode
def run_enhanced_url_gathering(domain):
    temp_files = {
        "gau": "temp_gau.txt",
        "waybackurls": "temp_waybackurls.txt",
        "hakrawler": "temp_hakrawler.txt",
        "katana": "temp_katana.txt",
        "xnLinkFinder": "temp_xnlinkfinder.txt",
        "waybackpy": "temp_waybackpy.txt",
        "paramspider": "temp_paramspider.txt",
    }

    commands = {
        "gau": f"gau {domain} > {temp_files['gau']}",
        "waybackurls": f"echo {domain} | waybackurls > {temp_files['waybackurls']}",
        "hakrawler": f"hakrawler -url https://{domain} -depth 2 -plain > {temp_files['hakrawler']}",
        "katana": f"katana -u https://{domain} -silent -o {temp_files['katana']}",
        "xnLinkFinder": f"python3 xnLinkFinder.py -i https://{domain} -o {temp_files['xnLinkFinder']} > /dev/null 2>&1",
        "waybackpy": f"waybackpy --url https://{domain} --urls > {temp_files['waybackpy']}",
        "paramspider": f"paramspider --domain {domain} --quiet > {temp_files['paramspider']}"
    }

    url_set = set()
    for tool, cmd in commands.items():
        run_command(tool, cmd, temp_files[tool], url_set)

    output_file = f"enhanced_output_{domain}.txt"
    with open(output_file, "w") as f:
        for url in sorted(url_set):
            f.write(f"{url}\n")
    for temp in temp_files.values():
        if os.path.exists(temp):
            os.remove(temp)
    print(colored(f"\n✅ All enhanced URLs saved to: {output_file}", "green"))

    return url_set

# Main execution
if __name__ == "__main__":
    init()
    print(colored('    Developed by Tanvir Ahammed\n', 'green'))

    mode = input("Select mode (1: Single Domain, 2: Multiple Domains): ").strip()
    if mode == "1":
        target = input("\nEnter the target domain (e.g., example.com): ").strip()
        if not target:
            print(colored("Target domain is required. Exiting.", "red"))
            exit()
        domains = [target]
    elif mode == "2":
        domain_file = input("\nEnter the path to the file containing domain list: ").strip()
        domains = load_domains_from_file(domain_file)
        print(f"Loaded {len(domains)} domains from {colored(domain_file, 'green')}.")
    else:
        print(colored("Invalid choice. Exiting.", "red"))
        exit()

    default_extensions = load_extensions_from_file()
    choice = input("Use custom file extensions or load from extensions.txt? (custom/load): ").strip().lower()
    if choice == "custom":
        file_extensions = input("Enter file extensions to filter (e.g., .zip,.pdf): ").strip().split(",")
    elif choice == "load" and default_extensions:
        file_extensions = default_extensions
    else:
        print(colored("No extensions found. Exiting.", "red"))
        exit()

    all_unique_urls = set()

    for target in domains:
        print(colored(f"\nProcessing domain: {target}", "blue"))
        process_domain(target, file_extensions)
        url_set = run_enhanced_url_gathering(target)
        all_unique_urls.update(url_set)

    unique_file = input("\nEnter the filename to save the UNIQUE results (default: unique_results.txt): ").strip()
    if not unique_file:
        unique_file = "unique_results.txt"

    with open(unique_file, "w") as uf:
        for url in sorted(all_unique_urls):
            uf.write(f"{url}\n")

    print(colored(f"\n✅ Unique URLs saved to: {unique_file}", "green"))
    print(colored("\nProcess complete for all domains.", "green"))
