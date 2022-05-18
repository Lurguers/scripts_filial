from math import comb
import requests
from time import sleep
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER

res = [28921, 28923, 8116, 28943, 29223, 29003, 10882, 8081, 29068, 8096, 8113, 8080]
comMov = []
contador = 0
for i in res:
    sleep(1)
    payload = {}
    headers = {
        'Authorization': TOKENUSER,
        'User-Access': ACCESSUSER
    }
    url = "https://rh.betha.cloud/rh/api/gestao-periodo-aquisitivo/"
    contador += 1
    response2 = requests.request("GET", url+str(i), headers=headers, data=payload)
    response2 = response2.json()
    if response2['movimentacoes']:
        comMov.append(response2)
    print(contador)
print(comMov)