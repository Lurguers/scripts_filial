import requests
from time import sleep
from configuracao.conexao import AUTORIZACAO, ACCESSUSER

hasNext = True
offset = 0
limit = 50
contador = 0
contador2= 0
ids = []

while hasNext:
  sleep(2)
  url = f"https://rh.betha.cloud/rh/api/matricula/manutencao-averbacao?ativos=false&limit={limit}&offset={offset}"
  contador +=1
  payload={}
  headers = {
    'Authorization': AUTORIZACAO,
    'User-Access': ACCESSUSER
  }
  offset+= limit
  response = requests.request("GET", url, headers=headers, data=payload)
  response = response.json()
  for i in response['content']:
    if (i['situacao']=='DEMITIDO' or i['situacao']=='TRABALHANDO') and i['averbacao'] is None:
      contador2 += 1
      ids.append([i['dataInicioContrato'],i['descricao']])
  hasNext = response['hasNext']
  print(f"\r{contador}",end="")
print()
print(contador2)
print(ids)
