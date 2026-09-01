numero=1005
H=""
while numero or H=="":
    H="0123456789ABCDEF"[numero%16]+H
    numero//=16
print(H)