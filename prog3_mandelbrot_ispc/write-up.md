# prog3

## Part 1: ISPC SIMD

用 8-wide SIMD 来计算 Mandelbrot 集合，Speedup 大约在6.0x，小于理论值 8.0x，原因可能是因为 Mandelbrot 集合的计算中存在分支（即不同的点可能需要不同数量的迭代），这会导致 SIMD 处理器无法完全利用其并行能力，从而降低了实际的加速效果。

## Part 2: ISPC Task Parallelism

利用task机制将计算任务分成多个子任务*并发执行*
- ISPC 会根据系统核心数量创建线程池，将task动态映射到线程池中的线程上执行
- task 较小时，受负载均衡的影响，加速曲线类似于 simple-thread
- task 增大后，工作负载更均衡。又因为ISPC的线程池机制，线程切换和调度开销较小，所以加速曲线更接近理想的线性加速