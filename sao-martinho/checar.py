import requests
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


url = "https://folha.betha.cloud/folha/api/matricula/matriculas-ferias-vencidas?competencia=2021-08&limit=300&offset=0"

payload={}
headers = {
  'Authorization': TOKENUSER,
  'User-Access': ACCESSUSER
}

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()
cont = 0
periodos = []
for i in response['content']:
  if i['situacao'] != 'DEMITIDO':
    continue
  url = f"https://folha.betha.cloud/folha/api/periodo-aquisitivo?filter=(matricula in ({i['id']}))&limit=100&offset=0"
  response2 = requests.request("GET", url, headers=headers, data=payload)
  response2 = response2.json()
  for j in response2['content']:
    if j['situacao'] == 'ADQUIRIDO':
      periodos.append(j['id'])
      cont += 1
print(periodos)
print(cont)
