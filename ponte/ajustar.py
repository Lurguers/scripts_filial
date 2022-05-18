import requests
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


url = "https://folha.betha.cloud/folha/api/periodo-aquisitivo-decimo/matriculas?filter=(tipo+in+(%22FUNCIONARIO%22,+%22ESTAGIARIO%22,+%22APOSENTADO%22,+%22PENSIONISTA%22))&limit=20&offset=0&selecaoAvancada=28989"

payload={}
headers = {
  'Authorization': TOKENUSER,
  'User-Access': ACCESSUSER
}

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()
lista = []
for i in response['content']:
    url = f"https://folha.betha.cloud/folha/api/periodo-aquisitivo-decimo?filter=(matricula+in+({i['id']}))&limit=50&offset=0&sort="

    payload = {}
    headers = {
        'Authorization': TOKENUSER,
        'User-Access': ACCESSUSER
    }

    response2 = requests.request("GET", url, headers=headers, data=payload)
    response2 = response2.json()
    for j in response2['content']:
        if j['situacao']!= 'EM_ANDAMENTO':
            lista.append(j['id'])
print(lista)
# lista = [10881881]
for k in lista:
    import requests
    import json

    url = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/periodo-aquisitivo-decimo-terceiro"

    payload = json.dumps([
        {
            "conteudo": {
                "id": k,
                "situacao": "QUITADO"

            }
        }
    ])
    headers = {
        'Authorization': AUTORIZACAO,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

