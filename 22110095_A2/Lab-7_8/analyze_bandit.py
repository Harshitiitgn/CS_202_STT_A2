import json
import os
import subprocess
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

# Directory containing all repos' JSON analysis folders
combined_analysis_dir = "."
output_file = "overall_analysis.txt"

# Dictionary to store results per commit
analysis_results = {}

# Function to get commit timestamp from Git inside the correct repo folder
def get_commit_time(commit_hash, repo_path):
    try:
        cmd = f'git -C "{repo_path}" show -s --format=%ci {commit_hash}'
        result = subprocess.check_output(cmd, shell=True, text=True).strip()
        return datetime.strptime(result, "%Y-%m-%d %H:%M:%S %z")
    except subprocess.CalledProcessError:
        print(f"Error fetching commit time for {commit_hash} in {repo_path}")
        return None

# Process each repository folder inside combined_analysis
for repo_name in os.listdir(combined_analysis_dir):
    repo_path = os.path.join(combined_analysis_dir, repo_name)

    # Ensure it's a directory before proceeding
    if not os.path.isdir(repo_path):
        continue

    print(f"Processing repository: {repo_name}")

    # Process each JSON file inside the repository folder
    for file in os.listdir(repo_path):
        if file.startswith("bandit_output_") and file.endswith(".json"):
            commit_hash = file.split("_")[-1].replace(".json", "")

            json_file_path = os.path.join(repo_path, file)
            with open(json_file_path, "r") as f:
                data = json.load(f)

            commit_time = get_commit_time(commit_hash, repo_path)
            if not commit_time:
                continue  # Skip commits with no timestamp

            high_confidence = 0
            medium_confidence = 0
            low_confidence = 0

            high_severity = 0
            medium_severity = 0
            low_severity = 0

            unique_cwes = set()

            for issue in data.get("results", []):
                # Count confidence levels
                confidence = issue.get("issue_confidence", "").upper()
                if confidence == "HIGH":
                    high_confidence += 1
                elif confidence == "MEDIUM":
                    medium_confidence += 1
                elif confidence == "LOW":
                    low_confidence += 1

                # Count severity levels
                severity = issue.get("issue_severity", "").upper()
                if severity == "HIGH":
                    high_severity += 1
                elif severity == "MEDIUM":
                    medium_severity += 1
                elif severity == "LOW":
                    low_severity += 1

                # Collect unique CWEs
                cwe_info = issue.get("issue_cwe", {}).get("id")
                if cwe_info:
                    unique_cwes.add(str(cwe_info))

            # Store results
            analysis_results[commit_time] = {
                "repo": repo_name,
                "commit_hash": commit_hash,
                "high_confidence": high_confidence,
                "medium_confidence": medium_confidence,
                "low_confidence": low_confidence,
                "high_severity": high_severity,
                "medium_severity": medium_severity,
                "low_severity": low_severity,
                "unique_cwes": list(unique_cwes),
            }

# Sort commits by time
sorted_commits = sorted(analysis_results.keys())

# Data for plotting
high_severity_timeline = []
medium_severity_timeline = []
low_severity_timeline = []
cwe_frequency = defaultdict(int)

# Save results and prepare for plotting
with open(output_file, "w") as f:
    for commit_time in sorted_commits:
        result = analysis_results[commit_time]
        f.write(f"Repo: {result['repo']}\n")
        f.write(f"Commit: {result['commit_hash']} ({commit_time})\n")
        f.write(f"  High Confidence Issues: {result['high_confidence']}\n")
        f.write(f"  Medium Confidence Issues: {result['medium_confidence']}\n")
        f.write(f"  Low Confidence Issues: {result['low_confidence']}\n")
        f.write(f"  High Severity Issues: {result['high_severity']}\n")
        f.write(f"  Medium Severity Issues: {result['medium_severity']}\n")
        f.write(f"  Low Severity Issues: {result['low_severity']}\n")
        f.write(f"  Unique CWEs: {', '.join(result['unique_cwes']) if result['unique_cwes'] else 'None'}\n")
        f.write("-" * 50 + "\n")

        # Append severity levels for plotting
        high_severity_timeline.append((commit_time, result["high_severity"]))
        medium_severity_timeline.append((commit_time, result["medium_severity"]))
        low_severity_timeline.append((commit_time, result["low_severity"]))

        # Count CWE occurrences
        for cwe in result["unique_cwes"]:
            cwe_frequency[cwe] += 1

print(f"Analysis completed! Results saved in {output_file}")

# Plot severity introduction and elimination trends (RQ1 & RQ2)
plt.figure(figsize=(12, 6))
plt.plot(*zip(*high_severity_timeline), label="High Severity", color="red", marker="o")
plt.plot(*zip(*medium_severity_timeline), label="Medium Severity", color="orange", marker="s")
plt.plot(*zip(*low_severity_timeline), label="Low Severity", color="green", marker="^")
plt.xlabel("Commit Time")
plt.ylabel("Number of Issues")
plt.title("Vulnerability Severity Introduction & Fixing Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.savefig("severity_trend.png")
plt.show()

# Plot CWE frequency (RQ3)
sorted_cwe = sorted(cwe_frequency.items(), key=lambda x: x[1], reverse=True)[:10]  # Top 10 CWE
cwe_labels, cwe_counts = zip(*sorted_cwe) if sorted_cwe else ([], [])

plt.figure(figsize=(10, 5))
plt.bar(cwe_labels, cwe_counts, color="blue")
plt.xlabel("CWE ID")
plt.ylabel("Occurrence Count")
plt.title("Top 10 Most Frequent CWEs")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.savefig("cwe_distribution.png")
plt.show()
