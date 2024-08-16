import json

import pytest
import os
import csv
import shutil
import stat
from unittest.mock import patch

BACK_UP_DIR = "temp_files"
NAME_DIR = 'ASA'
TEST_DIR = 'tests'

@pytest.fixture
def setup_dir():
    cwd = os.getcwd()
    if NAME_DIR not in cwd:
        test_path = os.path.join(os.getcwd(), "Dataset2", TEST_DIR, NAME_DIR)
        os.chdir(test_path)

    yield

    os.chdir(cwd)
    print(f"Changed directory to '{cwd}'.")

def move_temp_file(file_name):
    # Ensure the backup directory exists
    if not os.path.exists(BACK_UP_DIR):
        os.makedirs(BACK_UP_DIR)

    # Backup the test file if it exists

    if os.path.exists(file_name):
        shutil.move(file_name, BACK_UP_DIR)

def restore_file(file_name):
    backup_file = os.path.join(BACK_UP_DIR, file_name)

    if os.path.exists(backup_file):
        shutil.move(backup_file, os.path.join(os.getcwd(), file_name))

    # Remove the backup directory if it's empty
    if not os.listdir(BACK_UP_DIR):
        os.rmdir(BACK_UP_DIR)

@pytest.fixture
def remove_result_file(request, setup_dir):

    yield

    result_file_name = request.param

    # Construct the full file path if needed, e.g., if you have the file in a subdirectory
    file_path = os.path.join(os.getcwd(), result_file_name)

    # Check if the file exists
    if os.path.exists(file_path):
        # Remove the file
        os.remove(file_path)
        print(f"File '{result_file_name}' has been removed.")
    else:
        print(f"File '{result_file_name}' does not exist.")

@pytest.fixture
def manage_test_files(request, setup_dir):

    test_file = request.param

    move_temp_file(test_file)

    yield

    # Restore the files from the backup if they were removed

    restore_file(test_file)

@pytest.fixture
def invalidate_format(request, setup_dir):

    file_name = request.param

    # Define file names
    test_file = 'temp_file.csv'

    # Step 1: Read the content of the file and remove the last two lines
    with open(file_name, 'r', newline='') as infile:
        reader = csv.reader(infile, delimiter='\t')

        # Read all rows from the input file
        rows = list(reader)

    move_temp_file(file_name)

    # Remove the last two lines
    rows = rows[:-2]

    # Step 2: Remove specific columns
    columns_to_remove = ['type', 'tags', 'component', 'flows', 'organization', 'textRange', 'debt', 'key', 'hash',
                         'status']

    # Get header and identify columns to keep
    header = rows[0]
    columns_to_keep_indices = [i for i, col in enumerate(header) if col not in columns_to_remove]

    # Create new rows with specified columns removed
    filtered_rows = [
        [row[i] for i in columns_to_keep_indices]
        for row in rows
    ]

    # Write the filtered content to a temporary file
    with open(test_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerows([header[i] for i in columns_to_keep_indices])  # Write header
        writer.writerows(filtered_rows)  # Write data

    # Rename temp file to output file
    os.rename(test_file, file_name)

    yield

    os.remove(file_name)

    restore_file(file_name)


@pytest.fixture
def invalidate_content(request, setup_dir):

    file_names = request.param

    for file_name in file_names:

        # Define file names
        test_file = 'temp_file.csv'

        # Step 1: Read the content of the file and remove the last two lines
        with open(file_name, 'r', newline='') as infile:
            reader = csv.reader(infile, delimiter='\t')

            # Read all rows from the input file
            rows = list(reader)

        move_temp_file(file_name)

        # Remove the last two lines
        rows = rows[:-2]

        # Get header and index of the 'type' column
        header = rows[0]
        type_column_index = header.index('type')

        # Prepare the modified rows with the unchanged header
        modified_rows = [header]  # Start with the unchanged header

        # Modify the data rows to change all 'type' column values to 'BUG'
        # Skip the header row and modify data rows
        modified_rows.extend(
            row[:type_column_index] + ['BUG'] + row[type_column_index + 1:]
            for row in rows[1:]  # Skip the header row
        )

        # Open the output file for writing
        with open(test_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter='\t')
            writer.writerows(modified_rows)

        # Rename temp file to output file
        os.rename(test_file, file_name)

    yield

    for file_name in file_names:
        os.remove(file_name)
        restore_file(file_name)

@pytest.fixture
def remove_content(request, setup_dir):

    file_names = request.param

    for file_name in file_names:


        test_file = 'temp_file'

        # Open the input file and read the header
        with open(file_name, 'r', newline='') as infile:
            reader = csv.reader(infile, delimiter='\t')
            header = next(reader)  # Read the first row as the header

        # Write the header to the new file
        with open(test_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter='\t')
            writer.writerow(header)

        move_temp_file(file_name)

        # Rename temp file to output file
        os.rename(test_file, file_name)

    yield

    for file_name in file_names:
        os.remove(file_name)
        restore_file(file_name)

@pytest.fixture
def empty_dict(request, setup_dir):
    file_names = request.param

    for file_name in file_names:
        test_file = 'temp_file'

        # Write the header to the new file
        with open(test_file, 'w', newline='') as outfile:
            outfile.write("{}")

        move_temp_file(file_name)

        # Rename temp file to output file
        os.rename(test_file, file_name)

    yield

    for file_name in file_names:
        os.remove(file_name)
        restore_file(file_name)



@pytest.fixture
def adapt_test_files(request, setup_dir):
    file_names = request.param

    matches = dict()

    for file_name in file_names:

        # Find the position of '_test'
        start_index = file_name.find('_test')

        # Find the position of '.csv'
        end_index = file_name.find('.csv')

        # Check if '_test' and '.csv' are present and in the correct order
        if start_index != -1 and end_index != -1 and start_index < end_index:
            # Compute the start index of the part to keep
            start_of_keep = start_index
            # Extract the part before '_test' and the part after '.csv'
            new_file_name = file_name[:start_of_keep] + file_name[end_index:]
            os.rename(file_name, new_file_name)
            matches[file_name] = new_file_name

    yield

    for file_name in file_names:
        new_file_name = matches[file_name]
        os.rename(new_file_name, file_name)

@pytest.fixture
def invalidate_format_dict(request, setup_dir):
    dict_file_name = request.param

    move_temp_file(dict_file_name)

    # Write the content to the destination file and add an additional line
    with open(dict_file_name, 'w') as destination_file:
        destination_file.write("{{")  # Add the additional line

    yield

    os.remove(dict_file_name)
    restore_file(dict_file_name)




