### Receptor del mensaje
import socket
import pickle

### Funciones utilizadas para la implementacion de CRC
def sumarSegmentos(segmento1, segmento2):
    carrier = '0'
    suma = ''

    for item in range(7,-1,-1):
        a = int(segmento1[item])
        b = int(segmento2[item])
        
        resultadoAB = a + b + int(carrier)
        if resultadoAB == 0:
            suma = '0' + suma
            carrier = '0'
        elif resultadoAB == 1:
            suma = '1' + suma
            carrier = '0'
        elif resultadoAB == 2:
            suma = '0' + suma
            carrier = '1'
        elif resultadoAB == 3:
            suma = '1' + suma
            carrier = '1'

    if carrier != '0':
        suma = carrier + suma
    return suma
    
def recepcionCRC32(binario):
    n = 8
    arrayBinary = [binario[i:i+n] for i in range(0, len(binario), n)]
    arrayBinary.pop()
    sumaSegmentos = '00000000'

    for i in arrayBinary:
        sumaSegmentos = sumarSegmentos(sumaSegmentos, i)

        if len(sumaSegmentos) > 8:
            sumaSegmentos = sumaSegmentos[1:]
            sumaSegmentos = sumarSegmentos(sumaSegmentos, '00000001')

    return sumaSegmentos

def verificador(segmento1, segmento2):
    carrier = '0'
    suma = ''

    for item in range(7,-1,-1):
        a = int(segmento1[item])
        b = int(segmento2[item])
        
        resultadoAB = a + b + int(carrier)
        if resultadoAB == 0:
            suma = '0' + suma
            carrier = '0'
            return False
        elif resultadoAB == 1:
            suma = '1' + suma
            carrier = '0'
        elif resultadoAB == 2:
            suma = '0' + suma
            carrier = '1'
            return False
        elif resultadoAB == 3:
            suma = '1' + suma
            carrier = '1'
            return False

    return True

### Conexion por Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1',9000))

### Primero se recibe el mensaje por parte del emisor
mensajeRecibido = sock.recv(1024)
while mensajeRecibido:
    mensajeDesempacado = pickle.loads(mensajeRecibido)

    algoritmo = mensajeDesempacado[0]
    mensaje = mensajeDesempacado[1:]
    print(mensajeDesempacado)
    if algoritmo == '0':
        print('Verificacion Hamming')
        sep = mensaje.find(',')
        mensajeSeparado = mensaje[:sep]
        r = int(mensaje[sep+1:])
        print(mensajeSeparado) ## Este es el binario que generaste xD
        print(r) ## r

        # Esto es lo que tenes que quitar en el emisor y descomentar aca
        # Y copiar las funciones del emisor para Hammer y ponerlas hasta arriba :)
        #correction = VerFnl(mensajeSeparado, r) 
        #print("El error se ecuentra en  " + str(correction))

    else:
        print('Verificacion CRC-32')
        print(mensaje)

        verificar = recepcionCRC32(mensaje)
        segmento = mensaje[-8:]
        resultado = verificador(verificar,segmento)

        if resultado:
            print('True')
        else:
            print('False')

    mensajeRecibido = sock.recv(1024)

sock.close()
