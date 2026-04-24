try:
    libro = load_workbook("Mi_1er_excel.xlsx")
except FileNotFoundError:
        prin("El archivo no existe, adiós!")
        exit()
