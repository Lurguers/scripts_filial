import requests
from configuracao.conexao import executar
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


hasNext = True
contador = 0
limit = 100
offset = 0
contador2 = 0
while hasNext:
    url = f"https://pessoal.betha.cloud/service-layer/v1/api/matricula?offset={offset}&limit={limit}"

    payload = {}
    headers = {
        'Authorization': AUTORIZACAO
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    hasNext = response['hasNext']
    contador += 1
    offset = contador * limit
    print(f"\r Pagina: {contador}/{round(response['total']/limit)}", end ="")

    for i in response['content']:
        # print(i)
        executar(f"""INSERT INTO bethadba.controle_migracao_registro (sistema, tipo_registro, id_gerado,hash_chave_dsk, i_chave_dsk1,i_chave_dsk2,i_chave_dsk3)
                    VALUES (300,'matricula',{i['id']},bethadba.dbf_get_hash_chave_dsk(300,'matricula','1',{i['codigoMatricula']['numero']},null),'1',{i['codigoMatricula']['numero']},null);""")


