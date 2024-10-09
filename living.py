import pandas as pd
import re
import psycopg2
from config import *
from dotenv import load_dotenv

load_dotenv()

# Load the CSV file into a DataFrame
df = pd.read_csv('LivingExpense.csv')

# Define the function to extract expense value
def extract_value(expense):
    try:
        # Convert expense to string, handling NaN values
        if pd.isna(expense):
            return None  # Return None for NaN values
        expense = str(expense)  # Convert to string

        # If no range or plus is found, extract the first number in the fee string
        match = re.search(r'[\d,]+', expense)
        if match:
            # Extract the matched number with commas
            expense = match.group(0)
            if expense:  # Check if expense is not an empty string
                # Remove commas and convert to an integer
                expense_value = int(expense.replace(',', ''))
                return expense_value
        return None  # Return None if no match is found
    except Exception as e:
        print(e)
        return None

# Create a new column in the DataFrame by applying the extract_value function
df['extracted_expense'] = df['livingexpense'].apply(extract_value)

# Identify rows with None values in 'extracted_expense'
null_rows = df[df['extracted_expense'].isna()]

# Save the cleaned DataFrame to a new CSV file (excluding None values)
cleaned_df = df.dropna(subset=['extracted_expense'])
cleaned_df.to_csv("output_cleaned.csv", index=False)

# Save rows with exceptions or None values to a separate CSV file
null_rows.to_csv("output_nulls.csv", index=False)

try:
    # # Establish the connection to the database
    conn = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        port=PORT
    )
    print(HOST)

    # Create a cursor object
    cursor = conn.cursor()

    # Use a set to store unique queries
    queries = set()  # Initialize as a set to avoid duplicates

    # Create the update queries
    for index, row in cleaned_df.iterrows():
        if row['extracted_expense'] is not None:  # Only update if the fee is not None
            query = f"UPDATE programs SET living_expense_value = {row['extracted_expense']} WHERE livingexpense = '{row['livingexpense']}'"
            # print(query)
            queries.add(query)  # Add the query to the set
    print(len(queries))

    # Execute each unique query
    for query in queries:
        print(query)
        cursor.execute(query)

    # Commit the changes
    conn.commit()

except Exception as e:
    print(e)

finally:
    cursor.close()
    conn.close()
