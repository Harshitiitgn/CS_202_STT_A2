import json
import os

# Directory containing Bandit JSON reports
report_dir = "."  # Change this if reports are in a different folder
output_file = "bandit_analysis.txt"

# Dictionary to store results per commit
analysis_results = {}

# Process each JSON file
for file in os.listdir(report_dir):
    if file.startswith("bandit_output_") and file.endswith(".json"):
        commit_hash = file.split("_")[-1].replace(".json", "")

        with open(os.path.join(report_dir, file), "r") as f:
            data = json.load(f)

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

            # Extract CWEs correctly
            cwe_info = issue.get("issue_cwe", {})
            cwe_id = cwe_info.get("id")
            if cwe_id:
                unique_cwes.add(f"CWE-{cwe_id}")

        # Store results
        analysis_results[commit_hash] = {
            "high_confidence": high_confidence,
            "medium_confidence": medium_confidence,
            "low_confidence": low_confidence,
            "high_severity": high_severity,
            "medium_severity": medium_severity,
            "low_severity": low_severity,
            "unique_cwes": list(unique_cwes),
        }

# Save results to a file
with open(output_file, "w") as f:
    for commit, result in analysis_results.items():
        f.write(f"Commit: {commit}\n")
        f.write(f"  High Confidence Issues: {result['high_confidence']}\n")
        f.write(f"  Medium Confidence Issues: {result['medium_confidence']}\n")
        f.write(f"  Low Confidence Issues: {result['low_confidence']}\n")
        f.write(f"  High Severity Issues: {result['high_severity']}\n")
        f.write(f"  Medium Severity Issues: {result['medium_severity']}\n")
        f.write(f"  Low Severity Issues: {result['low_severity']}\n")
        f.write(f"  Unique CWEs: {', '.join(result['unique_cwes']) if result['unique_cwes'] else 'None'}\n")
        f.write("-" * 50 + "\n")

print(f"Analysis completed! Results saved in {output_file}")
