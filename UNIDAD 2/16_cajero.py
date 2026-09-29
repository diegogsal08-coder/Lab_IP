def consultar_saldo():
    print("Saldo 0.0")
def depositar():
    print("Deposito realizado ")
def retirar():
    print("Retiro realizado")
def salir():
    print("Saliendo del cajero")

while True:
    print("1. Consultar saldo")
    print("2. Depostiar")
    print("3. Retirar")
    print("4. Salir")

    opcion = input("Opcion:")
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

