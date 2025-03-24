import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# Path to your CSV file
csv_file_path = "final.csv"

# Load data
df = pd.read_csv(csv_file_path)

# Ensure commit index is sorted per repository
df = df.sort_values(by=["Repo", "Commit Index"])

# Get unique repositories
repos = df["Repo"].unique()

# Process CWE data for each repository
for repo in repos:
    repo_df = df[df["Repo"] == repo]  # Filter data for the repo
    cwe_counter = Counter()

    for cwe_list in repo_df["Unique CWEs"].dropna():
        cwes = eval(cwe_list) if isinstance(cwe_list, str) else []
        cwe_counter.update(cwes)

    # Top 10 CWEs
    top_cwes = cwe_counter.most_common(10)

    if not top_cwes:
        continue  # Skip if no CWEs exist

    sorted_cwes = sorted(top_cwes, key=lambda x: int(x[0]))
    cwe_ids = [f"CWE-{cwe[0]}" for cwe in sorted_cwes]
    counts = [cwe[1] for cwe in sorted_cwes]

    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(cwe_ids, counts)
    plt.xlabel("CWE")
    plt.ylabel("Frequency")
    plt.title(f"Top 10 CWEs - {repo}")
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()
