
from Model.RedditDocument import RedditDocument
from Model.ArxivDocument import ArxivDocument

class DocumentGenerator:
    
    @staticmethod
    def factory(type, titre, auteur, date, url, texte):
        if type == "Reddit": return RedditDocument(titre, auteur, date, url, texte)
        if type == "Arxiv": return ArxivDocument(titre, auteur, date, url, texte)
        
        assert 0, "erreur "+type
        
    
    