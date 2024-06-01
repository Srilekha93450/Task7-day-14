import requests

class BreweryDataFetcher:
    def __init__(self, url):
        self.url = url

    def fetch_breweries(self, state):
        response = requests.get(self.url, params={'by_state': state})
        if response.status_code == 200:
            breweries = response.json()
            return breweries
        else:
            print("Failed to fetch breweries from the API.")
            return None

    def list_breweries(self, states):
        for state in states:
            breweries = self.fetch_breweries(state)
            if breweries:
                print(f"\nBreweries in {state}:")
                for brewery in breweries:
                    print(brewery['name'])

    def count_breweries(self, states):
        for state in states:
            breweries = self.fetch_breweries(state)
            if breweries:
                print(f"\nNumber of breweries in {state}: {len(breweries)}")

    def count_brewery_types_by_city(self, states):
        for state in states:
            breweries = self.fetch_breweries(state)
            if breweries:
                print(f"\nTypes of breweries in {state} by city:")
                city_brewery_types = {}
                for brewery in breweries:
                    city = brewery['city']
                    brewery_type = brewery['brewery_type']
                    city_brewery_types[city] = city_brewery_types.get(city, set())
                    city_brewery_types[city].add(brewery_type)
                for city, types in city_brewery_types.items():
                    print(f"{city}: {', '.join(types)}")

    def count_breweries_with_websites(self, states):
        for state in states:
            breweries = self.fetch_breweries(state)
            if breweries:
                websites_count = sum(1 for brewery in breweries if brewery.get('website_url'))
                print(f"\nNumber of breweries with websites in {state}: {websites_count}")

# URL for Open Brewery DB API
url = "https://api.openbrewerydb.org/breweries"

# States of interest
states_of_interest = ['Alaska', 'Maine', 'New York']

brewery_fetcher = BreweryDataFetcher(url)

# 1.) List the names of all breweries present in the states of Alaska, Maine, and New York.
brewery_fetcher.list_breweries(states_of_interest)

# 2.) What is the count of breweries in each of the states mentioned above?
brewery_fetcher.count_breweries(states_of_interest)

# 3.) Count the number of types of breweries present in individual cities of the state mentioned above
brewery_fetcher.count_brewery_types_by_city(states_of_interest)

# 4.) Count and list how many breweries have websites in the states of Alaska, Maine, and New York.
brewery_fetcher.count_breweries_with_websites(states_of_interest)
