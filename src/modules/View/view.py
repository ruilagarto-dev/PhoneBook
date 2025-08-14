

from tkinter import *
from tkinter import ttk, filedialog, messagebox
from utils.colors import *

class PhoneBookView:
    def __init__(self, logger):
        self.logger = logger

        self.root = Tk()
        self.root.title("📒 PhoneBook")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        self.controller = None
        self.createWidgets()

    def setController(self, controller):
        self.controller = controller

    def createButton(self, parent, text, command=None, icon=None):
        display_text = f"{icon} {text}" if icon else text
        return Button(
            parent,
            text=display_text,
            command=command,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            font=("Helvetica", 11, "bold"),
            relief=FLAT,
            activebackground=BUTTON_ACTIVE_BG,
            activeforeground="white",
            cursor="hand2",
            bd=0,
            padx=15,
            pady=8
        )

    def createTableView(self, columns):
        frame = Frame(self.root, bg=BG_COLOR)
        frame.pack(padx=15, pady=15, fill=BOTH, expand=True)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=TREE_BG,
                        foreground="black",
                        rowheight=28,
                        fieldbackground=TREE_BG,
                        font=("Helvetica", 11))
        style.configure(
            "Treeview.Heading",
            font=("Helvetica", 12, "bold"),
            background=TREE_HEADING_BG,
            foreground=TREE_HEADING_FG
        )
        style.map('Treeview', background=[('selected', TREE_SELECTED_BG)])

        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.tag_configure('oddrow', background=TREE_ALT_BG)
        tree.tag_configure('evenrow', background=TREE_BG)

        for col, width in zip(columns, [250, 200]):
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=width, anchor=W)

        scrollbar = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        return tree

    def createWidgets(self):
        # Título
        self.labelTitle = Label(
            self.root, text="📞 PhoneBook", font=("Helvetica", 20, "bold"), bg=BG_COLOR
        )
        self.labelTitle.pack(pady=10)

        # Frame de pesquisa
        searchFrame = Frame(self.root, bg=BG_COLOR)
        searchFrame.pack(pady=5, padx=10, fill=X)

        self.searchEntry = Entry(searchFrame, font=("Helvetica", 12))
        self.searchEntry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))

        self.searchBtn = self.createButton(
            searchFrame,
            "Pesquisar",
            icon="🔍",
            command=self.on_search_clicked
        )
        self.searchBtn.pack(side=LEFT)
        self.searchEntry.bind("<Return>", lambda event: self.on_search_clicked())

        # Frame dos botões de ação
        btnFrame = Frame(self.root, bg=BG_COLOR)
        btnFrame.pack(pady=10)

        self.loadBtn = self.createButton(btnFrame, "Carregar VCF", command=self.on_load_vcf_clicked, icon="📂")
        self.loadBtn.grid(row=0, column=0, padx=20)

        self.refreshBtn = self.createButton(btnFrame, "Recarregar", command=lambda: self.controller.show_all_contacts(), icon="🔄")
        self.refreshBtn.grid(row=0, column=1, padx=20)

        self.exportBtn = self.createButton(btnFrame, "Exportar", command=self.on_export_clicked, icon="💾")
        self.exportBtn.grid(row=0, column=2, padx=20)

        for i in range(3):
            btnFrame.grid_columnconfigure(i, weight=1)

        # Tabela
        columns = ("nome", "numero")
        self.tree = self.createTableView(columns)

        # Binding duplo clique
        self.tree.bind("<Double-1>", self.on_double_click)

    # ----------------- Eventos -----------------
    def on_load_vcf_clicked(self):
        filepath = filedialog.askopenfilename(
            title="Selecione o arquivo VCF",
            filetypes=[("VCF files", "*.vcf"), ("Todos os arquivos", "*.*")]
        )
        if filepath and self.controller:
            self.controller.load_vcf(filepath)

    def on_search_clicked(self):
        search_term = self.searchEntry.get().strip()
        if self.controller:
            self.controller.search_contact(search_term)

    def on_export_clicked(self):
        if self.controller:
            filepath = filedialog.asksaveasfilename(
                title="Salvar contatos",
                defaultextension=".vcf",
                filetypes=[("VCF files", "*.vcf"), ("Todos os arquivos", "*.*")]
            )
            if filepath:
                self.controller.export_contacts(filepath)

    # ----------------- Duplo clique -----------------
    def on_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        contact = self.tree.item(selected_item[0], "values")
        nome, numero = contact
        self.open_edit_modal(nome, numero)

    # ----------------- Modal de edição -----------------
    def open_edit_modal(self, nome, numero):
        modal = Toplevel(self.root)
        modal.title("Editar Contato")
        modal.geometry("300x220")
        modal.resizable(False, False)
        modal.grab_set()  # Bloqueia a janela principal enquanto o modal estiver aberto

        Label(modal, text="Nome:").pack(pady=(20, 0))
        nome_entry = Entry(modal, font=("Helvetica", 12))
        nome_entry.pack(pady=5, fill=X, padx=20)
        nome_entry.insert(0, nome)

        Label(modal, text="Número:").pack(pady=(10, 0))
        numero_entry = Entry(modal, font=("Helvetica", 12))
        numero_entry.pack(pady=5, fill=X, padx=20)
        numero_entry.insert(0, numero)

        def save_changes():
            new_nome = nome_entry.get().strip()
            new_numero = numero_entry.get().strip()

            if len(new_numero.replace(" ", "").replace("+", "")) < 9:
                messagebox.showerror("Erro", "O número deve ter pelo menos 9 dígitos.")
                return

            if self.controller:
                self.controller.update_contact(nome, numero, new_nome, new_numero)
            modal.destroy()

        def delete_contact():
            if messagebox.askyesno("Confirmação", f"Deseja realmente excluir {nome}?"):
                if self.controller:
                    self.controller.remove_contact(nome, numero)
                modal.destroy()

        # Botões Salvar e Excluir
        btnFrame = Frame(modal)
        btnFrame.pack(pady=15)
        save_btn = Button(btnFrame, text="Salvar", command=save_changes, bg=BUTTON_BG, fg=BUTTON_FG, width=10)
        save_btn.pack(side=LEFT, padx=10)
        delete_btn = Button(btnFrame, text="Excluir", command=delete_contact, bg="red", fg="white", width=10)
        delete_btn.pack(side=LEFT, padx=10)

    # ----------------- Atualizar tabela -----------------
    def display_contacts(self, contacts):
        self.tree.delete(*self.tree.get_children())
        for i, contact in enumerate(contacts):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=contact, tags=(tag,))

    def start(self):
        self.root.mainloop()

