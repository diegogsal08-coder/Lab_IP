while True: 
    try: 
        edad = int(input("Ingrese su edad: "))
        if 0 <= edad <= 120:
            break
        else:
            print("Edad debe estar entre 0 y 120.")   
    except ValueError:
        print("Por favor, ingrese un número válido.")
print(f"Tu edad es {edad}")  