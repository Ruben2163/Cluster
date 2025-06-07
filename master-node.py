import multiprocessing as mp
import random
import time

# Generate synthetic stock price data
def generate_data(size=1000):
    random.seed(42)
    return [1000 + random.gauss(0, 10) for _ in range(size)]  # Prices around 1000

def main():
    # Configuration
    NUM_WORKERS = 12  # Match your laptop's 12 threads
    DATA_SIZE = 1000  # Total data points
    WINDOW = 20       # Moving average window

    # Generate data
    data = generate_data(DATA_SIZE)
    chunk_size = DATA_SIZE // NUM_WORKERS
    chunks = [(i, data[i * chunk_size:(i + 1) * chunk_size]) for i in range(NUM_WORKERS)]
    # Handle remainder
    if DATA_SIZE % NUM_WORKERS != 0:
        chunks.append((NUM_WORKERS, data[NUM_WORKERS * chunk_size:]))

    # Create pipes and start workers
    connections = []
    processes = []
    for i, chunk in chunks:
        parent_conn, child_conn = mp.Pipe()  # Create a pipe for this worker
        connections.append((i, parent_conn))
        # Start worker process, passing the child connection
        p = mp.Process(target=worker_main, args=(i, child_conn, chunk, WINDOW))
        p.start()
        processes.append(p)
        child_conn.close()  # Close child end in master
        print(f"Master started worker {i} with chunk size {len(chunk)}")

    # Collect results
    results = []
    for chunk_id, conn in connections:
        result = conn.recv()  # Receive result from worker
        results.append((chunk_id, result))
        print(f"Master received result for chunk {chunk_id} (size: {len(result)})")
        conn.close()

    # Clean up
    for p in processes:
        p.join()

    # Sort and combine results
    results.sort(key=lambda x: x[0])  # Ensure correct order
    combined_result = []
    for _, result in results:
        combined_result.extend(result)

    print(f"First 10 moving averages: {combined_result[:10]}")
    print(f"Total results: {len(combined_result)}")

# Worker main function (included here but run from worker.py)
def worker_main(worker_id, conn, chunk, window):
    from worker import compute_moving_average  # Import from worker.py
    result = compute_moving_average(chunk, window)
    conn.send(result)
    conn.close()
    print(f"Worker {worker_id} finished processing chunk (size: {len(chunk)})")

if __name__ == "__main__":
    main()