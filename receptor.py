### Receptor del mensaje
import socket
import pickle

### Conexion por Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1',9000))

### Primero se recibe el mensaje por parte del emisor
mensajeRecibido = sock.recv(1024)
while mensajeRecibido:
    mensajeDesempacado = pickle.loads(mensajeRecibido)
    print(mensajeDesempacado)

    mensajeRecibido = sock.recv(1024)

sock.close()
