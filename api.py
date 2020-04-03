import json

import requests

from web_data import *


def get_listings(option = "", start = 1, convert = "USD"):
    url_listings = LISTINGS_URL +"?convert=" + convert  + "&start="+str(start)

    request = requests.get(url_listings, headers = HEADERS)
    response = request.json()

    if option == "":
        return response["data"]
    elif option == "dict":
        crypto_dict = {}
        for currency in response["data"]:
            crypto_dict[currency["symbol"]] = currency["id"]  
        return crypto_dict

    
def get_info(url_id, convert = "USD", option=""):
    url_id_string = str(url_id)

    url_crypto_search = CRYPTO_SEARCH_URL + "?id=" + url_id_string+"&convert=" + convert
    request = requests.get(url_crypto_search, headers = HEADERS)

    response = request.json()

    data = response["data"][url_id_string]

    if option == "search":
        url_info = INFO_URL + "?id="+url_id_string
        request = requests.get(url_info, headers = HEADERS)
        response = request.json()
        info = response["data"][url_id_string]

        return data, info
    return data

def get_global():
    request = requests.get(GLOBAL_URL, headers = HEADERS)
    response = request.json()
    return response["data"]

def get_currencies():
    request = requests.get(FIAT_URL, headers = HEADERS)
    response = request.json()
    return response["data"]

# def get_blockchains():
#     url_blockchains = "https://pro-api.coinmarketcap.com/v1/blockchain/statistics/latest?symbol=BTC,LTC,ETH"

#     request = requests.get(url_blockchains, headers = HEADERS)
#     response = request.json()

#     print(response)
#     return response["data"]["BTC"], response["data"]["LTC"], response["data"]["ETH"]

