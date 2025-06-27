import socket

def master(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Master listening on {host}:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            message = input("Enter string to send to worker: ")
            conn.sendall(message.encode('utf-8'))

if __name__ == '__main__':
    master()
