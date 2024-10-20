import csv
import pprint


input_file = "top_websites.csv"
output_file = "top_websites_rem_dup.csv"

domain_to_row: dict[str, list[str]] = dict()

with open(input_file, mode="r", newline="", encoding="utf-8") as infile, open(
    output_file, mode="w", newline="", encoding="utf-8"
) as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        domain_to_row[row[1]] = row

    writer.writerows(domain_to_row.values())

pp = pprint.PrettyPrinter(sort_dicts=True)
pp.pprint(domain_to_row)
