from colorama import Back, Fore, Style
from prettytable import PrettyTable
import json

import api
import xlsxwriter



def extract_data(info):
    name = info["name"]
    symbol = info["symbol"]
    last_updated = info["last_updated"]
    price =  round(info["quote"]["USD"]["price"],2)
    market_cap = round(info["quote"]["USD"]["market_cap"], 2)
    volume = round(info["quote"]["USD"]["volume_24h"], 2)
    hour_change = round(info["quote"]["USD"]["percent_change_1h"],2)
    day_change = round(info["quote"]["USD"]["percent_change_24h"],2)
    week_change = round(info["quote"]["USD"]["percent_change_7d"],2)

    if hour_change > 0:
        hour_change = Back.GREEN + str(hour_change) + "%" + Style.RESET_ALL
    else:
        hour_change = Back.RED + str(hour_change) + "%" + Style.RESET_ALL
    if week_change > 0:
        week_change = Back.GREEN + str(week_change) + "%" + Style.RESET_ALL
    else:
        week_change = Back.RED + str(week_change) + "%" + Style.RESET_ALL
    if day_change > 0:
        day_change  = Back.GREEN + str(day_change ) + "%" + Style.RESET_ALL
    else:
        day_change  = Back.RED + str(day_change ) + "%" + Style.RESET_ALL

    return {"name" : name, "symbol" : symbol, "price" : price, "market_cap" : market_cap, "volume" : volume, "change_1h" : hour_change,
            "change_24h" : day_change, "change_7d" : week_change, "last_update" : last_updated}

def add_rows(table, data):
    table_values = ["name", "symbol", "price", "market_cap", "volume", "change_1h", "change_24h", "change_7d", "last_update"]
    values = []
    for el in table_values:
        if type(data[el]) == float:
            values.append("{:,}".format(data[el]))
        else:
            values.append(data[el])
        
    table.add_row(values)
    return table


def create_table(info, option):
    if option == "search" or option == "top_list":
        table = PrettyTable(["Name", "Symbol", "Price $", "Market Cap $", "Volume 24h $", "1h change %", "24h change %", "7d change %", "Last updated"])
        if option == "search":
            data = extract_data(info)
            table =  add_rows(table, data)
        elif option == "top_list":
            for currency in info:
                data = extract_data(currency)
                table = add_rows(table, data)
        return table

def create_table_for_futures(data, global_cap):

    table = PrettyTable(["Name", "Symbol", "% of total global cap", "Current", "7.7T (Gold)", "36.8 (Narrow Money)", "73T (World Stock Market)",
                        "90.4T (Broad Money)","217T (Real Estate)", "544T (Derivates)"])
    for currency in data:
        name = currency["name"]
        symbol = currency["symbol"]
        percentage_of_global_cap = float(currency["quote"]["USD"]["market_cap"]) / float(global_cap)
        current_price = round(float(currency["quote"]["USD"]["price"]), 2)
        available_supply = float(currency["total_supply"])

        trillion7price = round(7700000000000 * percentage_of_global_cap / available_supply, 2)
        trillion36price = round(36800000000000 * percentage_of_global_cap / available_supply, 2)
        trillion73price = round(73000000000000 * percentage_of_global_cap / available_supply, 2)
        trillion90price = round(90400000000000 * percentage_of_global_cap / available_supply, 2)
        trillion217price = round(217000000000000 * percentage_of_global_cap / available_supply, 2)
        trillion544price = round(544000000000000 * percentage_of_global_cap / available_supply, 2)

        percentage_of_global_cap_string = str(round(percentage_of_global_cap * 100, 2)) + "%"
        current_price_string = "$" + str(current_price)
        trillion7price_string = "${:,}".format(trillion7price)
        trillion36price_string = "${:,}".format(trillion36price)
        trillion73price_string = "${:,}".format(trillion73price)
        trillion90price_string = "${:,}".format(trillion90price)
        trillion217price_string = "${:,}".format(trillion217price)
        trillion544price_string = "${:,}".format(trillion544price)

        table.add_row([name,
                    symbol,
                    percentage_of_global_cap_string,
                    current_price_string,
                    trillion7price_string,
                    trillion36price_string,
                    trillion73price_string,
                    trillion90price_string,
                    trillion217price_string,
                    trillion544price_string])
    return table

def create_blockchains_table(data):
    table = PrettyTable(["Slug", "Symbol", "Total Transactions", "Pending Transactions", "Transactions per second 24h", "Blocks"])

    for el in data:
        slug = el["slug"]
        symbol = el["symbol"]
        total_transactions = el["total_transactions"]
        pending_transactions = el["pending_transactions"]
        tps_24 = el["tps_24h"]
        blocks = el["total_blocks"]
        table.add_row([slug,
                    symbol,
                    total_transactions,
                    pending_transactions,
                    tps_24,
                    blocks])
    return table

def create_xlsx_file():
    start = 1
    row = 1
    convert = input("Insert a fiat currency you want to convert >>> ").upper()
    workbook = xlsxwriter.Workbook("cryptocurrencies.xlsx")
    sheet = workbook.add_worksheet()
    sheet.write("A1", "Name")
    sheet.write("B1", "Symbol")
    sheet.write("C1", "Market Cap " + convert)
    sheet.write("D1", "Price " + convert)
    sheet.write("E1", "24h Volume " + convert)
    sheet.write("F1", "Hour Change %")
    sheet.write("G1", "Day Change %")
    sheet.write("H1", "Week Change %")
    sheet.write("I1", "Last Updated")
    for i in range(20):
        data = api.get_listings("", start, convert)
        for currency in data:
            name = currency["name"]
            symbol = currency["symbol"]
            market_cap = currency["quote"][convert]["market_cap"]
            price = currency["quote"][convert]["price"]
            volume_24h = currency["quote"][convert]["volume_24h"]
            hour_change = currency["quote"][convert]["percent_change_1h"]
            day_change = currency["quote"][convert]["percent_change_24h"]
            week_change = currency["quote"][convert]["percent_change_7d"]
            last_updated = currency["last_updated"]

            if volume_24h is None:
                volume_24h = 0
            if market_cap is None:
                market_cap = 0


            sheet.write(row,0,name)
            sheet.write(row,1,symbol)
            sheet.write(row,2,"{:,}".format(round(market_cap,2)))
            sheet.write(row,3,"{:,}".format(round(price,2)))
            sheet.write(row,4,"{:,}".format(round(volume_24h,2)))
            sheet.write(row,5,str(hour_change))
            sheet.write(row,6,str(day_change))
            sheet.write(row,7,str(week_change))
            sheet.write(row,8,last_updated)

            row += 1
        start += 100
        
    workbook.close()
