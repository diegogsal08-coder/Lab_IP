USUARIO = "diego"
CLAVE = "diego123" 

usuario = input("USUARIO: ").strip().lower()
clave = input("Contraseña: ")

if usuario == USUARIO and clave == CLAVE:
    print("Bienvenido ")
else:
   print("Credenciales incorrectas")