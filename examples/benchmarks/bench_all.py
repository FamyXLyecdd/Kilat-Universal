import time

# Loop
start = time.time()
for _ in range(50000000):
    pass
print(f"Loop Time: {time.time() - start}")

# Fib
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

start = time.time()
res = fib(25)
print(f"Fib(25) Result: {res}")
print(f"Fib Time: {time.time() - start}")

# Array
data = []
start = time.time()
for i in range(1000000):
    data.append(i)
print(f"Array Len: {len(data)}")
print(f"Array Time: {time.time() - start}")
