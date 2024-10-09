import pandas as pd
import re

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

print("Data cleaned and saved successfully.")
