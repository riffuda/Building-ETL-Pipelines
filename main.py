from utils.extract import scrape_page
from utils.transform import transform
from utils.load import export_csv, export_postgres, export_sheet

BASE_URL = "https://fashion-studio.dicoding.dev"

def fetch_all_pages():
    all_data = []

    print("[INFO] Fetching products from main page...")
    try:
        all_data += scrape_page(url=BASE_URL)
    except Exception as err:
        print(f"[ERROR] Main page fetch failed: {err}")

    for page in range(2, 51):
        page_url = f"{BASE_URL}/page{page}"
        print(f"[INFO] Fetching page {page}...")
        try:
            all_data += scrape_page(url=page_url)
        except Exception as err:
            print(f"[ERROR] Page {page} fetch failed: {err}")

    return all_data

def main():
    print("[INFO] Starting scraping workflow...")

    raw = fetch_all_pages()
    if not raw:
        print("[WARN] No data collected from any page.")
        return

    print(f"[INFO] Total products fetched: {len(raw)}")

    df = transform(raw)
    if df.empty:
        print("[WARN] Data transformation returned empty result.")
        return

    print("[INFO] Preview of transformed data:")
    print(df.head())

    export_csv(df)
    export_postgres(df)
    export_sheet(df, name='scraped_products')

if __name__ == '__main__':
    main()