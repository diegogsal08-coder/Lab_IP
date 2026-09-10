total = float(input("Total de la cuenta: "))
propina = float(input("Propina: "))
numpersonas = int(input("Número de personas: "))

propina = total * (propina / 100)
totalconpropina = total + propina
total_por_persona = totalconpropina / numpersonas

print (f"total de la propina: {propina: .2f}")
print (f"total con propina: {totalconpropina: .2f}")
print (f"total por persona: {total_por_persona: .2f}")