import gspread
import random
import os


def ct_alloc():
    # Define your Google Sheet and tab names
    GSHEET_NAME = 'CT Email Generator'
    TAB_NAME = 'Sheet1'
    credentialsPath = os.path.expanduser("cred/ct-email-generation-fd91c0d8a01e.json")

    if os.path.isfile(credentialsPath):
        # Authenticate and open the Google Sheet
        gc = gspread.service_account(filename=credentialsPath)
        sh = gc.open(GSHEET_NAME)
        worksheet = sh.worksheet(TAB_NAME)

        # Read data
        data = worksheet.get_all_records()

        # Define the email list
        emails = [
            'menaga.sounderaj@designcafe.com',
            'aruna.nagaraj@designcafe.com',
            'harishkumar.r@designcafe.com',
            'manjeshkar.reddy@designcafe.com',
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
            sign_up_date = row['Project Sign Up']
            payment_15_date = row['15% payment Date']
            kickoff_date = row['Kick-off Date']
            payment_35_date = row['35% Payment date']
            siri_date = row['Project to SIRI']
            payment_40_date = row['40% Payment Date']
            zero_snags_date = row['Zero Snags Date']
            eoj_date = row['EOJ Date']
            email_sign_up = row['CT-Email (Sign Up)']
            email_15 = row['CT-Email (15%)']
            email_35 = row['CT-Email (35%)']
            email_40 = row['CT-Email (40%)']
            email_zero_snags = row['CT-Email (ZeroSnags)']
            email_eoj = row['CT-Email (EOJ)']

            # Generate CT Emails based on conditions
            if not is_blank(sign_up_date) and is_blank(email_sign_up):
                ct_email = generate_ct_email()
                updates.append({'range': f'N{row_number}', 'values': [[ct_email]]})  # Update 'CT-Email (Sign Up)'

            if not is_blank(payment_15_date) and not is_blank(sign_up_date) and payment_15_date != sign_up_date and is_blank(email_15):
                ct_email = generate_ct_email()
                updates.append({'range': f'O{row_number}', 'values': [[ct_email]]})  # Update 'CT-Email (15%)'

            if not is_blank(kickoff_date) and not is_blank(payment_15_date) and not is_blank(sign_up_date) and payment_15_date == sign_up_date and is_blank(email_15):
                ct_email = generate_ct_email()
                updates.append({'range': f'O{row_number}', 'values': [[ct_email]]})  # Update 'CT-Email (15%)'

            if not is_blank(payment_35_date) and not is_blank(payment_15_date) and not is_blank(sign_up_date) and payment_35_date != payment_15_date and is_blank(email_35):
                ct_email = generate_ct_email()
                updates.append({'range': f'P{row_number}', 'values': [[ct_email]]})  # Update 'CT-Email (35%)'

            if not is_blank(siri_date) and not is_blank(payment_35_date) and not is_blank(payment_15_date) and not is_blank(sign_up_date) and payment_35_date == payment_15_date and is_blank(email_35):
                ct_email = generate_ct_email()
                updates.append({'range': f'P{row_number}', 'values': [[ct_email]]})  # Update 'CT-Email (35%)'

            if not is_blank(payment_35_date) and not is_blank(payment_15_date) and not is_blank(sign_up_date) and not is_blank(payment_40_date) and is_blank(email_40):
                ct_email = generate_ct_email()
                updates.append({'range': f'Q{row_number}', 'values': [[ct_email]]})  # Update 'CT-Email (40%)'

            if not is_blank(payment_35_date) and not is_blank(payment_15_date) and not is_blank(sign_up_date) and not is_blank(payment_40_date) and not is_blank(zero_snags_date) and is_blank(email_zero_snags):
                ct_email = generate_ct_email()
                updates.append({'range': f'R{row_number}', 'values': [[ct_email]]})  # Update 'CT-Email (ZeroSnags)'

            if not is_blank(payment_35_date) and not is_blank(payment_15_date) and not is_blank(sign_up_date) and not is_blank(payment_40_date) and not is_blank(zero_snags_date) and not is_blank(eoj_date) and is_blank(email_eoj):
                ct_email = generate_ct_email()
                updates.append({'range': f'S{row_number}', 'values': [[ct_email]]})  # Update 'CT-Email (EOJ)'

        # Execute batch update
        if updates:
            worksheet.batch_update(updates)
            print("CT Emails have been allocated successfully!")
        else:
            print("No updates were needed.")

    else:
        print(f"Credentials file not found at {credentialsPath}")



