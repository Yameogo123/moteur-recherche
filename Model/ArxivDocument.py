from Model.Document import Document


class ArxivDocument(Document):
    
    def __init__(self, titre, auteur, date, url, texte):
        super().__init__(titre, auteur, date, url, texte)
        self.setType("Arxiv")
    
    def __str__(self):
        return self.getType,": ",self.getTitre()