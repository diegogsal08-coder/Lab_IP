for numero in range(1, 7):
    cuadrado=numero**2
    print(numero,cuadrado)

materias = ["python", "Linux", "Interfaces"]

for posicion, materia in enumerate(materias, start=1):
    print(f"Materia {posicion}. {materia}")

    
materias = ["Python", "Linux", "Interfaces"]

for materia in materias:
    print(materia)

cadena = "123456789ABCDEF"
for letra in cadena:
    print(letra)

for numero in range(0, 7, 2):
    cuadrado=numero**2
    print(numero,cuadrado)