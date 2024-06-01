import requests
from requests.exceptions import ConnectionError, Timeout

class CountryDataFetcher:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        retries = 3
        timeout = 10
        for _ in range(retries):
            try:
                response = requests.get(self.url, timeout=timeout)
                if response.status_code == 200:
                    data = response.json()
                    # Extracting necessary data: country name, currencies
                    extracted_data = []
                    for country_data in data:
                        name = country_data.get('name', 'N/A')
                        currencies = country_data.get('currencies', [])
                        if isinstance(currencies, str):
                            currencies = [currencies]  # Convert to list if it's a string
                        extracted_data.append({'name': name, 'currencies': currencies})
                    return extracted_data
                else:
                    print("Failed to fetch data from the URL. Status code:", response.status_code)
                    return None
            except (ConnectionError, Timeout) as e:
                print("Connection timeout error:", e)
                print("Retrying...")
        print("Failed to fetch data after {} retries.".format(retries))
        return None

    def display_country_info(self):
        data = self.fetch_data()
        if data:
            for country_data in data:
                name = country_data['name']
                currencies = country_data['currencies']
                if isinstance(currencies, list):
                    currency_names = [currency.get('name', 'N/A') for currency in currencies]
                    currency_symbols = [currency.get('symbol', 'N/A') for currency in currencies]
                    print("Country: {}, Currencies: {}, Currency Symbols: {}".format(name, currency_names, currency_symbols))
                else:
                    # If currencies is not a list (but a string), treat it as a single currency
                    currency_name = currencies
                    print("Country: {}, Currency: {}".format(name, currency_name))

    def display_dollar_countries(self):
        data = self.fetch_data()
        if data:
            for country_data in data:
                name = country_data['name']
                currencies = country_data['currencies']
                for currency in currencies:
                    if 'USD' in currency.get('code', ''):
                        print(name)

    def display_euro_countries(self):
        data = self.fetch_data()
        if data:
            for country_data in data:
                name = country_data['name']
                currencies = country_data['currencies']
                for currency in currencies:
                    if 'EUR' in currency.get('code', ''):
                        print(name)

# Example usage:
url = "https://restcountries.com/v3.1/all"
country_fetcher = CountryDataFetcher(url)
country_fetcher.display_country_info()
print("\nCountries with Dollar currency:")
country_fetcher.display_dollar_countries()
print("\nCountries with Euro currency:")
country_fetcher.display_euro_countries()
