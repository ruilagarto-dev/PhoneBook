import os
import sqlite3
import re

class DataBase:
    def __init__(self, dbFolder="Data", dbName="phonebook.db"):
        # Cria a pasta caso não exista
        os.makedirs(dbFolder, exist_ok=True)
        self.dbPath = os.path.join(dbFolder, dbName)

        # Conecta ao banco (se não existir, SQLite cria automaticamente)
        self.conn = sqlite3.connect(self.dbPath)
        self.cursor = self.conn.cursor()

        # Garante que a tabela "contacts" exista
        self.createTable()

    def createTable(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            number TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def getAllContacts(self):
        try:
            self.cursor.execute("SELECT nome, number FROM contacts")
            return self.cursor.fetchall()
        except Exception as e:
            print("Erro ao buscar contatos:", e)
            return []

    def addContact(self, nome,  number):
        try:
            # Verifica se já existe contato com mesmo nome ou número
            
            if len(number) < 9:
                return False
            
            
            self.cursor.execute(
                "SELECT COUNT(*) FROM contacts WHERE LOWER(nome)=LOWER(?) OR number=?",
                (nome, number)
            )
            exists = self.cursor.fetchone()[0]

            if exists:
                print(f"Contato com nome '{nome}' ou número '{number}' já existe.")
                return False  # Retorna False para indicar que não adicionou

            # Caso não exista, insere o novo contato
            self.cursor.execute(
                "INSERT INTO contacts (nome,  number) VALUES (?,  ?)",
                (nome, number)
            )
            self.conn.commit()
            return True  # Retorna True para indicar sucesso

        except Exception as e:
            print("Erro ao adicionar contato:", e)
            return False



    def findContact(self, search=None):
        if not search:
            return []

        try:
            # detecta se é número (dígitos, espaços ou +)
            if re.fullmatch(r'[\d +]+', search):
                query = "SELECT nome,  number FROM contacts WHERE number LIKE ?"
                like_search = f"%{search}%"
                self.cursor.execute(query, (like_search,))
            else:
                query = "SELECT nome, number FROM contacts WHERE LOWER(nome) LIKE LOWER(?)"
                like_search = f"%{search}%"
                self.cursor.execute(query, (like_search,))

            return self.cursor.fetchall()
        except Exception as e:
            print("Erro ao buscar contato:", e)
            return []
        
    
    def removeContact(self, contact):
        pass



    def close(self):
        self.conn.close()
