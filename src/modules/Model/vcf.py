import quopri
import re

class VCF:
    def read(self, filePath):
        """Lê o ficheiro VCF e retorna o conteúdo."""
        try:
            with open(filePath, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print("❌ O ficheiro não foi encontrado.")
            return ""

    def parse(self, content):
        """Converte o conteúdo VCF numa lista de contactos (nome, numero)."""
        contatos = []
        bloco = []

        for linha in content.splitlines():
            linha = linha.strip()

            if linha.startswith("BEGIN:VCARD"):
                bloco = []

            elif linha.startswith("END:VCARD"):
                nome = ""
                telefone = ""

                for campo in bloco:
                    # Nome normal
                    if campo.startswith("FN:"):
                        nome = campo[3:]

                    # Nome codificado
                    elif campo.startswith("FN;CHARSET"):
                        encoded = campo.split(":", 1)[1]
                        nome = quopri.decodestring(encoded).decode("utf-8")

                    # Qualquer tipo de telefone
                    elif campo.startswith("TEL"):
                        telefone = campo.split(":", 1)[1]

                # Limpa espaços e hífens, mantém código do país se existir
                # numero_limpo = self.limpar_telefone(telefone)

                contatos.append((nome, telefone))

            else:
                bloco.append(linha)

        return contatos

    # def limpar_telefone(self, telefone):
    #     """Remove espaços e hífens, mantém código do país se houver."""
    #     return telefone.strip().replace(" ", "").replace("-", "")
