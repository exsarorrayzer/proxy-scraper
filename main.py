import os
import requests
from datetime import datetime
from rich import print


def timestamp():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[bold magenta][{now}][/bold magenta]"


def clean_proxies(text):
    lines = text.splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if 'socks5' in line.lower():
            continue
        if "://" in line:
            line = line.split("://", 1)[-1]

        if line.count(":") >= 2:
            parts = line.split(":")
            ip, port = parts[0], parts[1]
            if ip.replace('.', '').isdigit() and port.isdigit():
                cleaned.append(f"{ip}:{port}")
        elif line.count(":") == 1:
            ip, port = line.split(":")
            if ip.replace('.', '').isdigit() and port.isdigit():
                cleaned.append(f"{ip}:{port}")

    return cleaned


def fetch_proxies(urls):
    all_raw = ""

    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                all_raw += r.text + "\n"
                print(f"{timestamp()} [green]Fetched from {url}[/green]")
            else:
                print(f"{timestamp()} [red]Failed {url} (status: {r.status_code})[/red]")
        except Exception as e:
            print(f"{timestamp()} [red]Error fetching {url} - {e}[/red]")

    proxies = clean_proxies(all_raw)
    with open("proxies.txt", "w") as f:
        f.write("\n".join(proxies))

    print(f"{timestamp()} [cyan]Saved {len(proxies)} proxies to proxies.txt[/cyan]")


def load_links():
    if not os.path.exists("scr_rep.txt"):
        print("[red]scr_rep.txt not found![/red]")
        return []
    with open("scr_rep.txt") as f:
        return [line.strip() for line in f if line.strip()]


if __name__ == "__main__":
    fetch_proxies(load_links())
