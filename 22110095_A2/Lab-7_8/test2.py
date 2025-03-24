import pandas as pd

# Input and output CSV file paths
csv_file_path = "parsed_bandit_summary.csv"
output_file_path = "bandit_summary_with_commit_index.csv"

# Load CSV
df = pd.read_csv(csv_file_path)

# Convert timestamp column to datetime for sorting
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort by Repo and Timestamp
df.sort_values(by=["Repo", "Timestamp"], ascending=[True, True], inplace=True)

# Assign commit index per repository
df["Commit Index"] = df.groupby("Repo").cumcount() + 1  # Start indices from 1

# Save the updated CSV
df.to_csv(output_file_path, index=False)

print("✅ Commit indices updated successfully in:", output_file_path)
