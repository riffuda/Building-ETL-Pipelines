def save_to_csv(dataframe, path="cleaned_data.csv"):
    try:
        dataframe.to_csv(path, index=False)
        print(f"[INFO] CSV saved to: {path}")
    except Exception as err:
        print(f"[ERROR] Failed to save CSV: {err}")
