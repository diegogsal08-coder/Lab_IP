while True:
    nombre = input("Ingrese su nombre: ").strip()
    #print (nombre) 
    if nombre and nombre.replace(" ", "").isalpha():
        break

    print("Por favor, ingrese un nombre válido (solo letras y espacios).")

nombre_normalizado = nombre.title()
print(f"Hola, {nombre_normalizado}")