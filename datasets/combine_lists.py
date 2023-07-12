import os
import csv
from tqdm import tqdm

# Directory containing the text files
# directory = "/home/skanda/Desktop/service_worker/datasets"

# List of text file names
# file_names = [file for file in os.listdir(directory) if file.endswith(".txt")]

file_names = ["alexa.txt","majesticmillion.txt","tranco.txt","builtwith.txt","domcop.txt"]

# Dictionary to store website rankings
website_rankings = {}

# Count the number of URLs processed
url_count = 0

# Process each text file
for file_name in file_names:
    # with open(os.path.join(directory, file_name), "r") as file:
    with open(file_name, "r") as file:
        # next(file)  # Skip the header line
        for line in tqdm(file, desc="Processing " + file_name, unit="URL"):
            try:
                rank, website = line.strip().split(",")
                website_rankings.setdefault(website, {})[file_name] = rank
                url_count += 1
            except ValueError:
                print("Skipping line:", line)

# Write the combined rankings to a CSV file
output_file = "combined_rankings.csv"
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["website"] + file_names)  # Write the header

    # Write the website rankings
    for website, rankings in tqdm(website_rankings.items(), desc="Writing CSV", unit="URL"):
        row = [website]
        for file_name in file_names:
            rank = rankings.get(file_name, "-")
            row.append(rank)
        writer.writerow(row)

print("Combined rankings have been saved to", output_file)
