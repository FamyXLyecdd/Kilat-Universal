// Node.js Benchmark
const { performance } = require('perf_hooks');

// Loop
let start = performance.now();
for(let i=0; i<50000000; i++) {}
console.log(`Loop Time: ${(performance.now() - start)/1000}`);

// Fib
function fib(n) {
    if (n < 2) return n;
    return fib(n-1) + fib(n-2);
}
start = performance.now();
let res = fib(25);
console.log(`Fib(25) Result: ${res}`);
console.log(`Fib Time: ${(performance.now() - start)/1000}`);

// Array
let data = [];
start = performance.now();
for(let i=0; i<1000000; i++) {
    data.push(i);
}
console.log(`Array Len: ${data.length}`);
console.log(`Array Time: ${(performance.now() - start)/1000}`);
