import hashlib
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER
import requests
import funcoes

url = "https://rh.betha.cloud/rh/api/gestao-periodo-aquisitivo?limit=200"

payload={}
headers = {
  'Authorization': TOKENUSER,
  'User-Access': ACCESSUSER
}

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()
contador = 0
for i in response['content']:
    url = f"https://rh.betha.cloud/rh/api/gestao-periodo-aquisitivo/{i['id']}"
    contador +=1
    response2 = requests.request("GET", url, headers=headers, data=payload)
    response2 = response2.json()
    chave = hashlib.md5(str(response2['id']).encode()).hexdigest()
    sql = f"""
    INSERT INTO 
        bethadba.controle_migracao_registro 
        (sistema, 
        tipo_registro, 
        hash_chave_dsk, 
        descricao_tipo_reg, 
        id_gerado, 
        i_chave_dsk1, 
        i_chave_dsk2, 
        i_chave_dsk3)
    VALUES 
        (300, 
        'licencas-premio', 
        '{chave}', 
        'Periodos aquisitivos de licença premio no Cloud', 
        '{response2['id']}', 
        (SELECT i_chave_dsk1 FROM bethadba.controle_migracao_registro WHERE id_gerado = '{response2['matricula']['id']}' AND tipo_registro = 'matricula'), 
        (SELECT i_chave_dsk2 FROM bethadba.controle_migracao_registro WHERE id_gerado = '{response2['matricula']['id']}' AND tipo_registro = 'matricula'), 
        (SELECT i_licencas_premio FROM bethadba.licencas_premio_per WHERE i_entidades = (SELECT i_chave_dsk1 FROM bethadba.controle_migracao_registro WHERE id_gerado = '{response2['matricula']['id']}' AND tipo_registro = 'matricula') AND i_funcionarios = (SELECT i_chave_dsk2 FROM bethadba.controle_migracao_registro WHERE id_gerado = '{response2['matricula']['id']}' AND tipo_registro = 'matricula') AND dt_inicial >= '{i['dataInicial']}' AND dt_final <= '{i['dataFinal']}'));
    """
    inserir = funcoes.executar(sql)
    print(inserir)
print(contador)
