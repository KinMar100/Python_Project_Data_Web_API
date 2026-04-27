import pandas as pd
import logging
from extract import load_exchange_rates

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def transform_data(data: list) -> pd.DataFrame:
    logging.info("Transform data with Pandas...")

    df = pd.DataFrame(data=data)

    df = df.rename(columns={
        "currency": "currency_name",
        "code":"currency_code",
        "mid": "currency_avg"}
        )
    
    df = df.dropna()

    df["currency_load_date"] = pd.Timestamp.now()

    logging.info(f"Data ready. Number of currencies: {len(df)} \n")

    return df

if __name__ == "__main__":
    data = load_exchange_rates()

    if data:
        data_clean = transform_data(data=data)

        print(data_clean.head(10))

        print("\n")

        data_clean.info()
    else:
        logging.info(f"Problem with loading data.")