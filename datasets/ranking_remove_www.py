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

            # Modify the website entries
            modified_lines = []
            for line in lines:
                rank, website = line.strip().split(',')
                if "www." in website:
                    website = website.replace("www.", "")
                modified_lines.append(f"{rank},{website}\n")

        # Write the modified contents back to the file
        filename8 = folder_path+file_name+"1"
        new_file_name = os.path.splitext(file_name)[0] + '_modified.txt'

        with open(os.path.join(folder_path, new_file_name), 'w') as file:
            file.writelines(modified_lines)
