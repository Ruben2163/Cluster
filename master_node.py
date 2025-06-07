import socket
import pickle
import yfinance as yf
import numpy as np
from typing import List, Dict

class MasterNode:
    def __init__(self, port: int = 5050):
        self.port = port
        self.workers = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', port))
        self.server_socket.listen(5)

    def register_worker(self):
        conn, addr = self.server_socket.accept()
        self.workers.append((conn, addr))
        print(f"Worker registered: {addr}")

    def get_stock_data(self, symbols: List[str]) -> Dict:
        data = {}
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            data[symbol] = stock.history(period="100d")['Close'].values
        return data

    def distribute_work(self, data: Dict):
        chunks = np.array_split(list(data.items()), len(self.workers))
        results = []
        
        for worker, chunk in zip(self.workers, chunks):
            worker[0].send(pickle.dumps(chunk))
            results.append(pickle.loads(worker[0].recv(4096)))
            
        return {k: v for d in results for k, v in d.items()}

if __name__ == "__main__":
    master = MasterNode()
    print("Waiting for workers...")
    # Wait for workers to connect
    while len(master.workers) < 2:  # Wait for at least 2 workers
        master.register_worker()
    
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    data = master.get_stock_data(symbols)
    results = master.distribute_work(data)
    
    print("Results:", results)
