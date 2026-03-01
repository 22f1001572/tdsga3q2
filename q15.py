import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://sanand0.github.io/tdsdata/crawl_html/"
start_url = base_url + "index.html"

visited = set()
to_visit = [start_url]

while to_visit:
    url = to_visit.pop(0)
    if url in visited:
        continue
    visited.add(url)
    print(f"Visiting ({len(visited)}): {url}")  # track progress
    
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            full_url = urljoin(url, a["href"])
            if full_url.startswith(base_url) and full_url not in visited:
                to_visit.append(full_url)
    except:
        pass

pz_files = [f for f in visited if "P" <= f.split("/")[-1][0].upper() <= "Z"]
print(f"\nTotal crawled: {len(visited)}")
print(f"Files P-Z: {len(pz_files)}")