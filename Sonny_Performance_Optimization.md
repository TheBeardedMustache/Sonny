# Sonny Performance Optimization

This guide describes a deep profiling and performance tuning process for all Sonny microservices (frontend, backend_core, symbolic_ai). The goal is to analyze resource usage (CPU, memory, latency, throughput) and apply targeted optimizations to minimize latency, reduce memory and CPU consumption, and improve overall efficiency.

## 1. Profiling Methodology

### 1.1 Request Latency & Throughput
- Use HTTP benchmarking tools (e.g., `wrk`, `hey`) against service endpoints:
  ```bash
  # Example: measure 200 concurrent requests for 30s
  wrk -t4 -c200 -d30s http://localhost:${FRONTEND_PORT}/process/
  ```

### 1.2 CPU & Memory Profiling
- Leverage Python profilers and samplers:
  - `py-spy` for sampling CPU: `py-spy record -o app.svg -- python app.py`
  - `memory_profiler` for line-by-line memory usage: add `@profile` decorators.
  - `cProfile` for function-level timing: run via `python -m cProfile -o profile.prof module:main()`.

### 1.3 Flamegraphs & Visualization
- Generate flamegraphs with `py-spy` or `speedscope`:
  ```bash
  py-spy record -o profile.svg --pid <PID>
  ```

## 2. Tools & Setup

Install the necessary profiling tools:
```bash
pip install py-spy memory-profiler speedscope
sudo apt-get install wrk
```

## 3. Service-Specific Profiling

### 3.1 Frontend Service (Streamlit Proxy)
- Profile Streamlit startup and proxy layers.
- Identify slow UI components and caching gaps.

### 3.2 Backend Core Service (FastAPI Proxy)
- Profile request proxying, interpreter/response pipeline.
- Measure HTTP proxy overhead and Python-level processing costs.

### 3.3 Symbolic AI Service
- Profile LLM invocation paths (`interpret`, `respond`, `script`).
- Identify hotspots in parsing or network I/O.

## 4. Analysis & Bottleneck Identification

- Aggregate profiling data and pinpoint top-consuming functions.
- Focus on high-frequency code paths and I/O waits.

## 5. Performance Tuning Recommendations

- **Asynchronous I/O**: ensure all inter-service calls use `httpx.AsyncClient`.
- **Connection pooling**: reuse HTTP connections.
- **Caching**: memoize pure functions and state queries.
- **Worker tuning**: adjust Uvicorn/FastAPI worker count and use `uvloop`.
- **Optimize JSON**: use faster serializers (`orjson`).

## 6. Validation & Regression Testing

- Re-run benchmarks (`wrk`, `hey`) and profilers after each change.
- Document latency/throughput improvements in a change log.

## 7. Next Steps

- Iteratively refine optimizations based on monitored metrics.
- Integrate auto-scaling policies when deployed in production.