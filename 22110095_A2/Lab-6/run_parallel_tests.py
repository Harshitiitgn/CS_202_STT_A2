import subprocess
import time
import re
import json
import os

# Define the test configurations
n_values = ["1", "auto"]
parallel_threads_values = ["1", "auto"]
dist_modes = ["load", "no"]
repetitions = 3  # Number of times to run each configuration

# File to store results
RESULTS_FILE = "parallel_test_results.json"

# Store results
results = []

# Function to run pytest and collect execution time & failures
def run_pytest(n, parallel_threads, dist):
    cmd = [
        "pytest",
        f"-n={n}",
        f"--parallel-threads={parallel_threads}",
        f"--dist={dist}",
        "--tb=short"
    ]

    print(f"Running: {' '.join(cmd)}")
    
    total_time = 0
    failed_tests = set()

    for i in range(repetitions):
        start_time = time.perf_counter()
        
        # Run pytest and capture output
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        total_time += execution_time

        # Extract failed tests from output
        failed = re.findall(r"FAILED (.*?)::", result.stdout + result.stderr)
        failed_tests.update(failed)

        print(f"Run {i+1}: Time = {execution_time:.2f}s, Failures = {len(failed)}")

    # Compute average execution time
    avg_time = total_time / repetitions

    # Store results
    results.append({
        "n": n,
        "parallel_threads": parallel_threads,
        "dist": dist,
        "avg_time": round(avg_time, 2),
        "failed_tests": list(failed_tests)
    })

# Run tests for all combinations
for n in n_values:
    for parallel_threads in parallel_threads_values:
        for dist in dist_modes:
            run_pytest(n, parallel_threads, dist)

# Save results to a JSON file
with open(RESULTS_FILE, "w") as f:
    json.dump(results, f, indent=4)

# Print results
print("\n=== Final Results (Saved to test_results.json) ===")
for res in results:
    print(f"-n={res['n']}, --parallel-threads={res['parallel_threads']}, --dist={res['dist']}")
    print(f"  Avg Time: {res['avg_time']}s, Failed Tests: {res['failed_tests']}\n")
