import matplotlib.pyplot as plt
import numpy as np

# Data from results
configs = [
    "load (1, auto)", "no (1, auto)", "load (auto, 1)", "no (auto, 1)",
    "load (auto, auto)", "no (auto, auto)"
]
speedup_ratios = [0.08, 0.05, 0.74, 0.75, 0.07, 0.08]
execution_times = [85.51, 129.58, 9.57, 9.43, 103.98, 92.47]

# Create Speedup Ratio Plot
plt.figure(figsize=(10, 5))
plt.bar(configs, speedup_ratios, color="royalblue", alpha=0.7)
plt.xlabel("Configurations (Mode, Workers, Threads)")
plt.ylabel("Speedup Ratio")
plt.title("Speedup Ratios for Different Configurations")
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

# Create Execution Time Plot
plt.figure(figsize=(10, 5))
plt.bar(configs, execution_times, color="firebrick", alpha=0.7)
plt.xlabel("Configurations (Mode, Workers, Threads)")
plt.ylabel("Execution Time (s)")
plt.title("Execution Times for Different Configurations")
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
