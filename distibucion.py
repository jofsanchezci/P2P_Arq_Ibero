import socket
import threading

# Lista de servidores backend (pueden ser IPs diferentes)
backend_servers = [
    ('127.0.0.1', 8001),
    ('127.0.0.1', 8002),
    ('127.0.0.1', 8003)
]

# Índice para el algoritmo Round-Robin
current_server_index = 0
lock = threading.Lock()

def handle_client(client_socket):
    global current_server_index

    # Obtener el servidor backend usando Round-Robin
    with lock:
        backend_server = backend_servers[current_server_index]
        current_server_index = (current_server_index + 1) % len(backend_servers)

    # Conectar al servidor backend
    backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend_socket.connect(backend_server)

    # Redirigir la solicitud del cliente al backend
    request = client_socket.recv(1024)
    backend_socket.send(request)

    # Recibir la respuesta del backend y enviarla al cliente
    response = backend_socket.recv(1024)
    client_socket.send(response)

    # Cerrar los sockets
    backend_socket.close()
    client_socket.close()

def start_load_balancer(host='127.0.0.1', port=8000):
    # Crear el socket para el balanceador de carga
    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.bind((host, port))
    load_balancer_socket.listen(5)
    print(f"Load Balancer listening on {host}:{port}")

    while True:
        # Aceptar conexiones entrantes de clientes
        client_socket, addr = load_balancer_socket.accept()
        print(f"[CONNECTION] Client {addr} connected.")
        
        # Crear un hilo para manejar la conexión del cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_load_balancer()
