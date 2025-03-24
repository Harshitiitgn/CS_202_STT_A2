import pandas as pd
import re

# Path to your input text file and output CSV
txt_file_path = "overall_analysis.txt"
csv_file_path = "parsed_bandit_summary.csv"

# Regular expressions for parsing
repo_pattern = re.compile(r"Repo: (.+)")
commit_pattern = re.compile(r"Commit: (\w+) \((.+)\)")
high_conf_pattern = re.compile(r"High Confidence Issues: (\d+)")
med_conf_pattern = re.compile(r"Medium Confidence Issues: (\d+)")
low_conf_pattern = re.compile(r"Low Confidence Issues: (\d+)")
high_sev_pattern = re.compile(r"High Severity Issues: (\d+)")
med_sev_pattern = re.compile(r"Medium Severity Issues: (\d+)")
low_sev_pattern = re.compile(r"Low Severity Issues: (\d+)")
cwe_pattern = re.compile(r"Unique CWEs: (.+)")

# List to store extracted commit data
data = []

# Variables for storing commit info
current_repo = None
commit_index = 0

# Read and parse the file
with open(txt_file_path, "r") as file:
    for line in file:
        line = line.strip()

        # Detect repository name
        repo_match = repo_pattern.match(line)
        if repo_match:
            current_repo = repo_match.group(1)
            commit_index = 0  # Reset commit index for each repo

        # Detect commit details
        commit_match = commit_pattern.match(line)
        if commit_match and current_repo:
            commit_index += 1
            commit_hash = commit_match.group(1)
            timestamp = commit_match.group(2)

            # Initialize issue counts to zero
            high_conf = med_conf = low_conf = 0
            high_sev = med_sev = low_sev = 0
            unique_cwes = ""

        # Extract different issue types
        if (match := high_conf_pattern.match(line)):
            high_conf = int(match.group(1))
        elif (match := med_conf_pattern.match(line)):
            med_conf = int(match.group(1))
        elif (match := low_conf_pattern.match(line)):
            low_conf = int(match.group(1))
        elif (match := high_sev_pattern.match(line)):
            high_sev = int(match.group(1))
        elif (match := med_sev_pattern.match(line)):
            med_sev = int(match.group(1))
        elif (match := low_sev_pattern.match(line)):
            low_sev = int(match.group(1))
        elif (match := cwe_pattern.match(line)):
            unique_cwes = match.group(1)

            # Save extracted data (only after CWEs are found)
            data.append([
                current_repo, commit_index, commit_hash, timestamp,
                high_conf, med_conf, low_conf,
                high_sev, med_sev, low_sev,
                unique_cwes
            ])

# Convert to DataFrame
df = pd.DataFrame(data, columns=[
    "Repo", "Commit Index", "Commit Hash", "Timestamp",
    "High Confidence", "Medium Confidence", "Low Confidence",
    "High Severity", "Medium Severity", "Low Severity",
    "Unique CWEs"
])

# Save to CSV
df.to_csv(csv_file_path, index=False)

print(f"✅ Successfully saved all extracted data to {csv_file_path}")
