def consultar_saldo():
    print("Saldo 0.0")
def depositar():
    print("Deposito realizado ")
def retirar():
    print("Retiro realizado")
def salir():
    print("Saliendo del cajero")
def mostrar_menu():
    print("1. Consultar saldo")
    print("2. Depostiar")
    print("3. Retirar")
    print("4. Salir")
    return input("Opcion: ").strip()
def main():
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            consultar_saldo()
        elif opcion == "2":
            depositar()
        elif opcion == "3":
            retirar()
        elif opcion == "4":
            salir()
            break
        else:
            print("Opcion no valida")       
def login():
    USUARIO = "diego"
    CLAVE = "diego123" 

    usuario = input("USUARIO: ").strip().lower()
    clave = input("Contraseña: ")

    if usuario == USUARIO and clave == CLAVE:
        main()
    
    else:
        print("Credenciales no validas")
login()
