# ---- IMPORTS

import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
# ----- FUNÇÃO PARA CADASTRAR NOVO PEDIDO -----

def cadastrar_novo_pedido():
    print ('Cadastrar novo pedido'.upper())
    with open("dados.json", "r") as arquivo:
        dados = json.load(arquivo)
    dados["contador_pedidos"] += 1
    numero_pedido = dados["contador_pedidos"]
    logo_pedido = input("Insira o logo do pedido: ")
    quantidade = int(input("Insira a quantidade: "))
    vendedora = input("Insira o nome da vendedora: ")
    preço_str = input("Insira o preço: ")
    preço = float(preço_str.replace(',', '.'))
    data_do_pedido= input("Insira a data do pedido (DD/MM/AAAA): ")
    prazo_de_entrega = input("Insira o prazo de entrega (DD/MM/AAAA): ")
    pagamento = input("O pedido já foi pago? (sim/não): ").strip().lower()
    total = preço * quantidade
    codigo_pedido = f"pedido_{numero_pedido:04d}_{vendedora.replace(' ', '_').upper()}_{data_do_pedido.replace('/', '')}"
    pedido = {
        "codigo": codigo_pedido,
        "logo": logo_pedido,
        "quantidade": quantidade,
        "vendedora": vendedora,
        "preco_unitario": preço,
        "total": total,
        "data": data_do_pedido,
        "prazo": prazo_de_entrega,
        "pago": pagamento
    }
    dados["pedidos"].append(pedido)
    with open("dados.json", "w") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    print('Pedido cadastrado com sucesso')
    print(f'Valor do pedido: R$ {total:.2f}')
    print(f'Número do pedido: {numero_pedido}')

# ----- FUNÇÃO PARA CONSULTAR PEDIDO -----

def consultar_pedidos():
    print('CONSULTAR PEDIDOS')
    with open("dados.json", "r") as arquivo:
        dados = json.load(arquivo)
    pedidos = dados["pedidos"]
    if not pedidos:
        print("Nenhum pedido cadastrado.")
    else:
        for pedido in pedidos:
            print(f"Código: {pedido['codigo']}")
            print(f"Vendedora: {pedido['vendedora']}")
            print(f"Logo: {pedido['logo']}")
            print(f"Quantidade: {pedido['quantidade']}")
            print(f"Preço unitário: R$ {pedido['preco_unitario']:.2f}")
            print(f"Total: R$ {pedido['total']:.2f}")
            print(f"Data: {pedido['data']}")
            print(f"Prazo: {pedido['prazo']}")
            print(f"Pago: {pedido['pago'].upper()}")
            print("-" * 30)
            
# ----- FUNÇÃO PARA ALTERAR PEDIDO -----
def alterar_pedido():
    print('ALTERAR PEDIDO')
    with open("dados.json", "r") as arquivo:
        dados = json.load(arquivo)
    pedidos = dados["pedidos"]
    if not pedidos:
        print("Nenhum pedido cadastrado para alterar.")
        return
    
    codigo = input("Insira o código do pedido que deseja alterar: ")
    pedido_encontrado = None
    for pedido in pedidos:
        if pedido["codigo"] == codigo:
            pedido_encontrado = pedido
            break

    if not pedido_encontrado:
        print("Pedido não encontrado.")
        return

    print("\nDados atuais do pedido:")
    print(f"Logo: {pedido_encontrado['logo']}")
    print(f"Quantidade: {pedido_encontrado['quantidade']}")
    print(f"Preço unitário: R$ {pedido_encontrado['preco_unitario']:.2f}")
    print(f"Prazo: {pedido_encontrado['prazo']}")
    print(f"Pago: {pedido_encontrado['pago']}")

    print("\nDeixe em branco para não alterar o campo.")
    novo_logo = input(f"Novo logo ({pedido_encontrado['logo']}): ")
    if novo_logo.strip():
        pedido_encontrado["logo"] = novo_logo

    nova_quantidade = input(f"Nova quantidade ({pedido_encontrado['quantidade']}): ")
    if nova_quantidade.strip():
        pedido_encontrado["quantidade"] = int(nova_quantidade)
        pedido_encontrado["total"] = pedido_encontrado["preco_unitario"] * pedido_encontrado["quantidade"]

    novo_preco_str = input(f"Novo preço ({pedido_encontrado['preco_unitario']}): ")
    if novo_preco_str.strip():
        preco = float(novo_preco_str.replace(',', '.'))
        pedido_encontrado["preco_unitario"] = preco
        pedido_encontrado["total"] = preco * pedido_encontrado["quantidade"]

    novo_prazo = input(f"Novo prazo ({pedido_encontrado['prazo']}): ")
    if novo_prazo.strip():
        pedido_encontrado["prazo"] = novo_prazo

    novo_pago = input(f"Novo status pago (sim/não) ({pedido_encontrado['pago']}): ").strip().lower()
    if novo_pago in ['sim', 's', 'não', 'n', 'nao']:
        pedido_encontrado["pago"] = novo_pago

    with open("dados.json", "w") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    
    print("Pedido alterado com sucesso!")

# ----- FUNÇÃO PARA MENU PRINCIPAL
def menu_principal():
    while True:
        print ("Vendas - Prata & CriaRi.".capitalize().upper())
        print ('Menu Principal'.upper())    
        print ('1 - Cadastrar novo pedido'.upper())
        print ('2 - Consultar pedidos'.upper())
        print ('3 - Alterar pedido'.upper())
        print ('4 - Sair'.upper())
        opcao_menu = input('Escolha uma opção (1-4): ')      
        if opcao_menu == '1':
            cadastrar_novo_pedido()
        elif opcao_menu == '2':
            consultar_pedidos()
        elif opcao_menu == '3':
            alterar_pedido()
        elif opcao_menu == '4':
            print ('você escolheu sair do sistema. Até logo!'.upper())
            break
        else:
            print ('Opção inválida. Por favor, escolha uma opção válida.'.upper())
            break
        continuar = input("\nDeseja voltar ao menu principal? (s/n): ").strip().lower()
        if continuar != 's':
            print("Saindo do sistema. Até logo!")
            exit

# ----- CHAMANDO A FUNÇÃO DO MENU PRINCIPAL -----
menu_principal()
