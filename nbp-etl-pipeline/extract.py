import requests, json, logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_exchange_rates():
    url_A = "http://api.nbp.pl/api/exchangerates/tables/A/?format=json"
    url_B = "http://api.nbp.pl/api/exchangerates/tables/B/?format=json"
    logging.info(f"API connection...: {url_A} and {url_B}")

    try:
        result_A = requests.get(url_A, timeout=10)
        result_B = requests.get(url_B, timeout=10)
        print(result_A)
        print(result_B)

        result_A.raise_for_status()
        result_B.raise_for_status()

        data_json_A = result_A.json()
        data_json_B = result_B.json()

        #print(data_json_A)
        #print(data_json_B)

        logging.info("Data loaded.")

        table_currencies_A = data_json_A[0]["rates"]
        table_currencies_B = data_json_B[0]["rates"]
        table_currencies = table_currencies_A + table_currencies_B


        # sorted by "code" -> 'XXX'
        table_currencies = sorted(table_currencies, key=lambda item: item["code"])
        
        # test - data output by print
        """for elem in table_currencies:
            for key, value in elem.items():
                print(f"{key}: {value}, ", end="")
            print("\n")"""


        return table_currencies

    except requests.exceptions.HTTPError as error_http:
        logging.error(f"Communication error from API NBP: {error_http}")
    except requests.exceptions.Timeout:
        logging.error(f"Timeout for NBP data")
    except Exception as error:
        logging.error(f"Unexpected error: {error}")

    return None

if __name__ == "__main__":
    data = load_exchange_rates()

    if data:
        print("\n First 10 currencies: \n")
        print(json.dumps(data[:10], indent=4, ensure_ascii=False))
        print(f"\nNo. of currencies: {len(data)}.\n")
    else:
        print(f"\nData not loading. Check logs above.\n")
