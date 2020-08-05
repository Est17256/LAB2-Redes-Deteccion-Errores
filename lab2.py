### Emisor del mensaje
import re
import socket
import pickle

### Funciones utilizadas para la implementacion de Hamming
def VerRdn(m): 
    for i in range(m): 
        if(2**i >= m + i + 1): 
            return i 
def PosRdn(data, r): 
    j = 0
    k = 1
    m = len(data) 
    res = '' 
    for i in range(1, m + r+1): 
        if(i == 2**j): 
            res = res + '0'
            j += 1
        else: 
            res = res + data[-1 * k] 
            k += 1
    return res[::-1] 
def VerPrd(dat, r): 
    n = len(dat) 
    for i in range(r): 
        val = 0
        for j in range(1, n + 1): 
            if(j & (2**i) == (2**i)): 
                val = val ^ int(dat[-1 * j]) 
        dat = dat[:n-(2**i)] + str(val) + dat[n-(2**i)+1:] 
    return dat 
def VerFnl(dat, nr): 
    n = len(dat) 
    res = 0
    for i in range(nr): 
        val = 0
        for j in range(1, n + 1): 
            if(j & (2**i) == (2**i)): 
                val = val ^ int(dat[-1 * j]) 
        res = res + val*(10**i) 
    return int(str(res), 2)


Mensaje=input("Ingrese el mensaje: ")

### Conexion por Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1',9000))
sock.listen(1)
conexion, direccion = sock.accept()
print("Conexion relaizada con exito de la direccion", str(direccion))

### Procesamiento de capas del mensaje a enviar
mensajeEnviar = ''

### Convertir mensaje de STR -> BIN
Binario=' '.join(map(bin,bytearray(Mensaje,'utf8')))
Binario=Binario.replace("b","")
Binario=Binario.replace(" ","")
print("Mensaje en binario:", Binario)
m = len(Binario) 
r = VerRdn(m) 
dat = PosRdn(Binario, r) 
dat = VerPrd(dat, r) 
print(dat)
print("Error Data is " + dat)
correction = VerFnl(dat, r) 
print("El error se ecuentra en " + str(correction))
print(dat)

### Se ingresa el ruido al mensaje
ruido=int(input("Desea agregar ruido al mensaje, 1.Si 2.No (Seleccion un numero): "))
if ruido==1:
    Lista=list(dat)
    lista2=[]
    print(Lista)
    intervalo=int(input("Ingrese el intervalo del ruido: "))
    intervalo2=0
    for i in range(len(dat)):
        intervalo2+=1
        if intervalo2==intervalo:
            lista2.append("1")
            intervalo2=0
        else:
            lista2.append(Lista[i])
            # Lista[i]=Mensaje.replace(Mensaje[i],"q")
            # print(Lista)
        #print(lista2)
    objeto=""
    objeto=objeto.join(lista2)
    print("Ruido")
    print(objeto)
    print("Ruido")
    correction = VerFnl(objeto, r) 
    print("El error se ecuentra en  " + str(correction))
    dat = objeto

### Utilizamos pickle para hacer provecho del uso del paquete bitarray    
mensajeEnviar = pickle.dumps(dat)

### Se envia el objeto mensaje
conexion.send(mensajeEnviar)

conexion.close()
