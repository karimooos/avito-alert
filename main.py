import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
SEARCH_URL = os.environ.get("SEARCH_URL")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(SEARCH_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

ads = soup.find_all("a", href=True)

for ad in ads:
    link = ad["href"]

    if "/voitures_d_occasion/" in link:
        full_link = "https://www.avito.ma" + link
        title = ad.get_text(strip=True)

        parent = ad.find_parent()
        text_block = parent.get_text(" ", strip=True)

        # نتحقق واش فيه minutes
        if "minute" in text_block.lower():
            send_telegram(f"🚗 Nouvelle annonce:\n{title}\n{full_link}")
