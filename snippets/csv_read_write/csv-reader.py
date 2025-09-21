import csv
import os
from pathlib import Path


def main():
    csv_file = Path(__file__).parent / 'test_csv.csv'
    if not csv_file.exists():
        return
    """
    newline = ""
    to avoid creating blank lines between rows
    """
    csv_file_descriptor = csv_file.open('r', newline='')
    csv_reader = csv.reader(
        csv_file_descriptor,
        delimiter=',',
    )
    for fn, ln, phone, dob, sex, state, zipcode in csv_reader:
        print((fn, ln), sex, dob)
    csv_file_descriptor.close()


if __name__ == '__main__':
    os.system('cls')
    main()
