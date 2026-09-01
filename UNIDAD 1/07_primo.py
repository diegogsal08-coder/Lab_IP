n=input("Ingrese un número: ")
n=int(n)
if n<=1:
    print("no es primo")
    i=2
while i<n:
    if n%i==0:
        print("es primo")
    elif n%i==0:  i==n