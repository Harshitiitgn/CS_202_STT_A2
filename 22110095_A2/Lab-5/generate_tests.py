import os
import subprocess
import multiprocessing

# Configuration
BASE_DIR = "algorithms/"  # Target folder for test generation
OUTPUT_DIR = "generated_tests"  # Where test cases will be saved
MAX_SEARCH_TIME = 180  # Limit to 60 seconds per module
MAX_ITERATIONS = 100  # Reduce iterations for faster processing
PARALLEL_PROCESSES = 3  # Adjust based on your CPU cores
SEED = 42  # Fix randomness for consistent results

# Function to run Pynguin on a single module
def run_pynguin(module_name):
    command = [
        "pynguin",
        "--project-path=./",
        f"--module-name={module_name}",
        f"--output-path={OUTPUT_DIR}",
        "--maximum-search-time", str(MAX_SEARCH_TIME),
        "--maximum-iterations", str(MAX_ITERATIONS),
        "--seed", str(SEED),
    ]
    print(f"Running: {' '.join(command)}")
    subprocess.run(command)

# Collect all module names
modules = []
for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":  # Exclude __init__.py
            module_path = os.path.join(root, file)
            module_name = module_path.replace(os.path.sep, ".").replace(".py", "")
            modules.append(module_name)

# Run test generation in parallel
if __name__ == "__main__":
    with multiprocessing.Pool(PARALLEL_PROCESSES) as pool:
        pool.map(run_pynguin, modules)

    print("✅ Test case generation complete!")
