from modules.Model.database import *
from modules.Model.vcf import *


class PhoneBookModel:
    def __init__(self, logger):
        self.logger = logger.setupLogger("error", "error.log", level=logger.ERROR)
        self.db = DataBase()
        self.vcf = VCF()



    def get_all_contacts(self):
        return self.db.getAllContacts()

    def add_contact(self, nome, number):
        self.db.addContact(nome, number)

    def find_contact(self, search):
        return self.db.findContact(search)

    def close_database(self):
        self.db.close()
