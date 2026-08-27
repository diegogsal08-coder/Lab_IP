n = int(input("Introduce un numero: "))
i=2
while i<n:
    if n%i==0:
        print("No es primo")
        break
    i+=1
else:
    print("Es primo")