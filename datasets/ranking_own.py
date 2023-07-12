import csv

# Read the combined rankings from the CSV file
combined_rankings_file = "combined_rankings.csv"
combined_rankings = {}

with open(combined_rankings_file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        website = row["website"]
        rankings = [int(row[column]) for column in reader.fieldnames[1:-1] if row[column] != "-"]
        occurrences = len(rankings)
        combined_rankings[website] = {"rankings": rankings, "occurrences": occurrences}

# Calculate the "my_ranking" column
for website, data in combined_rankings.items():
    rankings = data["rankings"]
    occurrences = data["occurrences"]
    if occurrences > 0:
        my_ranking = sum(rankings) / occurrences
    else:
        my_ranking = "-"
    combined_rankings[website]["my_ranking"] = my_ranking

# Write the updated combined rankings to a new CSV file
output_file = "combined_rankings_with_my_ranking.csv"

with open(output_file, "w", newline="") as csvfile:
    fieldnames = ["website"] + reader.fieldnames[1:] + ["my_ranking"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for website, data in combined_rankings.items():
        row = {"website": website}
        row.update({column: "-" if column == "my_ranking" else "" for column in reader.fieldnames[1:]})

        my_ranking = data["my_ranking"]
        if my_ranking != "-":
            row["my_ranking"] = "{:.2f}".format(my_ranking)

        writer.writerow(row)

print("Combined rankings with 'my_ranking' have been saved to", output_file)
