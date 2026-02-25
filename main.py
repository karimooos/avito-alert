import requests
from bs4 import BeautifulSoup
import time

TOKEN = "8763454421:AAEA7zUmLVkXLBE6Hqty6RhdGwC9YvB2LcA"
CHAT_ID = "1664966725"
SEARCH_URL = "https://www.avito.ma/fr/maroc/voitures_d_occasion-%C3%A0_vendre?brand=49&model=megane&brand_model=49_megane&price=125000-145000&fuel=1&regdate=2017-2022&seller_type=0&has_price=true"

sent_links = set()

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

while True:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(SEARCH_URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        ads = soup.find_all("a", href=True)

        for ad in ads:
            link = ad["href"]

            if "/voitures_d_occasion/" in link:
                full_link = "https://www.avito.ma" + link

                if full_link not in sent_links:
                    sent_links.add(full_link)

                    title = ad.get_text(strip=True)

                    if "Megane" in title:
                        message = f"🚗 Nouvelle annonce:\n{title}\n{full_link}"
                        send_telegram(message)

        time.sleep(300)

    except Exception as e:
        print("Error:", e)
        time.sleep(300)