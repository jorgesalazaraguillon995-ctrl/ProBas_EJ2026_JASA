from fractions import Fraction
try:
    a = Fraction(input('Capture una fraccion: '))
except ZeroDivisionError:
    print('Fraccion invalida')
    