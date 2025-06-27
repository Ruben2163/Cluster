import socket

def worker(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = s.recv(1024)
        print(f"Worker received: {data.decode('utf-8')}")

if __name__ == '__main__':
    worker()
