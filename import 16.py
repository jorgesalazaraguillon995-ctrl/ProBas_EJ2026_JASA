import json, requests
# modifica los valores númericos para ver otros personajes
for i in range (1,58):
    url = "http://swapi.dev/api/people/"+str(i)+'/'
    response = requests.get(url)
    # si consultaramos alguna que no existe, es mejor terminar
    if response.status_code != 200:
        break
    infopersonaje = json.loads(response.text)
    print(infopersonaje)
    print(type(infopersonaje))
    