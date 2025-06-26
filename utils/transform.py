import pandas as pd
from datetime import datetime
import re

def transform_data(products):
    try:
        df = pd.DataFrame(products)

        if df.empty:
            print("Data kosong setelah scraping.")
            return pd.DataFrame()

        # Clean Price: convert "$xx" to int Rupiah (multiply by 16000)
        def convert_price(p):
            if not isinstance(p, str) or p.lower() == "price unavailable" or not p.startswith("$"):
                return None
            try:
                return int(float(p.replace("$", "").strip()) * 16000)
            except:
                return None
        df["price"] = df["price"].apply(convert_price)

        def clean_rating(r):
            try:
                r = str(r)
                # Cari angka desimal atau integer di dalam string
                match = re.search(r'(\d+\.\d+|\d+)', r)
                if match:
                    return float(match.group(1))
                return None
            except:
                return None
        df['rating'] = df['rating'].apply(clean_rating)
    
        # Clean Colors: "3 Colors" -> 3
        def clean_colors(c):
            try:
                return int(str(c).split()[0])
            except:
                return None
        df["colors"] = df["colors"].apply(clean_colors)

        # Clean Size & Gender (case-insensitive replace)
        df["size"] = df["size"].str.replace("size: ", "", case=False).str.strip()
        df["gender"] = df["gender"].str.replace("gender: ", "", case=False).str.strip()

        # Tambahkan timestamp (setelah dropna agar tidak terhapus)
        df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Buang produk tidak valid
        df = df[df["title"] != "Unknown Product"]

        # Drop rows dengan nilai null
        df = df.dropna()

        # Hapus duplikat
        df = df.drop_duplicates()

        # Set dtype
        df = df.astype({
            "title": "string",
            "price": "float64",
            "rating": "float64",
            "colors": "int64",
            "size": "string",
            "gender": "string",
            "timestamp": "string"
        })

        print("Transformasi data berhasil. Jumlah data valid:", len(df))
        return df.reset_index(drop=True)

    except Exception as e:
        print(f"Error in transform_data: {e}")
        return pd.DataFrame()