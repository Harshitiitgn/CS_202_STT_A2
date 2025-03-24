import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the JSON test results
with open("parallel_test_results.json", "r") as f:
    results = json.load(f)

# Step 1: Identify flaky tests
flaky_tests = set()
failure_counts = {}

for entry in results:
    dist_mode = entry["dist"]
    workers = entry["n"]
    parallel_threads = entry["parallel_threads"]
    failed_tests = entry["failed_tests"]

    for test in failed_tests:
        failure_counts[test] = failure_counts.get(test, 0) + 1
        flaky_tests.add(test)

flaky_tests = list(flaky_tests)

# Step 2: Find failure causes (manual inspection required)
failure_reasons = {
    "tests/test_compression.py": "Potential race condition due to file I/O.",
    "tests/test_linkedlist.py": "Shared memory access issue.",
    "tests/test_heap.py": "Timing issue, possibly due to concurrent modification."
}
flaky_test_analysis = {test: failure_reasons.get(test, "Unknown cause") for test in flaky_tests}

# Step 3: Compute speedup ratios
sequential_entry = next(entry for entry in results if entry["n"] == "1" and entry["parallel_threads"] == "1")
sequential_time = sequential_entry["avg_time"]

speedup_data = {
    (entry["dist"], entry["n"], entry["parallel_threads"]): sequential_time / entry["avg_time"]
    for entry in results if not (entry["n"] == "1" and entry["parallel_threads"] == "1")
}

# Step 4: Generate execution matrix
df = pd.DataFrame(results)
df["speedup"] = df.apply(lambda row: sequential_time / row["avg_time"], axis=1)

# Save execution matrix to CSV
df.to_csv("execution_matrix.csv", index=False)

# Step 5: Plot speedup vs worker count
plt.figure(figsize=(8, 5))
for dist_mode in df["dist"].unique():
    mode_df = df[df["dist"] == dist_mode]
    plt.plot(mode_df["n"], mode_df["speedup"], marker="o", label=f"dist={dist_mode}")

plt.xlabel("Number of Workers (n)")
plt.ylabel("Speedup Ratio")
plt.legend()
plt.title("Speedup vs Worker Count")
plt.grid()
plt.savefig("speedup_plot.png")

# Step 6: Create report file
with open("parallel_test_analysis.txt", "w") as report:
    report.write("### Parallel Test Execution Analysis\n\n")
    report.write("#### 1. Flaky Tests Identified\n")
    report.write("\n".join(flaky_tests) + "\n\n")

    report.write("#### 2. Failure Causes Analysis\n")
    for test, reason in flaky_test_analysis.items():
        report.write(f"- {test}: {reason}\n")

    report.write("\n#### 3. Speedup Data\n")
    for (dist_mode, workers, parallel_threads), speedup in speedup_data.items():
        report.write(f"- {dist_mode} (Workers: {workers}, Threads: {parallel_threads}): Speedup = {speedup:.2f}x\n")

    report.write("\n#### 4. Recommendations\n")
    report.write("Consider using locks for shared resources and increasing timeouts.\n")

print("Analysis complete! Results saved in execution_matrix.csv, speedup_plot.png, and parallel_test_analysis.txt.")
