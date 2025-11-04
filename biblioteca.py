import requests
import os
import json
from datetime import *
import calendar
from db import executar_comando

# criação dos arquivos para armazenamento das informações dos usuários / pacientes

# armazena o id do usuário logado no momento, para vincular todos os cadastros realizados no banco à esse usuário
usuario_logado_id = None

ficha_medica = {
    "Nome": "",
    "Idade (anos)": "",
    "Sexo (M/F)": "",
    "Altura (m)": "",
    "Peso (kg)": "",
    "CEP (somente núm.)": ""
}

usuario = {
    "Login": "",
    "Senha": "",
}

consulta = {
    "Nome do paciente": "",
    "Data da consulta:\nDia .....": "",
    "Mês .....": "",
    "Ano .....": "",
    "Motivo da consulta": "",
    "Observações (se houver)": "",
}

exame = {
    "Nome do paciente": "",
    "Data do exame:\nDia .....": "",
    "Mês .....": "",
    "Ano .....": "",
    "Nome do exame": "",
    "Motivo do exame": "",
    "Observações (se houver)": "",
}

# procedimento para exibir titulo formatado
def exibir_titulo(title: str) -> None:
    largura = len(title) * 2
    print("=" * largura)
    print(title.center(largura).upper())
    print("=" * largura)

# limpa a tela do terminal
def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear") 

# função para cadastro de usuário no banco de dados
def cadastrar_usuario(login: str, senha: str) -> bool:
    sql = "INSERT INTO challenge_python_usuarios (login, senha) VALUES (:1, :2)"
    executar_comando(sql, {"1": login, "2": senha}, fetch=False)

# função para atualizar a senha do usuário no banco de dados
def atualizar_senha(id_usuario: int, senha_atual: str, nova_senha: str) -> None:
    sql_verifica = "SELECT senha FROM challenge_python_usuarios WHERE id_usuario = :1"
    resultado = executar_comando(sql_verifica, {"1": id_usuario}, fetch=True)

    # verifica se senha atual está correta
    if not resultado or resultado[0][0] != senha_atual:
        return False
    else:
        sql_atualiza = "UPDATE challenge_python_usuarios SET senha = :1 WHERE id_usuario = :2"
        executar_comando(sql_atualiza, {"1": nova_senha, "2": id_usuario}, fetch=False)
        return True

# função para verificar se login e senha digitados correspondem a algum valor no banco de dados
def verificar_login(login: str, senha: str) -> int | None:
    sql = "SELECT * FROM challenge_python_usuarios WHERE login = :1 AND senha = :2"
    resultado = executar_comando(sql, {"1": login, "2": senha}, fetch=True)

    # verifica se query retornou um usuário, se sim instancia variável para guardar id do usuário, se não retorna falso.
    if resultado:
        global usuario_logado_id
        usuario_logado_id = resultado[0][0]
        return usuario_logado_id
    return None

# função para apagar dados do usuário do banco de dados
def apagar_dados_usuario(id_usuario) -> None:
    executar_comando("DELETE FROM challenge_python_fichas_medicas WHERE id_usuario = :1", {"1": id_usuario})
    executar_comando("DELETE FROM challenge_python_consultas WHERE id_usuario = :1", {"1": id_usuario})
    executar_comando("DELETE FROM challenge_python_exames WHERE id_usuario = :1", {"1": id_usuario})

def exportar_json(nome_arq: str, dados: list[dict]) -> None:
    try:
        pasta_exportacoes = "exportacoes"
        os.makedirs(pasta_exportacoes, exist_ok=True)

        caminho_arquivo = os.path.join(pasta_exportacoes, f"{nome_arq}.json")

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        print(f"\nDados exportados com sucesso para '{caminho_arquivo}'!\n")
    except Exception as e:
        print(f"Erro ao exportar dados para JSON: {e}")

# função para salvar dados da ficha médica no banco de dados
def salvar_ficha(ficha: dict, id_usuario: int) -> None:
    sql = """INSERT INTO challenge_python_fichas_medicas (nome, idade, sexo, altura, peso, cep, id_usuario)
            VALUES (:1, :2, :3, :4, :5, :6, :7)"""

    executar_comando(sql, {
        "1": ficha["Nome"],
        "2": ficha["Idade (anos)"],
        "3": ficha["Sexo (M/F)"].upper(),
        "4": ficha["Altura (m)"],
        "5": ficha["Peso (kg)"],
        "6": ficha["CEP (somente núm.)"],
        "7": id_usuario
    }, fetch=False)

# função para listar fichas médicas do banco de dados
def listar_fichas(id_usuario):
    sql = "SELECT id_ficha, id_usuario, nome, idade, sexo, altura, peso, cep FROM challenge_python_fichas_medicas WHERE id_usuario = :1 ORDER BY id_ficha"
    resultado = executar_comando(sql, {"1": id_usuario}, fetch=True)

    # usa o retorno da query para listar os dados formatados, caso hajam
    if not resultado:
        print("Não há fichas médicas cadastradas!")
    else:
        fichas_lista = []
        for ficha in resultado:
            try:
                response = requests.get(f'https://viacep.com.br/ws/{ficha[7]}/json/')
                if response.status_code == 200:
                    data = response.json()
                    endereco = f"{data['logradouro']}, {data['bairro']}, {data['localidade']}-{data['uf']}"
                else:
                    endereco = "Endereço não encontrado - Erro ao consultar API"
            except Exception as e:
                endereco = f"Endereço não encontrado - Erro na conexão com a API: {e}"

            exibir_titulo(f"ficha médica id {ficha[0]}")
            print(f"""Nome do paciente: {ficha[2]}
Idade do paciente: {ficha[3]}
Sexo (M/F): {ficha[4]}
Altura (m): {ficha[5]}m
Peso (kg): {ficha[6]}kg
Endereço: {endereco}""")
            print("")

            fichas_lista.append({
                "ID Ficha": ficha[0],
                "Nome do paciente": ficha[2],
                "Idade do paciente": ficha[3],
                "Sexo (M/F)": ficha[4],
                "Altura (m)": ficha[5],
                "Peso (kg)": ficha[6],
                "Endereço": endereco
            })

        exportar = input("Deseja exportar as fichas médicas para um arquivo JSON? (s/n): ").strip().lower()
        if exportar == 's':
            exportar_json("fichas_medicas", fichas_lista)

# função para salvar consulta agendada no banco de dados
def salvar_consulta(consulta, id_usuario: int) -> None:
    sql = """INSERT INTO challenge_python_consultas (nome_paciente, dia, mes, ano, motivo, observacoes, id_usuario)
            VALUES (:1, :2, :3, :4, :5, :6, :7)"""
    
    executar_comando(sql, {
        "1": consulta["Nome do paciente"],
        "2": consulta["Data da consulta:\nDia ....."],
        "3": consulta["Mês ....."],
        "4": consulta["Ano ....."],
        "5": consulta["Motivo da consulta"],
        "6": consulta["Observações (se houver)"],
        "7": id_usuario
    }, fetch=False)

# função para listar as consultas presentes no banco de dados
def listar_consultas(id_usuario):
    sql = "SELECT id_consulta, id_usuario, nome_paciente, dia, mes, ano, motivo, observacoes FROM challenge_python_consultas WHERE id_usuario = :1 ORDER BY id_consulta"
    resultado = executar_comando(sql, {"1": id_usuario}, fetch=True)

    # usa o retorno da query para listar os dados formatados, caso hajam
    if not resultado:
        print("Não há consultas cadastradas!")
    else:
        consultas_lista = []
        for consulta in resultado:
            exibir_titulo(f"consulta id {consulta[0]}")
            print(f"""Nome do paciente: {consulta[2]}
Data da consulta: {consulta[3]}/{consulta[4]}/{consulta[5]}
Motivo da consulta: {consulta[6]}
Observações (se houver): {consulta[7] if consulta[7] else "Nenhuma"}""")
            print("")

            consultas_lista.append({
                "ID Consulta": consulta[0],
                "Nome do paciente": consulta[2],
                "Data da consulta": f"{consulta[3]}/{consulta[4]}/{consulta[5]}",
                "Motivo da consulta": consulta[6],
                "Observações (se houver)": consulta[7] if consulta[7] else "Nenhuma"
            })

        exportar = input("Deseja exportar as consultas para um arquivo JSON? (s/n): ").strip().lower()
        if exportar == 's':
            exportar_json("consultas", consultas_lista)

# função para salvar exame agendado no banco de dados
def salvar_exame(exame, id_usuario) -> None:
    sql = """INSERT INTO challenge_python_exames (nome_paciente, dia, mes, ano, nome_exame, motivo, observacoes, id_usuario)
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8)"""
    
    executar_comando(sql, {
        "1": exame["Nome do paciente"],
        "2": exame["Data do exame:\nDia ....."],
        "3": exame["Mês ....."],
        "4": exame["Ano ....."],
        "5": exame["Nome do exame"],
        "6": exame["Motivo do exame"],
        "7": exame["Observações (se houver)"],
        "8": id_usuario
    }, fetch=False)

# função para listar os exames presentes no banco de dados
def listar_exames(id_usuario):
    sql = "SELECT id_exame, id_usuario, nome_paciente, dia, mes, ano, nome_exame, motivo, observacoes FROM challenge_python_exames WHERE id_usuario = :1 ORDER BY id_exame"
    resultado = executar_comando(sql, {"1": id_usuario}, fetch=True)

    # usa o retorno da query para listar os dados formatados, caso hajam
    if not resultado:
        print("Não há exames cadastrados!")
    else:
        exames_lista = []
        for exame in resultado:
            exibir_titulo(f"exame id {exame[0]}")
            print(f"""Nome do paciente: {exame[2]}
Data do exame: {exame[3]}/{exame[4]}/{exame[5]}
Nome do exame: {exame[6]}
Motivo do exame: {exame[7]}
Observações (se houver): {exame[8] if exame[8] else "Nenhuma"}""")
            print("")

            exames_lista.append({
                "ID Exame": exame[0],
                "Nome do paciente": exame[2],
                "Data do exame": f"{exame[3]}/{exame[4]}/{exame[5]}",
                "Nome do exame": exame[6],
                "Motivo do exame": exame[7],
                "Observações (se houver)": exame[8] if exame[8] else "Nenhuma"
            })

        exportar = input("Deseja exportar os exames para um arquivo JSON? (s/n): ").strip().lower()
        if exportar == 's':
            exportar_json("exames", exames_lista)


# função para apagar a ficha médica de um usuário do sistema
def apagar_ficha(id_usuario):
    select = """SELECT id_ficha, nome FROM challenge_python_fichas_medicas WHERE id_usuario = :1"""
    fichas = executar_comando(select, {"1": id_usuario})

    delete = """DELETE FROM challenge_python_fichas_medicas WHERE """

    if not fichas:
        print("Nenhuma ficha médica cadastrada.")

    executar_comando(delete, {
        "1": ficha_medica["Nome"],
        "2": ficha_medica["Idade (anos)"],
        "3": ficha_medica["Sexo (M/F)"],
        "4": ficha_medica["Altura (m)"],
        "5": ficha_medica["Peso (kg)"]
    }, fetch=False)

# função para apagar um usuário do banco, através da opção 3 do menu de login no sistema principal. Retorna booleano de acordo com sucesso ou fracasso da solicitação
def apagar_usuario(login, senha) -> bool:
    select = "SELECT id_usuario FROM challenge_python_usuarios WHERE login = :1 AND senha = :2"
    resultado = executar_comando(select, {"1": login, "2": senha}, fetch=True)
    
    if not resultado:
        return False

    id_usuario = resultado[0][0]
    
    delete = "DELETE FROM challenge_python_usuarios WHERE id_usuario = :1"
    executar_comando(delete, {"1": id_usuario}, fetch=False)

    return True

def validar_campo(campo: str, conteudo) -> bool:
    # verificação específica para campos sexo, idade, altura e peso
    match campo.lower():
        # verifica se campo é m ou f
        case 'sexo (m/f)':
            if conteudo.lower() == 'm' or conteudo.lower() == 'f':
                return True
            else:
                return False

        # verifica se idade está entre 0 e 200 anos
        case 'idade (anos)':
            return 0 < conteudo < 123
        
        # verifica se altura está entre 0.3m e 3m
        case 'altura (m)':
            return 0.3 < conteudo < 2.72

        # verifica se peso está entre 1kg e 600kg
        case 'peso (kg)':
            return 1 < conteudo < 600

        case 'cep (somente núm.)':
            # verifica se cep tem 8 dígitos
            if len(str(conteudo)) != 8:
                return False
             # faz requisição para API e verifica se cep existe
            response = requests.get(f'https://viacep.com.br/ws/{conteudo}/json/')
            data = response.json()
            if 'erro' in data:
                return False
            return True

        # retorna True caso seja outro campo
        case _:
            return True

# Função para verificar validade da data inserida (válida e maior que data atual)
# retorna booleano (True se data válida, False se data inválida)
def verifica_data(dia: str, mes: str, ano: str) -> bool:
    # verifica se todos os parâmetros da data são inteiros
    try:
        dia = int(dia)
        mes = int(mes)
        ano = int(ano)
    except ValueError:
        return False

    # instancia a data atual e as datas há 100 anos atrás e daqui 100 anos no futuro (limite)
    ano_atual = datetime.now().year
    mais_cem = ano_atual + 100
    menos_cem = ano_atual - 100

    # verifica se mês é válido (entre 1 e 12)
    if not (1 <= mes <= 12):
        return False

    # verifica se parâmetros da data podem ser convertidos para date
    try:
        data_inserida = date(ano, mes, dia)
    except ValueError:
        return False
    
    # instancia data atual e verifica se data inserida é maior que data atual (impossível marcar algo para o passado)
    data_atual = datetime.now().date()
    if data_inserida < data_atual:
        return False

    # instancia lista de dias totais de acordo com o mês (índice)
    dias_por_mes = [31,
                    29 if calendar.isleap(ano) else 28, # operador ternário para fevereiro em ano bissexto
                    31, 30, 31, 30,
                    31, 31, 30, 31, 30, 31]

    # verifica se dia é maior que 1 e menor que total de dias do mês correspondente
    if dia < 1 or dia > dias_por_mes[mes - 1]:
        return False

    # verifica se ano está dentro do limite (há 100 anos atrás ou daqui 100 anos no futuro)
    if ano > mais_cem or ano < menos_cem:
        return False

    return True

# procedimento para preencher um dicionario e adiciona-lo a lista de dicionarios
def preencher_dicionario(dicionario: dict) -> None:
    # preenche os values dos items do dicionario e adiciona o dicionario preenchido na lista de dicionarios
    for campo, valor in dicionario.items():
        campo_valido = False
        while not campo_valido:
            valor = input(f'{campo.upper()}: ')

            # verifica se valor digitado é vazio
            if "observações" not in campo.lower() and valor.strip() == '':
                print('Campo em branco! Digite um valor válido.')
            else:
                tipo = verificar_tipo(campo)
                
                # converte conteudo digitado para o tipo esperado para aquele campo, se possivel
                try:
                    # converte o conteúdo do campo para o tipo esperado dele
                    valor = tipo(valor)
                    
                    # verifica se campo é válido através do retorno da função validar_campo (bool)
                    campo_valido = validar_campo(campo, valor)
                    
                    # se campo não for valido, permanece no loop, se for valido, flag é automaticamente desativada
                    if not campo_valido:
                        print(f'Digite valor válido para {campo}!')
                    
                except ValueError:
                    print(f'Digite valor válido para {campo}!')
        
        # atribui conteudo do campo ao valor do item no dicionario
        dicionario[campo] = valor

# função para verificar o tipo esperado do conteúdo de um campo, retorna o tipo esperado
def verificar_tipo(campo: str) -> type:
    # verifica qual o conteúdo do campo, e instancia tipo esperado de acordo com ele
    if campo.upper() == 'idade (anos)'.upper():
        tipo_esperado = int
    elif campo.upper() == 'altura (m)'.upper() or campo.upper() == 'peso (kg)'.upper():
        tipo_esperado = float
    else:
        tipo_esperado = str
    
    return tipo_esperado



