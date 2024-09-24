import pandas as pd
import re
import psycopg2
from data import *
from config import *

# Read the CSV file
df = pd.read_csv("data.csv")

# Get the fees column as a list
fees = list(df["fees"])

# Initialize the output dictionary
output = {
    "plus": []
}
connection = psycopg2.connect(
        host=HOST, 
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        port=PORT  
    )
# Create a cursor object
cursor = connection.cursor()
pattern = r'NZ\$\s*([\d,]+)'
extracted_values = []

# Open a text file for writing
with open("output.txt", "w") as f:
    # Iterate through each fee
    for each in fees:
        if pd.isna(each):
            continue  # Skip NaN values
    
        if len(each)==len("NZ$31,500") and "NZ$" in each:
        # Iterate through the matches
            matches = re.findall(pattern, each)
            total_sum = 0
            for match in matches:
                # Remove commas and convert to float, then add to total sum
                value = float(match.replace(',', ''))
                total_sum += value
            # Write the output to the text file
            query = f"""UPDATE programs SET fees_new = {value} WHERE fees='{each}';"""
            # Print the query and parameters before execution
            print(query)
            # cursor.execute(query)


            f.write(f"Total Sum: NZ${total_sum:,.2f}, original: {each}\n")

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
