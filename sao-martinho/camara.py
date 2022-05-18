import requests
import json
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


url = f"https://folha.betha.cloud/folha/api/periodo-aquisitivo?limit=300"
payload = []
headers = {
  'Authorization': TOKENUSER,
  'User-Access': ACCESSUSER
}

response2 = requests.request("GET", url, headers=headers, data=payload)
response2 = response2.json()
contador =0
lista = []
for i in response2['content']:
  if i['matricula']['cargo']['id'] == 130672:
    contador += 1
    lista.append(i['id'])
print(contador)
print(lista)
