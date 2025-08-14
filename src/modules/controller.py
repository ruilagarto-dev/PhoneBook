# modules/controller.py
class PhoneBookController:
    def __init__(self, logger, view, model):
        self.logger = logger
        self.view = view
        self.model = model

        self.view.setController(self)
        self.show_all_contacts()

    def show_all_contacts(self):
        contacts = self.model.get_all_contacts()
        # Aqui você envia para a view, sem se preocupar com o DB
        self.view.display_contacts(contacts)

    def search_contact(self, search_term):
        results = self.model.find_contact(search_term)
        self.view.display_contacts(results)

    def add_new_contact(self, nome,  number):
        self.model.add_contact(nome,  number)

    # controller.py
    def load_vcf(self, filepath):
        try:
            content = self.model.vcf.read(filepath)  # lê texto
            contacts = self.model.vcf.parse(content)  # converte em lista de tuplas

            for nome, number in contacts:
                self.model.add_contact(nome,  number)

            self.show_all_contacts()

        except Exception as e:
            print(f"Erro ao carregar VCF: {e}")
