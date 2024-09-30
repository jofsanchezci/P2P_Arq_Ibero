import socket

def send_request_to_load_balancer():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8000))
    
    # Enviar una solicitud al balanceador
    request = "Hello Load Balancer".encode('utf-8')
    client_socket.send(request)
    
    # Recibir la respuesta
    response = client_socket.recv(1024)
    print(f"Received: {response.decode('utf-8')}")
    
    client_socket.close()

if __name__ == "__main__":
    send_request_to_load_balancer()
