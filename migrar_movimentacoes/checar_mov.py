import funcoes
import requests
from configuracao.conexao import AUTORIZACAO

resultado = funcoes.consultar("SELECT top 10000 start at 1 * FROM bethadba.controle_migracao_registro cmr WHERE tipo_registro = "
                              "'periodo-aquisitivo-ferias';")
offset = 0
total = []
naoGerados = []
for i in resultado:
    offset += 1
    url = f"https://pessoal.cloud.betha.com.br/service-layer/v1/api/periodo-aquisitivo-ferias/{i['id_gerado']}"

    payload = {}
    headers = {
        'Authorization': AUTORIZACAO
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        naoGerados.append(i['id_gerado'])
        continue

    response = response.json()

    if response['movimentacoes']:
        total.append(response['id'])

    if offset % 100 == 0:
        print(offset)

print(total)
print(naoGerados)
