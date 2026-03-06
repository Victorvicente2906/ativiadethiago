import os
from datetime import datetime
from ast import literal_eval 

def salvar_arquivo(nome_arquivo, lista_dados):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for d in lista_dados:
            f.write(repr(d) + "\n")


def carregar_arquivo(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return []

    lista = []
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        for linha in f.readlines():
            linha = linha.strip()
            if linha:
                try:
                    lista.append(literal_eval(linha))
                except (ValueError, SyntaxError):
                    continue
    return lista

def obter_entrada(prompt, tipo=str, pode_ser_vazio=False):
    while True:
        try:
            entrada = input(prompt).strip()
            
            if not entrada and not pode_ser_vazio:
                print("Este campo é obrigatório. Tente novamente.")
                continue
            
            if not entrada and pode_ser_vazio:
                return ""
            
            if tipo == int:
                return int(entrada)
            elif tipo == float:
                return float(entrada)
            elif tipo == str:
                return entrada
            else:
                return entrada

        except ValueError:
            print(f"Entrada inválida. Esperado um valor do tipo {tipo.__name__}.")
        except Exception as e:
            print(f"Ocorreu um erro na entrada: {e}")

clientes = carregar_arquivo("clientes.txt")
reservas = carregar_arquivo("reservas.txt")
pagamentos = carregar_arquivo("pagamentos.txt")


quartos = [
    {"numero": 101, "andar": 1, "status": "Livre"},
    {"numero": 102, "andar": 1, "status": "Livre"},
    {"numero": 201, "andar": 2, "status": "Livre"},
    {"numero": 202, "andar": 2, "status": "Livre"}
]

def cadastrar_cliente():
    print("\nCdastrar Cliente")
    try:
        id_cliente = len(clientes) + 1
        
        nome = obter_entrada("Nome: ")
        cpf = obter_entrada("CPF: ")
        
        telefone = obter_entrada("Telefone: ", pode_ser_vazio=True) 
        endereco = obter_entrada("Endereço: ", pode_ser_vazio=True) 

        cliente = {
            "id": id_cliente,
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone,
            "endereco": endereco
        }

        clientes.append(cliente)
        salvar_arquivo("clientes.txt", clientes)
        
        print("Cliente cadastrado com sucesso!")
        
    except Exception:
        print("Ocorreu um erro inesperado ao cadastrar o cliente.")


def listar_clientes():
    print("\nCadastros")
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
        
    for c in clientes:
        
        print(f"{c['id']} - {c['nome']} - CPF: {c['cpf']}")


def reservar_quarto():
    print("\nReseva Hotel")
    listar_clientes()
    
    if not clientes:
        print("Não há clientes cadastrados para realizar uma reserva.")
        return

    try:
        id_cliente = obter_entrada("ID do cliente: ", tipo=int)

        cliente = next((c for c in clientes if c["id"] == id_cliente), None)
        if not cliente:
            print("Cliente não encontrado.") 
            return

        print("\nQuartos disponíveis:")
        quartos_livres = [q for q in quartos if q["status"] == "Livre"]
        
        if not quartos_livres:
            print("Não há quartos livres no momento.")
            return

        for q in quartos_livres:
            
            print(f"Quarto {q['numero']} - Andar {q['andar']}")

        numero_quarto = obter_entrada("\nNúmero do quarto desejado: ", tipo=int)
        quarto = next((q for q in quartos if q["numero"] == numero_quarto), None)

        if not quarto or quarto["status"] != "Livre":
            print("Quarto indisponível.") 
            return

        # 'data' não pode ser vazio
        data = obter_entrada("Data da reserva (dd/mm/aaaa): ")

        reserva = {
            "id": len(reservas) + 1,
            "cliente": {"id": cliente["id"], "nome": cliente["nome"]},
            "quarto": {"numero": quarto["numero"], "andar": quarto["andar"]},
            "data": data,
            "status": "Reservado"
        }

        reservas.append(reserva)
        quarto["status"] = "Ocupado"

        salvar_arquivo("reservas.txt", reservas)

        print("Reserva concluída!") 

    except Exception:
        print("Ocorreu um erro inesperado ao tentar reservar o quarto.")


def check_out():
    print("\nCheck out")

    reservas_ativas = [r for r in reservas if r["status"] == "Reservado"]
    if not reservas_ativas:
        print("Nenhuma reserva ativa para check-out.")
        return
        
    for r in reservas_ativas:
        
        print(f"{r['id']} - {r['cliente']['nome']} - Quarto {r['quarto']['numero']} - {r['status']}")

    try:
        id_reserva = obter_entrada("ID da reserva para check-out: ", tipo=int)

        reserva = next((r for r in reservas_ativas if r["id"] == id_reserva), None)
        if not reserva:
            print("Reserva não encontrada.") 
            return

        reserva["status"] = "Finalizado"

        numero = reserva["quarto"]["numero"]
        quarto = next((q for q in quartos if q["numero"] == numero), None)
        
        if quarto:
            quarto["status"] = "Livre"
        
        salvar_arquivo("reservas.txt", reservas)

        print("Check-out realizado com sucesso!") 
        
    except Exception:
        print("Ocorreu um erro inesperado ao realizar o check-out.")


def pagamento_reserva():
    print("\nPagar Reserva")

    if not reservas:
        print("Nenhuma reserva registrada.")
        return
        
    for r in reservas:
        
        print(f"{r['id']} - {r['cliente']['nome']} - Status: {r['status']}")

    try:
        id_reserva = obter_entrada("ID da reserva: ", tipo=int)

        reserva = next((r for r in reservas if r["id"] == id_reserva), None)
        if not reserva:
            print("Reserva não encontrada.") 
            return

        valor = obter_entrada("Valor a pagar: ", tipo=float)
        
        if valor <= 0:
            print("O valor a pagar deve ser um número positivo.")
            return

        pagamento = {
            "id": len(pagamentos) + 1,
            "reserva_id": reserva["id"],
            "cliente": reserva["cliente"]["nome"],
            "valor": valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        pagamentos.append(pagamento)
        salvar_arquivo("pagamentos.txt", pagamentos)

        print("Pagamento registrado!") 
        
    except Exception:
        print("Ocorreu um erro inesperado ao registrar o pagamento.")


def menu():
    while True:
        
        print("SISTEMA DO HOTEL\n")
        print("[1] Cadastrar Cliente")
        print("[2] Listar Clientes")
        print("[3] Reservar Quarto")
        print("[4] Check-out")
        print("[5] Registrar Pagamento")
        print("[0] Sair")

        opc = input("Escolha: ")

        if opc == "1":
            cadastrar_cliente()
        elif opc == "2":
            listar_clientes()
        elif opc == "3":
            reservar_quarto()
        elif opc == "4":
            check_out()
        elif opc == "5":
            pagamento_reserva()
        elif opc == "0":
            
            print("Encerrando sistema...")
            break
        else:

            print("Opção inválida.")


if __name__ == "__main__":
    menu()