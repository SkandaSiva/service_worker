import csv

input_file = 'combined_rankings.csv'
output_file = 'output.csv'

# Read the input file
with open(input_file, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Extract the headers and data
headers = rows[0]
data = rows[1:]

# Determine the number of columns
num_columns = len(headers)

# Create a dictionary to store the ranks for each website
website_ranks = {}

# Iterate over the data rows
for row in data:
    website = row[0]
    ranks = [int(rank) if rank != '-' else None for rank in row[1:]]
    
    # Exclude '-' ranks from the calculation
    valid_ranks = [rank for rank in ranks if rank is not None]
    num_valid_ranks = len(valid_ranks)
    
    # Calculate the average rank
    if num_valid_ranks > 0:
        average_rank = sum(valid_ranks) / num_valid_ranks
    else:
        average_rank = None
    
    website_ranks[website] = average_rank

# Write the results to the output file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['website', 'my_rank'])
    
    # Write the data rows
    for website, rank in website_ranks.items():
        writer.writerow([website, rank])
