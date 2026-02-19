import matplotlib.pyplot as plt
import numpy as np
import subprocess
import re

def run_program(tasks_list: list[int]):
    results = []
    for numTasks in tasks_list:
        cmd1 = ['./mandelbrot_ispc', '-t', str(numTasks)]
        try:
            result = subprocess.run(cmd1, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
            continue
        
        ispc_speedup_match = re.search(r"([0-9.]+)x speedup from ISPC", result.stdout)
        task_speedup_match = re.search(r"([0-9.]+)x speedup from task ISPC", result.stdout)
        
        if ispc_speedup_match and task_speedup_match:
            ispc_speedup = float(ispc_speedup_match.group(1))
            task_speedup = float(task_speedup_match.group(1))
            results.append((numTasks, task_speedup / ispc_speedup))
            print(f"Tasks: {numTasks}, ISPC Speedup: {ispc_speedup}x, Task Speedup: {task_speedup}x, Rate: {task_speedup / ispc_speedup}x")
        else:
            print(f"Could not find speedup in output: {result.stdout}")
    return results

if __name__ == "__main__":
    taskss_list = [1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 50, 80, 100, 200, 400, 800]
    results = run_program(taskss_list)
    if results:
        threads, opt_speedup = zip(*results)
        plt.plot(threads, opt_speedup, marker='o')
        plt.legend(['Optimized Speedup'])
        plt.xlabel('Number of Tasks')
        plt.ylabel('Speedup')
        plt.title('Mandelbrot Speedup vs Number of Tasks')
        plt.grid(True)
        plt.savefig("speedup_plot.png")
        plt.close()
    else:
        print("No results to plot.")


        
    