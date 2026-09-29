MAX = 3

for intento in range(1, MAX + 1):
    usuario = input("Usuario: ")
    clave = input("Contraseña: ")

    if usuario == "diego" and clave == "hola":
        print("Bienvenido pendejote")
        break 

    print("Credenciales incorrectas")
else:
    print("Acceso bloqueado")