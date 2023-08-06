"""
Generates performance reports for your stock portfolio.
"""
from pathlib import Path
import argparse
import csv
import sys
import requests

def main():
    """Entrypoint into programme"""
    args = get_args()
    #Only continues if arguments were given
    if len(sys.argv) > 1:
        create_report(args)

def get_args(args=None):
    """Initialises and parses arguments from console window"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--input", help="source of your portfolio")
    parser.add_argument("-out", "--output", help="destination where the report will be saved")
    args = parser.parse_args(args)
    #No arguments given will return the help menu
    if len(sys.argv) == 1:
        parser.print_help()
    return args

def create_report(args):
    """Creates report from given CSV portfolio"""
    if args.input is None:
        print("An input file is required!\nPlease include an input CSV")
    else:
        try:
            input_path = string_to_path(args.input)
            report = read_portfolio(input_path)
            get_market_price(report)
            calculate_book_value(report)
            calculate_market_value(report)
            calculate_gain_loss(report)
            calculate_percent_change(report)
            #Saves report to user provided path or a default if none provided
            if args.output is None:
                save_report(report)
                print("Your report was saved at " + str(Path.cwd() / "new_report.csv"))
            else:
                output_path = string_to_path(args.output)
                save_report(report, filename=output_path)
                print("Your report was saved at " + str(output_path))
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException):
            print("\nAn error has occurred in reaching the API.  Try again later")
        except FileNotFoundError:
            print("This is an invalid directory")

def string_to_path(filepath):
    """Creates a path variable from a user input string"""
    if not isinstance(filepath, str):
        raise ValueError
    #Path is rooted in current working directory
    path = Path.cwd() / filepath
    #Removes invalid filename characters
    name = "".join(char for char in path.name if char not in r'*|\/?<>:"')
    #Generates generic filename if empty
    if name == "":
        name = "new.csv"
    path = path.parent / name
    #Adds .csv suffix to filepaths if left out
    if path.suffix != ".csv":
        path = path.parent / (path.name + ".csv")
    return path

def dictionary_list_check(var):
    """Ensures that the list contains only dictionaries"""
    if not isinstance(var, list):
        raise ValueError
    removed = False
    #Temporarily stores items to be removed
    invalid = []
    for item in var:
        #Checks to see if list items are dictionaries removes others
        if not isinstance(item, dict):
            invalid.append(item)
            print(f"{item} was removed because of invalid formatting")
            removed = True
        #Checks to see if dictionary has requisite number of columns
        elif len(item) >= 3:
            #Checks all dictionary entries for missing data removes parent dictionary
            for entry in item:
                if item[entry] is None or item[entry] == "":
                    invalid.append(item)
                    print(f"{item} was removed because of missing value")
                    removed = True
        else:
            print("The input csv did not have enough columns")
            raise ValueError
    for item in invalid:
        var.remove(item)
    #Raises error if whole list had no dictionaries
    if len(var) == 0:
        print("The input list held no valid entries")
        raise ValueError
    #Prints warning if an item has been removed
    if removed:
        print(f"There are still {len(var)} item(s) in your report")

def read_portfolio(filename):
    """Returns data from a CSV file"""
    if not isinstance(filename, Path):
        raise ValueError
    with open(filename, newline='') as file:
        portfolio = []
        for holding in csv.DictReader(file):
            portfolio.append(holding)
        return portfolio

def get_market_price(portfolio):
    """Gets current price of holding from IEX"""
    dictionary_list_check(portfolio)
    #Creates list of symbols from user's portfolio
    symbols = [holding["symbol"] for holding in portfolio]
    #Attempts to reach the IEX API and get relevant stock prices
    try:
        uri = "https://api.iextrading.com/1.0/tops/last?symbols=" + ",".join(symbols)
        response = requests.get(uri)
        #Raises HTTP errors
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as error:
        print(error)
        raise error
    data = response.json()
    #Temporarily stores dictionaries with invalid symbols
    removed = []
    for holding in portfolio:
        #Attempts to find portfolio-data pair and marks for removal if none found
        try:
            price = next(entry for entry in data if entry["symbol"] == holding["symbol"])["price"]
            holding["latest_price"] = price
        except StopIteration:
            removed.append(holding)
            print(holding["symbol"] + " was not found; it is invalid!")
    for holding in removed:
        portfolio.remove(holding)

def calculate_book_value(report):
    """Calculates the initial value of the stocks"""
    dictionary_list_check(report)
    for holding in report:
        holding["book_value"] = round(int(holding["units"]) * float(holding["cost"]), 2)
    return report

def calculate_market_value(report):
    """Calculates the current value of the stocks"""
    dictionary_list_check(report)
    for holding in report:
        holding["market_value"] = round(int(holding["units"]) * float(holding["latest_price"]), 2)
    return report

def calculate_gain_loss(report):
    """Calculates the monetary value change"""
    dictionary_list_check(report)
    for holding in report:
        holding["gain_loss"] = round(
            float(holding["market_value"]) - float(holding["book_value"]), 2)
    return report

def calculate_percent_change(report):
    """Calculates the precentage value change"""
    dictionary_list_check(report)
    for holding in report:
        book_value = float(holding["book_value"])
        holding["change"] = round((float(holding["market_value"]) - book_value) / book_value, 2)
    return report

def save_portfolio(portfolio, filename=Path.cwd() / 'new_portfolio.csv'):
    """Saves data to a CSV file"""
    if not isinstance(filename, Path):
        raise ValueError
    dictionary_list_check(portfolio)
    with open(filename, "w", newline='') as file:
        #Creates then writes dictionary/csv header
        writer = csv.DictWriter(file, ['symbol', 'units', 'cost'])
        writer.writeheader()
        #Writes data to path
        writer.writerows(portfolio)

def save_report(report, filename=Path.cwd() / 'new_report.csv'):
    """Saves report to a CSV file"""
    if not isinstance(filename, Path):
        raise ValueError
    dictionary_list_check(report)
    with open(filename, "w", newline='') as file:
        #Creates then writes dictionary/csv header
        header = ['symbol', 'units', 'cost', 'latest_price',
                  'book_value', 'market_value', 'gain_loss', 'change']
        writer = csv.DictWriter(file, header)
        writer.writeheader()
        #Writes data to path
        writer.writerows(report)

if __name__ == '__main__':
    main()
