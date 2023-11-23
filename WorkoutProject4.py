# Michael Nguyen
# michael_n35@yahoo.com

'''
All imported Modules used to use api data and plot it
'''
import urllib.request
import json
import sys
from urllib.error import HTTPError
import matplotlib.pyplot as plt


def run_again():
    '''
    Function to ask the user if they want
    to run the program again
    '''
    user_input = input("Want to run again? (Y for yes, N for no): ")
    if user_input.lower() == "y":
        main()
    elif user_input.lower() == "n":
        sys.exit()
    else:
        print("Invalid choice")
        run_again()


def ask_currencies():
    '''
    Function to ask for user_inputs for
    the type of currency codes wanted with
    filename
    '''
    print("Welcome to currency graph, enter 5 currency")
    currency1 = input("Enter Currency1 (Not USD): ")
    currency2 = input("Enter Currency2 (Not USD): ")
    currency3 = input("Enter Currency3 (Not USD): ")
    currency4 = input("Enter Currency4 (Not USD): ")
    currency5 = input("Enter Currency5 (Not USD): ")
    file_name = input("Enter file_name for plot: ")
    currencies = [currency1, currency2, currency3, currency4, currency5]
    for currency in currencies:
        if len(currency) != 3:
            print("\nInvalid currency code, run again")
            main()
    return currencies, file_name


def get_currency_data(api_key, currency_data):
    '''
    Function to make and call the api url
    and retrieving currency data from it
    '''
    currencies, file_name = currency_data
    i = 0
    all_data = {}
    try:
        for currency in currencies:
            url = "https://v6.exchangerate-api.com/v6/" + api_key + \
                    "/pair/USD/" + currency

            request = urllib.request.Request(url)
            with urllib.request.urlopen(request) as response:
                response_data = response.read()
                data_object = json.loads(response_data)
                all_data[f"data{i}"] = data_object
                i += 1
        return all_data, file_name
    except HTTPError as error:
        print(f"\nERROR INVALID CURRENCY CODE/URL: {error}")
        run_again()
        return None


def add_data_to_file(data, file_name):
    '''
    Function for file io, writing the data
    from the api into a new file
    '''
    with open(f"{file_name}.txt", "w", encoding="UTF-8") as my_file:
        json.dump(data, my_file)


def sort_data_plot(data):
    '''
    Function that retrieves the data
    from the api and sorts the currency code
    and value into lists
    '''
    currency_code = []
    currency_value = []
    for i in range(5):
        currency_code.append(data.get(f"data{i}", {}).get("target_code"))
        currency_value.append(data.get(f"data{i}", {}).get("conversion_rate"))
    return currency_code, currency_value


def create_currency_plot(data, file_name):
    '''
    Function that takes in the data
    and file_name to create a bar graph
    of currency data
    '''
    currency_code, currency_value = sort_data_plot(data)
    bar_plotting = plt.bar(currency_code, currency_value)
    plt.bar_label(bar_plotting)
    plt.xlabel("Currency Code Type")
    plt.ylabel("Money Amount")
    plt.title("Money Conversion from $1 USD")
    plt.savefig(f"{file_name}.jpg")
    plt.show()


def main():
    '''
    Main code run that takes the different
    functions and uses them, includes any
    hardcoded aspects like api_key
    '''
    api_key = "5ee2204cf10a720c8643c426"
    data, file_name = get_currency_data(api_key, ask_currencies())
    add_data_to_file(data, file_name)
    create_currency_plot(data, file_name)
    run_again()


if __name__ == "__main__":
    main()
