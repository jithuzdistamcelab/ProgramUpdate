import re

# Example fee string
fee_string = "NZ$20,400 plus NZ$2400"

# Regular expression pattern to extract numeric values
pattern = r'NZ\$\s*([\d,]+)'

# Find all matches for the pattern in the fee string
matches = re.findall(pattern, fee_string)

# Initialize a variable to store the total sum
total_sum = 0

# Iterate through the matches
for match in matches:
    # Remove commas and convert to float, then add to total sum
    value = float(match.replace(',', ''))
    total_sum += value

# Print the total sum
print(f"Total Sum: NZ${total_sum:,.2f}")
