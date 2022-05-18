from os.path import join, dirname
from pyodbc import connect, DatabaseError
from os import getenv
from dotenv import load_dotenv


load_dotenv(join(dirname(__file__), '../.env'))
AUTORIZACAO = getenv("TOKEN")
if not (AUTORIZACAO.lower().startswith('bearer')):
    AUTORIZACAO = f'bearer {AUTORIZACAO}'
TOKENUSER = getenv("TOKENUSER")
if not (TOKENUSER.lower().startswith('bearer')):
    TOKENUSER = f'bearer {TOKENUSER}'
ACCESSUSER = getenv("ACCESSUSER")
APPCONTEXT = getenv("APPCONTEXT")
ODBC = getenv("ODBC")


def conectar():
    conexao = None
    try:
        conexao = connect(f'DSN={ODBC}', ConnectionIdleTimeout=0)
    except (Exception, DatabaseError) as e:
        print(f'\n* Erro ao executar função "conectar". {e}')
    finally:
        return {'cursor': conexao.cursor(), 'conexao': conexao}


def executar(comando, registro=None, unico=True):
    conexao = conectar()
    try:
        if unico:
            if registro:
                conexao['cursor'].execute(comando, registro)
            else:
                conexao['cursor'].execute(comando)
        else:
            conexao['cursor'].executemany(comando, registro)
        conexao['conexao'].commit()
    except (Exception, DatabaseError) as e:
        print(f'\n* Erro ao executar função "executar". {e}')
    finally:
        conexao['cursor'].close()


def consultar(comando):
    conexao = conectar()
    lista_dado = []
    try:
        conexao['cursor'].execute(comando)
        resultado = conexao['cursor'].fetchall()
        for i, descricao in enumerate(resultado):
            lista_dado.append({})
            for j, valor in enumerate([d[0] for d in conexao['cursor'].description]):
                lista_dado[i][valor] = descricao[j]
    except (Exception, DatabaseError) as e:
        print(f'\n* Erro ao executar função "consultar". {e}')
    finally:
        conexao['cursor'].close()
        return lista_dado
