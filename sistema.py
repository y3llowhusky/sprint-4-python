import os
from biblioteca import *


while True:
    # seta flags da tela de login e da tela principal - primeiro a tela de login é ativada
    logando = True
    executa_programa = False

    while logando:
        limpar_tela()
        exibir_titulo("menu de login")
        # input para escolher a opção no menu de login - cadastrar usuario, logar com usuario existente, apagar usuario ou sair do sistema
        opcao = input("""Cadastrar novo usuário ou fazer login com usuário existente?

[1] - Cadastrar novo usuário
[2] - Logar com usuário existente
[3] - Apagar usuário existente
[0] - Sair          
                      
-> """)

        # estrutura de if/else para corresponder a opção escolhida - conexão com banco de dados na opção 1
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
                # desativa flag do menu e ativa flag do programa principal caso o login esteja correto
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

            # tenta apagar o usuário digitado do banco e retorna erro (Exception as e) caso não haja usuário / esteja incorreto
            try:
                if apagar_usuario(login, senha):
                    exibir_titulo("usuário apagado com sucesso!")
                else:
                    print("Usuário não encontrado ou login / senha incorreto(a).")
            except Exception as e:
                exibir_titulo(f"ERRO: {e}")
        elif opcao == "0":
            print('Obrigado por utilizar!')
            input('Pressione qualquer tecla para sair . . . ')
            # força o encerramento do programa, saindo do loop principal while True
            exit()
        else:
            print("Opção inválida! Digite 1, 2 ou 3.")
        
        input("Pressione qualquer tecla para continuar . . .")

    while executa_programa:
        limpar_tela()
        # exibe menu toda vez que retornar ao while executa_programa (flag ativada)
        exibir_titulo('HC AUXILIA - AREA DO CUIDADOR E FAMILIAR')
        print('''
[1] - Cadastrar ficha médica
[2] - Exibir fichas médicas
[3] - Marcar consultas
[4] - Exibir consultas
[5] - Marcar exames
[6] - Exibir exames
[7] - Voltar para tela de login
[8] - Atualizar senha do usuário
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

                    exibir_titulo("ficha médica cadastrada!")
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

                    exibir_titulo("consulta marcada!")
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

                    exibir_titulo("exame marcado!")
                    input('Pressione qualquer tecla para continuar . . . ')

                case 6: # exibir exames
                    limpar_tela()
                    exibir_titulo("EXIBIR EXAMES")

                    listar_exames(usuario_logado_id)
                    input("Pressione qualquer tecla para continuar . . . ")

                case 7: # voltar para tela de login
                    limpar_tela()
                    # desativa flag de execução do programa principal e reativa flag de login do sistema, retornando ao menu de login
                    executa_programa = False
                    logando = True

                case 8: # atualizar senha do usuário
                    limpar_tela()
                    exibir_titulo("ATUALIZAR SENHA DO USUÁRIO")
                    senha_atual = input("Senha atual: ")
                    nova_senha = input("Nova senha: ")

                    if atualizar_senha(usuario_logado_id, senha_atual, nova_senha):
                        print("Senha atualizada com sucesso!")
                    else:
                        print("Senha atual incorreta. Tente novamente.")

                    input("Pressione qualquer tecla para continuar . . . ")

                case 0: # sair
                    print('Obrigado por utilizar!')
                    input('Pressione qualquer tecla para sair . . . ')
                    # força o encerramento do programa, saindo do loop principal while True
                    exit()

                case _: # opção inválida
                    print('Opção inválida! Tente novamente.')
                    input('Pressione qualquer tecla para continuar.')

        except ValueError: # trata erro caso a opção digitada não seja um número inteiro
            print('Opção inválida! Tente novamente.')
            input('Pressione qualquer tecla para continuar . . . ')