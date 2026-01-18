import subprocess
import psutil
import time
import os
import threading

RESULTS_FILE = "kilat_benchmarks.txt"

def monitor_process(pid, result_dict):
    try:
        proc = psutil.Process(pid)
        peak_memory = 0
        while proc.is_running():
            try:
                mem = proc.memory_info().rss / 1024 / 1024 # MB
                if mem > peak_memory:
                    peak_memory = mem
                time.sleep(0.01)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break
        result_dict['memory'] = peak_memory
    except:
        result_dict['memory'] = 0

def run_command(name, cmd):
    print(f"Running {name}...")
    start_time = time.time()
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    
    mem_stats = {'memory': 0}
    monitor_thread = threading.Thread(target=monitor_process, args=(process.pid, mem_stats))
    monitor_thread.start()
    
    stdout, stderr = process.communicate()
    end_time = time.time()
    monitor_thread.join()
    
    duration = end_time - start_time
    output = stdout.decode('utf-8')
    
    # Parse output for internal timer if available (more accurate for logic), 
    # but we will use wall clock for the whole process as the baseline.
    
    log = f"[{name}]\n"
    log += f"Command: {' '.join(cmd)}\n"
    log += f"Time (Wall): {duration:.4f}s\n"
    log += f"Peak Memory: {mem_stats['memory']:.2f} MB\n"
    log += f"Output:\n{output}\n"
    if stderr:
        log += f"Stderr:\n{stderr.decode('utf-8')}\n"
    log += "-" * 40 + "\n"
    
    return log

report = "=== KILAT SOVEREIGN ECOSYSTEM BENCHMARK ===\n"
report += f"Date: {time.ctime()}\n"
report += "Platform: Windows (Rust/Python/Node)\n\n"

# 1. Compile Kilat Release
print("Compiling Kilat (Release)...")
subprocess.run(["cargo", "build", "--release"], check=True)
kilat_exe = os.path.abspath("target/release/kilat.exe")

# 2. Loop Benchmark
report += "--- TEST 1: LOOP (50M Iterations) ---\n"
report += run_command("Kilat Loop", [kilat_exe, "run", "benchmarks/bench_loop.klt"])
# Note: Python/Node run all tests in one file, so I'll create temp files or run the suite.
# Actually, for granular comparison, I'll run the 'bench_all' scripts and parse them, 
# or just run specific snippets. The bench_all prints specific sections.
# To keep it comparable, I'll run the full bench_all script and capture it as one block 
# vs running Kilat individually.

# Run Kilat Fib and Array
report += "--- TEST 2: RECURSION (Fib 25) ---\n"
report += run_command("Kilat Fib", [kilat_exe, "run", "benchmarks/bench_fib.klt"])

report += "--- TEST 2b: ITERATION (Fib 25) ---\n"
report += run_command("Kilat Fib Iter", [kilat_exe, "run", "benchmarks/bench_fib_iter.klt"])

report += "--- TEST 3: MEMORY (Array 1M) ---\n"
report += run_command("Kilat Array", [kilat_exe, "run", "benchmarks/bench_array.klt"])

# 3. Python Suite
report += "\n=== PYTHON REFERENCE ===\n"
report += run_command("Python Suite", ["python", "benchmarks/bench_all.py"])

# 4. Node.js Suite
report += "\n=== NODE.JS REFERENCE ===\n"
report += run_command("Node.js Suite", ["node", "benchmarks/bench_all.js"])

with open(RESULTS_FILE, "w") as f:
    f.write(report)

print(f"Benchmark complete. Saved to {RESULTS_FILE}")
