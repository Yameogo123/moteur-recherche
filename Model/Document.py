

class Document:
    
    def __init__(self, titre, auteur, date, url, texte):
        self._titre= titre
        self._auteur= auteur
        self._date= date
        self._url= url
        self._texte= texte
        self._type=""
        
    #getters
    def getTitre(self):
        return self._titre
    def getAuteur(self):
        return self._auteur
    def getDate(self):
        return self._date
    def getUrl(self):
        return self._url
    def getText(self):
        return self._texte
    def getType(self):
        return self._type
    
    #setters
    def setTitre(self, titre):
        self._titre= titre
    def setAuteur(self, auteur):
        self._auteur= auteur
    def setDate(self, date):
        self._date= date
    def setUrl(self, url):
        self._url= url
    def setText(self, texte):
        self._texte= texte
    def setType(self, typ):
        self._type= typ
        
    def __str__(self):
        return self.getTitre()
    
    