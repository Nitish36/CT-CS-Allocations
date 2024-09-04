import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
import os


def read_and_sort_csv():
    # Link= https://drive.google.com/file/d/1OFOfdas3mWOZiz8paFaWcRF9JCxOADpj/view?usp=sharing
    url = "https://drive.google.com/uc?export=download&id=1OFOfdas3mWOZiz8paFaWcRF9JCxOADpj"
    dataset = pd.read_csv(url)

    # Select the relevant columns
    data = {
        "Created date": dataset["Created date"],
        "Client ID": dataset["Client ID"],
        "Client name": dataset["Client name"],
        "Store/EC": dataset["Store/EC"],
        "Lead Tagging": dataset["Lead Tagging"],
        "City": dataset["City"],
        "Project values": dataset["Project values"],
        "Client Email ID": dataset["Client Email ID"],
        "Client Contact": dataset["Client Contact"],
        "Cabinet Specialist": dataset["Cabinet Specialist"],
        "Project Value": dataset["Project Value"],
        "Issue priority": dataset["Issue priority"],
        "Ticket Number": dataset["Ticket Number"],
        "Ticket Status": dataset["Ticket Status"],
        "Escalation Stage": dataset["Escalation Stage"],
        "Escalation Source": dataset["Escalation Source"],
        "Ticket Type": dataset["Ticket Type"],
        "Initial Attribution": dataset["Initial Attribution"],
        "SIRI issue Type": dataset["SIRI issue Type"],
        "Maintenance Issue Type": dataset["Maintenance Issue Type"],
        "Design issue Type": dataset["Design issue Type"],
        "Client Issue Type": dataset["Client Issue Type"],
        "Remarks ,If any": dataset["Remarks ,If any"],
        "SPOC 1": dataset["SPOC 1"],
        "Acceptance by SPOC": dataset["Acceptance by SPOC"],
        "Resolution by SPOC": dataset["Resolution by SPOC"],
        "Escalation Budget/ Cost": dataset["Escalation Budget/ Cost"],
        "Resolution decision date": dataset["Resolution decision date"],
        "Resolution Date/Escalation Closure date": dataset["Resolution Date/Escalation Closure date"],
        "Resolution Communicated to Cx?": dataset["Resolution Communicated to Cx?"],
        "Proof of RCA attached": dataset["Proof of RCA attached"],
        "Follow up date": dataset["Follow up date"],
        "Closed month and year": dataset["Closed month and year"],
        "RCA Points": dataset["RCA Points"],
        "TAT for resolution decision": dataset["TAT for resolution decision"],
        "TAT between created and resolution date": dataset["TAT between created and resolution date"],
        "TAT Status": dataset["TAT Status"],
        "TAT Breach Remarks": dataset["TAT Breach Remarks"],
        "Resolution Ageing": dataset["Resolution Ageing"],
        "Request Raised Date": dataset["Request Raised Date"],
        "Request Assigned Date": dataset["Request Assigned Date"],
        "MONTH-YEAR/Request Raised": dataset["MONTH-YEAR/Request Raised"],
        "Month year request assigned": dataset["Month year request assigned"],
        "Today's Date": dataset["Today's Date"],
        "1st Payment Signup Date": dataset["1st Payment Signup Date"],
        "1st Payment Signup Rating": dataset["1st Payment Signup Rating"],
        "1st Payment Signup Difference": dataset["1st Payment Signup Difference"],
        "Handover Date of Feedback": dataset["Handover Date of Feedback"],
        "Handover Date Rating": dataset["Handover Date Rating"],
        "Handover Date Difference": dataset["Handover Date Difference"],
        "EOJ Date of Feedback": dataset["EOJ Date of Feedback"],
        "EOJ Rating": dataset["EOJ Rating"],
        "EOJ Difference": dataset["EOJ Difference"],
        "Bucket": dataset["Bucket"],
        "Escalation resolution feedback form sent?":dataset["Escalation resolution feedback form sent?"]
    }

    final_data = pd.DataFrame(data)

    # Convert the 'Project Sign Up' column to datetime
    final_data['Request Raised Date'] = pd.to_datetime(final_data['Request Raised Date'], errors='coerce')

    # Sort the dataframe based on 'Project Sign Up' date
    final_data = final_data.sort_values(by='Request Raised Date',ascending=False)

    return final_data


def write_df():
    df = read_and_sort_csv()
    GSHEET_NAME = 'Qarpentri Escalation data for Wednesday call'
    TAB_NAME = 'Qarpentri Escalation Tracker Master'
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



