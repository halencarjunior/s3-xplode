import re
import requests
import warnings
from xml.etree import ElementTree as ET

# ANSI escape codes for text color
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

warnings.filterwarnings("ignore", category=DeprecationWarning, module="re")
# Define the XML namespace
XML_NAMESPACE = "{http://s3.amazonaws.com/doc/2006-03-01/}"

logo = """
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█░▄▄█░▄▄░████░█░█▀▄▄▀██░████▀▄▄▀█░▄▀█░▄▄█
█▄▄▀███▄▀█▄▄█▀▄▀█░▀▀░██░████░██░█░█░█░▄▄█
█▄▄▄█░▀▀░████▄█▄█░█████░▀▀░██▄▄██▄▄██▄▄▄█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
Version: 1.0
Author : bt0
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
"""

# Function to read patterns from a file and create a dictionary of name and pattern pairs
def read_patterns_from_file(filename):
    patterns = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Ignore empty lines
                name, pattern = line.split(' ', 1)
                patterns[name] = re.compile(pattern)
    return patterns

def scan_public_s3_bucket(bucket_name, regex_patterns):
    matches = []

    # Define the base URL for the S3 bucket
    bucket_url = f'https://{bucket_name}.s3.amazonaws.com/'

    try:
        # Fetch the bucket's content listing
        response = requests.get(bucket_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the XML response with the specified namespace.
        root = ET.fromstring(response.text.replace(XML_NAMESPACE, ""))

        # Extract object keys from the XML response.
        object_keys = [element.find(f'{XML_NAMESPACE}Key').text for element in root.findall(f'.//{XML_NAMESPACE}Contents')]

        # Scan each object for secrets.
        for key in object_keys:
            object_url = f'https://{bucket_name}.s3.amazonaws.com/{key}'

            # Download the object content
            response = requests.get(object_url)
            response.raise_for_status()

            # Read the downloaded content.
            contents = response.text

            # Search for secrets using the provided regex patterns
            secrets_found = {}
            for name, pattern in regex_patterns.items():
                matches = pattern.findall(contents)
                # Filter out blank secrets and add matches to the dictionary.
                non_blank_secrets = [secret for secret in matches if secret.strip()]
                if non_blank_secrets:
                    secrets_found[name] = non_blank_secrets

            # If any secrets were found, add them to the matches list.
            if secrets_found:
                matches.append((key, secrets_found))
                print(f'File: {key}')
                print(f'{GREEN}Secrets Found:{RESET}')
                for name, secret_list in secrets_found.items():
                    print(f' {GREEN}[+] {name}:{RESET}')
                    for secret in secret_list:
                        print(f'{RED}     {secret}{RESET}')
                
                print("\n")

    except requests.exceptions.RequestException as e:
        print(f'Failed to fetch object list: {RED}{e}{RESET}')
    except Exception as e:
        print(f'An error occurred: {RED}{e}{RESET}')

    return matches

if __name__ == '__main__':
    print(logo)
    option = input('Choose an option:\n\n1. Scan a single AWS S3 bucket\n2. Read from a file with a list of buckets\n\nEnter your choice (1 or 2): ')

    if option == '1':
        bucket_name = input('Enter the name of the public S3 bucket to scan: ')
        regex_patterns = read_patterns_from_file('patterns.config')
        print("\n")
        matches = scan_public_s3_bucket(bucket_name, regex_patterns)

        if not matches:
            print(' [-] No objects containing secrets were found in the bucket.\n')

    elif option == '2':
        file_name = input('Enter the name of the file containing a list of bucket names: ')

        try:
            with open(file_name, 'r') as file:
                bucket_names = [line.strip() for line in file.readlines()]

            regex_patterns = read_patterns_from_file('patterns.config')

            for bucket_name in bucket_names:
                print(f'Scanning bucket: {bucket_name}')
                matches = scan_public_s3_bucket(bucket_name, regex_patterns)

                if not matches:
                    print(f' [-] No objects containing secrets were found in the bucket: {bucket_name}\n')
                else:
                    print(f'Secrets found in bucket: {bucket_name}')

        except FileNotFoundError:
            print(f'File not found: {file_name}')
        except Exception as e:
            print(f'An error occurred: {RED}{e}{RESET}')

    else:
        print('Invalid option. Please choose 1 or 2.')
