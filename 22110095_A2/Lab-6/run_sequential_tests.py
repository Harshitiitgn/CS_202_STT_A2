import subprocess

# Define output file
output_file = "sequential_output.txt"

# Open the file in write mode
with open(output_file, "w") as f:
    for i in range(1, 11):  # Run 10 times
        f.write(f"Run {i}:\n")
        result = subprocess.run(["pytest"], capture_output=True, text=True)
        f.write(result.stdout)  # Store test output
        f.write("\n" + "=" * 50 + "\n")  # Separator for clarity

print(f"Sequential test results saved in {output_file}")
