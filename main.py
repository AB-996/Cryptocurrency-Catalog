import os
import api
import tables
from menu import header, user_prompt

crypto_dict = {}
currencies = []

def check_crypto_dict():
    global crypto_dict
    if crypto_dict == {}:
        crypto_dict = api.get_listings("dict")

def search_crypto():
    global crypto_dict
    os.system("cls")

    check_crypto_dict()

    for el in crypto_dict:
        print(el, end = " ")
    print("")

    symbol = input("Enter symbol of crypto currency: ")
    url_id = crypto_dict[symbol.upper()]
    data, info = api.get_info(url_id, option="search")

    table = tables.create_table(data, "search")

    os.system("cls")
    print(table)
    print("Description: " + info["description"])
    print("Website: " + info["urls"]["website"][0]) if info["urls"]["website"]  else  print("Website: /")
    print("Source code: " + info["urls"]["source_code"][0]) if info["urls"]["source_code"]  else  print("Souce Code: /")
    print("")

    choice = input("Do you want to search again? (y/n) ")
    search_crypto() if choice.lower() == "y" or choice.lower() =="yes" else main()


def fiat_currency():
    global crypto_dict
    global currencies
    os.system("cls")

    check_crypto_dict()

    for el in crypto_dict:
        print(el, end = " ")

    if currencies == []:
        currencies = api.get_currencies()

    pick = input("Insert cryptocurrency: >>").upper()
    print("")

    for currency in currencies:
        print(currency["symbol"], end=" ")

    fiat = input("Insert fiat currency: >>").upper()

    data = api.get_info(crypto_dict[pick], fiat)

    last_updated = data["last_updated"]
    date = last_updated.split("T")[0]
    time = last_updated.split("T")[1][:-1]

    price = round(data["quote"][fiat]["price"],2)

    print("")
    print("Value of {0} for {1} on {2} at {3} is {4} {5}".format(pick, fiat, date, time, price, fiat))

    choice = input("Do you want to search again? (y/n) ")
    fiat_currency() if choice.lower() == "y" or choice.lower() =="yes" else main()

def top_list():
    data = api.get_listings()

    table = tables.create_table(data,"top_list")
    print(table)

    input("Press any key to return to Main Menu...")
    main()

def future_values():
    data = api.get_global()

    total_market_cap = data["quote"]["USD"]["total_market_cap"]

    listings = api.get_listings()

    table = tables.create_table_for_futures(listings, total_market_cap)
    print(table)
    input("Press any key to return to Main Menu...")
    main()

def create_xlsx():
    tables.create_xlsx_file()
    os.system("cls")
    print("Excel workbook finished!")
    input("Press any key to return to Main Menu...")
    main()

# def blockchains():
#     os.system("cls")
#     btc_info, ltc_info, eth_info = api.get_blockchains()
#     table = tables.create_blockchains_table([btc_info,ltc_info,eth_info])
#     print(table)
#     input("Press any key to return to Main Menu...")
#     main()


def main():

    os.system("cls")

    header()
    user_prompt()

    choice = input(">>> ")
    if choice == "1":
        search_crypto()
    elif choice == "2":
        fiat_currency()
    elif choice  == "3":
        top_list()
    elif choice == "4":
        future_values()
    elif choice == "5":
        create_xlsx()
        


if __name__ == "__main__":

    main()
