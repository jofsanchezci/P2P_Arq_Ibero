# Red P2P en Python

Este es un programa simple que implementa una red Peer-to-Peer (P2P) en Python. El programa permite que varios nodos se comuniquen directamente entre sí, actuando tanto como clientes como servidores, según su rol en la red.

## Características

- Cada nodo puede actuar tanto como servidor (aceptando conexiones) como cliente (enviando y recibiendo mensajes).
- Soporta comunicación multi-hilo para que los nodos puedan enviar y recibir mensajes simultáneamente.
- Manejo de errores para problemas de conexión y desconexiones inesperadas.
- Los mensajes se pueden intercambiar de manera bidireccional entre los nodos.
- La red opera localmente usando `127.0.0.1` (localhost), pero puede adaptarse para IPs remotas.

## Requisitos

- Python 3.x
- No se necesitan bibliotecas externas. La implementación está basada en los módulos estándar de Python: `socket` y `threading`.

## Cómo Usar

### 1. Ejecutar como Servidor
Para iniciar un nodo en modo servidor, sigue estos pasos:

1. Abre una terminal y ejecuta el script:

    ```bash
    python p2p.py
    ```

2. Cuando se te pregunte, elige iniciar como servidor escribiendo `s`.

3. El servidor comenzará a escuchar en `127.0.0.1:5000`. Aceptará conexiones entrantes de otros pares.

### 2. Ejecutar como Cliente
Para conectarte a otro par que actúa como servidor:

1. Abre otra terminal y vuelve a ejecutar el script:

    ```bash
    python p2p.py
    ```

2. Cuando se te pregunte, elige conectarte a un par escribiendo `c`.

3. Introduce la dirección IP (`127.0.0.1` para pruebas locales) y el puerto (`5000` para pruebas locales) del servidor.

4. Una vez conectado, puedes comenzar a enviar mensajes. Usa la terminal para ingresar mensajes, que se enviarán al par. También puedes recibir mensajes del par.

5. Para salir de la conexión, escribe `exit`.

### 3. Envío y Recepción Simultáneos
- El programa maneja tanto el envío como la recepción de mensajes usando hilos separados, lo que garantiza que puedas comunicarte en ambas direcciones sin bloqueo.
- Los mensajes recibidos de los pares se imprimirán en la terminal.
- Puedes enviar mensajes escribiéndolos en la terminal.

## Manejo de Errores
- Si la conexión con un par se pierde inesperadamente, el programa capturará el error y te informará.
- Si intentas enviar un mensaje a un par desconectado, el programa te notificará que la conexión está rota.

## Personalización

- **Cambiar el Host/Puerto:** Puedes cambiar el `HOST` y `PORT` predeterminados en el script modificando las variables `HOST` y `PORT` en la parte superior del código.
- **Conexiones Remotas:** Para conexiones remotas, reemplaza `127.0.0.1` con la dirección IP adecuada del par.

## Ejemplo

1. Inicia un servidor en una terminal:

    ```
    python p2p.py
    ```

    Elige el modo servidor (`s`), y el servidor comenzará a escuchar en `127.0.0.1:5000`.

2. Inicia un cliente en otra terminal:

    ```
    python p2p.py
    ```

    Elige el modo cliente (`c`), y proporciona la IP del servidor (`127.0.0.1`) y el puerto (`5000`).

3. Intercambia mensajes entre el servidor y el cliente en ambas terminales.

## Notas

- Esta es una implementación básica de una arquitectura P2P y no soporta características más avanzadas como descubrimiento de pares, difusión de mensajes o intercambio de archivos.
- El programa está diseñado con fines de aprendizaje y puede extenderse para manejar escenarios más complejos, como múltiples conexiones de pares, descubrimiento remoto de pares o cifrado de mensajes.

# Balanceador de Carga con Round-Robin en Python

Este proyecto es un balanceador de carga simple implementado en Python que utiliza el algoritmo Round-Robin para distribuir las solicitudes entre varios servidores backend. Cada solicitud que llega al balanceador se redirige a uno de los servidores en la lista de backend de forma secuencial.

## Características

- **Distribución de Carga con Round-Robin:** Las solicitudes de los clientes se distribuyen equitativamente entre los servidores backend de forma secuencial.
- **Soporte para Múltiples Servidores:** El balanceador de carga puede manejar múltiples servidores backend en diferentes puertos o direcciones IP.
- **Multi-hilo:** Se utiliza `threading` para manejar múltiples conexiones de clientes de manera simultánea.
- **Comunicación Cliente-Servidor:** El balanceador actúa como intermediario, recibiendo solicitudes de los clientes y reenviándolas a los servidores backend.

## Requisitos

- Python 3.x
- No se requieren bibliotecas externas. El programa utiliza las bibliotecas estándar de Python (`socket` y `threading`).

## Estructura del Proyecto

El proyecto tiene dos componentes principales:

1. **Balanceador de Carga:** Escucha en un puerto específico y distribuye las solicitudes entrantes a los servidores backend utilizando el algoritmo Round-Robin.
   
2. **Servidores Backend:** Varios servidores que reciben las solicitudes distribuidas por el balanceador y responden al cliente. Estos pueden estar en diferentes puertos o incluso en diferentes máquinas.

## Cómo Usar

### 1. Ejecutar los Servidores Backend

Primero, debes iniciar los servidores backend que manejarán las solicitudes:

1. Abre tres terminales y ejecuta el siguiente script en cada uno, cambiando el puerto para cada servidor:

    ```bash
    python backend_server.py
    ```

    - Para el primer servidor: usa el puerto `8001` y cambia el nombre a `Server 1`.
    - Para el segundo servidor: usa el puerto `8002` y cambia el nombre a `Server 2`.
    - Para el tercer servidor: usa el puerto `8003` y cambia el nombre a `Server 3`.

2. El código del servidor backend es el siguiente:

    ```python
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
            response = f"Response from {server_name}
".encode('utf-8')
            client_socket.send(response)
            client_socket.close()

    if __name__ == "__main__":
        start_backend_server('127.0.0.1', 8001, 'Server 1')
        # Cambiar puerto y nombre para Server 2, Server 3, etc.
    ```

### 2. Ejecutar el Balanceador de Carga

En otra terminal, ejecuta el balanceador de carga:

```bash
python load_balancer.py
```

El balanceador estará escuchando en el puerto `8000` para recibir las solicitudes de los clientes y redirigirlas a los servidores backend.

### 3. Enviar Solicitudes a través del Cliente

Finalmente, puedes usar el siguiente código para simular un cliente que envía solicitudes al balanceador de carga:

```python
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
```

Este cliente enviará una solicitud al balanceador de carga, y el balanceador se encargará de redirigirla a uno de los servidores backend disponibles. La respuesta se recibirá desde el backend y se imprimirá en la terminal del cliente.

### 4. Ejemplo de Ejecución

1. Inicia tres servidores backend:
    - `Server 1` en el puerto 8001.
    - `Server 2` en el puerto 8002.
    - `Server 3` en el puerto 8003.

2. Inicia el balanceador de carga, que escuchará en el puerto 8000.

3. Ejecuta el cliente varias veces. Verás que las solicitudes se distribuyen de forma equitativa entre los servidores backend, utilizando el algoritmo Round-Robin.

## Personalización

- **Cambiar la Lista de Servidores:** Puedes modificar la lista de servidores backend en el script del balanceador de carga. Simplemente agrega o elimina servidores de la lista `backend_servers`.
- **Conexiones Remotas:** Si deseas probar con servidores en diferentes máquinas, cambia la dirección IP de los servidores backend en la lista a direcciones IP remotas.
