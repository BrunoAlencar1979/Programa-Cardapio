import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json

def salvar_cardapio(cardapio, cardapio_imagens, arquivo_cardapio='cardapio.json', arquivo_imagens='cardapio_imagens.json'):
    with open(arquivo_cardapio, 'w') as f:
        json.dump(cardapio, f)
    with open(arquivo_imagens, 'w') as f:
        json.dump(cardapio_imagens, f)

def carregar_cardapio(arquivo_cardapio='cardapio.json', arquivo_imagens='cardapio_imagens.json'):
    try:
        with open(arquivo_cardapio, 'r') as f:
            cardapio = json.load(f)
        with open(arquivo_imagens, 'r') as f:
            cardapio_imagens = json.load(f)
    except FileNotFoundError:
        cardapio = {}
        cardapio_imagens = {}
    return cardapio, cardapio_imagens

# Inicializa o cardápio e imagens carregando-os dos arquivos
cardapio, cardapio_imagens = carregar_cardapio()

is_admin = False

def login():
    global is_admin
    username = username_entry.get()
    password = password_entry.get()
    if username == 'admin' and password == 'admin':
        is_admin = True
        messagebox.showinfo("Login", "Bem-vindo, Administrador!")
    else:
        messagebox.showerror("Erro de Login", "Usuário ou senha incorretos!")
    login_window.destroy()
    abrir_janela_cardapio()

def entrar_como_convidado():
    global is_admin
    is_admin = False
    login_window.destroy()
    abrir_janela_cardapio()

def mostrar_login_window():
    global login_window, username_entry, password_entry
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Usuário:").pack(pady=(10,0))
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Senha:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Entrar", command=login).pack(pady=5)
    tk.Button(login_window, text="Free", command=entrar_como_convidado).pack()

def abrir_janela_cardapio():
    cardapio_window = tk.Toplevel(root)
    cardapio_window.title("Cardápio")
    cardapio_window.geometry("600x400")

    frame_principal = tk.Frame(cardapio_window)
    frame_principal.pack(padx=20, pady=20)

    frame_lista = tk.Frame(frame_principal)
    frame_lista.pack(side=tk.LEFT, padx=10)

    pratos_listbox = tk.Listbox(frame_lista, width=30, height=10)
    pratos_listbox.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(frame_lista, orient=tk.VERTICAL)
    scrollbar.config(command=pratos_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    pratos_listbox.config(yscrollcommand=scrollbar.set)

    imagem_label = tk.Label(frame_lista)
    imagem_label.pack(pady=10)

    frame_botoes = tk.Frame(frame_principal)
    frame_botoes.pack(side=tk.RIGHT, padx=10)

    descricao_button = tk.Button(frame_botoes, text="Mostrar Descrição", command=lambda: mostrar_descricao_e_imagem(pratos_listbox.get(tk.ACTIVE)))
    descricao_button.pack(pady=(10,5), padx=10, fill=tk.X)

    adicionar_button = tk.Button(frame_botoes, text="Adicionar/Atualizar Prato", state=tk.NORMAL if is_admin else tk.DISABLED, command=lambda: abrir_janela_adicionar(pratos_listbox))
    adicionar_button.pack(pady=5, padx=10, fill=tk.X)

    mostrar_cardapio(pratos_listbox)

def mostrar_descricao_e_imagem(prato_selecionado):
    detalhes_window = tk.Toplevel(root)
    detalhes_window.title(prato_selecionado)
    detalhes_window.geometry("600x400")

    descricao = cardapio.get(prato_selecionado, "Descrição não disponível.")
    imagem_path = cardapio_imagens.get(prato_selecionado, "")
    try:
        if imagem_path:
            imagem = Image.open(imagem_path)
            imagem = imagem.resize((300, 300), Image.LANCZOS)
            imagem_tk = ImageTk.PhotoImage(imagem)
            imagem_label = tk.Label(detalhes_window, image=imagem_tk)
            imagem_label.image = imagem_tk
            imagem_label.pack(pady=10)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível carregar a imagem: {e}", parent=detalhes_window)

    descricao_label = tk.Label(detalhes_window, text=descricao, wraplength=500)
    descricao_label.pack(pady=10)

    voltar_button = tk.Button(detalhes_window, text="Voltar", command=detalhes_window.destroy)
    voltar_button.pack(pady=10)

def mostrar_cardapio(pratos_listbox):
    pratos_listbox.delete(0, tk.END)
    for prato in sorted(cardapio.keys()):
        pratos_listbox.insert(tk.END, prato)

def escolher_imagem():
    caminho_imagem = filedialog.askopenfilename(title="Selecione uma imagem", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
    return caminho_imagem

def abrir_janela_adicionar(pratos_listbox):
    adicionar_window = tk.Toplevel(root)
    adicionar_window.title("Adicionar/Atualizar Prato")
    adicionar_window.geometry("300x300")

    tk.Label(adicionar_window, text="Nome do Prato:").pack(pady=(10, 0))
    nome_prato_entry = tk.Entry(adicionar_window)
    nome_prato_entry.pack(pady=5)

    tk.Label(adicionar_window, text="Descrição do Prato:").pack()
    descricao_entry = tk.Entry(adicionar_window)
    descricao_entry.pack(pady=5)

    caminho_imagem = tk.StringVar(adicionar_window)
    caminho_imagem.set("Nenhuma imagem selecionada")

    escolher_imagem_button = tk.Button(adicionar_window, text="Escolher Imagem", command=lambda: caminho_imagem.set(escolher_imagem()))
    escolher_imagem_button.pack(pady=10)

    tk.Label(adicionar_window, textvariable=caminho_imagem, wraplength=250).pack(pady=5)

    tk.Button(adicionar_window, text="Adicionar/Atualizar", command=lambda: adicionar_ou_alterar_prato(nome_prato_entry.get(), descricao_entry.get(), caminho_imagem.get(), pratos_listbox, adicionar_window)).pack(pady=10)

def adicionar_ou_alterar_prato(nome_prato, descricao_prato, caminho_imagem, pratos_listbox, adicionar_window):
    if nome_prato and caminho_imagem != "Nenhuma imagem selecionada":
        cardapio[nome_prato] = descricao_prato if descricao_prato else "Descrição não disponível."
        cardapio_imagens[nome_prato] = caminho_imagem
        mostrar_cardapio(pratos_listbox)
        messagebox.showinfo("Atualização de Cardápio", f"O prato '{nome_prato}' foi {'atualizado' if nome_prato in cardapio else 'adicionado'} com sucesso. Imagem atualizada.")
        adicionar_window.destroy()
        salvar_cardapio(cardapio, cardapio_imagens)  # Salvar após adicionar/atualizar
    else:
        messagebox.showwarning("Ação Requerida", "Por favor, insira o nome do prato e selecione uma imagem.")

root = tk.Tk()
root.title("Sistema de Cardápio")
root.geometry("300x100")

tk.Button(root, text="Abrir Login", command=mostrar_login_window).pack(pady=20)

# Certifique-se de salvar o cardápio ao fechar o aplicativo
root.protocol("WM_DELETE_WINDOW", lambda: [salvar_cardapio(cardapio, cardapio_imagens), root.destroy()])

root.mainloop()
