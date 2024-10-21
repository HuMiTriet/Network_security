import requests
import csv
import os
import warnings
import validators

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_csv_file = os.path.join(script_dir, 'top_websites_rem_dup.csv')
output_csv_file = os.path.join(script_dir, 'csp_results.csv')

results = []

with open(input_csv_file, 'r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        root_domain = row.get('Root Domain')
        if root_domain:
            root_domain = root_domain.strip()

            if validators.domain(root_domain):
                if not root_domain.startswith(('http://', 'https://')):
                    url = 'https://' + root_domain
                else:
                    url = root_domain

                try:
                    response = requests.get(url, timeout=10, verify=False)
                
                    csp_header = response.headers.get('Content-Security-Policy')
                    
                    results.append({'Domain': root_domain, 'CSP Header': csp_header or ''})
                except Exception as e:
                    results.append({'Domain': root_domain, 'CSP Header': ''})
                    print(f'Error accessing {url}: {e}')
            else:
                results.append({'Domain': root_domain, 'CSP Header': ''})
        else:
            print('No')

with open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:
    fieldnames = ['Domain', 'CSP Header']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for result in results:
        writer.writerow(result)