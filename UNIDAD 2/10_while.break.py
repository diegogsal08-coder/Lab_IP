while True:
    opcion = input("eliga A, B o C: "). strip().upper()

    if opcion in ("A", "B", "C"):
        break

    print("Opción inválida. intentalo de nuevo")

print(f"Elegiste la opción {opcion}")