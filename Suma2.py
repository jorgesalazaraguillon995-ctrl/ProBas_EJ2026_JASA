def suma(a,b):
    try:
        return a + b
    except Exception as e:
        return "Ha ocurrido un error: " + str(e)


print(suma(5,10))
print(suma(5.5,10.4))
print(suma(5,10.5))
print(suma('a','b'))
print(suma(5,'c'))
print(suma(10,10))
