import socket

def start_backend_server(host, port, server_name):
    backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend_socket.bind((host, port))
    backend_socket.listen(5)
    print(f"{server_name} listening on {host}:{port}")

    while True:
        client_socket, addr = backend_socket.accept()
        print(f"[{server_name}] Connection from {addr}")
        request = client_socket.recv(1024)

        # Responder al cliente
        response = f"Response from {server_name}\n".encode('utf-8')
        client_socket.send(response)
        client_socket.close()

if __name__ == "__main__":
    # Cambiar 'Server 1', 'Server 2', 'Server 3' según el puerto
    start_backend_server('127.0.0.1', 8001, 'Server 1')
    # Para otros servidores, puedes cambiar el puerto a 8002, 8003, etc.
