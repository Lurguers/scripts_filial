from re import match
from datetime import datetime
from configuracao.conexao import bethadba

from configuracao.conexao import executar, consultar
from requests import get, post, delete
from hashlib import md5


AUTORIZACAO = 'Bearer 5f9b5b63-d635-466a-9b42-79fa89083243'
def validar_certidao(certidao) -> bool:
    if not certidao:
        return False
    numero = [int(digit) for digit in certidao if digit.isdigit()]
    if len(numero) != 32:
        return True
    valida = Certidao()
    return valida.validate(certidao)


def validar_cpf(cpf) -> bool:
    if not cpf:
        return False
    numero = [int(digit) for digit in cpf if digit.isdigit()]
    if len(numero) != 11 or len(set(numero)) == 1:
        return False
    valida = CPF()
    return valida.validate(cpf)


def validar_lote(tipo_registro=None, incosistencia=None):
    if incosistencia is None:
        incosistencia = {'registro': 0, 'lote': 0}
    try:
        print('# Iniciando validação de lote(s) pendente(s)')
        total_validado = 0
        total_lote = 0
        pendencia = True
        while pendencia:
            comando = 'SELECT id_lote, url_consulta FROM bethadba.controle_migracao_lotes WHERE Status not in (3, 4, 5)'
            if tipo_registro is not None:
                comando += f" AND tipo_registro = '{tipo_registro}'"
            resultado = consultar(comando)
            total = len(resultado)
            pendencia = False
            if total <= 0:
                print(f'\r- Não há lote(s) pendente(s) para validação', end='\n')
                return
            if total_lote == 0:
                total_lote = total
                print(f'# Verificando {total} lote(s) pendente(s)')
            for lote in resultado:
                print(f'\r- Lotes executados: {total_validado}/{total_lote}', end='')
                endereco = lote['url_consulta']
                # sleep(0.5)

                requisicao = get(endereco, headers={'authorization': AUTORIZACAO, 'content-type': 'application/json'})

                if requisicao.ok:
                    retorno = requisicao.json()
                    if 'id' in retorno:
                        id_lote = retorno['id']
                    elif 'idLote' in retorno:
                        id_lote = retorno['idLote']
                    elif 'idLot' in retorno:
                        id_lote = retorno['idLot']
                    else:
                        id_lote = ''
                    if 'status' in retorno:
                        status = retorno['status']
                    elif 'situacao' in retorno:
                        status = retorno['situacao']
                    elif 'statusLote' in retorno:
                        status = retorno['statusLote']
                    elif 'statusLot' in retorno:
                        status = retorno['statusLot']
                    else:
                        status = ''
                    if status in ['AGUARDANDO_EXECUCAO', 'EXECUTANDO', 'QUEUE', 'PROCESSING']:
                        pendencia = True
                    else:
                        incosistencia = analisar_lote(incosistencia, retorno, id_lote, tipo_registro)
                        total_validado += 1
                        print(f'\r- Lotes executados: {total_validado}/{total_lote}', end='')
                else:
                    raise Exception(requisicao.text)
        if incosistencia["registro"] > 0:
            print(f'\n- {incosistencia["registro"]} registro(s) com inconsistência. ')
        else:
            print('\n- Nenhuma inconsistência encontrada no(s) registro(s)')
        if incosistencia["lote"] > 0:
            print(f'- {incosistencia["lote"]} lote(s) com inconsistência. ')
        else:
            print('- Nenhuma inconsistência encontrada no(s) lote(s)')
        print(f'- Consulta de lotes finalizada')
    except Exception as e:
        print(f'\n* Erro ao executar função "validar_lote" {e}')
        validar_lote(tipo_registro, incosistencia)


def analisar_lote(incosistencia, retorno, id_lote, tipo_registro):
    status_lote = None
    lista_lote = []
    lista_ocorrencia = []
    try:
        if 'status' in retorno:
            status_lote = retorno['status']
        elif 'situacao' in retorno:
            status_lote = retorno['situacao']
        elif 'statusLote' in retorno:
            status_lote = retorno['statusLote']
        elif 'statusLot' in retorno:
            status_lote = retorno['statusLot']
        elif 'situacao' in retorno:
            status_lote = retorno['situacao']

        if status_lote in ['EXECUTADO', 'PROCESSADO', 'PROCESSED', 'EXECUTADO_OK']:
            status_lote = 3
        elif status_lote in ['EXECUTADO_PARCIALMENTE', 'EXECUTADO_PARCIALMENTE_OK']:
            status_lote = 4
        else:
            status_lote = 5
        if status_lote in [4, 5]:
            incosistencia['lote'] += 1
        if 'id' in retorno:
            id_registro = retorno["id"]
        elif 'idLote' in retorno:
            id_registro = retorno["idLote"]
        elif 'idLot' in retorno:
            id_registro = retorno["idLot"]
        else:
            id_registro = ''
        if 'updatedIn' in retorno:
            if match('\d{2}\.\d+$', retorno['updatedIn']):
                data_hora_ret = datetime.strptime(retorno['updatedIn'], '%Y-%m-%dT%H:%M:%S.%f')
            elif match('\d{2}:\d{2}:\d{2}$', retorno['updatedIn']):
                data_hora_ret = datetime.strptime(retorno['updatedIn'], '%Y-%m-%dT%H:%M:%S')
            else:
                data_hora_ret = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            data_hora_ret = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comando = """UPDATE bethadba.controle_migracao_lotes
                     SET Status = {}
                     WHERE id_lote = '{}'""".format(status_lote, id_registro)
        executar(comando)
        if 'retorno' in retorno:
            tipo = 'retorno'
        elif 'messageList' in retorno:
            tipo = 'messageList'
        else:
            raise Exception('* Sem tipo de retorno: ', retorno)
        for registro in retorno[tipo]:
            sistema = '0'
            status = None
            id_gerado = None
            id_integracao = None
            mensagens = None
            id_existente = None
            if 'mensagens' in registro:
                mensagens = registro['mensagens']
            elif 'message' in registro:
                mensagens = registro['message']
            elif 'mensagem' in registro:
                mensagens = registro['mensagem']
            if 'idExistente' in registro and tipo_registro != 'funcionario':
                id_existente = registro['idExistente']
            elif 'idExistente' in registro and tipo_registro == 'funcionario' and registro['idExistente'] is not None:
                inserir_registro([{'sistema': '1',
                                   'tipo_registro': 'pessoa',
                                   'descricao_tipo_registro': 'Cadastro de pessoa',
                                   'hash_chave_dsk': encurtar('1',
                                                              'pessoa',
                                                              registro['idExistente'],
                                                              registro['idIntegracao']),
                                   'id_gerado': registro['idExistente'],
                                   'i_chave_dsk1': registro['idIntegracao']}])
            if 'idIntegracao' in registro:
                id_integracao = registro['idIntegracao']
            elif 'clientId' in registro:
                id_integracao = registro['clientId']
            if 'status' in registro:
                status = registro['status']
            elif 'situacao' in registro:
                status = registro['situacao']
            elif 'mostCritical' in registro:
                status = registro['mostCritical']
            if status in ['SUCESSO', 'SUCESS', 'EXECUTADO', 'WARNING']:
                if 'id' in registro:
                    if 'iGruposMateriais' in registro['id']:
                        id_gerado = registro['id']['iGruposMateriais']
                    # elif 'iUnidadesMedidas' in registro['id']:
                    #     id_gerado = registro['id']['iUnidadesMedidas']
                    else:
                        id_gerado = registro['id'][[id_registro for id_registro in registro['id']][-1]]
                elif 'idGerados' in registro:
                    if 'idAluno' in registro['idGerados']:
                        id_gerado = registro['idGerados']['idAluno']
                    # elif 'idDisciplina' in registro['idGerados']:
                    #     id_gerado = registro['idGerados']['idDisciplina']
                    elif 'idMatricula' in registro['idGerados']:
                        id_gerado = registro['idGerados']['idMatricula']
                        if 'idEnturmacao' in registro['idGerados']:
                            inserir_registro([{'sistema':'1',
                                               'tipo_registro':'enturmacao',
                                               'descricao_tipo_registro':'Cadastro de enturmaca',
                                               'hash_chave_dsk':encurtar('1',
                                                                         'enturmaca',
                                                                         registro['idGerados']['idEnturmacao']),
                                               'id_gerado':registro['idGerados']['idEnturmacao'],
                                               'id_desktop':registro['idGerados']['idMatricula'],
                                               'i_chave_dsk1':registro['idGerados']['idMatricula']}])
                    else:
                        id_gerado = registro['idGerados'][[id_registro for id_registro in registro['idGerados']][-1]]
                elif 'idGerado' in registro:

                    # if 'iPessoas' in registro['idGerado']:
                    #     id_gerado = registro['idGerado']['iPessoas']
                    if isinstance(registro['idGerado'], int):
                        id_gerado = registro['idGerado']
                    # else:
                    #     id_gerado = registro['idGerado']
                    else:
                        id_gerado = registro['idGerado'][[id_registro for id_registro in registro['idGerado']][-1]]
                hash_chave = id_integracao
                if id_gerado is None:
                    print('\n@ id_gerado: ', registro)

                # if hash_chave is None:
                #     print('\n@ hash_chave: ', registro)
                if id_gerado is not None and hash_chave is not None:
                    lista_lote.append([id_gerado, hash_chave])
            elif status in ['ERRO', 'ERROR']:
                if 'mensagem' in registro and registro['mensagem'] is not None:
                    if registro['mensagem'] == "Essa avaliação já foi registrada":
                        id_existente = 1
                        mensagens = ''
                    if registro['mensagem'] == "Este registro de falta já foi cadastrado":
                        id_existente = 2
                        mensagens = ''
                if id_existente is not None:
                    id_gerado = id_existente
                    hash_chave = id_integracao
                    if id_gerado is not None and hash_chave is not None:
                        lista_lote.append([id_gerado, hash_chave])
                else:
                    # print('\n* Envio invalido: ', mensagens)
                    incosistencia['registro'] += 1
                    registro_status = 1
                    registro_resolvido = 1
                    lista_ocorrencia.append((id_integracao, sistema, tipo_registro, None, 9, registro_status,
                                             registro_resolvido, 1, id_lote, mensagens, '', '', id_existente))
            else:
                print('\n@ JSON: ', registro)
        print(lista_ocorrencia)
        # inserir_ocorrencia(lista_ocorrencia)
        # atualizar_lote(lista_lote)
    except Exception as e:
        print(f'\n* Erro ao executar função "analisar_lote" {e}')
    finally:
        return incosistencia


def inserir_ocorrencia(lista_registro):
    if len(lista_registro) <= 0:
        return
    try:
        # print('+ Inserindo dados na tabela de controle de ocorrências.')
        comando = """INSERT INTO bethadba.controle_migracao_registro_ocor
                     (hash_chave_dsk, sistema, tipo_registro, id_gerado, origem, situacao, resolvido,
                     i_sequencial_lote, id_integracao, mensagem_erro, mensagem_ajuda, json_enviado, id_existente)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        for registro in lista_registro:
            executar(comando, registro)
    except Exception as e:
        print(f'\n* Erro ao executar função "inserir_ocorrencia". {e}')


def atualizar_lote(lista_registro, limite=500):
    if len(lista_registro) <= 0:
        return
    try:
        comando = "UPDATE bethadba.controle_migracao_registro SET id_gerado = %s WHERE hash_chave_dsk = %s"
        lista_dado = []
        for registro in lista_registro:
            lista_dado.append((registro[0], registro[1]))
        lista_cortada = ([lista_dado[i:i + limite] for i in range(0, len(lista_dado), limite)])
        for registro in lista_cortada:
            executar(comando, registro, False)
    except Exception as e:
        print(f'\n* Erro ao executar função "atualizar_lote". {e}')


def validar_pis(pis) -> bool:
    if not pis:
        return False
    valida = PIS()
    return valida.validate(pis)


def validar_email(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if match(regex, email) and "@." not in email:
        return True
    return False


def gerar_cnpj(ponto: bool = False) -> str:
    return CNPJ().generate(ponto)


def validar_cnpj(cnpj) -> bool:
    if not cnpj:
        return False
    numero = [int(digit) for digit in cnpj if digit.isdigit()]
    if len(numero) != 14 or len(set(numero)) == 1:
        return False
    valida = CNPJ()
    return valida.validate(cnpj)


def permissao(comando: str) -> str:
    if bethadba:
        return """
                CALL bethadba.dbp_conn_gera(1, 2021, 300);
                set option wait_for_commit = 'on';
                set option fire_triggers = 'off';
                {}
                COMMIT; 
                set option fire_triggers = 'on';
            """.format(comando)
    else:
        return """
                CALL bethadba.dbp_conn_gera(1, 2021, 300);
                set option wait_for_commit = 'on';
                CALL bethadba.pg_habilitartriggers('off'); 
                {}
                COMMIT; 
                CALL bethadba.pg_habilitartriggers('on');   
            """.format(comando)


def iniciar_analise(lista_tipo_inconsistencia):
    inicio = analisar()
    quantidade = 0
    try:
        for tipo_inconsistencia in lista_tipo_inconsistencia:
            quantidade += iniciar(list(tipo_inconsistencia))
    except Exception as e:
        print(f'\n* Erro durante a execução da função "iniciar_analise" {e}')
    finally:
        print(f'\n# Total de inconsistencias encontradas: {quantidade}')
        analisar(inicio)


def iniciar(tipo_inconsistencia):
    tipo_inconsistencia.sort(key=str)
    # inicio = analisar()
    quantidade = 0
    try:
        # print(tipo_inconsistencia[1])
        modulo = __import__(f'consulta.{tipo_inconsistencia[1]}', globals(), locals(), ['analisar', 'ajustar'])
        quantidade = modulo.analisar()
        if quantidade > 0 and tipo_inconsistencia[0]:
            print(f'- Iniciando ajuste de dados')
            modulo.ajustar()
            print(f'- Ajuste do registro {tipo_inconsistencia[1]} finalizada')
    except Exception as e:
        print(f'\n* Erro durante a execução da função "iniciar" {e}')
    finally:
        # analisar(inicio)
        return quantidade


def analisar(dh_inicio=None):
    if dh_inicio is None:
        return datetime.now()
    else:
        print(f'@ Processo finalizado. ({round((datetime.now() - dh_inicio).total_seconds(), 2)} segundos)')


def inserir_registro(lista_registro, limite=200):
    if len(lista_registro) <= 0:
        return
    try:
        lista_dado = []
        comando = """INSERT INTO bethadba.controle_migracao_registro 
                     (sistema, tipo_registro, hash_chave_dsk, descricao_tipo_registro, id_gerado, i_chave_dsk1, 
                     i_chave_dsk2, i_chave_dsk3, i_chave_dsk4, i_chave_dsk5, i_chave_dsk6, i_chave_dsk7, 
                     i_chave_dsk8,i_chave_dsk9, i_chave_dsk10, i_chave_dsk11, i_chave_dsk12) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                     ON CONFLICT (hash_chave_dsk) DO UPDATE SET
                     json_enviado = EXCLUDED.json_enviado,id_gerado = %s"""
        for registro in lista_registro:
            dado = (
                registro.get('sistema'),
                registro.get('tipo_registro'),
                registro.get('hash_chave_dsk'),
                registro.get('descricao_tipo_registro'),
                registro.get('id_gerado'),
                registro.get('i_chave_dsk1'),
                None if 'i_chave_dsk2' not in registro else registro.get('i_chave_dsk2'),
                None if 'i_chave_dsk3' not in registro else registro.get('i_chave_dsk3'),
                None if 'i_chave_dsk4' not in registro else registro.get('i_chave_dsk4'),
                None if 'i_chave_dsk5' not in registro else registro.get('i_chave_dsk5'),
                None if 'i_chave_dsk6' not in registro else registro.get('i_chave_dsk6'),
                None if 'i_chave_dsk7' not in registro else registro.get('i_chave_dsk7'),
                None if 'i_chave_dsk8' not in registro else registro.get('i_chave_dsk8'),
                None if 'i_chave_dsk9' not in registro else registro.get('i_chave_dsk9'),
                None if 'i_chave_dsk10' not in registro else registro.get('i_chave_dsk10'),
                None if 'i_chave_dsk11' not in registro else registro.get('i_chave_dsk11'),
                None if 'i_chave_dsk12' not in registro else registro.get('i_chave_dsk12'),
                None if 'id_gerado' not in registro else registro.get('id_gerado')
            )
            lista_dado.append(dado)
        lista_cortada = ([lista_dado[i:i + limite] for i in range(0, len(lista_dado), limite)])
        for registro in lista_cortada:
            executar(comando, registro, False)
    except Exception as e:
        print(f'\n* Erro ao executar função "inserir_registro". {e}')


def encurtar(*lista_chave):
    texto = ''
    hash_chave = None
    try:
        for chave in lista_chave:
            texto += str(chave)
        hash_chave = md5(texto.encode('utf-8')).hexdigest()
    except Exception as e:
        print(f'\n* Erro durante a execução da função "encurtar" {e}')
    finally:
        return hash_chave
