import socket
import threading

# Definir el host y puerto
HOST = '127.0.0.1'  # Localhost
PORT = 5002         # Puerto para conectar

# Función para manejar la recepción de mensajes
def handle_receive(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            if not msg:  # Si el mensaje es vacío, desconecta
                print(f"[DISCONNECTED] {addr} disconnected.")
                break
            print(f"[{addr}] {msg}")
        except ConnectionResetError:
            print(f"[ERROR] Connection with {addr} lost.")
            break
        except Exception as e:
            print(f"[ERROR] Unexpected error with {addr}: {e}")
            break
    conn.close()

# Función para enviar mensajes a un nodo
def send_message(peer_socket):
    while True:
        try:
            message = input("Enter message: ")
            if message.lower() == 'exit':
                print("[EXITING] Closing connection...")
                peer_socket.close()
                break
            peer_socket.send(message.encode('utf-8'))
        except BrokenPipeError:
            print("[ERROR] Unable to send message, connection lost.")
            break

# Crear el servidor P2P para aceptar conexiones
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_receive, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

# Crear un cliente P2P que se conecta a otro nodo
def connect_to_peer(peer_host, peer_port):
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        peer_socket.connect((peer_host, peer_port))
        print(f"[CONNECTED] Connected to peer at {peer_host}:{peer_port}")
    except Exception as e:
        print(f"[ERROR] Unable to connect to peer: {e}")
        return
    
    # Crear un hilo para recibir mensajes
    thread_receive = threading.Thread(target=handle_receive, args=(peer_socket, (peer_host, peer_port)))
    thread_receive.start()

    # Crear un hilo para enviar mensajes
    thread_send = threading.Thread(target=send_message, args=(peer_socket,))
    thread_send.start()

# Función principal para iniciar el nodo P2P
def start_p2p():
    print("Welcome to the P2P network!")
    mode = input("Do you want to start a server (s) or connect to a peer (c)? ")

    if mode == 's':
        start_server()
    elif mode == 'c':
        peer_host = input("Enter peer's IP: ")
        peer_port = int(input("Enter peer's Port: "))
        connect_to_peer(peer_host, peer_port)
    else:
        print("Invalid option. Exiting.")

if __name__ == "__main__":
    start_p2p()
