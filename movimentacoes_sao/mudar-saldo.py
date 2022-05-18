import json
from configuracao.conexao import AUTORIZACAO
import requests

url = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/periodo-aquisitivo-licenca-premio?limit=400"

payload={}
headers = {
  'Authorization': AUTORIZACAO,
  'content-type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()

mandar = []
contador = 0
contador2= 0
contCanc = 0
contAqui = 0
contQui  = 0
naoMuda  = 0
tamanho = len(response['content'])
for i in response['content']:
    if i['situacao'] == 'CANCELADO' and i['saldo']>0:
        contCanc += 1
        mandar.append({
            "idIntegracao": str(i['id']),
            "conteudo": {
                "id": i['id'],
                "saldo": 0.0
            }
        })
    elif i['situacao'] == 'ADQUIRIDO':
        totalMov = 0
        for j in i['movimentacoes']:
            totalMov += j['quantidade']
        novoSaldo = i['direito'] - totalMov
        if novoSaldo != i['saldo']:
            contAqui += 1
            if novoSaldo == 0:
                i['situacao'] = 'QUITADO'
            mandar.append({
                "idIntegracao": str(i['id']),
                "conteudo": {
                    "id": i['id'],
                    "saldo": novoSaldo,
                    "situacao": i['situacao']
                }
            })
        else:
            naoMuda += 1
    elif i['situacao'] == 'QUITADO':
        if i['saldo'] > 0:
            contQui +=1
            mandar.append({
                "idIntegracao": str(i['id']),
                "conteudo": {
                    "id": i['id'],
                    "saldo": 0.0
                }
            })
        else:
            naoMuda += 1
    else:
        naoMuda += 1
    contador += 1
    # if contador % 100 == 0 or contador == tamanho:
    #     mandar = json.dumps(mandar)
    #     url = "https://pessoal.cloud.betha.com.br/service-layer/v1/api/periodo-aquisitivo-licenca-premio/"
    #     response2 = requests.request("POST", url, headers=headers, data=mandar)
    #     print(response2.json())
    #     print(mandar)
    #     mandar = []
    #     contador2 += 1
    #     print("lote:", contador2)
print("total registro",contador)
print("cancelados",contCanc)
print("adquiridos",contAqui)
print("quitados",contQui)
print("nao muda",naoMuda)
print("total",contCanc+contAqui+contQui+naoMuda)
