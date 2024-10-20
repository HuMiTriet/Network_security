import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import Counter
import re

def create_csp_count_pie_chart():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    csv_file = os.path.join(script_dir, 'csp_results.csv')

    df = pd.read_csv(csv_file)

    df = df.dropna(subset=['CSP Header'])
    df = df[df['CSP Header'].str.strip() != '']

    directive_counts = Counter()

    for csp in df['CSP Header']:
        directives = csp.split(';')
        for directive in directives:
            directive = directive.strip()
            if directive == '':
                continue 
            parts = directive.split(None, 1)
            directive_name = parts[0].lower()
            directive_counts[directive_name] += 1

    print("Directive Counts:")
    for directive, count in directive_counts.items():
        print(f"{directive}: {count}")

    labels = list(directive_counts.keys())
    sizes = list(directive_counts.values())

    labels_sizes = sorted(zip(labels, sizes), key=lambda x: x[1], reverse=True)
    labels, sizes = zip(*labels_sizes)

    total = sum(sizes)
    labels_filtered = []
    sizes_filtered = []
    others_size = 0
    for label, size in zip(labels, sizes):
        if (size / total) * 100 >= 2: 
            labels_filtered.append(label)
            sizes_filtered.append(size)
        else:
            others_size += size

    if others_size > 0:
        labels_filtered.append('Others')
        sizes_filtered.append(others_size)

    plt.figure(figsize=(10, 8))
    plt.pie(sizes_filtered, labels=labels_filtered, autopct='%1.1f%%', startangle=140)
    plt.title('CSP Directive Usage')
    plt.axis('equal')  

    plt.tight_layout()
    plt.show()

    plt.savefig(os.path.join(script_dir, 'csp_directive_pie_chart.png'))


def create_csp_usage_pie_chart():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    csv_file = os.path.join(script_dir, 'csp_results.csv')  # Replace with your actual CSV file name

    df = pd.read_csv(csv_file)

    total_websites = len(df)

    websites_with_csp = df['CSP Header'].notna() & df['CSP Header'].str.strip().astype(bool)
    num_with_csp = websites_with_csp.sum()

    num_without_csp = total_websites - num_with_csp

    labels = ['Websites with CSP Header', 'Websites without CSP Header']
    sizes = [num_with_csp, num_without_csp]

    # percent_with_csp = (num_with_csp / total_websites) * 100
    # percent_without_csp = (num_without_csp / total_websites) * 100
    # print(f"Total websites: {total_websites}")
    # print(f"Websites with CSP Header: {num_with_csp} ({percent_with_csp:.2f}%)")
    # print(f"Websites without CSP Header: {num_without_csp} ({percent_without_csp:.2f}%)")

    plt.figure(figsize=(8, 6))
    colors = ['#66b3ff', '#ff9999']  
    explode = (0.05, 0)  

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140,
            colors=colors, explode=explode, shadow=True)

    plt.title('Percentage of Websites Using CSP Headers')
    plt.axis('equal')  
    plt.tight_layout()
    plt.show()

    plt.savefig(os.path.join(script_dir, 'csp_usage_pie_chart.png'))


def create_csp_params_pie_chart():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the CSV file containing the CSP headers
    csv_file = os.path.join(script_dir, 'csp_results.csv')  # Replace with your actual CSV file name

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Drop rows where 'CSP Header' is NaN or empty
    df_csp = df.dropna(subset=['CSP Header'])
    df_csp = df_csp[df_csp['CSP Header'].str.strip() != '']

    # Total number of websites with CSP headers
    total_csp_websites = len(df_csp)

    # Initialize counts
    nonce_count = 0
    hash_count = 0
    unsafe_count = 0
    sri_count = 0
    none_of_above_count = 0

    # Regular expressions
    nonce_pattern = re.compile(r"'nonce-[^']+'")
    hash_pattern = re.compile(r"'sha(256|384|512)-[A-Za-z0-9+/=]+'")
    unsafe_pattern = re.compile(r"'unsafe-inline'|'unsafe-eval'")
    sri_pattern = re.compile(r'\brequire-sri-for\b')

    # Iterate over the CSP headers
    for csp in df_csp['CSP Header']:
        csp_lower = csp.lower()

        # Check for nonce
        has_nonce = bool(nonce_pattern.search(csp_lower))
        # Check for hash
        has_hash = bool(hash_pattern.search(csp_lower))
        # Check for unsafe directives
        has_unsafe = bool(unsafe_pattern.search(csp_lower))
        # Check for SRI
        has_sri = bool(sri_pattern.search(csp_lower))

        # Categorize each website into one or more categories
        if has_nonce:
            nonce_count += 1
        if has_hash:
            hash_count += 1
        if has_unsafe:
            unsafe_count += 1
        if has_sri:
            sri_count += 1

    # Websites that do not fall into any of the above categories
    none_of_above_count = total_csp_websites - (nonce_count + hash_count + unsafe_count + sri_count)

    # Avoid negative count in case of overlapping categories
    if none_of_above_count < 0:
        none_of_above_count = 0

    # Prepare data for the pie chart
    labels = ['Nonce', 'Hash', 'Unsafe Directives', 'SRI', 'None of the Above']
    counts = [nonce_count, hash_count, unsafe_count, sri_count, none_of_above_count]

    # Calculate percentages
    percentages = [(count / total_csp_websites) * 100 for count in counts]

    # Print the counts and percentages
    print(f"Total websites with CSP headers: {total_csp_websites}\n")
    for label, count, percentage in zip(labels, counts, percentages):
        print(f"{label}: {count} ({percentage:.2f}%)")

    # Since websites can be in multiple categories, the sum may exceed total_csp_websites
    # For the pie chart, we can focus on the proportions of each feature among total features counted

    # Sum of counts (for features)
    total_features = nonce_count + hash_count + unsafe_count + sri_count + none_of_above_count

    # Calculate proportions for the pie chart
    proportions = [(count / total_features) * 100 for count in counts]

    # Create the pie chart
    plt.figure(figsize=(10, 8))
    plt.pie(proportions, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('CSP Feature Usage Among Websites with CSP Headers')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Optionally, save the plot to a file
    plt.savefig(os.path.join(script_dir, 'csp_features_pie_chart.png'))


if __name__ == "__main__":
    create_csp_count_pie_chart()
    create_csp_usage_pie_chart()