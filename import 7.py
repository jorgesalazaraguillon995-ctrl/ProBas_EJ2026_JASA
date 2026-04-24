import os
if os.path.exists("demofile.txt"):
    R = input(int(print("desea continuar con la eliminacion  <1=si/2=no?:")))
    if(R==1):
    os.remove("demofile.txt")
    else:
    print("eliminacion cancelada")
else:
    print("el archivo no existe")