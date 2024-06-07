import subprocess
import re

def get_user_input():
    domain = input("Enter the domain name: ")
    return domain

def run_subfinder(domain):
    print("Running subfinder...")
    subprocess.run(["subfinder", "-d", domain, "-o", "subs.txt"])

def run_httpx():
    print("Resolving subdomains with httpx...")
    subprocess.run(["httpx", "-l", "subs.txt", "-o", "resolved_subs.txt"])

def run_waybackurls(domain):
    print("Fetching URLs from waybackurls...")
    with open("resolved_subs.txt", "r") as file:
        subs = file.read().splitlines()
    
    wayback_urls = set()
    for sub in subs:
        result = subprocess.run(["waybackurls", sub], capture_output=True, text=True)
        wayback_urls.update(result.stdout.splitlines())

    with open("wayback_urls.txt", "w") as file:
        for url in wayback_urls:
            file.write(f"{url}\n")

def filter_urls():
    print("Filtering URLs with parameters...")
    param_urls = set()
    with open("wayback_urls.txt", "r") as file:
        urls = file.read().splitlines()
    
    param_pattern = re.compile(r"(https?://[^?]+)\?([^#]+)")
    for url in urls:
        match = param_pattern.match(url)
        if match:
            base_url = match.group(1)
            params = match.group(2).split("&")
            new_params = [f"{p.split('=')[0]}=*" for p in params]
            new_url = f"{base_url}?{'&'.join(new_params)}"
            param_urls.add(new_url)
    
    with open("output_params.txt", "w") as file:
        for url in param_urls:
            file.write(f"{url}\n")

def main():
    domain = get_user_input()
    run_subfinder(domain)
    run_httpx()
    run_waybackurls(domain)
    filter_urls()
    print("Process completed. Check output_params.txt for the results.")

if __name__ == "__main__":
    main()

