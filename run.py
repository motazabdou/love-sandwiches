import gspread 
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to ensure correct string data is provided, and
    the loop breaks when correct data type is provided and function returns sales data """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, seperated by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Please enter your data here in the format shown above: ")
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data entered is valid")
            break

    return sales_data


def validate_data(values):
    """ 
    Inside the try, the function will convert string values into integers. 
    Function will raise value errors if the input cannot be converted into an integer,
    or if the number of items in the values list is not equal to 6
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"Exactly 6 values are required. You provided {len(values)}\n")
    
    except ValueError as e:
        print(f"Invalid data {e}, please try again\n")
        print("--------------------------------------\n")
        return False

    return True

def update_worksheet(sheet, data):
    print(f"Updating {sheet} worksheet...")
    intended_worksheet = SHEET.worksheet(sheet)
    intended_worksheet.append_row(data)
    print(f"Updated {sheet} successfully")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus for each item

    The surplus is defined as the sales figure subtracted from the stock.
    - Positive surplus indicates waste
    - Negative surplus indicates extra sandwiches made when the stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[len(stock) - 1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from worksheet, collecting
    the last five entries of sandwiches and returns the data 
    as a list of lists
    """
    sales = SHEET.worksheet("sales")
    
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns


def main():
    """Run all program functions"""
    data = get_sales_data()
    print(data)
    sales_data = [int(num) for num in data]
    update_worksheet("sales", sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet("surplus", new_surplus_data)

print("Welcome to Love Sandwiches data automation")
# main()
sales_columns = get_last_5_entries_sales()