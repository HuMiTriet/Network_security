import csv
import re

input_file = 'universities.txt'  
output_file = 'universities.csv'  

with open(input_file, 'r') as file:
    data = file.read()

pattern = r"(.+?)(?:\s+\(([^)]+)\))?\s*$"
matches = re.findall(pattern, data, re.MULTILINE)

# Write to CSV
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['University', 'Domain'])  # Header
    for name, domain in matches:
        writer.writerow([name.strip(), domain.strip() if domain else "N/A"])

print(f"CSV file '{output_file}' created successfully.")
