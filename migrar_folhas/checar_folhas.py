import requests
import funcoes
from configuracao.conexao import AUTORIZACAO, TOKENUSER, ACCESSUSER


url = 'https://folha.betha.cloud/folha/api/folha/listagem-folhas?filter=(competencia = "2013-05" and ((' \
      'tipoProcessamento = "MENSAL" and subTipoProcessamento = "ADIANTAMENTO") or (tipoProcessamento = "MENSAL" and ' \
      'subTipoProcessamento = "INTEGRAL") or (tipoProcessamento = "MENSAL" and subTipoProcessamento = "COMPLEMENTAR") '\
      'or (tipoProcessamento = "DECIMO_TERCEIRO_SALARIO" and subTipoProcessamento = "ADIANTAMENTO") or (' \
      'tipoProcessamento = "DECIMO_TERCEIRO_SALARIO" and subTipoProcessamento = "INTEGRAL") or (tipoProcessamento = ' \
      '"RESCISAO" and subTipoProcessamento = "INTEGRAL") or (tipoProcessamento = "RESCISAO" and subTipoProcessamento ' \
      '= "COMPLEMENTAR") or (tipoProcessamento = "FERIAS" and subTipoProcessamento = ' \
      '"INTEGRAL")))&limit=200&offset=0&processamento=&selecaoAvancada=&sort= '

payload = {}
headers = {
    'Authorization': TOKENUSER,
    'User-Access': ACCESSUSER
}

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()

for i in response["content"]:
    if i["tipoProcessamento"] == 'FERIAS':
        url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-ferias/{i['calculo']['id']}"
    elif i["tipoProcessamento"] == 'MENSAL':
        url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-mensal/{i['calculo']['id']}"
    else:
        url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-decimo-terceiro/{i['calculo']['id']}"

    url = f"https://pessoal.betha.cloud/service-layer/v1/api/calculo-folha-mensal/{i['calculo']['id']}"
    payload = {}
    headers = {
        'Authorization': AUTORIZACAO
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    if i['matricula']['id'] != response["calculoFolhaMatriculas"][0]["matricula"]["id"]:
        print(i['matricula']['id'], ',')

    # print(f"UPDATE bethadba.controle_migracao_registro set i_chave_dsk2 = {i['id']} WHERE id_gerado = {i[
    # 'matricula']['id']}")
