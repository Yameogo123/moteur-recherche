from Model.Document import Document


class RedditDocument(Document):
    
    def __init__(self, titre, auteur, date, url, texte):
        Document.__init__(self, titre, auteur, date, url, texte)
        self.setType("Reddit")
        
    def __str__(self):
        return self.getType,": ",self.getTitre()
    
    