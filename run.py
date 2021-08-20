import gspread 
from google.oauth2.service_account import Credentials

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
    """Get sales input figures from the user"""
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


data = get_sales_data()