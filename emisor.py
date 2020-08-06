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
    
def emisionCRC32(binario):
    n = 8
    arrayBinary = [binario[i:i+n] for i in range(0, len(binario), n)]
    sumaSegmentos = '00000000'

    for i in arrayBinary:
        sumaSegmentos = sumarSegmentos(sumaSegmentos, i)

        if len(sumaSegmentos) > 8:
            sumaSegmentos = sumaSegmentos[1:]
            sumaSegmentos = sumarSegmentos(sumaSegmentos, '00000001')

    return xor(sumaSegmentos)
    
def xor(segmento):
    resultado = ''
    for i in segmento:
        if i == '0':
            resultado = resultado + '1'
        else:
            resultado = resultado + '0'

    return resultado
    
### Conexion por Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1',9000))
sock.listen(1)
conexion, direccion = sock.accept()
print("Conexion relaizada con exito de la direccion", str(direccion))

### Procesamiento de capas del mensaje a enviar
Mensaje=input("Ingrese el mensaje: ")
mensajeEnviar = ''

### Convertir mensaje de STR -> BIN
Binario=' '.join(map(bin,bytearray(Mensaje,'utf8')))
Binario=Binario.replace("b","")
Binario=Binario.replace(" ","")
print("Mensaje en binario:", Binario)
binarioDeteccion = Binario

opcionita=int(input("Cual algoritmo desea probar, 1.Hamming 2.CRC-32 (Seleccion un numero): "))
if opcionita == 1:
    m = len(Binario) 
    r = VerRdn(m)
    dat = PosRdn(Binario, r) 
    dat = VerPrd(dat, r) 
    print(dat)
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
        objeto=""
        objeto=objeto.join(lista2)
        print("Ruido")
        print(objeto)
        print("Ruido")
        dat = objeto

    ### Utilizamos pickle para hacer provecho del uso del paquete bitarray    
    dat = '0' + dat + ',' + str(r)
    mensajeEnviar = pickle.dumps(dat)

else:
    dat = Binario
    ### Se ingresa el ruido al mensaje
    ruido=int(input("Desea agregar ruido al mensaje, 1.Si 2.No (Seleccion un numero): "))
    if ruido==1:
        Lista=list(Binario)
        lista2=[]
        print(Lista)
        intervalo=int(input("Ingrese el intervalo del ruido: "))
        intervalo2=0
        for i in range(len(Binario)):
            intervalo2+=1
            if intervalo2==intervalo:
                lista2.append("1")
                intervalo2=0
            else:
                lista2.append(Lista[i])
        objeto=""
        objeto=objeto.join(lista2)
        print("Ruido")
        print(objeto)
        print("Ruido")
        dat = objeto


    complemento = emisionCRC32(dat)
    mensaje = '1' + Binario + complemento

    ### Utilizamos pickle para hacer provecho del uso del paquete bitarray    
    mensajeEnviar = pickle.dumps(mensaje)

### Se envia el objeto mensaje
conexion.send(mensajeEnviar)

conexion.close()
