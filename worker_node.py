import socket
import pickle
import numpy as np

def calculate_ma(data, window=25):
    return np.convolve(data, np.ones(window)/window, mode='valid')

class WorkerNode:
    def __init__(self, master_host: str = 'localhost', master_port: int = 5050):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((master_host, master_port))

    def process_data(self):
        while True:
            data = pickle.loads(self.socket.recv(4096))
            results = {}
            
            for symbol, prices in data:
                ma25 = calculate_ma(prices)
                results[symbol] = ma25.tolist()
                
            self.socket.send(pickle.dumps(results))

if __name__ == "__main__":
    worker = WorkerNode()
    worker.process_data()
