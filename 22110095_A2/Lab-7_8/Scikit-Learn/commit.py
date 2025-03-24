import os
import subprocess

# File to store commit hashes
commit_file = "commits.txt"

# Get the last 100 non-merge commit hashes
try:
    result = subprocess.run(
        ["git", "log", "--no-merges", "-n", "100", "--pretty=format:%H"],
        capture_output=True,
        text=True,
        check=True
    )
    
    commits = result.stdout.strip().split("\n")
    
    # Save commit hashes to a file
    with open(commit_file, "w") as file:
        file.write("\n".join(commits))
    
    print(f"Stored {len(commits)} commits in {commit_file}")
    
except subprocess.CalledProcessError as e:
    print(f"Error fetching commits: {e}")
