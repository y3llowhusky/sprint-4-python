import os
from biblioteca import *


while True:
    # seta flags da tela de login e da tela principal - primeiro a tela de login é ativada
    logando = True
    executa_programa = False

    while logando:
        limpar_tela()
        exibir_titulo("menu de login")
        opcao = input("""Cadastrar novo usuário ou fazer login com usuário existente?

1 - Cadastrar novo usuário
2 - Logar com usuário existente
3 - Apagar usuário existente
                                
-> """)

        if opcao == "1":
            limpar_tela()
            exibir_titulo("cadastro de novo usuário")
            login = input("Login: ")
            senha = input("Senha: ")
            cadastrar_usuario(login, senha)
            print("Usuário cadastrado com sucesso!")
        elif opcao == "2":
            while True:
                limpar_tela()
                exibir_titulo("fazer login")
                login = input("Login: ")
                senha = input("Senha: ")
                usuario_logado_id = verificar_login(login, senha)
                if usuario_logado_id:
                    print("Login realizado com sucesso!")
                    logando = False
                    executa_programa = True
                    break
                else:
                    print("Login ou senha incorretos. Tente novamente.")
                    input("Pressione qualquer tecla para continuar . . . ")
        elif opcao == "3":
            limpar_tela()
            exibir_titulo("apagar usuário existente")
            login = input("Login do usuário a ser apagado: ")
            senha = input("Senha do usuário a ser apagado: ")

            try:
                if apagar_usuario(login, senha):
                    exibir_titulo("usuário apagado com sucesso!")
                else:
                    print("Usuário não encontrado ou login / senha incorreto(a).")
            except Exception as e:
                exibir_titulo(f"ERRO: {e}")

        else:
            print("Opção inválida! Digite 1, 2 ou 3.")
        
        input("Pressione qualquer tecla para continuar . . .")

    while executa_programa:
        limpar_tela()
        # exibe menu toda vez que retornar ao while
        exibir_titulo('HC AUXILIA - AREA DO CUIDADOR E FAMILIAR')
        print('''
[1] - Cadastrar ficha médica
[2] - Exibir fichas médicas
[3] - Marcar consultas
[4] - Exibir consultas
[5] - Marcar exames
[6] - Exibir exames
[7] - Voltar para tela de login
[0] - Sair\n''')
        opcao = input('-> ')

        # verifica tipo da opção inserida
        try:
            opcao = int(opcao)
            match opcao:
                case 1: # cadastrar fichas médicas
                    limpar_tela()
                    exibir_titulo("CADASTRAR FICHA MÉDICA")
                    preencher_dicionario(ficha_medica)
                    salvar_ficha(ficha_medica, usuario_logado_id)

                    exibir_titulo("Ficha médica cadastrada!")
                    input('Pressione qualquer tecla para continuar . . . ')

                case 2: # exibir fichas médicas
                    limpar_tela()
                    exibir_titulo("EXIBIR FICHAS MÉDICAS")
                    listar_fichas(usuario_logado_id)
                    input("Pressione qualquer tecla para continuar . . . ")

                case 3: # marcar consultas
                    limpar_tela()
                    exibir_titulo("MARCAR CONSULTAS")

                    # verifica se data da consulta é válida, só sai do loop se data for válida
                    while True:
                        preencher_dicionario(consulta)
                        if verifica_data(consulta["Data da consulta:\nDia ....."], consulta["Mês ....."], 
                                        consulta["Ano ....."]):
                            salvar_consulta(consulta, usuario_logado_id)
                            break
                        else:
                            print('--\nData inválida! Tente novamente.\n--')

                    exibir_titulo("Consulta marcada!")
                    input('Pressione qualquer tecla para continuar . . . ')

                case 4: # exibir consultas
                    limpar_tela()
                    exibir_titulo("EXIBIR CONSULTAS")

                    listar_consultas(usuario_logado_id)
                    input('Pressione qualquer tecla para continuar . . . ')

                case 5: # marcar exames
                    limpar_tela()
                    exibir_titulo("MARCAR EXAMES")

                    # verifica se data do exame é válida, só sai do loop se data for válida
                    while True:
                        preencher_dicionario(exame)
                        if verifica_data(exame["Data do exame:\nDia ....."], exame["Mês ....."], exame["Ano ....."]):
                            salvar_exame(exame, usuario_logado_id)
                            break
                        else:
                            print('--\nData inválida! Tente novamente.\n--')

                    input('Pressione qualquer tecla para continuar . . . ')

                case 6: # exibir exames
                    limpar_tela()
                    exibir_titulo("EXIBIR EXAMES")

                    listar_exames(usuario_logado_id)
                    input("Pressione qualquer tecla para continuar . . . ")

                case 7:
                    # desativa flag de execução do programa principal e reativa flag de login do sistema, retornando ao menu de login
                    executa_programa = False
                    logando = True

                case 0: # sair
                    print('Obrigado por utilizar!')
                    input('Pressione qualquer tecla para sair . . . ')
                    # força o encerramento do programa, saindo do loop principal while True
                    exit()

                case _:
                    print('Opção inválida! Tente novamente.')
                    input('Pressione qualquer tecla para continuar.')

        except ValueError:
            print('Opção inválida! Tente novamente.')
            input('Pressione qualquer tecla para continuar . . . ')