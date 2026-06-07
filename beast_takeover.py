#!/usr/bin/env python3
import subprocess
import requests
import argparse
import os
import time
from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import track

console = Console()

# Common takeover fingerprints
SIGNATURES = {
    "github": "There isn't a GitHub Pages site here.",
    "aws_s3": "NoSuchBucket",
    "aws_s3_alt": "The specified bucket does not exist",
    "aws_s3_key": "NoSuchKey",
    "azure_removed": "The resource you are looking for has been removed",
    "azure_notfound": "404 Web Site not found",
    "azure_stopped": "This web app has been stopped",
    "heroku": "No such app",
    "heroku_error": "Heroku | Application error",
    "unbounce": "The requested URL was not found on this server",
    "wordpress": "Do you want to register",
    "fastly": "Fastly error: unknown domain",
    "cloudfront": "The requested bucket does not exist",
    "shopify": "Sorry, this shop is currently unavailable",
    "pantheon": "The site you are looking for could not be found",
    "tumblr": "There's nothing here.",
    "bitbucket": "Repository not found",
    "squarespace": "No site configured at this address",
    "zendesk": "Help Center Closed",
    "ghost": "The page you are looking for could not be found",
    "readthedocs": "This page does not exist",
    "surge": "project not found",
    "cargo": "404 Not Found",
    "mashery": "Unrecognized domain",
    "acquia": "Site not found",
    "bigcartel": "Oops! We couldn’t find that shop",
    "tictail": "This store couldn’t be found",
    "helpjuice": "We couldn’t find this page",
    "desk": "This site is no longer available",
}

def print_banner():
    f = Figlet(font="slant")
    banner = f.renderText("BEAST TAKEOVER")
    console.print(f"[bold yellow]{banner}[/bold yellow]")
    console.print("[cyan]Hunt Down Subdomain Takeovers![/cyan]\n")

def run_dig(domain, record_type="A"):
    try:
        result = subprocess.check_output(["dig", domain, record_type, "+short"], stderr=subprocess.DEVNULL)
        return result.decode().strip().splitlines()
    except Exception:
        return []

def check_http(domain):
    try:
        resp = requests.get(f"http://{domain}", timeout=6)
        return resp.status_code, resp.text[:500]
    except Exception as e:
        return None, str(e)

def analyze(domain):
    a_records = run_dig(domain, "A")
    cname_records = run_dig(domain, "CNAME")
    status, body = check_http(domain)

    text = Text()
    text.append(f"[+] Target: {domain}\n", style="bold blue")
    text.append(f"A Records   : {', '.join(a_records) if a_records else 'None'}\n")
    text.append(f"CNAME       : {', '.join(cname_records) if cname_records else 'None'}\n")
    text.append(f"HTTP Status : {status if status else 'Error'}\n")

    takeover = False
    if body:
        for provider, signature in SIGNATURES.items():
            if signature in body:
                takeover = True
                text.append(f"[!] Possible takeover detected ({provider})\n", style="bold red")
                break
    if not takeover:
        text.append("[+] No takeover indicators found\n", style="green")

    color = "red" if takeover else "green"
    console.print(Panel(text, border_style=color))
    return takeover

def clean_url(raw):
    raw = raw.strip()
    if raw.startswith("http://") or raw.startswith("https://"):
        raw = raw.split()[0]
        raw = raw.replace("http://", "").replace("https://", "")
    return raw

def main():
    parser = argparse.ArgumentParser(description="Beast Takeover — Subdomain Takeover Scanner")
    parser.add_argument("domain", nargs="?", help="Single domain to check")
    parser.add_argument("-l", "--list", help="File containing domains list (httpx output)")
    parser.add_argument("-o", "--output", help="Save results to file")
    args = parser.parse_args()

    print_banner()
    results = []

    if args.list:
        if not os.path.exists(args.list):
            console.print(f"[red]File not found: {args.list}[/red]")
            return
        with open(args.list) as f:
            domains = [clean_url(line) for line in f if line.strip()]
        for d in track(domains, description="Scanning for Takeovers..."):
            res = analyze(d)
            results.append((d, res))
            time.sleep(0.3)
    elif args.domain:
        d = clean_url(args.domain)
        res = analyze(d)
        results.append((d, res))
    else:
        parser.print_help()
        return

    if args.output:
        with open(args.output, "w") as f:
            for d, res in results:
                f.write(f"{d} : {'TAKEOVER?' if res else 'Clean'}\n")
        console.print(f"\n[+] Results saved to {args.output}")

    console.print("\n[cyan]-------------- * Stay Hungry. Stay Beastly. * --------------[/cyan]")

if __name__ == "__main__":
    main()
