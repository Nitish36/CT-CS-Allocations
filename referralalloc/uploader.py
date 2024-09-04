import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
import os


def read_and_sort_csv():
    # Link= https://drive.google.com/file/d/1ljlbGkAw41cd5SnRCT1bBPxmAOu9039X/view?usp=sharing
    url = "https://drive.google.com/uc?export=download&id=1ljlbGkAw41cd5SnRCT1bBPxmAOu9039X"
    dataset = pd.read_csv(url)

    # Select the relevant columns
    data = {
        "Client ID": dataset["Client ID"],
        "Client Name": dataset["Client Name"],
        "City": dataset["City"],
        "Project Sign Up": dataset["Project Sign Up"],
        "Zero Snags Date": dataset["Zero Snags Date"],
        "Assigned To": dataset["Assigned To"]
    }

    final_data = pd.DataFrame(data)

    # Convert the 'Project Sign Up' column to datetime
    final_data['Project Sign Up'] = pd.to_datetime(final_data['Project Sign Up'], errors='coerce')

    # Sort the dataframe based on 'Project Sign Up' date
    final_data = final_data.sort_values(by='Project Sign Up')

    return final_data


def write_df():
    df = read_and_sort_csv()
    GSHEET_NAME = 'Referral Alloc (Python)'
    TAB_NAME = 'Sheet1'
    credentialsPath = os.path.expanduser("cred/ct-email-generation-fd91c0d8a01e.json")

    if os.path.isfile(credentialsPath):
        # Authenticate and open the Google Sheet
        gc = gspread.service_account(filename=credentialsPath)
        sh = gc.open(GSHEET_NAME)
        worksheet = sh.worksheet(TAB_NAME)

        set_with_dataframe(worksheet, df)

        # Now, 'df' contains the data from the Google Sheet
        print("Data loaded successfully!! Have fun!!")
        print(df)
    else:
        print(f"Credentials file not found at {credentialsPath}")



