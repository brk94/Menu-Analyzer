import tkinter as tk
import ttkbootstrap as ttk
import os
import sqlite3
from datetime import datetime
from ttkbootstrap import Style
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import Toplevel, Label
from tkinter import scrolledtext
from tkinter import messagebox

# Caminhos
caminho_db = 'projeto1.db'
schema_path = 'schema.sql'

# Verifica se o banco já existe
novo_banco = not os.path.exists(caminho_db)

# Conexão
try:
    conexao = sqlite3.connect(caminho_db)
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    # Verifica se já existem tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()

    if novo_banco or len(tabelas) == 0:
        print("Criando estrutura do banco de dados a partir de schema.sql...")
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            cursor.executescript(schema_sql)
            conexao.commit()

except sqlite3.Error as err:
    print(f"Erro ao conectar ou inicializar o banco de dados: {err}")
    conexao = None
    cursor = None

# Função para centralizar a janela

def centralizar_janela(janela):
    janela.update_idletasks()
    largura_janela = janela.winfo_width()
    altura_janela = janela.winfo_height()
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura_janela // 2)
    y = (altura_tela // 2) - (altura_janela // 2)
    janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

# Classe para controle de telas

class App:
    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        self.frames = {}
        self.nome_usuario = ""
        self.caminho_base_padrao = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagens do Projeto")
        self.check_box1_tela_dois = tk.IntVar()

        # Cria os frames
        self.criar_frame_inicial()
        self.criar_frame_tela_inicio()
        self.criar_frame_tela_perfil()
        self.criar_frame_tela_carrinho()

        # Exibe a tela inicial
        self.mostrar_frame("inicial")

    # Métodos de Limpeza do Banco de Dados

    def limpar_carrinho_antes_de_sair(self):
        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row   # Permite acessar colunas por nome
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM carrinho")
                conexao.commit()

                # Reseta o contador de autoincremento
                cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'carrinho'")
                conexao.commit()
        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")

    def fechar_aplicacao(self):
        self.limpar_carrinho_antes_de_sair()
        self.root.destroy()

    # Métodos de Navegação entre Telas

    def mostrar_frame(self, nome):
        if nome == 'tela_carrinho':
            self.atualizar_tela_carrinho()

        frame = self.frames[nome]  # agora sempre será definido
        frame.tkraise()

    def atualizar_tela_carrinho(self):
        # Remove o frame atual do carrinho se ele existir
        if "tela_carrinho" in self.frames:
            self.frames["tela_carrinho"].destroy()
            del self.frames["tela_carrinho"]

        # Recria o frame do carrinho com dados atualizados
        self.criar_frame_tela_carrinho()

    def trocar_para_segunda_tela(self, nome_usuario, placeholder_text):
        flag = 0

        if nome_usuario == placeholder_text:
            print("Preencha o nome corretamente.")
        else:
            self.nome_usuario = nome_usuario

            try:
                with sqlite3.connect('projeto1.db') as conexao:
                    conexao.row_factory = sqlite3.Row  # Permite acessar colunas por nome
                    cursor = conexao.cursor()
                    # SELECT na Tabela usuários para coletar todos os usuários
                    query = "SELECT nome FROM usuarios"
                    cursor.execute(query)
                    resultado = cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Erro ao acessar o banco de dados: {e}")
            
            for linha in resultado:
                if linha['nome'] == nome_usuario:
                    self.criar_frame_segunda_tela_old_user()
                    self.mostrar_frame("segunda_old_user")
                    flag = 1
                    break

            if flag == 0:
                self.criar_frame_segunda_tela()
                self.mostrar_frame("segunda")

    def trocar_para_terceira_tela(self, flag, email_usuario=""):
        if flag == 1:
            self.email_usuario = email_usuario

            try:
                with sqlite3.connect('projeto1.db') as conexao:
                    cursor = conexao.cursor()
                    sql = "INSERT INTO usuarios (nome, email) VALUES (?, ?)"
                    valores = (self.nome_usuario, self.email_usuario)
                    cursor.execute(sql, valores)
                    id_usuario = cursor.lastrowid

                    for entry in self.alergenicos_entries:
                        nome_alergia = entry.get().strip().capitalize()
                        if not nome_alergia or nome_alergia == 'Digite aqui seu alergênico...':
                            continue

                        cursor.execute("SELECT id_alergenico FROM alergenicos WHERE nome = ?", (nome_alergia,))
                        resultado = cursor.fetchone()
                        if resultado:
                            id_alergenico = resultado[0]
                            try:
                                cursor.execute("INSERT INTO usuarios_alergenicos (id_usuario, id_alergenico) VALUES (?, ?)", (id_usuario, id_alergenico))
                            except sqlite3.IntegrityError:
                                print(f"Alergia '{nome_alergia}' já associada ao usuário.")
                        else:
                            print(f"Alergia não encontrada: {nome_alergia}")

                    conexao.commit()
                    print("Usuário e alergênicos inseridos/atualizados com sucesso!")
            except sqlite3.Error as err:
                print(f"Erro ao inserir/atualizar usuário e alérgenos no banco de dados: {err}")

        self.criar_frame_tela_perfil()
        self.mostrar_frame("tela_inicio")

    def trocar_para_tela_perfil(self):
        self.mostrar_frame("tela_perfil")
    
    def trocar_para_tela_carrinho(self):
        self.mostrar_frame('tela_carrinho')

    # Métodos de Criação das Telas

    def criar_frame_tela_perfil(self):
        frame = ttk.Frame(self.root)
        frame.place(relwidth=1, relheight=1)
        self.frames["tela_perfil"] = frame

        # Fundo com imagem
        caminho_imagem_fundo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagens do Projeto", "Tela Perfil.png")
        imagem = Image.open(caminho_imagem_fundo)
        imagem_tk = ImageTk.PhotoImage(imagem)
        label_imagem = tk.Label(frame, image=imagem_tk)
        label_imagem.image = imagem_tk
        label_imagem.place(relwidth=1, relheight=1)

        self.botoes_perfil = [
            {"nome": "Inicio", "imagem": "InicioOFF.png", "relx": 0.166, "rely": 0.964},
            {"nome": "Carrinho", "imagem": "CarrinhoOFF.png", "relx": 0.499, "rely": 0.964},
            {"nome": "Perfil", "imagem": "PerfilON.png", "relx": 0.833, "rely": 0.964},
            {"nome": "Meus Pedidos", "imagem": "Meus Pedidos.png", "relx": 0.498, "rely": 0.63},
            {"nome": "Editar Alergias", "imagem": "Editar Alerg.png", "relx": 0.498, "rely": 0.69},
            {"nome": "Feedback", "imagem": "Feedback.png", "relx": 0.498, "rely": 0.75},
            {"nome": "Ver Feedback", "imagem": "Ver Feedback.png", "relx": 0.498, "rely": 0.81},
        ]

        # Cria uma área com rolagem para exibir os alergênicos
        scroll_frame = ttk.Frame(frame)
        scroll_frame.place(relx=0.50, rely=0.43, relwidth=0.6, relheight=0.25, anchor="center")

        canvas = tk.Canvas(scroll_frame, bg="#FFFFFF", highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame_perfil = scrollable_frame

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        scrollable_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Força o foco no canvas para garantir que o scroll funcione desde o início
        canvas.focus_set()

        # Adiciona evento de rolagem ao canvas
        def on_mousewheel(event):
            if not canvas.winfo_exists():
                return

            # Limita rolagem para cima e para baixo
            if canvas.yview()[0] <= 0 and (event.delta > 0 or event.num == 4):
                return
            if canvas.yview()[1] >= 1 and (event.delta < 0 or event.num == 5):
                return

            # Scroll cross-platform
            if event.delta:
                canvas.yview_scroll(-1 * int(event.delta / 120), "units")
            elif event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

        # Vincula o evento de rolagem do mouse ao canvas
        canvas.bind("<MouseWheel>", on_mousewheel)  # Windows
        canvas.bind("<Button-4>", on_mousewheel)  # Outros sistemas (scroll up)
        canvas.bind("<Button-5>", on_mousewheel)  # Outros sistemas (scroll down)
        # Ajusta a largura do scrollable_frame ao tamanho do canvas
        def resize_scrollable_frame(event):
            canvas.itemconfig(scrollable_window, width=event.width)

        canvas.bind("<Configure>", resize_scrollable_frame)

        # Leitura de dados para o usuário conectado (nome e alergias)
        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row
                cursor = conexao.cursor()

                # Obter o id do usuário
                cursor.execute("SELECT id_usuario FROM usuarios WHERE nome = ?", (self.nome_usuario,))
                usuario = cursor.fetchone()
                if usuario:
                    id_usuario = usuario["id_usuario"]

                    # Obter os nomes dos alérgenos associados ao usuário
                    query = """SELECT a.nome FROM alergenicos a
                        JOIN usuarios_alergenicos ua ON a.id_alergenico = ua.id_alergenico
                        WHERE ua.id_usuario = ?
                    """
                    cursor.execute(query, (id_usuario,))
                    resultados = cursor.fetchall()

                    # Lista com os nomes das alergias
                    self.labels_alergenicos = [row["nome"] for row in resultados]
                else:
                    self.labels_alergenicos = []
        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")
            self.labels_alergenicos = []
            
        # Verifica se há alergias cadastradas
        if self.labels_alergenicos:
            # Cria labels para cada alergia e insere no frame com rolagem
            for alergia in self.labels_alergenicos:
                label = ttk.Label(scrollable_frame, foreground='black', text=alergia, font=("Figtree", 18, "bold"), anchor="center", justify="center", 
                                  background='#FFFFFF', wraplength=500)
                label.pack(pady=5, fill='x')
        else:
            # Caso não tenha alergias cadastradas, exibe uma mensagem informativa
            label = ttk.Label(scrollable_frame, foreground='black', text="Nenhuma alergia cadastrada", font=("Figtree", 18, "bold"), justify="center", background='#FFFFFF')
            label.pack(padx=60, pady=5)

        # Label para mostrar o nome (inicialmente vazio, será atualizado depois)
        self.label_nome = tk.Label(frame, font=("Montserrat", 40, "bold"), anchor='center', width=25)
        self.label_nome.place(relx=0.035, rely=0.05)
        self.label_nome.config(text=f'{self.nome_usuario}', background='#FFFFFF', foreground='#FB7470', borderwidth=0, highlightthickness=0)  # Atualiza o texto
        self.perfil_criar_botoes(frame)

    def criar_frame_inicial(self):
        frame = ttk.Frame(self.root)
        frame.place(relwidth=1, relheight=1)
        self.frames["inicial"] = frame

        # Fundo com imagem
        caminho_imagem_fundo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagens do Projeto", "Primeira Tela.jpeg")
        imagem = Image.open(caminho_imagem_fundo)
        imagem_tk = ImageTk.PhotoImage(imagem)
        label_imagem = tk.Label(frame, image=imagem_tk)
        label_imagem.image = imagem_tk
        label_imagem.place(relwidth=1, relheight=1)

        # Placeholder
        placeholder_text = 'Digite aqui seu nome..'

        nome_usuario = ttk.Entry(frame, width=38, justify='center')
        nome_usuario.insert(0, placeholder_text)
        nome_usuario.place(relx=0.31, rely=0.88, relheight=0.05)

        def on_focus_in(event):
            if nome_usuario.get() == placeholder_text:
                nome_usuario.delete(0, tk.END)
                nome_usuario.config(foreground='black')

        def on_focus_out(event):
            if not nome_usuario.get():
                nome_usuario.insert(0, placeholder_text)
                nome_usuario.config(foreground='grey')

        nome_usuario.bind("<FocusIn>", on_focus_in)
        nome_usuario.bind("<FocusOut>", on_focus_out)

        # Estilo de botão transparente (sem fundo/borda)
        style.configure("TTransparent.TButton",
                        background="",
                        borderwidth=0)
        style.map("TTransparent.TButton",
                background=[("active", ""), ("pressed", ""), ("disabled", "")],
                relief=[("pressed", "flat"), ("!pressed", "flat")])
        
        # Botão com imagem
        botao = tk.Button(frame, image=seta, borderwidth=0, highlightthickness=0,
                  background='#ffffff', activebackground='#ffffff',
                  command=lambda: self.trocar_para_segunda_tela(nome_usuario.get(), placeholder_text))
        botao.place(relx=0.928, rely=0.94, anchor="center", width=46, height=34)
        botao.config(cursor="hand2")

    def criar_frame_segunda_tela_old_user(self):
        frame = tk.Frame(self.root)
        frame.place(relwidth=1, relheight=1)
        self.frames["segunda_old_user"] = frame

        # Fundo com imagem
        caminho_imagem_fundo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagens do Projeto", "Segunda Tela 2.png")
        imagem = Image.open(caminho_imagem_fundo)
        imagem_tk = ImageTk.PhotoImage(imagem)
        label_imagem = tk.Label(frame, image=imagem_tk)
        label_imagem.image = imagem_tk
        label_imagem.place(relwidth=1, relheight=1)

         # Label para mostrar o nome
        self.label_nome = tk.Label(frame, text=self.nome_usuario, font=("Montserrat", 42, "bold"), justify='center')
        self.label_nome.config(background='#F3F1F1', foreground='#F97570')
        self.label_nome.pack(pady=120)  # ou pady=(100, 0) para empurrar mais para baixo

        # Buscar o email do usuário já cadastrado
        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row  # Permite acessar por nome da coluna
                cursor = conexao.cursor()

                cursor.execute("SELECT email FROM usuarios WHERE nome = ?", (self.nome_usuario,))
                resultado = cursor.fetchone()

                if resultado:
                    email_usuario = resultado["email"]

        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")

         # Botão com imagem
        botao = tk.Button(frame, image=seta, borderwidth=0, highlightthickness=0,
                  background='#ffffff', activebackground='#ffffff',
                  command=lambda: self.trocar_para_terceira_tela(2, email_usuario))
        botao.place(relx=0.928, rely=0.94, anchor="center", width=46, height=34)
        botao.config(cursor="hand2")

    def criar_frame_segunda_tela(self):
        # Criação do Frame principal diretamente no root
        frame = tk.Frame(self.root, bg="#E4DFE0")
        frame.place(relwidth=1, relheight=1)

        # Registra o frame interno no dicionário de frames
        self.frames["segunda"] = frame

        # Fundo com imagem
        try:
            caminho_imagem_fundo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Imagens do Projeto", "Segunda Tela.png")
            imagem = Image.open(caminho_imagem_fundo)
            imagem_tk = ImageTk.PhotoImage(imagem)
            fundo_label = tk.Label(frame, image=imagem_tk)
            fundo_label.image = imagem_tk  # Evita garbage collector
            fundo_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Erro: A imagem de fundo não foi encontrada no caminho especificado.")

        # Lista para armazenar os widgets Entry dinamicamente
        self.alergenicos_entries = []

        # Dicionário para armazenar os valores dos Entries
        self.alergenicos_values = {}

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                cursor = conexao.cursor()
                cursor.execute("SELECT nome FROM alergenicos ORDER BY nome ASC")
                resultados = cursor.fetchall()
        except sqlite3.Error as err:
                print(f"Erro ao buscar alergenicos na tabela alergenicos: {err}")

        self.opcoes_alergenicos = [resultado[0] for resultado in resultados]
    
        # Função para criar um Entry com placeholder
        def criar_entry_com_placeholder(parent, texto, valor_existente=""):
            entry = ttk.Entry(parent, width=40, justify='center')
            entry.insert(0, valor_existente if valor_existente else texto)
            entry.config(foreground='grey' if not valor_existente else 'black')

            def on_focus_in(event):
                if entry.get() == texto:
                    entry.delete(0, tk.END)
                    entry.config(foreground='black')

            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, texto)
                    entry.config(foreground='grey')

            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
            return entry
        
        style = ttk.Style()
        style.configure("Combobox.TCombobox",
                        fieldbackground="#E4DFE0",
                        background="#E4DFE0")

        # Função para criar um Combobox
        def criar_combobox_com_valor(parent, valor_existente=""):
            combobox = ttk.Combobox(parent, values=self.opcoes_alergenicos, state="readonly", width=40, justify='center', style="Combobox.TCombobox")
            combobox.set(valor_existente if valor_existente else self.opcoes_alergenicos[0])
            return combobox

        # Função para atualizar dinamicamente os Combobox
        def atualizar_entries():
            for i, combobox in enumerate(self.alergenicos_entries):
                current_value = combobox.get()
                self.alergenicos_values[i] = current_value

            for widget in self.alergenicos_entries:
                widget.destroy()
            self.alergenicos_entries.clear()

            for i, _ in enumerate(self.alergenicos_entries_placeholders):
                valor_existente = self.alergenicos_values.get(i, "")
                combobox = criar_combobox_com_valor(frame, valor_existente)
                combobox.place(relx=0.07, rely=0.59 + (i * 0.06), relwidth=0.75, relheight=0.035)
                self.alergenicos_entries.append(combobox)

        # Função para adicionar um novo Entry
        def adicionar_entry():
            if len(self.alergenicos_entries_placeholders) >= 7:
                print("Limite máximo de 7 alergênicos atingido.")
                return
            self.alergenicos_entries_placeholders.append("")  # Apenas um marcador de posição
            atualizar_entries()

        # Função para remover o último Entry
        def remover_entry():
            if self.alergenicos_entries_placeholders:
                # Remove o último placeholder
                self.alergenicos_entries_placeholders.pop()
                # Limpa valores apenas do índice removido
                self.alergenicos_values = {i: value for i, value in self.alergenicos_values.items() if i < len(self.alergenicos_entries_placeholders)}
                atualizar_entries()

        # Função para remover todos os Entries e resetar
        def resetar_entries():
            self.alergenicos_entries_placeholders.clear()  # Remove todos os placeholders
            self.alergenicos_values.clear()  # Limpa todos os valores associados
            atualizar_entries()  # Atualiza os Entries na tela

        # Inicializa a lista de placeholders para os Entries
        self.alergenicos_entries_placeholders = []

        # Checkbox para ativar/desativar Entries
        self.check_box1_tela_dois = tk.BooleanVar(value=False)

        def clique_checkbox():
            if self.check_box1_tela_dois.get():
                if not self.alergenicos_entries_placeholders:
                    adicionar_entry()
                botao_adicionar.place(relx=0.85, rely=0.57)
                botao_remover.place(relx=0.85, rely=0.62)
            else:
                resetar_entries()  # Reseta tudo ao desativar o checkbox
                botao_adicionar.place_forget()
                botao_remover.place_forget()

        checkbox = ttk.Checkbutton(frame, variable=self.check_box1_tela_dois, command=clique_checkbox)
        checkbox.place(relx=0.045, rely=0.515)

        # Criar label com o nome do usuário
        self.label_total_valor = ttk.Label(frame, text=f"{self.nome_usuario}", font=("Segoe UI", 24, "bold"), foreground="#F47070")
        self.label_total_valor.place(relx=0.125, rely=0.035)

        # Criar entry para o email
        entry_email = criar_entry_com_placeholder(frame, "Informe aqui seu e-mail..", valor_existente="")
        entry_email.place(relx=0.07, rely=0.44, relwidth=0.75, relheight=0.04)

        # Estilo para os botões "Adicionar" e "Remover" com cor de fundo personalizada e sem efeito hover
        style = ttk.Style()
        style.configure("Red.TButton", background="#F47070", foreground="white", borderwidth=0, focusthickness=0)
        style.map("Red.TButton", background=[("active", "#F47070")])  # Remove alteração ao passar o mouse

        # Botões para adicionar/remover Entries
        botao_adicionar = ttk.Button(frame, text="+", width=3, command=adicionar_entry, style="Red.TButton")
        botao_adicionar.config(cursor="hand2")
        botao_remover = ttk.Button(frame, text="-", width=3, command=remover_entry, style="Red.TButton")
        botao_adicionar.config(cursor="hand2")

        def ao_clicar_botao_continuar():
            email_digitado = entry_email.get().strip()
            
            # Verifica se está vazio ou se ainda é o placeholder
            if not email_digitado or email_digitado == "Informe aqui seu e-mail..":
                self.perfil_exibir_mensagem(self.root, "Por favor, preencha o e-mail antes de continuar.", "Campo obrigatório")
                return

            self.trocar_para_terceira_tela(1, email_digitado)

        botao = tk.Button(frame, image=seta, borderwidth=0, highlightthickness=0, command=ao_clicar_botao_continuar)
        botao.place(relx=0.928, rely=0.95, anchor="center", width=46, height=34)
        botao.config(cursor="hand2")

    def criar_frame_tela_carrinho(self):
        frame = tk.Frame(self.root)
        frame.place(relwidth=1, relheight=1)
        self.frames["tela_carrinho"] = frame

        # Fundo com imagem
        caminho_base = os.path.join(self.caminho_base_padrao + "\\Tela Carrinho.png")
        imagem = Image.open(caminho_base)
        imagem_tk = ImageTk.PhotoImage(imagem)
        self.label_imagem = tk.Label(frame, image=imagem_tk)
        self.label_imagem.image = imagem_tk
        self.label_imagem.place(relwidth=1, relheight=1)

        # Cria os botões da tela carrinho
        self.carrinho_criar_botoes(frame)

        # Frame visível com scroll para os itens do carrinho
        self.frame_carrinho_scroll = ttk.Frame(frame)
        self.frame_carrinho_scroll.place(relx=0.5, rely=0.13, relwidth=0.88, relheight=0.56, anchor="n")

        canvas = tk.Canvas(self.frame_carrinho_scroll, bg="#FFFFFF", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)  # Canvas primeiro

        scrollbar_carrinho = tk.Scrollbar(self.frame_carrinho_scroll, orient="vertical", command=canvas.yview)
        scrollbar_carrinho.pack(side="right", fill="y")  # Scrollbar depois

        canvas.configure(yscrollcommand=scrollbar_carrinho.set)

        self.scrollable_carrinho_frame = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_carrinho_frame, anchor="nw")

        # Atualiza scrollregion e largura
        def atualizar_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        self.scrollable_carrinho_frame.bind("<Configure>", atualizar_scroll)
        canvas.bind("<Configure>", atualizar_scroll)

        # Scroll com roda do mouse (ativado globalmente dentro do frame)
        def ativar_scroll_carrinho():
            def mousewheel_global(event):
                if not canvas.winfo_exists():
                    return
                if canvas.yview()[0] <= 0 and event.delta > 0:
                    return
                if canvas.yview()[1] >= 1 and event.delta < 0:
                    return
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            canvas.master.bind_all("<MouseWheel>", mousewheel_global)

        ativar_scroll_carrinho()

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                cursor = conexao.cursor()
                # Carrega os itens do carrinho do usuário atual
                query = "SELECT * FROM carrinho WHERE nome_item IS NOT NULL"
                cursor.execute(query)
                resultados = cursor.fetchall()

        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")

        self.itens_carrinho = []  # Zera a lista de controle

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                cursor = conexao.cursor()
                # Consulta para calcular o valor total dos produtos no carrinho ao abrir a tela
                query = "SELECT * FROM carrinho WHERE nome_item IS NOT NULL"
                cursor.execute(query)
                resultados = cursor.fetchall()

        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")

        # Calcula o total inicial
        total_inicial = sum(item['preco_unitario'] * item['quantidade'] for item in resultados)

        # Label de total
        self.label_total_valor = ttk.Label(frame, text=f"Total: R$ {total_inicial:.2f}", font=("Segoe UI", 24, "bold"), foreground="#F47070")
        self.label_total_valor.place(relx=0.16, rely=0.83)

        def atualizar_total_carrinho():
            total = 0
            for item in self.itens_carrinho:
                total += item['preco'] * item['qtd_var'].get()
            self.label_total_valor.config(text=f"Total: R$ {total:.2f}")

        def remover_item_do_carrinho(item, qtd_var, card):
            card.destroy()

            # Remove da lista com base no ID único do item
            self.itens_carrinho = [i for i in self.itens_carrinho if i['id'] != item['id_carrinho']]

            try:
                with sqlite3.connect('projeto1.db') as conexao:
                    cursor = conexao.cursor()
                    # Remove do banco
                    cursor.execute("DELETE FROM carrinho WHERE id_carrinho = ?", (item['id_carrinho'],))
                    conexao.commit()

            except sqlite3.Error as err:
                print(f"Erro ao remover item do banco de dados: {err}")

            atualizar_total_carrinho()

        # Botão "+"
        def adicionar(item, var):
            if var.get() < 10:
                novo_valor = var.get() + 1
                var.set(novo_valor)

            try:
                with sqlite3.connect('projeto1.db') as conexao:
                    cursor = conexao.cursor()
                    # Atualiza no banco
                    cursor.execute("UPDATE carrinho SET quantidade = ? WHERE id_carrinho = ?", (novo_valor, item['id_carrinho']))
                    conexao.commit()

            except sqlite3.Error as err:
                print(f"Erro ao atualizar item no banco de dados: {err}")

            atualizar_total_carrinho()

        # Botão "-"
        def subtrair(item, var):
            if var.get() > 1:
                novo_valor = var.get() - 1
                var.set(novo_valor)

                try:
                    with sqlite3.connect('projeto1.db') as conexao:
                        cursor = conexao.cursor()
                        # Atualiza no banco
                        cursor.execute("UPDATE carrinho SET quantidade = ? WHERE id_carrinho = ?", (novo_valor, item['id_carrinho']))
                        conexao.commit()

                except sqlite3.Error as err:
                    print(f"Erro ao atualizar item no banco de dados: {err}")

                atualizar_total_carrinho()

        # Criação dos cards dos produtos no carrinho
        for item in resultados:
            nome = item['nome_item']
            preco = item['preco_unitario']
            qtd = item['quantidade']
            adicionados = item['ingredientes_adicionados']
            removidos = item['ingredientes_removidos']

            card = ttk.Frame(self.scrollable_carrinho_frame, padding=10, relief="ridge", borderwidth=2)
            card.pack(fill='x', padx=10, pady=6)
            card.bind("<Button-1>", lambda e, item=item: print(f"Card clicado: {item['nome_item']}"))

            # Lado esquerdo
            frame_esquerda = ttk.Frame(card)
            frame_esquerda.pack(side="left", fill="both", expand=True)

            ttk.Label(frame_esquerda, text=nome, font=("Segoe UI", 12, "bold"), foreground='#F47070').pack(anchor='w')
            ttk.Label(frame_esquerda, text=f"R$ {preco:.2f}", font=("Segoe UI", 10, "bold"), foreground='black').pack(anchor='w')

            if adicionados:
                ttk.Label(frame_esquerda, text=f"Adicionados: {adicionados}", font=("Segoe UI", 9), foreground="green").pack(anchor='w')
            if removidos:
                ttk.Label(frame_esquerda, text=f"Removidos: {removidos}", font=("Segoe UI", 9), foreground="red").pack(anchor='w', pady=(2, 0))

            # Frame da direita do card
            frame_direita = ttk.Frame(card, width=120, height=60)  # ajuste o tamanho conforme necessário
            frame_direita.pack(side="right", padx=8, pady=4)
            frame_direita.pack_propagate(False)  # evita que o frame encolha

            qtd_var = tk.IntVar(value=qtd)

            self.itens_carrinho.append({'preco': preco, 'qtd_var': qtd_var, 'card': card, 'id': item['id_carrinho']})

            # Label da quantidade (posição central)
            label_qtd = ttk.Label(frame_direita, textvariable=qtd_var, width=3, foreground='#F47070', anchor="center", font=("Segoe UI", 10))
            label_qtd.place(x=50, y=20)  # ponto central

            botao_mais = tk.Button(frame_direita, image=plus3, command=lambda item=item, var=qtd_var: adicionar(item, var),
                                background="#ffffff", activebackground='#ffffff', borderwidth=0, highlightthickness=0)
            botao_mais.image = plus3
            botao_mais.place(x=80, y=5)  # acima à direita da label
            botao_mais.config(cursor="hand2")

            botao_menos = tk.Button(frame_direita, image=minus3, command=lambda item=item, var=qtd_var: subtrair(item, var),
                                    background="#ffffff", activebackground='#ffffff', borderwidth=0, highlightthickness=0)
            botao_menos.image = minus3
            botao_menos.place(x=80, y=35)  # abaixo à direita da label
            botao_menos.config(cursor="hand2")

            # Botão de lixeira (à esquerda da label)
            botao_lixeira = tk.Button(frame_direita, image=lixeira, command=lambda item=item, var=qtd_var, c=card: remover_item_do_carrinho(item, var, c),
                                    background="#ffffff", activebackground='#ffffff', borderwidth=0, highlightthickness=0)
            botao_lixeira.image = lixeira
            botao_lixeira.place(x=10, y=19)
            botao_lixeira.config(cursor="hand2")

    def criar_frame_tela_inicio(self):
        frame = tk.Frame(self.root)
        frame.place(relwidth=1, relheight=1)
        self.frames["tela_inicio"] = frame

        # Fundo com imagem
        caminho_base = os.path.join(self.caminho_base_padrao + "\\Tela Inicio.png")
        imagem = Image.open(caminho_base)
        imagem_tk = ImageTk.PhotoImage(imagem)
        self.label_imagem = tk.Label(frame, image=imagem_tk)
        self.label_imagem.image = imagem_tk
        self.label_imagem.place(relwidth=1, relheight=1)

        # Frame visível onde os pratos serão exibidos (limitado a uma área)
        self.frame_pratos_scroll = ttk.Frame(frame)
        self.frame_pratos_scroll.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.62, anchor="n")  # ajuste o relheight como necessário

        # Canvas + Scrollbar
        canvas = tk.Canvas(self.frame_pratos_scroll, bg="#FFFFFF", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame_pratos_scroll, orient="vertical", command=canvas.yview)
        self.scrollable_pratos_frame = ttk.Frame(canvas)

        self.scrollable_pratos_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_pratos_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def bind_scroll(canvas):
            def _on_mousewheel(event):
                if canvas.yview()[0] <= 0 and event.delta > 0:
                    return
                if canvas.yview()[1] >= 1 and event.delta < 0:
                    return
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            self.frame_pratos_scroll.bind("<Enter>", lambda e: self.frame_pratos_scroll.bind_all("<MouseWheel>", _on_mousewheel))
            self.frame_pratos_scroll.bind("<Leave>", lambda e: self.frame_pratos_scroll.unbind_all("<MouseWheel>"))

        bind_scroll(canvas)

        # Dicionário para armazenar os botões das páginas
        self.botoes_paginas = {}
        
        # Mapeamento de botões com imagem e posição
        self.botoes_inicio = [
            {"nome": "Entradas", "imagem": "EntradasON.png", "relx": 0.137, "rely": 0.19},
            {"nome": "Almoços", "imagem": "AlmoçosOFF.png", "relx": 0.281, "rely": 0.19},
            {"nome": "Lanches", "imagem": "LanchesOFF.png", "relx": 0.428, "rely": 0.19},
            {"nome": "Doces", "imagem": "DocesOFF.png", "relx": 0.573, "rely": 0.19},
            {"nome": "Veganos", "imagem": "VeganosOFF.png", "relx": 0.718, "rely": 0.19},
            {"nome": "Bebidas", "imagem": "BebidasOFF.png", "relx": 0.864, "rely": 0.19},
            {"nome": "Inicio", "imagem": "InicioON.png", "relx": 0.166, "rely": 0.964},
            {"nome": "Carrinho", "imagem": "CarrinhoOFF.png", "relx": 0.499, "rely": 0.964},
            {"nome": "Perfil", "imagem": "PerfilOFF.png", "relx": 0.833, "rely": 0.964},
        ]

        self.inicio_carregar_dados_iniciais()
        self.inicio_criar_botoes(frame)

        # Já carrega as opções de Entradas para evitar problema no código
        self.inicio_alterar_botoes('Entradas')

    # Métodos utilizados na Tela de Início

    def inicio_popup_confirmacao_alergenico(self, prato):
        largura_popup = 400
        altura_popup = 200

        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela // 2) - (largura_popup // 2)
        y = (altura_tela // 2) - (altura_popup // 2)

        # Variável de controle para retorno
        resposta = tk.IntVar(value=-1)

        popup = tk.Toplevel(self.root)
        popup.title("Atenção: Alérgenos detectados")
        popup.geometry(f"{largura_popup}x{altura_popup}+{x}+{y}")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        alergenicos = prato.get('alergenicos')
        if isinstance(alergenicos, str):
            alergenicos = [alergenicos]
        elif alergenicos is None:
            alergenicos = []

        alergenicos_formatados = [a.title() for a in alergenicos]

        style = Style()
        style.configure("Red.TLabel", foreground="#F47070")

        msg = "Este prato contém os seguintes alérgenos que estão na sua lista:\n\n"
        msg += ", ".join(alergenicos_formatados) if alergenicos_formatados else "Nenhum alérgeno identificado."
        msg += "\n\nDeseja continuar mesmo assim?"

        label = ttk.Label(popup, text=msg, style="Red.TLabel", wraplength=380, justify="left", font=("Arial", 10, "bold"))
        label.pack(pady=(20, 10))

        def confirmar():
            resposta.set(1)
            popup.destroy()

        def cancelar():
            resposta.set(0)
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", cancelar)

        botoes_frame = tk.Frame(popup)
        botoes_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("Custom.TButton", background="red", foreground="white", borderwidth=0, focusthickness=0, padding=6)
        style.map("Custom.TButton", background=[("active", "#F47070"), ("!disabled", "#F47070")])

        botao_confirmar = ttk.Button(botoes_frame, text="Confirmar", style="Custom.TButton", command=confirmar, width=12)
        botao_confirmar.pack(side="left", padx=10)
        botao_confirmar.config(cursor="hand2")
        botao_cancelar = ttk.Button(botoes_frame, text="Cancelar", style="Custom.TButton", command=cancelar, width=12)
        botao_cancelar.pack(side="left", padx=10)
        botao_cancelar.config(cursor="hand2")

        # Espera o popup ser fechado
        self.root.wait_window(popup)

        # Retorna 1 (confirmado) ou 0 (cancelado)
        return resposta.get()

    def inicio_adicionar_carrinho(self, prato, qtd, nome_pagina, popup):
            # Dados base
            id_item = prato[nome_pagina]
            tipo_item = nome_pagina.split("_")[1]  # Ex: "entradas"
            nome_item = prato['nome']
            preco_unitario = float(prato['preco'])

            ingredientes_adicionados = []
            ingredientes_removidos = []

            if self.flag_alergia:
                flag_validacao = self.inicio_popup_confirmacao_alergenico(prato)
                if not flag_validacao:
                    return  # O usuário cancelou o popup

            # Esta parte deve ser feita sempre, independentemente da alergia
            for nome, var in self.ingredientes_selecionados_adicionar.items():
                if var.get() == 1:
                    ingredientes_adicionados.append(nome)
            for nome, var in self.ingredientes_selecionados_remover.items():
                if var.get() == 0:
                    ingredientes_removidos.append(nome)

            # Inserção no carrinho (com ou sem alergia)
            adicionados_str = ', '.join(ingredientes_adicionados)
            removidos_str = ', '.join(ingredientes_removidos)

            try:
                with sqlite3.connect('projeto1.db') as conexao:
                    cursor = conexao.cursor()
                    cursor.execute("""
                        INSERT INTO carrinho (id_item, tipo_item, nome_item, preco_unitario, quantidade,
                            ingredientes_removidos, ingredientes_adicionados) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (id_item, tipo_item, nome_item, preco_unitario, qtd, removidos_str, adicionados_str))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Item adicionado ao carrinho!")
                    self.ingredientes_selecionados_adicionar.clear()
                    self.ingredientes_selecionados_remover.clear()
                    popup.unbind_all("<MouseWheel>")
                    popup.destroy()
            except sqlite3.Error as err:
                print("Erro ao inserir no carrinho:", err)
                messagebox.showerror("Erro", f"Não foi possível adicionar ao carrinho.\n{err}")

    def inicio_carregar_dados_iniciais(self):
        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row  # Permite acessar colunas por nome
                cursor = conexao.cursor()
                # Executa a consulta para obter todas as entradas
                query = "SELECT * FROM entradas"
                cursor.execute(query)
                resultados = cursor.fetchall()
                extensao_padrao = ".jpg"  # Formato das imagens
                # Cria um dicionário para mapear ID do produto para o caminho da imagem
                mapeamento_imagens = {}
                for row in resultados:
                    # Código para pegar a parte de mapeamento de imagens
                    id_produto = row['id_entradas']
                    nome_arquivo = f"{id_produto}{extensao_padrao}"  # Exemplo: "1.jpg"
                    caminho_completo = os.path.join(self.caminho_base_padrao, nome_arquivo)
                    mapeamento_imagens[id_produto] = caminho_completo

                # Atualiza self.botoes_inicio com os caminhos das imagens
                for item in self.botoes_inicio:
                    if item["nome"] in mapeamento_imagens:
                        # Extrai apenas o nome do arquivo para a lógica de carregamento
                        item["imagem"] = os.path.basename(mapeamento_imagens[item["nome"]])  # Exemplo: "1.jpg"
                    elif item["nome"] not in ['Entradas', 'Almoços', 'Lanches', 'Doces', 'Veganos', 'Bebidas', 'Inicio', 'Carrinho', 'Perfil']:
                        print(f"Aviso: Caminho de imagem não gerado para o produto '{item['nome']}'")

        except sqlite3.Error as err:
            print(f"Erro ao buscar nomes de produtos do banco de dados: {err}")

    def inicio_abrir_detalhes_prato(self, prato, nome_pagina):
        # Nome da categoria para usar para acessar o caminho correto das URLs
        nome_categoria = nome_pagina.split("_", 1)[1]
        str(nome_categoria).capitalize()
        
        popup = tk.Toplevel(self.root)
        popup.title("Detalhes do Prato")

        # Centraliza popup
        largura = 700
        altura = 700
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2
        popup.geometry(f"{largura}x{altura}+{x}+{y}")
        popup.resizable(False, False)

        # Torna popup modal (scroll exclusivo, foco, bloqueia fundo)
        popup.transient(self.root)
        popup.grab_set()

        # Crie um estilo novo com a cor desejada
        style = Style()
        style.configure("Red.TLabel", foreground="#F47070")

        # Nome do prato
        nome_label = ttk.Label(popup, text=prato['nome'], style="Red.TLabel", font=("Arial", 20, "bold"))
        nome_label.place(x=30, y=20)

        # Botões: Descrição e Detalhes
        def trocar_texto(conteudo):
            texto_box.configure(state="normal")
            texto_box.delete("1.0", tk.END)
            texto_box.insert(tk.END, conteudo)
            texto_box.configure(state="disabled")

        btn_descricao = tk.Button(popup, image=descricao, background="#ffffff", activebackground='#ffffff', fg="white", borderwidth=0, highlightthickness=0, command=lambda: trocar_texto(prato['descricao']))
        btn_descricao.place(x=25, y=70)
        btn_descricao.config(cursor="hand2")
        
        btn_detalhes = tk.Button(popup, image=historia, background="#ffffff", activebackground='#ffffff', fg="white", borderwidth=0, highlightthickness=0, command=lambda: trocar_texto(prato['detalhes']))
        btn_detalhes.place(x=205, y=70)
        btn_detalhes.config(cursor="hand2")

        # Texto scrollável
        texto_box = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=45, height=5, font=("Arial", 10))
        texto_box.place(x=30, y=110)
        texto_box.insert(tk.END, prato['descricao'])
        texto_box.configure(state="disabled")

        # Alergênicos
        alerg_label = ttk.Label(popup, text="Alergênicos: ", style="Red.TLabel", font=("Arial", 10, "bold"))
        alerg_label.place(x=25, y=210)

        alergenicos = prato.get('alergenicos') or ''

        if alergenicos == '':
            alerg_info = ttk.Label(popup, text="Não contém nenhum ingrediente alergênico", style="Red.TLabel", font=("Arial", 10, "bold"))
        else:
            alergenicos = ', '.join([alergia.strip().capitalize() for alergia in alergenicos.split(',')])
            alerg_info = ttk.Label(popup, text=f"Contém {alergenicos}", style="Red.TLabel", font=("Arial", 10, "bold"))
        alerg_info.place(x=108, y=210)

        # Caminho URL da imagem do prato
        caminho_imagem = os.path.join(self.caminho_base_padrao, nome_categoria)
        caminho_imagem = os.path.join(caminho_imagem, str(prato[f'{nome_pagina}']))
        caminho_imagem = caminho_imagem + '.jpg'

        # Abre a imagem do prato
        img = Image.open(caminho_imagem)
        img_tk = ImageTk.PhotoImage(img)

        # Cria a label da imagem
        label_nome_prato = tk.Label(popup, image=img_tk, bg="#f0f0f0")
        label_nome_prato.image = img_tk  # Mantém a referência!
        label_nome_prato.place(x=440, y=40)  # Posição no popup

        # Caminho URL da imagem de alerta de alergênico
        caminho_imagem = os.path.join(self.caminho_base_padrao, 'alert.png')

        def criar_tooltip(widget, texto):
            tooltip = None

            def mostrar_tooltip(event):
                nonlocal tooltip
                tooltip = tk.Toplevel(widget)
                tooltip.wm_overrideredirect(True)  # Remove bordas
                tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

                # Estilo para tooltip (com cor personalizada)
                style.configure("Tooltip.TLabel",foreground="#F47070", background="#ffffff", font=("Arial", 9), borderwidth=1, relief="solid")
                label = ttk.Label(tooltip, text=texto, style='Tooltip.TLabel').pack()

            def esconder_tooltip(event):
                nonlocal tooltip
                if tooltip:
                    tooltip.destroy()
                    tooltip = None

            widget.bind("<Enter>", mostrar_tooltip)
            widget.bind("<Leave>", esconder_tooltip)

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row
                cursor = conexao.cursor()

                # Busca o ID do usuário
                cursor.execute("SELECT id_usuario FROM usuarios WHERE nome = ?", (self.nome_usuario,))
                resultado_usuario = cursor.fetchone()
                if not resultado_usuario:
                    raise Exception("Usuário não encontrado.")
                id_usuario = resultado_usuario["id_usuario"]

                # Busca os nomes das alergias do usuário
                query = """
                    SELECT a.nome
                    FROM alergenicos a
                    JOIN usuarios_alergenicos ua ON a.id_alergenico = ua.id_alergenico
                    WHERE ua.id_usuario = ?
                """
                cursor.execute(query, (id_usuario,))
                resultados = cursor.fetchall()

        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")
            resultados = []

        # Processamento de alergias
        alergias_usuario = [row["nome"].strip().lower() for row in resultados]
        alergias_prato = prato.get('alergenicos')

        if alergias_prato:
            lista_prato = [a.strip().lower() for a in alergias_prato.split(',')]

            # Verifica interseção
            self.flag_alergia = any(alergia in lista_prato for alergia in alergias_usuario)

            if self.flag_alergia:
                # Mostra imagem de alerta
                img = Image.open(caminho_imagem)
                img_tk = ImageTk.PhotoImage(img)
                label_alerta = tk.Label(popup, image=img_tk, bg="#f0f0f0")
                label_alerta.image = img_tk
                label_alerta.place(x=380, y=21)
                criar_tooltip(label_alerta, "O usuário possui alergia a algum ingrediente do prato.")

        # Frame scrollável
        frame_externo = tk.Frame(popup, width=640, height=350, bg="black")
        frame_externo.place(x=26, y=260)

        canvas = tk.Canvas(frame_externo, bg="white", width=640, height=350)

        def bind_scroll(canvas_popup):
            def _on_mousewheel(event):
                # Impede rolagem para além do topo
                if canvas_popup.yview()[0] <= 0 and event.delta > 0:
                    return
                # Impede rolagem além do fim
                if canvas_popup.yview()[1] >= 1 and event.delta < 0:
                    return
                canvas_popup.yview_scroll(int(-1 * (event.delta / 120)), "units")

            canvas_popup.bind("<Enter>", lambda e: canvas_popup.bind_all("<MouseWheel>", _on_mousewheel))
            canvas_popup.bind("<Leave>", lambda e: canvas_popup.unbind_all("<MouseWheel>"))

            def atualizar_scrollregion(event=None):
                canvas_popup.configure(scrollregion=canvas_popup.bbox("all"))

            canvas_popup.bind("<Configure>", atualizar_scrollregion)

        bind_scroll(canvas)
        scrollbar = tk.Scrollbar(frame_externo, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Variáveis com o valor real do prato
        preco_base = float(prato['preco'])
        
        # Use ttk.Label com o estilo aplicado
        preco_label = ttk.Label(popup, text=f'R${preco_base:.2f}', style="Red.TLabel", font=("Arial", 14))
        preco_label.place(x=217, y=641)

        def atualizar_preco():
            try:
                qtd = int(qtd_var.get() or 1)
                preco_total = qtd * preco_base
                preco_label.config(text=f"R${preco_total:.2f}")
            except Exception as e:
                print("Erro ao atualizar preço:", e)

        def validar_entrada(valor):
            if valor == "":
                return True  # Permite apagar temporariamente
            if valor.isdigit():
                val = int(valor)
                return 1 <= val <= 10
            return False
        
        # Quantidade inicial no Spinbox
        qtd_var = tk.StringVar(value="1")

        # Registrando a função de validação
        vcmd = (root.register(validar_entrada), "%P")

        # Spinbox
        spinbox = ttk.Spinbox(
            popup, from_=1, to=10, textvariable=qtd_var, width=2, font=("Arial", 12), validate="key", validatecommand=vcmd,
            command=atualizar_preco  # <- Isso aqui que faz funcionar ao clicar nas setas
        )

        spinbox.place(x=310, y=638)

        # Botão adicionar ao carrinho
        botao_adicionar = tk.Button(popup, image=adicionar, background="#ffffff", activebackground='#ffffff', fg="white", 
                            borderwidth=0, highlightthickness=0, command=lambda: self.inicio_adicionar_carrinho(prato, qtd_var.get(), nome_pagina, popup))
        botao_adicionar.place(x=372, y=635)
        botao_adicionar.config(cursor="hand2")

        # Parte de criação dos cards
        titulo = ttk.Label(scroll_frame, text="Deseja adicionar algum ingrediente?", font=("Arial", 12, "bold"), style='Red.TLabel')
        titulo.pack(anchor="w", padx=5, pady=(5, 10))

        # Separa os ingredientes adicionáveis da sua variável text no BD
        ingredientes_str = prato.get("ingredientes_adicionaveis", "")
        ingredientes = [i.strip() for i in ingredientes_str.split(",") if i.strip()]

        # Separa os ingredientes removíveis da sua variável text no BD
        ingredientes_removiveis_str = prato.get("ingredientes_removiveis", "")
        ingredientes_removiveis = [i.strip() for i in ingredientes_removiveis_str.split(",") if i.strip()]

        # Salvar os ingredientes que vão ser adicionados
        self.ingredientes_selecionados_adicionar = {}

        # Salvar os ingredientes que vão ser removidos
        self.ingredientes_selecionados_remover = {}

        # For para os adicionáveis
        for ingrediente in ingredientes:
            card = tk.Frame(scroll_frame, bg="#f9f9f9", height=60, width=610, bd=1, relief="solid")
            card.pack(fill="x", pady=5, padx=5)

            # Nome do ingrediente
            lbl = ttk.Label(card, text=ingrediente.capitalize(), style="Red.TLabel", font=("Arial", 12, "bold"))
            lbl.place(x=10, y=18)

            # Quantidade (com controle)
            qtd_ingrediente_var = tk.IntVar(value=0)

            # Cria e armazena a variável no dicionário
            qtd_ingrediente_var = tk.IntVar(value=0)
            self.ingredientes_selecionados_adicionar[ingrediente] = qtd_ingrediente_var

            def criar_callback(qv=qtd_ingrediente_var, nome=ingrediente):
                def aumentar():
                    if qv.get() < 1:
                        qv.set(qv.get() + 1)
                def diminuir():
                    if qv.get() > 0:
                        qv.set(qv.get() - 1)
                return aumentar, diminuir

            mais, menos = criar_callback()
   
            botao_menos = tk.Button(card, image=minus2, command=menos, borderwidth=0, highlightthickness=0, background='#ffffff', activebackground='#ffffff')
            botao_menos.place(x=400, y=20)
            botao_menos.config(cursor="hand2")

            label_qtd = ttk.Label(card, textvariable=qtd_ingrediente_var, style="Red.TLabel", font=("Arial", 10))
            label_qtd.place(x=443.5, y=22)

            botao_mais = tk.Button(card, image=plus2, command=mais, borderwidth=0, highlightthickness=0, background='#ffffff', activebackground='#ffffff')
            botao_mais.place(x=470, y=20)
            botao_mais.config(cursor="hand2")

        # Label para ingredientes removíveis
        titulo_remover = ttk.Label(scroll_frame, text="Deseja remover algum ingrediente?", font=("Arial", 12, "bold"), style='Red.TLabel')
        titulo_remover.pack(anchor="w", padx=5, pady=(15, 10))

        # For para os removíveis
        for ingrediente in ingredientes_removiveis:
            card = tk.Frame(scroll_frame, bg="#f9f9f9", height=60, width=610, bd=1, relief="solid")
            card.pack(fill="x", pady=5, padx=5)

            # Nome do ingrediente
            label = ttk.Label(card, text=ingrediente.capitalize(), style="Red.TLabel", font=("Arial", 12, "bold"))
            label.place(x=10, y=18)

            # Quantidade (com controle)
            qtd_remover_var = tk.IntVar(value=1)

            # Armazena a variável
            self.ingredientes_selecionados_remover[ingrediente] = qtd_remover_var

            def criar_callback_remover(qv=qtd_remover_var, nome=ingrediente):
                def aumentar():
                    if qv.get() < 1:
                        qv.set(qv.get() + 1)
                def diminuir():
                    if qv.get() > 0:
                        qv.set(qv.get() - 1)
                return aumentar, diminuir

            mais, menos = criar_callback_remover()

            botao_menos = tk.Button(card, image=minus2, command=menos, borderwidth=0, highlightthickness=0, background='#ffffff', activebackground='#ffffff')
            botao_menos.place(x=400, y=20)
            botao_menos.config(cursor="hand2")

            label_qtd = ttk.Label(card, textvariable=qtd_remover_var, style="Red.TLabel", font=("Arial", 10))
            label_qtd.place(x=443.5, y=22)

            botao_mais = tk.Button(card, image=plus2, command=mais, borderwidth=0, highlightthickness=0, background='#ffffff', activebackground='#ffffff')
            botao_mais.place(x=470, y=20)
            botao_mais.config(cursor="hand2")

        # Aguarda o fechamento da janela para liberar a janela principal
        self.root.wait_window(popup)

    def inicio_criar_botoes(self, frame):
        for botao_info in self.botoes_inicio:
            if "imagem" in botao_info:  # Cria botões apenas se a informação da imagem estiver presente
                caminho_imagem = os.path.join(self.caminho_base_padrao, botao_info["imagem"])
                try:
                    imagem = ImageTk.PhotoImage(Image.open(caminho_imagem))
                    nome_botao = botao_info["nome"]

                    btn = tk.Button(frame, image=imagem, borderwidth=0, highlightthickness=0, background='#ffffff', activebackground='#ffffff',
                                    command=lambda n=nome_botao: self.inicio_alterar_botoes(n))
                    btn.image = imagem
                    btn.config(cursor="hand2")
                    self.botoes_paginas[nome_botao] = btn

                    if nome_botao in ['Inicio', 'Perfil', 'Carrinho']:
                        btn.place(relx=botao_info["relx"], rely=botao_info["rely"], anchor="center", width=299, height=61)
                    else:
                        btn.place(relx=botao_info["relx"], rely=botao_info["rely"], anchor="center", width=132, height=54)
                except FileNotFoundError:
                    print(f"Erro: Imagem não encontrada em {caminho_imagem}")

    def inicio_alterar_botoes(self, nome_botao_pagina):
        mapeamento_botao_paginas = {
            'Entradas': ('EntradasON.png', 'EntradasOFF.png'),
            'Almoços': ('AlmoçosON.png', 'AlmoçosOFF.png'),
            'Lanches': ('LanchesON.png', 'LanchesOFF.png'),
            'Doces': ('DocesON.png', 'DocesOFF.png'),
            'Veganos': ('VeganosON.png', 'VeganosOFF.png'),
            'Bebidas': ('BebidasON.png', 'BebidasOFF.png'),
        }

        if nome_botao_pagina not in ['Inicio', 'Carrinho', 'Perfil']:
            for nome, (img_on, img_off) in mapeamento_botao_paginas.items():
                img_nome = img_on if nome == nome_botao_pagina else img_off
                caminho_completo = os.path.join(self.caminho_base_padrao, img_nome)
                try:
                    nova_imagem = Image.open(caminho_completo)
                    nova_imagem_tk = ImageTk.PhotoImage(nova_imagem)
                    botao = self.botoes_paginas[nome]
                    botao.config(image=nova_imagem_tk)
                    botao.image = nova_imagem_tk
                except FileNotFoundError:
                    print(f"Imagem não encontrada: {caminho_completo}")

            # Carregamento de dados da categoria selecionada 
            try:
                lowercase = nome_botao_pagina.lower()
                try:
                    with sqlite3.connect('projeto1.db') as conexao:
                        conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                        cursor = conexao.cursor()
                        # Consulta dinâmica com nome da tabela variável
                        query = f"SELECT * FROM {lowercase}"
                        cursor.execute(query)
                        resultados = cursor.fetchall()

                except sqlite3.Error as err:
                    print(f"Erro ao acessar o banco de dados: {err}")

                nome_pagina = "id_" + lowercase

                self.pratos = []
                for linha in resultados:
                    prato = {}
                    for coluna, valor in dict(linha).items():
                        if valor is not None:
                            prato[coluna] = valor
                    self.pratos.append(prato)

                # Atualiza a área scrollável com os pratos
                for widget in self.scrollable_pratos_frame.winfo_children():
                    widget.destroy()

                # Organiza os pratos em duas colunas
                for i, prato in enumerate(self.pratos):
                    nome = prato["nome"]
                    preco = prato["preco"]
                    id_prato = prato[nome_pagina]
        
                    caminho_img = os.path.join(self.caminho_base_padrao, nome_botao_pagina, f"{id_prato}.jpg")

                    try:
                        imagem = Image.open(caminho_img).resize((200, 180))
                        imagem_tk = ImageTk.PhotoImage(imagem)

                        card = ttk.Frame(self.scrollable_pratos_frame, padding=10)
                        row = i // 2
                        column = i % 2
                        card.grid(row=row, column=column, padx=80, pady=20, sticky="n")
                        btn = tk.Button(card, image=imagem_tk, borderwidth=0, highlightthickness=0, bg="#FFFFFF",
                                        command=lambda p=prato: self.inicio_abrir_detalhes_prato(p, nome_pagina))
                        btn.image = imagem_tk
                        btn.pack()
                        btn.config(cursor="hand2")

                        info = ttk.Label(card, text=f"{nome}\nR$ {preco:.2f}", font=("Figtree", 13, "bold"), background="#FFFFFF", foreground="#F47070", justify="center")

                        info.pack(pady=5)

                    except FileNotFoundError:
                        print(f"Imagem não encontrada para o prato {id_prato}")

            except sqlite3.Error as err:
                print(f"Erro ao buscar dados da categoria '{nome_botao_pagina}': {err}")
        elif nome_botao_pagina == 'Inicio':
            pass
        elif nome_botao_pagina == 'Carrinho':
            self.trocar_para_tela_carrinho()
        elif nome_botao_pagina == 'Perfil':
            self.trocar_para_tela_perfil()

    # Métodos utilizados na Tela de Carrinho

    def carrinho_finalizar_compra(self, n):
        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                cursor = conexao.cursor()
                # Busca todos os itens do carrinho
                cursor.execute("SELECT * FROM carrinho")
                itens_carrinho = cursor.fetchall()

                if not itens_carrinho:
                    messagebox.showinfo("Carrinho vazio", "Adicione itens ao carrinho antes de finalizar a compra.")
                    return

                try:
                    conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                    cursor.execute("SELECT id_usuario FROM usuarios WHERE nome = ?", (self.nome_usuario,))
                    usuario = cursor.fetchone()

                    if not usuario:
                        messagebox.showerror("Erro", "Usuário não encontrado.")
                        return

                    id_usuario = usuario['id_usuario']
                    preco_total = sum(item['preco_unitario'] * item['quantidade'] for item in itens_carrinho)

                    try:
                        conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                        cursor.execute("INSERT INTO pedidos (id_usuario, preco_total) VALUES (?, ?)", (id_usuario, preco_total))
                        conexao.commit()
                        id_pedido = cursor.lastrowid  # ID gerado automaticamente

                        for item in itens_carrinho:
                            categoria_prato = item['tipo_item']
                            nome_prato = item['nome_item']
                            ingredientes_adicionados = item['ingredientes_adicionados']
                            ingredientes_removidos = item['ingredientes_removidos']
                            quantidade = item['quantidade']

                            # Insere na tabela itens_pedido com os novos campos
                            cursor.execute("""INSERT INTO itens_pedido (id_pedido, nome_prato, categoria, ingredientes_adicionados,
                                ingredientes_removidos, quantidade) VALUES (?, ?, ?, ?, ?, ?)""", 
                                (id_pedido, nome_prato, categoria_prato, ingredientes_adicionados, ingredientes_removidos, quantidade))

                        cursor.execute("DELETE FROM carrinho")
                        conexao.commit()

                        # Reseta o contador de autoincremento
                        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'carrinho'")
                        conexao.commit()
                        
                        messagebox.showinfo("Pedido Concluído", "Seu pedido foi realizado com sucesso!")

                        self.atualizar_tela_carrinho()  # Atualiza a tela com carrinho limpo

                    except Exception as e:
                        conexao.rollback()
                        messagebox.showerror("Erro no Pedido", f"Ocorreu um erro ao finalizar o pedido: {e}")

                except Exception as e:
                    messagebox.showerror("Erro no Banco de Dados", f"Ocorreu um erro ao buscar o usuário: {e}")

        except Exception as e:
            messagebox.showerror("Erro no Banco de Dados", f"Ocorreu um erro ao acessar o carrinho: {e}")

    def carrinho_criar_botoes(self, frame):
        botoes_carrinho = [
            {"nome": "Inicio", "imagem": "InicioOFF.png", "relx": 0.166, "rely": 0.964},
            {"nome": "Carrinho", "imagem": "CarrinhoON.png", "relx": 0.499, "rely": 0.964},
            {"nome": "Perfil", "imagem": "PerfilOFF.png", "relx": 0.833, "rely": 0.964},
        ]

        for botao_info in botoes_carrinho:
            caminho_imagem = os.path.join(self.caminho_base_padrao, botao_info["imagem"])

            try:
                imagem = ImageTk.PhotoImage(Image.open(caminho_imagem))
                nome_botao = botao_info["nome"]

                btn = tk.Button(frame, image=imagem, borderwidth=0, highlightthickness=0, background='#ffffff',
                                activebackground='#ffffff', command=lambda n=nome_botao: self.carrinho_alterar_botoes(n))
                btn.image = imagem
                btn.config(cursor="hand2")
                self.botoes_paginas[nome_botao] = btn

                btn.place(relx=botao_info["relx"], rely=botao_info["rely"], anchor="center", width=300, height=61)

            except FileNotFoundError:
                print(f"Erro: Imagem não encontrada em {caminho_imagem}")


        botao_adicionar_items = tk.Button(frame, image=adicionar_items, borderwidth=0, highlightthickness=0, background='#ffffff', activebackground='#ffffff',
                                  highlightbackground="#ffffff", highlightcolor="#ffffff", takefocus=False, command=lambda: self.mostrar_frame('tela_inicio'))
        botao_adicionar_items.place(relx=0.38, rely=0.73)
        botao_adicionar_items.config(cursor="hand2")

        botao_finalizar_comprar = tk.Button(frame, image=finalizar_compra, borderwidth=0, highlightthickness=0, background='#ffffff', activebackground='#ffffff',
                                    command=lambda n=nome_botao: self.carrinho_finalizar_compra(n))
        botao_finalizar_comprar.place(relx=0.5, rely=0.83)
        botao_finalizar_comprar.config(cursor="hand2")

    def carrinho_alterar_botoes(self, nome_botao_pagina):
        if nome_botao_pagina == 'Inicio':
            self.mostrar_frame('tela_inicio')
        elif nome_botao_pagina == 'Perfil':
            self.mostrar_frame('tela_perfil')
        else:
            pass

    # Métodos utilizados na Tela de Perfil

    def perfil_criar_botoes(self, frame):
        for botao_info in self.botoes_perfil:
            if "imagem" in botao_info:  # Cria botões apenas se a informação da imagem estiver presente
                caminho_imagem = os.path.join(self.caminho_base_padrao, botao_info["imagem"])

                try:
                    imagem = ImageTk.PhotoImage(Image.open(caminho_imagem))
                    nome_botao = botao_info["nome"]

                    btn = tk.Button(frame, image=imagem, borderwidth=0, highlightthickness=0, background='#ffffff', activebackground='#ffffff',
                                    command=lambda n=nome_botao: self.perfil_alterar_botoes(n))
                    btn.image = imagem
                    btn.config(cursor="hand2")

                    self.botoes_paginas[nome_botao] = btn

                    if nome_botao in ['Inicio', 'Carrinho', 'Perfil']:
                        btn.place(relx=botao_info["relx"], rely=botao_info["rely"], anchor="center", width=300, height=61)
                    else:
                        btn.place(relx=botao_info["relx"], rely=botao_info["rely"], anchor="center", width=300, height=40)

                except FileNotFoundError:
                    print(f"Erro: Imagem não encontrada em {caminho_imagem}")

    def perfil_salvar_feedback(self, nome, email, mensagem, pop_up_perfil):
        placeholders = ['Informe seu nome..', 'Informe seu e-mail..', 'Informe sua mensagem de feedback..']
        largura_popup = 350
        altura_popup = 40

        # Obtem tamanho da tela
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()

        # Calcula posição central
        x = (largura_tela // 2) - (largura_popup // 2)
        y = (altura_tela // 2) - (altura_popup // 2)

        popup = tk.Toplevel(self.root)
        popup.geometry(f"{largura_popup}x{altura_popup}+{x}+{y}")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.protocol("WM_DELETE_WINDOW", lambda: None)
        popup.grab_set()

        label = ttk.Label(popup, foreground='#F97570', font=("Montserrat", 12, "bold"), justify="center")
        label.place(relx=0.5, rely=0.4, anchor="center")

        if (not nome or nome in placeholders) or (not email or email in placeholders) or (not mensagem or mensagem in placeholders):
            popup.title("Mensagem de Erro")
            label.config(text="Todos os campos devem estar preenchidos!")
            popup.after(2000, popup.destroy)
        else:
            popup.title("Mensagem de Sucesso")
            label.config(text="Feedback realizado com sucesso!")
            try:
                with sqlite3.connect('projeto1.db') as conexao:
                    cursor = conexao.cursor()

                    # Obter o id_usuario com base no nome
                    cursor.execute("SELECT id_usuario FROM usuarios WHERE nome = ?", (self.nome_usuario,))
                    resultado_usuario = cursor.fetchone()

                    if not resultado_usuario:
                        print(f"Usuário '{nome}' não encontrado.")
                    else:
                        id_usuario = resultado_usuario[0]

                        # Inserir o feedback com o id_usuario como chave estrangeira
                        query = "INSERT INTO feedback (nome, email, feedback, id_usuario) VALUES (?, ?, ?, ?)"
                        valores = (nome, email, mensagem, id_usuario)
                        cursor.execute(query, valores)

                        conexao.commit()
                        
            except sqlite3.Error as err:
                print(f"Erro ao salvar feedback: {err}")
            popup.after(2000, lambda: (popup.destroy(), pop_up_perfil.destroy()))

    def perfil_buscar_feedbacks(self, frame_interno):
        # Sempre cria um novo container para feedbacks
        self.container_cards = ttk.Frame(frame_interno)
        self.container_cards.pack(fill='both', expand=True)

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row
                cursor = conexao.cursor()

                # Buscar o id_usuario a partir do nome do usuário logado
                cursor.execute("SELECT id_usuario FROM usuarios WHERE nome = ?", (self.nome_usuario,))
                resultado_usuario = cursor.fetchone()

                if not resultado_usuario:
                    raise Exception("Usuário não encontradoasdsad.")

                id_usuario = resultado_usuario["id_usuario"]

                # Buscar os feedbacks vinculados a esse id_usuario
                query = "SELECT nome, feedback FROM feedback WHERE id_usuario = ?"
                cursor.execute(query, (id_usuario,))
                resultados = cursor.fetchall()

        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")
            resultados = []
        except Exception as e:
            print(str(e))
            resultados = []

        # Exibe feedbacks encontrados ou mensagem de vazio
        if not resultados:
            mensagem_texto = "Você ainda não enviou nenhum feedback."
            ttk.Label(
                self.container_cards, text=mensagem_texto, font=("Montserrat", 12, "bold"), foreground="#F97570",
                anchor="center",justify="center").pack(pady=20)
        else:
            for resultado in resultados:
                card = ttk.Frame(self.container_cards, padding=15, relief="raised", borderwidth=2)
                card.pack(fill='x', padx=10, pady=10)

                nome_label = ttk.Label(card, text=f"Nome do Usuário: {resultado['nome']}", font=("Segoe UI", 12, "bold"),foreground="#F47070")
                nome_label.pack(anchor='w', pady=(0, 5))

                feedback_label = ttk.Label(
                    card, text=f"Mensagem de Feedback: {resultado['feedback']}", font=("Segoe UI", 11),
                    foreground="#444444", wraplength=620, justify="left")
                feedback_label.pack(anchor='w')

    def perfil_tela_meus_feedbacks(self, popup):
        popup.title("Meus Feedbacks")
        popup.geometry("700x700")
        popup.resizable(False, False)

        def ao_fechar():
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", ao_fechar)

        # Frame com Canvas (sem Scrollbar)
        frame_scroll = ttk.Frame(popup)
        frame_scroll.pack(fill='both', expand=True)

        canvas = tk.Canvas(frame_scroll, borderwidth=0)
        canvas.pack(side='left', fill='both', expand=True)

        frame_interno = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=frame_interno, anchor='nw')

        def atualizar_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        frame_interno.bind("<Configure>", atualizar_scroll)
        canvas.bind("<Configure>", atualizar_scroll)

        # Scroll com roda do mouse (sem barra visível)
        def on_mousewheel(event):
            if not canvas.winfo_exists():
                return
            try:
                if canvas.yview()[0] <= 0 and event.delta > 0:
                    return
                if canvas.yview()[1] >= 1 and event.delta < 0:
                    return
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass  # canvas já foi destruído

        def ativar_scroll_popup_feedbacks():
            def mousewheel_global(event):
                if not canvas.winfo_exists():
                    return
                if canvas.yview()[0] <= 0 and event.delta > 0:
                    return
                if canvas.yview()[1] >= 1 and event.delta < 0:
                    return
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            popup.bind_all("<MouseWheel>", mousewheel_global)

            def remover_scroll():
                popup.unbind_all("<MouseWheel>")

            popup.protocol("WM_DELETE_WINDOW", lambda: [remover_scroll(), popup.destroy()])

        ativar_scroll_popup_feedbacks()

        # Label Meus Feedbacks
        titulo_label = ttk.Label(frame_interno, text="Meus Feedbacks", font=("Segoe UI", 20, "bold"), foreground="#F47070",
                                anchor="center",justify="center")
        titulo_label.pack(pady=(20, 10), fill='x')

        # Entrada e botão de busca
        self.perfil_buscar_feedbacks(frame_interno)

        #  Container Inicial dos Cards
        self.container_cards = ttk.Frame(frame_interno)
        self.container_cards.pack(fill='both', expand=True)

        # Força rolagem para o topo após construção do layout
        popup.after_idle(lambda: canvas.yview_moveto(0))

    def perfil_exibir_mensagem(self, parent, mensagem, titulo="Mensagem"):
        # Criar uma nova janela (Toplevel) para exibir a mensagem
        janela_mensagem = Toplevel(parent)
        janela_mensagem.title(titulo)  # Define o título dinamicamente
        janela_mensagem.geometry("300x150")  # Define o tamanho da janela
        janela_mensagem.resizable(False, False)  # Desativa redimensionamento

        # Centralizar a janela na tela
        largura_janela = 300
        altura_janela = 75
        largura_tela = janela_mensagem.winfo_screenwidth()
        altura_tela = janela_mensagem.winfo_screenheight()
        posicao_x = (largura_tela // 2) - (largura_janela // 2)
        posicao_y = (altura_tela // 2) - (altura_janela // 2)
        janela_mensagem.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

        # Adicionar mensagem
        label_mensagem = ttk.Label(janela_mensagem, text=mensagem, foreground='#F97570', font=("Montserrat", 10, "bold"), wraplength=280)
        label_mensagem.pack(pady=10)

        # Centralizar a janela em relação ao parent
        janela_mensagem.transient(parent)  # Garante que a janela fique na frente do parent
        janela_mensagem.grab_set()  # Bloqueia interação com outras janelas enquanto o erro está ativo
        parent.wait_window(janela_mensagem)  # Aguarda o fechamento da janela

    def perfil_atualizar_labels_alergenicos(self):
        # Limpa todos os widgets do scrollable_frame_perfil
        for widget in self.scrollable_frame_perfil.winfo_children():
            widget.destroy()
        self.labels_alergenicos.clear()

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row
                cursor = conexao.cursor()

                # Busca o ID do usuário pelo nome
                cursor.execute("SELECT id_usuario FROM usuarios WHERE nome = ?", (self.nome_usuario,))
                resultado_usuario = cursor.fetchone()
                if not resultado_usuario:
                    raise Exception("Usuário não encontrado.")

                id_usuario = resultado_usuario["id_usuario"]

                # Busca os nomes das alergias associadas ao usuário
                query = """
                    SELECT a.nome FROM alergenicos a
                    JOIN usuarios_alergenicos ua ON a.id_alergenico = ua.id_alergenico
                    WHERE ua.id_usuario = ?
                    ORDER BY a.nome ASC
                """
                cursor.execute(query, (id_usuario,))
                resultados = cursor.fetchall()

        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")
            resultados = []

        # Atualiza os labels na tela com as alergias
        if resultados:
            for row in resultados:
                alergia = row["nome"]
                label = ttk.Label(
                    self.scrollable_frame_perfil, foreground='black', text=alergia,
                    font=("Figtree", 18, "bold"), anchor="center", justify="center",
                    background='#FFFFFF', wraplength=500
                )
                label.pack(pady=5, fill='x')
                self.labels_alergenicos.append(label)
        else:
            label = ttk.Label(
                self.scrollable_frame_perfil, foreground='black', text="Nenhuma alergia cadastrada.",
                font=("Figtree", 18, "bold"), justify="center", background='#FFFFFF'
            )
            label.pack(anchor="center", pady=5)
            self.labels_alergenicos.append(label)

    def perfil_atualizar_alergias(self, popup):
        # Remove valores vazios e junta os valores em uma string separada por ", "
        alergias_atualizadas = []
        for item in self.alergia_entries:
            valor = item["combobox"].get().strip().capitalize()
            if valor and valor != "Alergênico não definido":
                alergias_atualizadas.append(valor)

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                cursor = conexao.cursor()
                # Consulta os valores atuais no banco de dados
                query_atual = """SELECT a.nome FROM alergenicos a
                JOIN usuarios_alergenicos ua ON a.id_alergenico = ua.id_alergenico
                JOIN usuarios u ON u.id_usuario = ua.id_usuario
                WHERE u.nome = ?
                """
                cursor.execute(query_atual, (self.nome_usuario,))
                resultados = cursor.fetchall()

        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")

        # Verifica se os valores preenchidos são os mesmos do banco
        #alergias_atuais = resultado_atual['alergenicos'] if resultado_atual else ""
        alergias_atuais = [row["nome"] for row in resultados] if resultados else ["Alergênico não definido"]

        if alergias_atualizadas == alergias_atuais:
            # Exibe mensagem de erro se não houver alterações
            self.perfil_exibir_mensagem(
                popup, "Nenhuma alteração foi realizada no cadastro. Por favor, modifique os dados antes de salvar.",
                titulo="Erro de Validação"
            )
            return  # Interrompe o processo de salvamento

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                cursor = conexao.cursor()

                # Obter o ID do usuário
                cursor.execute("SELECT id_usuario FROM usuarios WHERE nome = ?", (self.nome_usuario,))
                resultado_usuario = cursor.fetchone()
                if not resultado_usuario:
                    print("Usuário não encontrado.")
                    return
                id_usuario = resultado_usuario[0]
                # Apagar todas as alergias antigas do usuário
                cursor.execute("DELETE FROM usuarios_alergenicos WHERE id_usuario = ?", (id_usuario,))

                # Inserir as novas alergias
                for nome_alergia in alergias_atualizadas:
                    cursor.execute("SELECT id_alergenico FROM alergenicos WHERE nome = ?", (nome_alergia,))
                    resultado_alergia = cursor.fetchone()
                    if resultado_alergia:
                        id_alergenico = resultado_alergia[0]
                        cursor.execute(
                            "INSERT INTO usuarios_alergenicos (id_usuario, id_alergenico) VALUES (?, ?)",
                            (id_usuario, id_alergenico)
                        )
                    else:
                        print(f"Alergia '{nome_alergia}' não encontrada na tabela 'alergenicos'.")

                conexao.commit()
                # Atualizar os labels dos alérgenos na tela de perfil
                self.perfil_atualizar_labels_alergenicos()
                # Exibir mensagem de sucesso
                self.perfil_exibir_mensagem(popup, f"As alergias foram atualizadas com sucesso para o usuário {self.nome_usuario}!", titulo="Operação Bem-Sucedida")
                popup.destroy()

        except sqlite3.IntegrityError as e:
            self.perfil_exibir_mensagem(popup, f"Você está tentando cadastrar mais de uma vez uma mesma alergia no seu perfil.", titulo="Erro de Validação")
        except sqlite3.Error as e:
            # Exibir mensagem de erro em caso de falha no banco de dados
            self.perfil_exibir_mensagem(popup, f"Ocorreu um erro ao atualizar as alergias: {str(e)}", titulo="Erro de Validação")

    def perfil_abrir_detalhes_pedido(self, id_pedido):
        largura_popup = 500
        altura_popup = 500

        # Centralização
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela // 2) - (largura_popup // 2)
        y = (altura_tela // 2) - (altura_popup // 2)

        popup = tk.Toplevel(self.root)
        popup.geometry(f"{largura_popup}x{altura_popup}+{x}+{y}")
        popup.title("Detalhes do Pedido")
        popup.transient(self.root)
        popup.grab_set()
        popup.resizable(False, False)

        def ao_fechar():
            popup.grab_release()
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", ao_fechar)

        # Frame com scrollbar
        frame_scroll = ttk.Frame(popup)
        frame_scroll.pack(fill="both", expand=True)

        canvas = tk.Canvas(frame_scroll, borderwidth=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        frame_interno = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=frame_interno, anchor="nw")

        def atualizar_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        frame_interno.bind("<Configure>", atualizar_scroll)
        canvas.bind("<Configure>", atualizar_scroll)

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                cursor = conexao.cursor()
                # Buscar data da compra
                cursor.execute("SELECT data_hora_compra FROM pedidos WHERE id_pedido = ?", (id_pedido,))
                pedido_info = cursor.fetchone()
                if pedido_info and pedido_info['data_hora_compra']:
                    # SQLite geralmente retorna datas como string, então precisamos convertê-la
                    data_hora_str = pedido_info['data_hora_compra']
                    data_hora = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M:%S')
                    data_formatada = data_hora.strftime('%d/%m/%Y %H:%M:%S')  # Inclui os segundos
                else:
                    data_formatada = "Data desconhecida"    

        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")

        # Título e data
        ttk.Label(frame_interno, text="Detalhes do Pedido", font=("Segoe UI", 16, "bold"), foreground="#F47070").pack(pady=(15, 5))
        ttk.Label(frame_interno, text=f"Pedido Nº {id_pedido} - Data: {data_formatada}",
                font=("Segoe UI", 10), foreground="#F47070").pack(pady=(0, 15))

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                cursor = conexao.cursor()
                # Buscar os itens do pedido
                cursor.execute("""
                    SELECT nome_prato, categoria, ingredientes_adicionados, ingredientes_removidos, quantidade
                    FROM itens_pedido
                    WHERE id_pedido = ?
                """, (id_pedido,))
                itens = [dict(row) for row in cursor.fetchall()]

        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")

        total = 0

        for item in itens:
            nome = item['nome_prato']
            tipo = item['categoria']
            adicionados = item.get('ingredientes_adicionados', '') # Usando .get para evitar KeyError caso a chave não exista
            removidos = item.get('ingredientes_removidos', '')   # Usando .get para evitar KeyError caso a chave não exista
            quantidade = item.get('quantidade') # Supondo que a chave 'quantidade' exista no seu dicionário, padrão para 1 caso não exista
            
            try:
                with sqlite3.connect('projeto1.db') as conexao:
                    conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                    cursor = conexao.cursor()
                    cursor.execute(f"SELECT preco FROM {tipo} WHERE nome = ?", (nome,))
                    prato = cursor.fetchone()
            
            except sqlite3.Error as err:
                print(f"Erro ao acessar o banco de dados: {err}")

            preco_unitario = prato['preco'] if prato else 0
            preco_item = preco_unitario * quantidade
            total += preco_item

            frame_item = ttk.Frame(frame_interno)
            frame_item.pack(fill='x', padx=20, pady=10)

            ttk.Label(frame_item, text=f"{nome} (x{quantidade})", font=("Segoe UI", 11, "bold"), foreground="#F47070").pack(side='left')
            ttk.Label(frame_item, text=f"R$ {preco_item:.2f}", font=("Segoe UI", 10), foreground="#F47070").pack(side='right')

            if adicionados:
                ttk.Label(frame_interno, text=f"Adicionados: {adicionados}", font=("Segoe UI", 9), foreground="green").pack(anchor='w', padx=25)
            if removidos:
                ttk.Label(frame_interno, text=f"Removidos: {removidos}", font=("Segoe UI", 9), foreground="red").pack(anchor='w', padx=25)

        ttk.Label(frame_interno, text=f"Total do Pedido: R$ {total:.2f}", font=("Segoe UI", 12, "bold"), foreground="#F47070").pack(pady=20)

        # Espera o fechamento do popup
        self.root.wait_window(popup)

    def perfil_tela_meus_pedidos(self, popup):
        popup.title("Meus Pedidos")
        popup.geometry("700x700")
        popup.resizable(False, False)

        def ao_fechar():
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", ao_fechar)

        # Frame com Canvas (sem Scrollbar)
        frame_scroll = ttk.Frame(popup)
        frame_scroll.pack(fill='both', expand=True)

        def on_mousewheel(event):
            if canvas.yview()[0] <= 0 and event.delta > 0:
                return
            if canvas.yview()[1] >= 1 and event.delta < 0:
                return
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Criação do Canvas
        canvas = tk.Canvas(frame_scroll, borderwidth=0)
        canvas.pack(side='left', fill='both', expand=True)

        canvas.focus_set()

        # Adiciona a Scrollbar visível
        scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno dentro do Canvas
        frame_interno = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=frame_interno, anchor='nw')

        # Atualiza scrollregion e largura
        def atualizar_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        frame_interno.bind("<Configure>", atualizar_scroll)
        canvas.bind("<Configure>", atualizar_scroll)

        # Scroll com mouse em qualquer lugar do popup
        def ativar_scroll_mouse():
            def mousewheel_global(event):
                if canvas.yview()[0] <= 0 and event.delta > 0:
                    return
                if canvas.yview()[1] >= 1 and event.delta < 0:
                    return
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            popup.bind_all("<MouseWheel>", mousewheel_global)

            def remover_scroll_mouse():
                popup.unbind_all("<MouseWheel>")

            # Remove bind quando o popup for fechado
            popup.protocol("WM_DELETE_WINDOW", lambda: [remover_scroll_mouse(), popup.destroy()])

        ativar_scroll_mouse()

        # Título da tela
        titulo_label = ttk.Label(frame_interno, text="Meus Pedidos", font=("Segoe UI", 20, "bold"), foreground="#F47070", 
                                 anchor="center", justify="center")
        titulo_label.pack(pady=(20, 10), fill='x')

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                cursor = conexao.cursor()
                # Primeiro, buscamos o id_usuario com base no nome de usuário
                cursor.execute("SELECT id_usuario FROM usuarios WHERE nome = ?", (self.nome_usuario,))
                resultado = cursor.fetchone()

        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")

        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
                cursor = conexao.cursor()

                if resultado:
                    id_usuario = resultado['id_usuario']

                    # Agora usamos o id_usuario para buscar os pedidos
                    cursor.execute("""SELECT P.id_pedido, P.preco_total, COUNT(I.id_item) AS quantidade_total
                        FROM pedidos P JOIN itens_pedido I ON P.id_pedido = I.id_pedido
                        WHERE P.id_usuario = ?
                        GROUP BY P.id_pedido, P.preco_total
                        ORDER BY P.id_pedido
                    """, (id_usuario,))

                    pedidos_db = cursor.fetchall()

        except sqlite3.Error as err:
            print(f"Erro ao acessar o banco de dados: {err}")

        if pedidos_db:
            for pedido in pedidos_db:
                id_pedido = pedido['id_pedido']
                total = pedido['preco_total'] or 0
                quantidade = pedido['quantidade_total'] or 0

                # Criar card do pedido
                card = ttk.Frame(frame_interno, padding=15, relief="raised", borderwidth=2)
                card.pack(fill='x', padx=10, pady=10)

                info_frame = ttk.Frame(card)
                info_frame.pack(side='left', expand=True, fill='both')

                style = ttk.Style()
                style.configure("Pedido.TLabel", font=("Segoe UI", 12, "bold"), foreground="#F47070")
                style.configure("Info.TLabel", font=("Segoe UI", 10), foreground="#F47070")
                style.configure("Total.TLabel", font=("Segoe UI", 10, "bold"), foreground="#F47070")
                style.configure("Custom.TButton", background="#F47070", foreground="#ffffff", font=("Segoe UI", 10, "bold"), padding=6,
                                borderwidth=0,focusthickness=3,focuscolor='none')

                style.map("Custom.TButton", background=[("active", "#d95c5c")], foreground=[("active", "#ffffff")])

                ttk.Label(info_frame, text=f"Pedido Nº {id_pedido}", style="Pedido.TLabel").pack(anchor='w')
                ttk.Label(info_frame, text=f"Quantidade: {quantidade}", style="Info.TLabel").pack(anchor='w')
                ttk.Label(info_frame, text=f"Total: R$ {total:.2f}", style="Total.TLabel").pack(anchor='w')

                ver_detalhes = ttk.Button(card, text="Ver Detalhes", width=15, style="Custom.TButton", command=lambda p=id_pedido: self.perfil_abrir_detalhes_pedido(p))
                ver_detalhes.pack(side='right', padx=10, pady=10)
                ver_detalhes.config(cursor="hand2")

        else:
            ttk.Label(frame_interno, text="Nenhum pedido encontrado.", foreground='#F47070', font=("Segoe UI", 12)).pack(pady=20)

        # Força rolagem para o topo após construção do layout
        popup.after_idle(lambda: canvas.yview_moveto(0))

    def perfil_tela_dar_feedbacks(self, popup, largura_popup, altura_popup):
            popup.title("Feedback")
            # Caminho da imagem de fundo (altere para o seu caminho correto)
            caminho_imagem = os.path.join(self.caminho_base_padrao, "Tela Feedback.png")
            imagem_fundo = ImageTk.PhotoImage(Image.open(caminho_imagem).resize((largura_popup, altura_popup)))

            # Label com a imagem de fundo preenchendo a janela toda
            label_bg = tk.Label(popup, image=imagem_fundo)
            label_bg.image = imagem_fundo  # Mantém a referência
            label_bg.place(relwidth=1, relheight=1)

            botao_enviar = tk.Button(popup, image=enviar, borderwidth=0, highlightthickness=0,
                    background='#ffffff', activebackground='#ffffff',
                    command=lambda: self.perfil_salvar_feedback(nome_usuario_feedback.get(), email_usuario_feedback.get(), mensagem_usuario_feedback.get("1.0", "end-1c"), popup))
            botao_enviar.place(relx=0.49, rely=0.69, anchor="center", width=119, height=35)
            botao_enviar.config(cursor="hand2")

            # Método para colocar placeholder em campos de texto caso necessário
            def criar_entry_com_placeholder(frame, placeholder_text, largura=40, justificar='center'):
                entry = ttk.Entry(frame, font=("Montserrat", 14), width=largura, justify=justificar)

                # Verifica se é para tratar como placeholder
                if placeholder_text in ("", "Alergenico.."):
                    entry.insert(0, "Alergenico..")
                    entry.config(foreground='grey')
                    entry.placeholder_ativo = True
                else:
                    entry.insert(0, placeholder_text)
                    entry.config(foreground='black')
                    entry.placeholder_ativo = False

                def on_focus_in(event):
                    if entry.placeholder_ativo:
                        entry.delete(0, tk.END)
                        entry.config(foreground='black')
                        entry.placeholder_ativo = False

                def on_key_release(event):
                    if entry.get() == "" and entry.placeholder_ativo:
                        entry.config(foreground='black')
                        entry.placeholder_ativo = False

                entry.bind("<FocusIn>", on_focus_in)
                entry.bind("<KeyRelease>", on_key_release)

                return entry


            nome_usuario_feedback = criar_entry_com_placeholder(popup, placeholder_text=self.nome_usuario, largura=18, justificar='center')
            email_usuario_feedback = criar_entry_com_placeholder(popup, placeholder_text=self.email_usuario, largura=18, justificar='center')

            nome_usuario_feedback.place(relx=0.242, rely=0.315, relheight=0.065)
            nome_usuario_feedback.config(font=("Montserrat", 12))

            email_usuario_feedback.place(relx=0.50, rely=0.315, relheight=0.065)
            email_usuario_feedback.config(font=("Montserrat", 12))

            # Precisa ser um text porque o entry só funciona bem para uma única linha
            mensagem_usuario_feedback = tk.Text(popup, height=8, width=38, font=("Montserrat", 12))
            mensagem_usuario_feedback.place(relx=0.242, rely=0.4)
            mensagem_usuario_feedback.insert("1.0", 'Informe sua mensagem de feedback..')
            mensagem_usuario_feedback.config(foreground='grey')

            def on_focus_in(event):
                if mensagem_usuario_feedback.get("1.0", "end-1c") == 'Informe sua mensagem de feedback..':
                    mensagem_usuario_feedback.delete("1.0", "end")
                    mensagem_usuario_feedback.config(foreground="black")

            def on_focus_out(event):
                if mensagem_usuario_feedback.get("1.0", "end-1c").strip() == "":
                    mensagem_usuario_feedback.insert("1.0", 'Informe sua mensagem de feedback..')
                    mensagem_usuario_feedback.config(foreground="grey")

            # Liga os eventos de foco
            mensagem_usuario_feedback.bind("<FocusIn>", on_focus_in)
            mensagem_usuario_feedback.bind("<FocusOut>", on_focus_out)
        
    def perfil_editar_alergias(self, popup, largura_popup, altura_popup):
        popup.title("Alterar Alergias")
        
        # Caminho da imagem de fundo
        caminho_imagem = os.path.join(self.caminho_base_padrao, "Tela Alterar Alergias.png")
        imagem_fundo = ImageTk.PhotoImage(Image.open(caminho_imagem).resize((largura_popup, altura_popup)))

        # Criação do container principal
        container_frame = ttk.Frame(popup)
        container_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        # Label com a imagem de fundo
        label_bg = tk.Label(container_frame, image=imagem_fundo)
        label_bg.image = imagem_fundo  # Mantém a referência
        label_bg.place(relwidth=1, relheight=1)

        # Canvas para rolagem
        scroll_frame = ttk.Frame(container_frame)
        scroll_frame.place(relx=0.5, rely=0.2, relwidth=0.85, relheight=0.65, anchor="n")  # Ajuste no eixo Y

        canvas = tk.Canvas(scroll_frame, bg="#FFFFFF", highlightthickness=0)

        # Empacota o canvas
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame = ttk.Frame(canvas)

        def ajustar_largura(e):
            canvas.itemconfig("frame", width=e.width)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="frame")
        canvas.bind("<Configure>", ajustar_largura)

        # Configuração para ajustar o tamanho do scrollable_frame dinamicamente
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        def ativar_scroll_popup_editar_alergias():
            def mousewheel_global(event):
                if not canvas.winfo_exists():
                    return
                if canvas.yview()[0] <= 0 and event.delta > 0:
                    return
                if canvas.yview()[1] >= 1 and event.delta < 0:
                    return
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            popup.bind_all("<MouseWheel>", mousewheel_global)

            def remover_scroll():
                popup.unbind_all("<MouseWheel>")

            popup.protocol("WM_DELETE_WINDOW", lambda: [remover_scroll(), popup.destroy()])

        ativar_scroll_popup_editar_alergias()

        # Carrega as opções de alergenicos do banco
        try:
            with sqlite3.connect('projeto1.db') as conexao:
                cursor = conexao.cursor()
                cursor.execute("SELECT nome FROM alergenicos ORDER BY nome ASC")
                resultados = cursor.fetchall()
                self.opcoes_alergenicos = [row[0] for row in resultados]
        except sqlite3.Error as err:
            print(f"Erro ao carregar alergenicos: {err}")
            self.opcoes_alergenicos = ["Alergênico não definido"]

        # Função para criar um card novo
        def adicionar_card(alergia_text="Alergênico não definido"):
            card = ttk.Frame(scrollable_frame, padding=10, relief="raised", borderwidth=2)
            card.pack(fill="x", padx=20, pady=10)

            titulo = ttk.Label(card, text=f"Alergia {len(self.alergia_entries) + 1}", font=("Segoe UI", 12, "bold"), foreground="#F47070")
            titulo.pack(anchor="w", padx=10, pady=5)

            combobox = ttk.Combobox(card, values=self.opcoes_alergenicos, state="readonly", font=("Montserrat", 12), justify='center')
            combobox.set(alergia_text if alergia_text in self.opcoes_alergenicos else self.opcoes_alergenicos[0])
            combobox.pack(fill="x", padx=10, pady=5)

            self.alergia_entries.append({
                "frame": card,
                "combobox": combobox
            })

        # Função para remover o último card
        def remover_card():
            if self.alergia_entries:
                ultimo = self.alergia_entries.pop()
                ultimo["frame"].destroy()

        # Botão Alterar
        botao_alterar = tk.Button(
            container_frame, image=alterar, borderwidth=0, highlightthickness=0,
            background='#ffffff', activebackground='#ffffff',
            command=lambda: self.perfil_atualizar_alergias(popup)
        )
        botao_alterar.place(relx=0.5, rely=0.96, anchor="center", width=148, height=50)
        botao_alterar.config(cursor="hand2")
        

        # Botão -
        botao_remover = tk.Button(
            container_frame, image=minus, borderwidth=0, highlightthickness=0, background='#ffffff', activebackground='#ffffff', command=remover_card)
        botao_remover.place(relx=0.3, rely=0.96, anchor="center")
        botao_remover.config(cursor="hand2")

        # Botão +
        botao_adicionar = tk.Button(container_frame, image=plus, borderwidth=0, highlightthickness=0,
            background='#ffffff', activebackground='#ffffff', command=lambda: adicionar_card())
        botao_adicionar.place(relx=0.7, rely=0.96, anchor="center")
        botao_adicionar.config(cursor="hand2")

        # Botão para salvar alterações
        botao_alterar = tk.Button(container_frame, image=alterar, borderwidth=0, highlightthickness=0,
            background='#ffffff', activebackground='#ffffff', command=lambda: self.perfil_atualizar_alergias(popup)
        )
        botao_alterar.place(relx=0.5, rely=0.96, anchor="center", width=148, height=50)
        botao_alterar.config(cursor="hand2")

        # Lista para armazenar os widgets Entry
        self.alergia_entries = []

       # Carregar as alergias atuais do usuário
        try:
            with sqlite3.connect('projeto1.db') as conexao:
                conexao.row_factory = sqlite3.Row
                cursor = conexao.cursor()

                cursor.execute("SELECT id_usuario FROM usuarios WHERE nome = ?", (self.nome_usuario,))
                resultado_usuario = cursor.fetchone()

                if not resultado_usuario:
                    raise Exception("Usuário não encontrado.")

                id_usuario = resultado_usuario["id_usuario"]

                cursor.execute("""SELECT a.nome FROM alergenicos a
                    JOIN usuarios_alergenicos ua ON a.id_alergenico = ua.id_alergenico
                    WHERE ua.id_usuario = ?
                    ORDER BY a.nome ASC
                """, (id_usuario,))
                resultados = cursor.fetchall()

                alergias_atuais = [row["nome"] for row in resultados] if resultados else []

        except sqlite3.Error as err:
            print(f"Erro ao carregar alergias do usuário: {err}")
            alergias_atuais = []

        # Criação dos cards baseados nas alergias atuais do usuário
        for alergia in alergias_atuais:
            adicionar_card(alergia)

        # Desvincula o evento de rolagem ao fechar o popup
        def on_close():
            canvas.unbind_all("<MouseWheel>")
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

    def perfil_abrir_popup(self, nome_botao_pagina):
        largura_popup = 700
        altura_popup = 700

        # Obtem tamanho da tela
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()

        # Calcula posição central
        x = (largura_tela // 2) - (largura_popup // 2)
        y = (altura_tela // 2) - (altura_popup // 2)

        popup = tk.Toplevel(self.root)
        popup.geometry(f"{largura_popup}x{altura_popup}+{x}+{y}")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
   
        if nome_botao_pagina == 'Meus Pedidos':
            self.perfil_tela_meus_pedidos(popup)

        elif nome_botao_pagina == 'Ver Feedback':
            self.perfil_tela_meus_feedbacks(popup)

        elif nome_botao_pagina == 'Feedback':
            self.perfil_tela_dar_feedbacks(popup, largura_popup, altura_popup)
        
        elif nome_botao_pagina == 'Editar Alergias':
            self.perfil_editar_alergias(popup, largura_popup, altura_popup)

    def perfil_alterar_botoes(self, nome_botao_pagina):
        if nome_botao_pagina not in ('Inicio', 'Carrinho', 'Perfil'):
            self.perfil_abrir_popup(nome_botao_pagina)
        elif nome_botao_pagina == 'Inicio':
            self.mostrar_frame('tela_inicio')
        elif nome_botao_pagina == 'Carrinho':
            self.mostrar_frame('tela_carrinho')
        else:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    style = Style(theme='cerculean')
    root.title('Menu Analyzer')
    root.geometry('900x850')
    root.resizable(False, False)

    # Obtém o diretório do script atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_imagens = os.path.join(diretorio_atual, "Imagens do Projeto")

    # Imagens do Projeto
    seta = PhotoImage(file=os.path.join(caminho_imagens, "seta1.png"))
    back = PhotoImage(file=os.path.join(caminho_imagens, "back.png"))
    enviar = PhotoImage(file=os.path.join(caminho_imagens, "enviar.png"))
    buscar = PhotoImage(file=os.path.join(caminho_imagens, "buscar.png"))
    alterar = PhotoImage(file=os.path.join(caminho_imagens, "alterar.png"))
    plus = PhotoImage(file=os.path.join(caminho_imagens, "+.png"))
    minus = PhotoImage(file=os.path.join(caminho_imagens, "-.png"))
    plus2 = PhotoImage(file=os.path.join(caminho_imagens, "+ 2.png"))
    minus2 = PhotoImage(file=os.path.join(caminho_imagens, "- 2.png"))
    plus3 = PhotoImage(file=os.path.join(caminho_imagens, "+ 3.png"))
    minus3 = PhotoImage(file=os.path.join(caminho_imagens, "- 3.png"))
    adicionar = PhotoImage(file=os.path.join(caminho_imagens, "adicionar.png"))
    descricao = PhotoImage(file=os.path.join(caminho_imagens, "descricao.png"))
    historia = PhotoImage(file=os.path.join(caminho_imagens, "historia.png"))
    finalizar_compra = PhotoImage(file=os.path.join(caminho_imagens, "finalizar.png"))
    adicionar_items = PhotoImage(file=os.path.join(caminho_imagens, "adicionar_items.png"))
    lixeira = PhotoImage(file=os.path.join(caminho_imagens, "lixeira.png"))
    buscar_feedbacks = PhotoImage(file=os.path.join(caminho_imagens, "buscar_feedbacks.png"))

    centralizar_janela(root)

    app = App(root)
    root.mainloop()