import oracledb

# faz a conexão com o banco sql e cria os cursores para as operações do crud
def conectar():
    try:
        connection = oracledb.connect(
            user="rm563717",
            password="310307",
            dsn="oracle.fiap.com.br:1521/ORCL"
        )

        cursors = {
            "cadastro": connection.cursor(),
            "consulta": connection.cursor(),
            "alteracao": connection.cursor(),
            "exclusao": connection.cursor()
        }
    except Exception as e:
        print("Erro na conexão: ", e)
        return None, None
    else:
        return connection, cursors

# recebe o código sql e o tipo de cursor para fazer a operação equivalente no banco
def executar_comando(sql, params=None, fetch=True, tipo="consulta"):
    connection, cursors = conectar()
    if not connection:
        return None
    
    cursor = cursors.get(tipo, cursors["consulta"])

    try:
        cursor.execute(sql, params or {})
        resultado = None
        if fetch:
            resultado = cursor.fetchall()
        connection.commit()
    except Exception as e:
        print("Erro ao executar comando: ", e)
        resultado = None
    finally:
        for cursor in cursors.values():
            cursor.close()
        connection.close()
    
    return resultado