while True: 
        edad = int(input("Ingrese su edad: "))
        if not type(edad) == int:
                    print("Escribe un número entero válido.")
        if 0 <= edad <= 120:
            break
        else:
            print("Edad debe estar entre 0 y 120.")   
print(f"Tu edad es {edad}")  