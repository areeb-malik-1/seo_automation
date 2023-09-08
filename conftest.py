import csv
import os
import sys

import gspread
import pytest

# Columns in internal_all.csv to be included in formatted_internal_all.csv
VALID_COLUMNS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64)

# Columns in gsheet which should be used for pass/fail comparison
ACTUAL_COLUMNS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 52, 53, 54, 55, 56, 57)
#ACTUAL_COLUMNS = (0, 1, 2, 3, 4, 5)

OLD_FILES = ("output/crawl.seospider", "output/internal_all.csv", "output/formatted_internal_all.csv")


def delete_old_files():
    for file in OLD_FILES:
        f = os.getcwd() + "/" + file
        if os.path.exists(f):
            os.remove(f)


def create_formatted_result():
    with open("output/internal_all.csv", 'r') as source:
        reader = csv.reader(source)
        with open("output/formatted_internal_all.csv", 'w') as result:
            writer = csv.writer(result)
            for r in reader:
                writer.writerow((r[i] for i in VALID_COLUMNS))


def read_csv_rows():
    list_of_rows = []
    with open('output/formatted_internal_all.csv', 'r') as source:
        reader = csv.reader(source)
        for row in reader:
            list_of_rows.append(row)
    return list_of_rows


def get_row_count():
    count = 0
    for _ in open('output/formatted_internal_all.csv', 'r'):
        count += 1
    return count


def pytest_addoption(parser):
    parser.addoption("--gsheet", action="store")
    parser.addoption("--index", action="store")


GSHEET = sys.argv[2][9:]
INDEX = sys.argv[3][8:]

delete_old_files()
gc = gspread.service_account(filename='oauth2.json')
gh = gc.open_by_key(GSHEET)
WORKSHEET = gh.get_worksheet(int(INDEX))
W_ROWS = WORKSHEET.get_all_values()
url_list = WORKSHEET.col_values(1)[1:]
with open('output/urls.txt', 'w') as f:
    for url in url_list:
        f.write(url + "\n")
cwd = os.getcwd()
print(cwd)
os.system('screamingfrogseospider --crawl-list {cwd}//output//urls.txt --headless --output-folder "{cwd}//output//" --export-format csv --export-tabs Internal:All')
create_formatted_result()
