import matplotlib.pyplot as plt
import numpy as np
import subprocess
import re

def run_program(threads_list: list[int]):
    results = []
    for numThreads in threads_list:
        cmd1 = ['./mandelbrot', '--threads', str(numThreads)]
        try:
            result = subprocess.run(cmd1, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
            continue
        
        simple_speedup_match = re.search(r"([0-9.]+)x speedup", result.stdout)

        cmd2 = ['./mandelbrot', '--threads', str(numThreads), '-b']
        try:
            result = subprocess.run(cmd2, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
            continue

        opt_speedup_match = re.search(r"([0-9.]+)x speedup", result.stdout)
        
        if opt_speedup_match and simple_speedup_match:
            opt_speedup = float(opt_speedup_match.group(1))
            simple_speedup = float(simple_speedup_match.group(1))
            results.append((numThreads, opt_speedup, simple_speedup))
            print(f"Threads: {numThreads}, Speedup: {simple_speedup}x, opt speedup: {opt_speedup}")
        else:
            print(f"Could not find speedup in output: {result.stdout}")
    return results

if __name__ == "__main__":
    threads_list = range(1, 32)
    results = run_program(threads_list)
    if results:
        threads, simple_speedups, opt_speedup = zip(*results)
        plt.plot(threads, simple_speedups, marker='o')
        plt.plot(threads, opt_speedup, marker='o')
        plt.legend(['Simple Speedup', 'Optimized Speedup'])
        plt.xlabel('Number of Threads')
        plt.ylabel('Speedup')
        plt.title('Mandelbrot Speedup vs Number of Threads')
        plt.grid(True)
        plt.savefig("speedup_plot.png")
        plt.close()
    else:
        print("No results to plot.")


        
    