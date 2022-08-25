import csv


with open('key_search_terms_cynthia.csv', 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        # prints normalized term
        print(row)