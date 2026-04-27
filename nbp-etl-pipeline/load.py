import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from extract import load_exchange_rates
from transform import transform_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_to_db(df: pd.DataFrame):

    logging.info("Connection to DB PostgreSQL...")
    
    db_url = "postgresql://admin:password@localhost:5432/nbp_data"
    
    try:
        engine = create_engine(url=db_url)
        
        table_name = "exchange_rates"

        df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
        
        logging.info(f"Saved {len(df)} records to data base in table '{table_name}'.")
        
    except SQLAlchemyError as db_error:
        logging.error(f"Connection error with Data Base: {db_error}.")
    except Exception as error:
        logging.error(f"Unexpected error: {error}.")


if __name__ == "__main__":
    logging.info("ETL process...\n")

    data = load_exchange_rates()

    if data:
        data_clean = transform_data(data=data)

        load_to_db(df=data_clean)
    else:
        logging.error("The ETL process has been interrupted: No data from API NBP")
   