import os

def header():
    width = os.get_terminal_size().columns
    print("Welcome to Cryptocurrency Catalog".center(width))

def user_prompt():
    print("")
    print("Choose one of the following options: ")
    print("1 - Search cryptocurrency by symbol")
    print("2 - See value of cryptocurrency for specific fiat currency")
    print("3 - See top 100 cryptocurrencies")
    print("4 - See possible future values")
    print("5 - Export list of cryptocurrencies as xslx")
