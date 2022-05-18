import requests
from configuracao.conexao import AUTORIZACAO, ACCESSUSER, TOKENUSER


maisPaginas = True
iniciaEm = 0
nRegistros = 100
contador = 0
contador2 = 0

while maisPaginas:
    url = f"https://e-gov.betha.com.br/glb/service-layer/v2/api/pessoas?iniciaEm={iniciaEm}&nRegistros={nRegistros}"

    payload={}
    headers = {
      'Authorization': AUTORIZACAO
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    maisPaginas =response['maisPaginas']
    iniciaEm = nRegistros * contador
    contador +=1
    print(f"\r {contador}",end="")
    for i in response['conteudo']:
        contador2+=1
        if 'pessoa-fisica' in i and i['pessoaFisica']['cpf']=='04539074903':
            print(i)
print("\n")
print(contador2)