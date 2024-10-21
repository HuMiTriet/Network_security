import csv
import pprint
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_csv_file = os.path.join(script_dir, 'top_websites.csv')
output_csv_file = os.path.join(script_dir, "top_websites_rem_dup.csv")

domain_to_row: dict[str, list[str]] = dict()

with open(input_csv_file, mode="r", newline="", encoding="utf-8") as infile, open(
    output_csv_file, mode="w", newline="", encoding="utf-8"
) as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        domain_to_row[row[1]] = row

    writer.writerows(domain_to_row.values())

pp = pprint.PrettyPrinter(sort_dicts=True)
pp.pprint(domain_to_row)
