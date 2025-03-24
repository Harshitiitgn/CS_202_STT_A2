import subprocess

# Read commit hashes from file
with open("commits.txt", "r") as file:
    commits = file.read().splitlines()

for commit in commits:
    try:
        print(f"Checking out commit: {commit}")
        subprocess.run(["git", "checkout", commit], check=True)

        # Run Bandit and save output to JSON file
        output_file = f"bandit_output_{commit}.json"
        print(f"Running Bandit on {commit} and saving results to {output_file}")
        
        subprocess.run(["bandit", "-r", ".", "-f", "json", "-o", output_file], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error processing commit {commit}: {e}")

print("Analysis completed for all commits.")
