import gspread
import random
import os

def ct_alloc():
    # Define your Google Sheet and tab names
    GSHEET_NAME = 'Referral Alloc (Python)'
    TAB_NAME = 'Sheet1'
    credentialsPath = os.path.expanduser("cred/ct-email-generation-fd91c0d8a01e.json")

    if os.path.isfile(credentialsPath):
        # Authenticate and open the Google Sheet
        gc = gspread.service_account(filename=credentialsPath)
        sh = gc.open(GSHEET_NAME)
        worksheet = sh.worksheet(TAB_NAME)

        # Define expected headers to avoid issues with non-unique headers
        expected_headers = [
            'Client ID', 'Client Name', 'City', 'Project Sign Up', 'Zero Snags Date', 'Assigned To'
        ]

        # Read data, ensuring the use of expected headers
        data = worksheet.get_all_records(expected_headers=expected_headers)

        # Debug: print the data to see what's being read
        print("Data read from Google Sheet:")
        for i, row in enumerate(data):
            print(f"Row {i+2}: {row}")

        # Define the email list
        emails = [
            'aruna.nagaraj@designcafe.com',
            'harishkumar.r@designcafe.com',
            'sarita.vishwakarma@designcafe.com',
            'sowmya.br@designcafe.com',
            'babitha.g@designcafe.com',
            'rohini.pawar@designcafe.com',
            'tarannum.ayesha@designcafe.com',
            'sanjog.zimbar@designcafe.com',
            'utkarshani.raj@designcafe.com',
            'menaga.sounderaj@designcafe.com',
            'manjeshkar.reddy@designcafe.com',
            'raksha.suvarna@designcafe.com'
        ]

        # Function to generate a random email
        def generate_ct_email():
            return random.choice(emails)

        # Function to check if a cell is blank
        def is_blank(value):
            return value is None or value.strip() == ''

        # Collect updates to be made in a batch
        updates = []

        # Process each row and allocate emails
        for i, row in enumerate(data):
            row_number = i + 2  # Google Sheets is 1-indexed and 1 is the header row

            # Extract values
            zero_snags_date = row['Zero Snags Date']
            assigned_to = row['Assigned To']

            # Debug: print the values before checking conditions
            print(f"Processing Row {row_number}: Zero Snags Date = {zero_snags_date}, Assigned To = {assigned_to}")

            # Ensure we only assign emails to rows where 'Assigned To' is blank
            if not is_blank(zero_snags_date) and is_blank(assigned_to):
                ct_email = generate_ct_email()
                updates.append({'range': f'F{row_number}', 'values': [[ct_email]]})  # Update 'Assigned To' (column 6)
                print(f"Row {row_number}: Assigned To set to {ct_email}")
            else:
                print(f"Row {row_number}: No change needed")

        # Execute batch update
        if updates:
            worksheet.batch_update(updates)
            print("CT Emails have been allocated successfully!")
        else:
            print("No updates were needed.")

    else:
        print(f"Credentials file not found at {credentialsPath}")
