Mensaje="luis"
Lista=list(Mensaje)
lista2=[]
print(Lista)
intervalo=int(input("Ingrese el intervalo del ruido"))
intervalo2=0
for i in range(len(Mensaje)):
    intervalo2+=1
    if intervalo2==intervalo:
        lista2.append("q")
        intervalo2=0
    else:
        lista2.append(Lista[i])
        # Lista[i]=Mensaje.replace(Mensaje[i],"q")
        # print(Lista)

    print(lista2)
asd=""
asd=asd.join(lista2)
print(asd)