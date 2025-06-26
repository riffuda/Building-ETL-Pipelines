import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as err:
        print(f"[ERROR] Failed to access: {url} → {err}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all("div", class_="collection-card")
    if not cards:
        print("[INFO] No products found.")
        return []

    data = []
    for card in cards:
        title = card.find("h3", class_="product-title")
        price = card.find("span", class_="price")

        specs = {
            "rating": "N/A",
            "colors": "N/A",
            "size": "N/A",
            "gender": "N/A"
        }

        for p in card.find_all("p", style=lambda s: s and "font-size" in s):
            text = p.text.strip().lower()
            if "rating:" in text:
                specs["rating"] = text.replace("rating:", "").strip()
            elif "colors" in text:
                specs["colors"] = p.text.strip()
            elif "size:" in text:
                specs["size"] = text.replace("size:", "").strip()
            elif "gender:" in text:
                specs["gender"] = text.replace("gender:", "").strip()

        data.append({
            "title": title.text.strip() if title else "Unknown",
            "price": price.text.strip() if price else "Unavailable",
            "rating": specs["rating"],
            "colors": specs["colors"],
            "size": specs["size"],
            "gender": specs["gender"],
            "timestamp": datetime.now().isoformat()
        })

    return data

if __name__ == "__main__":
    url = "https://fashion-studio.dicoding.dev/page2"
    for product in scrape_page(url):
        print(product)
