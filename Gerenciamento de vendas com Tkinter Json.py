import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# Inicializa o JSON se não existir
try:
    with open("dados. json", "r") as arquivo:
        dados = json.load(arquivo)
except (FileNotFoundError, json.JSONDecodeError):
    dados = {"contador_pedidos": 0, "pedidos": []}
    with open("dados.json", "w") as arquivo:
        json. dump(dados, arquivo, indent=4, ensure_ascii=False)

# ----- FUNÇÕES DE VALIDAÇÃO -----
def validar_data(data_str):
    """Valida formato de data DD/MM/AAAA"""
    try: 
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_quantidade(quantidade_str):
    """Valida se quantidade é um número inteiro positivo"""
    try:
        qtd = int(quantidade_str)
        return qtd > 0
    except ValueError:
        return False

def validar_preco(preco_str):
    """Valida se preço é um número positivo"""
    try:
        preco = float(preco_str. replace(',', '.'))
        return preco > 0
    except ValueError: 
        return False

def validar_pago(pago_str):
    """Valida se status pago é sim ou não"""
    return pago_str.lower() in ['sim', 's', 'não', 'n', 'nao']

# ----- FUNÇÕES DE ARMAZENAMENTO -----
def carregar_dados():
    """Carrega dados do arquivo JSON"""
    try:
        with open("dados.json", "r") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"contador_pedidos": 0, "pedidos": []}

def salvar_dados(dados_atualizados):
    """Salva dados no arquivo JSON"""
    with open("dados.json", "w") as arquivo:
        json. dump(dados_atualizados, arquivo, indent=4, ensure_ascii=False)

# ----- FUNÇÃO PARA CADASTRAR NOVO PEDIDO -----
def cadastrar_novo_pedido(janela, entries):
    try:
        logo_pedido = entries['logo']. get().strip()
        quantidade_str = entries['quantidade'].get().strip()
        vendedora = entries['vendedora'].get().strip()
        preco_str = entries['preco'].get().strip()
        data_do_pedido = entries['data']. get().strip()
        prazo_de_entrega = entries['prazo'].get().strip()
        pagamento = entries['pago'].get().strip().lower()

        # Validações
        if not logo_pedido:
            messagebox.showerror("Erro", "Logo do pedido é obrigatório.")
            return
        if not vendedora:
            messagebox. showerror("Erro", "Nome da vendedora é obrigatório.")
            return
        if not validar_quantidade(quantidade_str):
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo.")
            return
        if not validar_preco(preco_str):
            messagebox.showerror("Erro", "Preço deve ser um número positivo (use .  ou , para decimal).")
            return
        if not validar_data(data_do_pedido):
            messagebox.showerror("Erro", "Data do pedido inválida.  Use formato DD/MM/AAAA.")
            return
        if not validar_data(prazo_de_entrega):
            messagebox.showerror("Erro", "Prazo de entrega inválido.  Use formato DD/MM/AAAA.")
            return
        if not validar_pago(pagamento):
            messagebox. showerror("Erro", "Status pago deve ser 'sim' ou 'não'.")
            return

        # Carrega dados, adiciona novo pedido e salva
        dados_atualizados = carregar_dados()
        dados_atualizados["contador_pedidos"] += 1
        numero_pedido = dados_atualizados["contador_pedidos"]
        
        quantidade = int(quantidade_str)
        preco = float(preco_str.replace(',', '.'))
        total = preco * quantidade
        codigo_pedido = f"pedido_{numero_pedido: 04d}_{vendedora. replace(' ', '_').upper()}_{data_do_pedido.replace('/', '')}"
        
        pedido = {
            "codigo":  codigo_pedido,
            "logo": logo_pedido,
            "quantidade": quantidade,
            "vendedora": vendedora,
            "preco_unitario": preco,
            "total": total,
            "data":  data_do_pedido,
            "prazo":  prazo_de_entrega,
            "pago": pagamento
        }
        
        dados_atualizados["pedidos"].append(pedido)
        salvar_dados(dados_atualizados)
        
        messagebox.showinfo("Sucesso", f'Pedido cadastrado com sucesso\nValor do pedido: R$ {total:. 2f}\nNúmero do pedido: {numero_pedido}')
        janela.destroy()
    except Exception as e:
        messagebox. showerror("Erro", f"Erro ao cadastrar pedido: {str(e)}")

# ----- FUNÇÃO PARA CONSULTAR PEDIDOS -----
def consultar_pedidos(janela_consulta):
    dados_atual = carregar_dados()
    pedidos = dados_atual["pedidos"]
    if not pedidos:
        messagebox.showinfo("Info", "Nenhum pedido cadastrado.")
        janela_consulta.destroy()
        return

    tree = ttk.Treeview(janela_consulta, columns=("Código", "Vendedora", "Logo", "Quantidade", "Preço Unitário", "Total", "Data", "Prazo", "Pago"), show="headings", height=15)
    tree.heading("Código", text="Código")
    tree.heading("Vendedora", text="Vendedora")
    tree.heading("Logo", text="Logo")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Preço Unitário", text="Preço Unitário")
    tree.heading("Total", text="Total")
    tree.heading("Data", text="Data")
    tree.heading("Prazo", text="Prazo")
    tree.heading("Pago", text="Pago")
    
    # Ajusta largura das colunas
    tree.column("Código", width=150)
    tree.column("Vendedora", width=100)
    tree.column("Logo", width=80)
    tree.column("Quantidade", width=80)
    tree.column("Preço Unitário", width=100)
    tree.column("Total", width=100)
    tree.column("Data", width=80)
    tree.column("Prazo", width=80)
    tree.column("Pago", width=60)
    
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for pedido in pedidos:
        tree.insert("", tk.END, values=(
            pedido['codigo'],
            pedido['vendedora'],
            pedido['logo'],
            pedido['quantidade'],
            f"R$ {pedido['preco_unitario']:.2f}",
            f"R$ {pedido['total']:.2f}",
            pedido['data'],
            pedido['prazo'],
            pedido['pago']. upper()
        ))

# ----- FUNÇÃO PARA ALTERAR PEDIDO -----
def alterar_pedido(janela, entries, codigo):
    try:
        dados_atualizados = carregar_dados()
        pedido_encontrado = None
        for p in dados_atualizados["pedidos"]:
            if p["codigo"] == codigo:
                pedido_encontrado = p
                break
        if not pedido_encontrado: 
            raise ValueError("Pedido não encontrado.")

        novo_logo = entries['logo'].get().strip()
        if novo_logo:
            pedido_encontrado["logo"] = novo_logo

        nova_quantidade = entries['quantidade'].get().strip()
        if nova_quantidade:
            if not validar_quantidade(nova_quantidade):
                messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo.")
                return
            pedido_encontrado["quantidade"] = int(nova_quantidade)
            pedido_encontrado["total"] = pedido_encontrado["preco_unitario"] * pedido_encontrado["quantidade"]

        novo_preco_str = entries['preco'].get().strip()
        if novo_preco_str:
            if not validar_preco(novo_preco_str):
                messagebox.showerror("Erro", "Preço deve ser um número positivo (use . ou , para decimal).")
                return
            preco = float(novo_preco_str.replace(',', '.'))
            pedido_encontrado["preco_unitario"] = preco
            pedido_encontrado["total"] = preco * pedido_encontrado["quantidade"]

        novo_prazo = entries['prazo'].get().strip()
        if novo_prazo:
            if not validar_data(novo_prazo):
                messagebox.showerror("Erro", "Prazo deve estar no formato DD/MM/AAAA.")
                return
            pedido_encontrado["prazo"] = novo_prazo

        novo_pago = entries['pago'].get().strip().lower()
        if novo_pago:
            if not validar_pago(novo_pago):
                messagebox. showerror("Erro", "Status pago deve ser 'sim' ou 'não'.")
                return
            pedido_encontrado["pago"] = novo_pago

        salvar_dados(dados_atualizados)
        messagebox.showinfo("Sucesso", "Pedido alterado com sucesso!")
        janela.destroy()
    except ValueError as e:
        messagebox. showerror("Erro", f"Valor inválido: {str(e)}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao alterar pedido: {str(e)}")

# ----- FUNÇÕES PARA ABRIR JANELAS -----
def abrir_janela_cadastro():
    janela_cad = tk.Toplevel(root)
    janela_cad.title("Cadastrar Novo Pedido")
    janela_cad.geometry("400x500")
    janela_cad.configure(bg="#141414")

    labels = ["Logo do pedido:", "Quantidade:", "Nome da vendedora:", "Preço (use . ou ,):", "Data do pedido (DD/MM/AAAA):", "Prazo de entrega (DD/MM/AAAA):", "O pedido já foi pago?  (sim/não):"]
    chaves = ['logo', 'quantidade', 'vendedora', 'preco', 'data', 'prazo', 'pago']
    entries = {}

    for label_text, chave in zip(labels, chaves):
        tk.Label(janela_cad, text=label_text, bg="#000000", fg="#ffffff").pack(pady=5)
        entry = tk.Entry(janela_cad, bg="#000000", fg="#ffffff", insertbackground="#ffffff")
        entry.pack()
        entries[chave] = entry

    btn_salvar = tk.Button(janela_cad, text="Salvar", command=lambda: cadastrar_novo_pedido(janela_cad, entries), bg="#4CAF50", fg="#ffffff")
    btn_salvar.pack(pady=20)

def abrir_janela_consulta():
    janela_cons = tk.Toplevel(root)
    janela_cons.title("Consultar Pedidos")
    janela_cons.geometry("1000x600")
    janela_cons.configure(bg="#0F0F0F")
    consultar_pedidos(janela_cons)

def abrir_janela_alterar():
    janela_alt = tk.Toplevel(root)
    janela_alt.title("Alterar Pedido")
    janela_alt.geometry("400x450")
    janela_alt.configure(bg="#000000")

    tk.Label(janela_alt, text="Código do pedido:", bg="#000000", fg="#ffffff").pack(pady=5)
    entry_codigo = tk.Entry(janela_alt, bg="#000000", fg="#ffffff", insertbackground="#ffffff")
    entry_codigo.pack()

    def carregar_dados_form():
        codigo = entry_codigo.get().strip()
        if not codigo:
            messagebox.showerror("Erro", "Insira o código do pedido.")
            return

        dados_atualizados = carregar_dados()
        pedido_encontrado = None
        for p in dados_atualizados["pedidos"]:
            if p["codigo"] == codigo: 
                pedido_encontrado = p
                break

        if not pedido_encontrado:
            messagebox.showerror("Erro", "Pedido não encontrado.")
            return

        # Limpa janela e mostra campos para edição
        for widget in janela_alt.winfo_children():
            widget. destroy()

        tk.Label(janela_alt, text=f"Dados atuais (deixe em branco para manter):", bg="#111010", fg="#ffffff").pack(pady=10)

        labels = ["Novo logo:", "Nova quantidade:", "Novo preço:", "Novo prazo:", "Novo pago (sim/não):"]
        chaves = ['logo', 'quantidade', 'preco', 'prazo', 'pago']
        entries = {}
        for label_text, chave in zip(labels, chaves):
            tk.Label(janela_alt, text=label_text, bg="#000000", fg="#ffffff").pack(pady=5)
            entry = tk.Entry(janela_alt, bg="#000000", fg="#ffffff", insertbackground="#ffffff")
            entry.pack()
            entries[chave] = entry

        btn_salvar = tk.Button(janela_alt, text="Salvar Alterações", command=lambda: alterar_pedido(janela_alt, entries, codigo), bg="#2196F3", fg="#ffffff")
        btn_salvar.pack(pady=20)

    tk.Button(janela_alt, text="Carregar Pedido", command=carregar_dados_form, bg="#FFC107", fg="#000000").pack(pady=10)

# ----- JANELA PRINCIPAL (MENU COM BOTÕES) -----
root = tk.Tk()
root.title("Vendas - Prata & CriaRi")
root.geometry("500x300")
root.configure(bg="#595656")

tk.Label(root, text="Menu Principal", font=("Arial", 16, "bold"), bg="#2D2C2C", fg="#ffffff").pack(pady=10)

btn_cadastrar = ttk.Button(root, text="Cadastrar Novo Pedido", command=abrir_janela_cadastro, width=30)
btn_cadastrar.pack(pady=10)

btn_consultar = ttk.Button(root, text="Consultar Pedidos", command=abrir_janela_consulta, width=30)
btn_consultar.pack(pady=10)

btn_alterar = ttk.Button(root, text="Alterar Pedido", command=abrir_janela_alterar, width=30)
btn_alterar.pack(pady=10)

btn_sair = ttk.Button(root, text="Sair", command=root.quit, width=30)
btn_sair.pack(pady=10)


root.mainloop()
