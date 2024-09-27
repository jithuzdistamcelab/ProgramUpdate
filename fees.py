import pandas as pd
import re
import psycopg2
from config import *
from dotenv import load_dotenv

load_dotenv()



# Read the CSV file
df = pd.read_csv('data.csv')

# Access the 'fees' and 'duration' columns
data = df[["fees", "duration"]]

# Initialize the count of ignored and range-related values
count_of_ignored_value = 0
range_value = 0
get_total_value_added = 0
ignored_rows = []  # List to store ignored rows for writing to CSV

# Function to extract and add fees in case of a "plus" condition
def extract_integer(fee_string, duration_string):
    global count_of_ignored_value  # Declare as global to modify the count_of_ignored_value
    global range_value
    global get_total_value_added
    global ignored_rows  # Reference the ignored_rows list

    # Convert the fee_string to a string to handle non-string types like NaN
    fee_string = str(fee_string)

    # Define the list of unwanted words
    unwanted_data = ["years", "year", "per", "points", "pts", "semester"]
    exception_from_unwanted_data = ["1.5"]
    ranger = ["-", "–"]  # Symbols that indicate range

    # If any unwanted word is in the fee_string, return None
    for each in unwanted_data:
        if each in fee_string.lower():  # Case-insensitive matching
            count_of_ignored_value += 1
            check_continue = False
            for every in exception_from_unwanted_data:
                if every in fee_string.lower():
                    check_continue = True
                    count_of_ignored_value -= 1
            
            if not check_continue:
                ignored_rows.append({'fees': fee_string, 'duration': duration_string})  # Store ignored row
                return None

    # Check if the fee string contains a range (e.g., "27,500 - 55,000")
    for symbol in ranger:
        if symbol in fee_string:
            range_value += 1
            # Split the string on the range symbol and take the right-hand side
            right_side = fee_string.split(symbol)[-1]
            # Find the first number in the right-hand side
            match = re.search(r'[\d,]+', right_side)
            if match:
                # Extract the number, remove commas, and convert to integer
                fee_value = int(match.group(0).replace(',', ''))
                return fee_value
            return None

    # Check if the fee string contains the "plus" keyword (e.g., "32,500 plus 240")
    if "plus" in fee_string.lower():
        get_total_value_added += 1
        # Split the string on the "plus" keyword
        parts = re.split(r'plus', fee_string, flags=re.IGNORECASE)
        total_value = 0
        for part in parts:
            match = re.search(r'[\d,]+', part)
            if match:
                # Remove commas and convert to integer
                total_value += int(match.group(0).replace(',', ''))
        return total_value

    # If no range or plus is found, extract the first number in the fee string
    match = re.search(r'[\d,]+', fee_string)
    if match:
        # Extract the matched number with commas
        fee = match.group(0)
        # Remove commas and convert to an integer
        fee_value = int(fee.replace(',', ''))
        return fee_value

    return None

# Apply the function to each entry in the 'fees' and 'duration' columns
df['extracted_fees'] = data.apply(lambda row: extract_integer(row['fees'], row['duration']), axis=1)

# Display the DataFrame with the extracted fees
filtered_data = df[["duration", 'fees', 'extracted_fees']].dropna(subset=['extracted_fees'])


# Save the filtered data to a new CSV file
filtered_data.to_csv("a.csv", index=False)

# Write ignored rows to a new CSV file
if ignored_rows:
    ignored_df = pd.DataFrame(ignored_rows)
    ignored_df.to_csv("ignored_values.csv", index=False)

# Print the count of ignored values, range values, and "plus" additions
print("count_of_ignored_value =", count_of_ignored_value)
print("range_value =", range_value)
print("get_total_value_added =", get_total_value_added)


try:

    # # Establish the connection to the database
    conn  = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        port=PORT
    )
    print(HOST)

    # Create a cursor object
    cursor = conn.cursor()
    # Update the fees_new column for each extracted fee
    for index, row in filtered_data.iterrows():
        if row['extracted_fees'] is not None:  # Only update if the fee is not None
            query=f"UPDATE programs SET fees_new = {row['extracted_fees']} WHERE fees = '{row['fees']}'"
            print(query)
            cursor.execute(query)

    # Commit the changes
    conn.commit()

except Exception as e:
    print(e)

finally:
    cursor.close()
    conn.close()






