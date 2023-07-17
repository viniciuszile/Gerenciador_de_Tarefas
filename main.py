import json
import os
import getpass
import time
import datetime 
from datetime import date

def obter_usuario():
    usuario = getpass.getuser()
    return usuario

def obter_data():
    data_atual = date.today()
    return data_atual

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastrar_tarefa(dados):
    data = obter_data()
    usario = obter_usuario()

    flag_cadastro = False

    while not flag_cadastro:
        titulo = input("Digite o título da tarefa: ")
        tipo = input("Digite o tipo da tarefa: ")
        categoria = input("Digite a categoria da tarefa: ")
        dias = input("A tarefa deverá ser concluída em quantos dias: ")

        if len(titulo) <= 0 or len(tipo) <= 0 or len(categoria) <= 0:
            print("****************************************")
            print("*       PREENCHA TODOS OS CAMPOS       *")
            print("****************************************")

            # Delay de 1.5 segundos
            time.sleep(1.5)

            limpar_terminal()
            continue

        try:
            dias = int(dias)
        except ValueError:
            print("O valor informado para os dias não é válido.")
            continue

        data_conclusao = data + datetime.timedelta(days=dias)
        situacao = "Atrasada" if data_conclusao < data else "No prazo"

        ids_numericos = [int(id) for id in dados.keys() if id.isdigit()]
        id = max(ids_numericos, default=0) + 1

        nova_tarefa = {
            "id": id,
            "criacao": data.strftime("%Y-%m-%d"),
            "autor": usario,
            "titulo": titulo,
            "tipo": tipo,
            "categoria": categoria,
            "conclusao": data_conclusao.strftime("%Y-%m-%d"),
            "situacao": situacao
        }

        dados[str(id)] = nova_tarefa

        with open('dados.json', 'w') as arquivo:
            json.dump(dados, arquivo)

        print("Tarefa adicionada com sucesso!")
        time.sleep(1.5)
        limpar_terminal()
        break
    

def listar_tarefas(dados):
    limpar_terminal()
    print("=-" * 30)
    print("Listagem de tarefas")
    if not dados:
        print("Nenhuma tarefa cadastrada.")
    else:
        for id, tarefa in dados.items():
            print("-" * 30)
            print(f"Tarefa de número: {tarefa.get('id', '')}")
            print("Data de criação:", tarefa.get("criacao", ""))
            print("Autor:", tarefa.get("autor", ""))
            print("Título:", tarefa.get("titulo", ""))
            print("Tipo:", tarefa.get("tipo", ""))
            print("Categoria:", tarefa.get("categoria", ""))
            print("Data de conclusão:", tarefa.get("conclusao", ""))
            print("Situação:", tarefa.get("situacao", ""))
            print("-" * 30)
    sair = input("Visualizou o que você deseja? Pressione Enter para retornar ao menu.")

    
def modificar_tarefa(dados, usuario):
    limpar_terminal()
    
    print("=-" * 30)
    print("Modificação de tarefas")
    id_tarefa = input("Digite o ID da tarefa que deseja modificar: ")
    conclusao = input("Deseja mudar a 1 - situação ou 2 - informações: ")
    
    tarefa = dados.get(id_tarefa)
    
    if tarefa:
        if tarefa["usuario"] == usuario:
            if conclusao == "1":
                situacao = input("A tarefa foi concluída? [s]im ou [n]ão: ")
                
                if situacao[0] == "s":
                    # Mudar situação para concluída
                    tarefa["situacao"] = "Concluída"
                    print("Situação da tarefa modificada para 'Concluída'.")
                    print("=-" * 30)
                    time.sleep(1.5)
                else:
                    print("Opção inválida.")
                    print("=-" * 30)
            elif conclusao == "2":
                print("=-" * 30)
                print("Tarefa encontrada:")
                print("ID:", tarefa.get("id"))
                print("Título:", tarefa.get("titulo"))
                print("Tipo:", tarefa.get("tipo"))
                print("Categoria:", tarefa.get("categoria"))
                print("=-" * 30)
                print("1 - Mudar nome.")
                print("2 - Mudar tipo.")
                print("3 - Mudar categoria.")
                opcao = input("Digite a opção desejada: ")
                print("=-" * 30)

                if opcao == '1':
                    novo_nome = input("Digite o novo nome: ")
                    tarefa['titulo'] = novo_nome
                    print("Nome da tarefa modificado com sucesso!")
                    print("=-" * 30)
                elif opcao == '2':
                    novo_tipo = input("Digite o novo tipo: ")
                    tarefa['tipo'] = novo_tipo
                    print("Tipo da tarefa modificado com sucesso!")
                    print("=-" * 30)
                elif opcao == '3':
                    novo_categoria = input("Digite a nova categoria: ")
                    tarefa['categoria'] = novo_categoria
                    print("Categoria da tarefa modificada com sucesso!")
                    print("=-" * 30)
                else:
                    print("Opção inválida.")
                    print("=-" * 30)
                time.sleep(1.5)
        else:
            print("Você não tem permissão para modificar esta tarefa.")
            print("=-" * 30)
    else:
        print("Tarefa não encontrada.")
        print("=-" * 30)


def excluir_tarefa(dados, usuario):
    limpar_terminal()
    print("=-" * 30)
    print("Exclusão de tarefa")
    id_tarefa = input("Digite o ID da tarefa que deseja excluir: ")

    tarefa = dados.get(id_tarefa)
    if tarefa:
        if tarefa["usuario"] == usuario:
            confirmacao = input("Tem certeza que deseja excluir a tarefa? (s/n): ")
            if confirmacao.lower() == 's':
                del dados[id_tarefa]
                print("Tarefa excluída com sucesso!")
            else:
                print("Exclusão da tarefa cancelada.")
        else:
            print("Você não tem permissão para excluir esta tarefa.")
    else:
        print("Tarefa não encontrada.")

    limpar_terminal()   

def main():
    limpar_terminal()
    usuario = obter_usuario()

    dados = {}

    if os.path.isfile('dados.json') and os.path.getsize('dados.json') > 0:
        with open('dados.json') as arquivo:
            dados = json.load(arquivo)

    uso = 0
    while uso != '5':
        limpar_terminal()
        print("=-" * 30)
        print(f"Seja bem-vindo à sua lista de tarefas, {usuario}!")
        print("Por favor, digite a opção desejada:")
        print("1 - Cadastrar nova tarefa.")
        print("2 - Ver tarefas cadastradas.")
        print("3 - Editar tarefa.")
        print("4 - Excluir tarefa.")
        print("5 - Sair.")
        uso = input("Digite aqui sua opção: ")
        print("=-" * 30)
        limpar_terminal()

        if uso == '1':
            cadastrar_tarefa(dados)
        elif uso == '2':
            listar_tarefas(dados)
        elif uso == '3':
            modificar_tarefa(dados)
        elif uso == '4':
            excluir_tarefa(dados)
        elif uso == '5':
            break
        else:
            print("Opção inválida.")

    with open('dados.json', 'w') as arquivo:
        json.dump(dados, arquivo)

    print("Volte sempre! Obrigado por usar nosso programa.")

if __name__ == "__main__":
    main()
