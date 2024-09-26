import pandas as pd
import re
import psycopg2
from config import *
from dotenv import load_dotenv

load_dotenv()

# Read the CSV file
df = pd.read_csv("data.csv")

# Get the fees column as a list
fees = list(df["fees"])

# Initialize the output dictionary
output = {
    "plus": []
}

# Establish the connection to the database
connection = psycopg2.connect(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
    port=PORT
)

# Create a cursor object
cursor = connection.cursor()

# Pattern to extract fees in NZ$
pattern = r'NZ\$\s*([\d,]+)'

# Open a text file for writing
with open("output.txt", "w") as f:
    # Iterate through each fee in the DataFrame
    for each in fees:
        if pd.isna(each):
            continue  # Skip NaN values

        # Find all matches for the pattern
        matches = re.findall(pattern, each)
        
        if matches:
            total_sum = 0
            for match in matches:
                # Remove commas and convert to float
                value = float(match.replace(',', ''))
                total_sum += value

            # Prepare an SQL query using parameterized values to prevent SQL injection
            query = f"UPDATE programs SET fees_new = %s WHERE fees = %s;"
            
            try:
                # Execute the query with parameterized values
                cursor.execute(query, (total_sum, each))
                f.write(f"Total Sum: NZ${total_sum:,.2f}, original: {each}\n")
                
            except Exception as e:
                # Print the error if something goes wrong
                print(f"Error executing query for {each}: {e}")

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
