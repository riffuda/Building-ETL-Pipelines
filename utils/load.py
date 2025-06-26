import pandas as pd
from sqlalchemy import create_engine
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def export_csv(df: pd.DataFrame, path='products.csv'):
    try:
        df.to_csv(path, index=False)
        print(f"[INFO] CSV saved to: {path}")
    except Exception as err:
        print(f"[ERROR] Failed to save CSV: {err}")

def export_postgres(df: pd.DataFrame, table='products'):
    try:
        engine = create_engine("postgresql://postgres:postgresqlku@localhost:5432/etl_db")
        df.to_sql(table, engine, if_exists='replace', index=False)
        print(f"[INFO] Data written to PostgreSQL table: {table}")
    except Exception as err:
        print(f"[ERROR] PostgreSQL write failed: {err}")

def export_sheet(df: pd.DataFrame, name='Scraped Products'):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'google-sheets-api.json', scope
        )
        client = gspread.authorize(creds)

        sheet = client.create(name)
        sheet.share(None, perm_type='anyone', role='writer')

        worksheet = sheet.sheet1
        data = [df.columns.tolist()] + df.values.tolist()
        worksheet.update(data)

        print(f"[INFO] Data uploaded to Google Sheets: {sheet.url}")
    except Exception as err:
        print(f"[ERROR] Google Sheets export failed: {err}")
