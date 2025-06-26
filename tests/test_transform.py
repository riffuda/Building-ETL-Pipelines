import pandas as pd

def transform(data):
    df = pd.DataFrame(data)

    # Filter: remove missing, duplicates, and unknown products
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df = df[df['Title'] != 'Unknown Product'].reset_index(drop=True)

    # Convert price to float and IDR
    df['Price'] = (
        df['Price']
        .str.replace('$', '', regex=False)
        .astype(float) * 16000
    )

    df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
    df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(int)
    df['Size'] = df['Size'].str.replace('Size: ', '', regex=False).str.strip()
    df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=False).str.strip()

    df = df.astype({
        'Title': 'string',
        'Price': 'float',
        'Rating': 'float',
        'Colors': 'int',
        'Size': 'string',
        'Gender': 'string',
        'Timestamp': 'string'
    })

    return df
