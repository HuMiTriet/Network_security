import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import Counter

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


# nonce, hash, unsafe, sri, 

if __name__ == "__main__":
    # create_csp_count_pie_chart()
    create_csp_usage_pie_chart()