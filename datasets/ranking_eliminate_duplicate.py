import os

# Define the folder path where the text files are located
folder_path = '/home/skanda/Desktop/service_worker/datasets'

# Get the list of files in the folder
file_list = os.listdir(folder_path)

# Process each text file in the folder
for file_name in file_list:
    # Check if the file is a text file
    if file_name.endswith('.txt'):
        # Read the contents of the file
        with open(os.path.join(folder_path, file_name), 'r') as file:
            lines = file.readlines()

        # Create a dictionary to store the rankings of unique websites
        websites = {}

        # Iterate over the lines and extract the website and its rank
        for line in lines:
            rank, website = line.strip().split(',')
            rank = int(rank)

            # Check if the website is already present in the dictionary
            if website not in websites:
                websites[website] = rank
            else:
                # Update the rank only if the current rank is lower
                if rank < websites[website]:
                    websites[website] = rank

        # Sort the websites based on their rankings
        sorted_websites = sorted(websites.items(), key=lambda x: x[1])

        # Create a new file name
        output_file = os.path.splitext(file_name)[0] + '_output.txt'

        # Write the unique websites and their rankings to the new file
        with open(os.path.join(folder_path, output_file), 'w') as file:
            for website, rank in sorted_websites:
                file.write(f"{rank},{website}\n")

        print(f"Unique websites and their rankings from {file_name} have been written to {output_file}.")
