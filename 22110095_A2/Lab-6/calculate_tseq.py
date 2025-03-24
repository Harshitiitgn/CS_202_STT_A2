import subprocess
import time

# Define output file
output_file = "sequential_execution_times.txt"
execution_times = []
num_runs = 5  # Number of times to run the test suite

# Run the test suite 5 times and measure execution time
for i in range(1, num_runs + 1):
    print(f"Executing test suite: Run {i}/{num_runs}")
    
    start_time = time.time()
    subprocess.run(["pytest", "--tb=short"], capture_output=True, text=True)
    end_time = time.time()
    
    exec_time = end_time - start_time
    execution_times.append(exec_time)

# Calculate average execution time (Tseq)
Tseq = sum(execution_times) / num_runs

# Save results
with open(output_file, "w") as f:
    f.write("Sequential Execution Times:\n")
    for idx, t in enumerate(execution_times, 1):
        f.write(f"Run {idx}: {t:.2f} seconds\n")
    f.write(f"\nAverage Sequential Execution Time (Tseq): {Tseq:.2f} seconds\n")

print(f"\nAll execution times saved in {output_file}")
print(f"Average Sequential Execution Time (Tseq): {Tseq:.2f} seconds")
