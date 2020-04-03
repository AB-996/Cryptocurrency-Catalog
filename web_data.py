f = open("API_KEY.txt", "r")
API_KEY = f.readline()
f.close()
HEADERS = {"Accept": "application/json", "X-CMC_PRO_API_KEY": API_KEY}
GLOBAL_URL = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
CRYPTO_SEARCH_URL =  "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
INFO_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
FIAT_URL = "https://pro-api.coinmarketcap.com/v1/fiat/map"
LISTINGS_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"