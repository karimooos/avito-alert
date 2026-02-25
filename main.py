import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
SEARCH_URL = os.environ.get("SEARCH_URL")

DATA_FILE = "seen_links.txt"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

# Load seen links
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        seen_links = set(line.strip() for line in f.readlines())
else:
    seen_links = set()

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(SEARCH_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

ads = soup.find_all("a", href=True)

current_links = set()

for ad in ads:
    link = ad["href"]

    if "/voitures_d_occasion/" in link:
        full_link = "https://www.avito.ma" + link
        current_links.add(full_link)

        title = ad.get_text(strip=True)

        if full_link not in seen_links:
            send_telegram(f"🚗 Nouvelle annonce:\n{title}\n{full_link}")

# Keep only last 500 links
updated_links = list(seen_links.union(current_links))[-500:]

with open(DATA_FILE, "w") as f:
    for link in updated_links:
        f.write(link + "\n")
