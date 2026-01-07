from bs4 import BeautifulSoup
from urllib.parse import urlparse
from args import args
import shodanurls
import request_shodan
import random
import os
from colorama import Fore
import time
from pathlib import Path

found_hosts = set()
home = Path.home()

print(Fore.CYAN + "[*] Script started..." + Fore.RESET)

# ---- output file ----
output_file_path = None
if not args.no_output:
    home_dir = Path.home()
    os.makedirs(f"{home_dir}/shodan4all/logs", exist_ok=True)
    output_file_path = f"{home_dir}/shodan4all/logs/{random.randint(1, 8000)}.txt"

total_devices = None
stats_printed = False

# ---- main loop ----
for url in shodanurls.shodan_urls:
    query=url[29:100]
    query=query.replace("%20"," ")
    query=query.replace("&"," ")
    r = request_shodan.session.get(url, timeout=600)

    if "Please log in to use search filters" in r.text:
        print(Fore.RED + "Seems like your cookies were not recognized, please check its integrity." + Fore.RESET)
        exit()

    if "No results found" in r.text:
        print(Fore.RED + f"Your query returned no results. Query:{query}" + Fore.RESET)
        continue

    time.sleep(args.sleep)
    soup = BeautifulSoup(r.text, "html.parser")

    # ---- total devices (print ONCE at start) ----
    if not stats_printed:
        total_tag = soup.select_one("h4.total-results")
        if total_tag:
            total_devices = total_tag.text.strip()
            print(
                Fore.CYAN
                + f"[+] Total devices reported by Shodan: {total_devices}"
                + Fore.RESET
            )
            stats_printed = True

    # ---- results ----
    for result in soup.select("div.result"):
        host_link = result.select_one('a[href^="/host/"]')
        ext_link = result.select_one('a[href^="http"]')

        if not host_link or not ext_link:
            continue

        ip = host_link["href"].split("/host/")[1]

        parsed = urlparse(ext_link["href"])
        port = parsed.port or (443 if parsed.scheme == "https" else 80)

        combo = f"{ip}:{port}"

        if combo in found_hosts:
            continue

        # ---- country detection ----
        country = "Unknown"
        flag = result.select_one("img.flag")
        if flag and flag.get("title"):
            country = flag["title"]

        # ---- honeypot detection ----
        honeypot = any(
            tag.text.strip().lower() == "honeypot"
            for tag in result.select("a.tag")
        )

        found_hosts.add(combo)

        # ---- output ----
        if not args.no_output:
            if not args.allow_honeypot and honeypot != True:
                with open(output_file_path, "a", encoding="utf-8") as f:
                    f.write(f"{combo}\n")
            elif args.allow_honeypot:
                with open(output_file_path, "a", encoding="utf-8") as f:
                    f.write(f"{combo}\n")

        if not args.silent:
            print(
                Fore.GREEN
                + f"[+] Found: {combo} | {country} | honeypot={honeypot} | '{query}'"
                + Fore.RESET
            )

# ---- summary ----
print(
    Fore.CYAN
    + f"\nTotal unique services found: {len(found_hosts)}"
    + (f"\nSaved to: {output_file_path}" if output_file_path else "")
    + Fore.RESET
)
