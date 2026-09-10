inicio = int(input("Inicio: "))
final = int(input("Final:"))
for i in range(inicio, final):
    if i%2 != 0:
        print (i, "es impar")