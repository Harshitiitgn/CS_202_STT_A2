import pandas as pd
import matplotlib.pyplot as plt

# Path to your CSV file
csv_file_path = "final.csv"

# Load data
df = pd.read_csv(csv_file_path)

# Ensure commit index is sorted per repository
df = df.sort_values(by=["Repo", "Commit Index"])

# Get unique repositories
repos = df["Repo"].unique()

# Plot for each repository
for repo in repos:
    repo_df = df[df["Repo"] == repo]  # Filter data for the repo

    plt.figure(figsize=(12, 7))
    plt.plot(repo_df["Commit Index"], repo_df["High Severity"], label="High Severity", marker='o')
    plt.plot(repo_df["Commit Index"], repo_df["Medium Severity"], label="Medium Severity", marker='s')
    plt.plot(repo_df["Commit Index"], repo_df["Low Severity"], label="Low Severity", marker='^')

    plt.xlabel("Commit Index")
    plt.ylabel("Number of Issues")
    plt.title(f"Severity Trends Over Time - {repo}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
