import pandas as pd
import numpy as np
import re
import string
from math import log
from nltk.stem.snowball import SnowballStemmer

class Corpus:
        
    def __init__(self, nom="", authors={}, id2doc={}, ndoc=0, naut=0):
        self._nom=nom
        self._authors= authors
        self._id2doc=id2doc
        self._ndoc=ndoc
        self._naut=naut
        self._all=" ".join([v.getText() for v in id2doc.values()])
        self._mots= list(self.occurence().keys())
        #self._mattfidf= self.mat_TFIDF()
        self._matdoc= self.matDocMot()
        
        
    #getters
    def getNom(self):
        return self._nom
    def getAuthors(self):
        return self._authors
    def getId2doc(self):
        return self._id2doc
    def getNdoc(self):
        return self._ndoc
    def getNaut(self):
        return self._naut
    
    #setters
    def setNom(self, nom):
        self._nom=nom
    def addAuthor(self, aut):
        n=aut.getName()
        if n not in self._authors.keys():
            self._authors[n]=aut
            self._naut+=1
    def addDocument(self, doc):
        if doc not in self._id2doc.values():
            self._id2doc[self._ndoc]= doc
            self._ndoc+=1
            
    #others methodes
    #filter documents by date
    def docByDate(self, n=3):
        doc=self._id2doc.values()
        doc= sorted([x for x in doc], key=lambda x: x.getDate())[:n]
        return doc 
    
    def getDocByTitle(self, title): 
        do= [self._id2doc[i] for i in range(self._ndoc) if self._id2doc[i].getTitre()==title]
        return do
    
    #permet de sauvegarder le corpus courant
    def save(self):
        dico={"documents": [], "auteurs": [] }
        for doc in self._id2doc.values():
            dico["documents"].append(doc)
            dico["auteurs"].append(self._authors[doc.getAuteur()])
        df=pd.DataFrame.from_dict(dico)
        df.to_csv("{}.csv".format(self._nom))
    
    #permet de recuperer un corpus sauvegarder
    def load(self, titre="test.csv"):
        df= pd.read_csv(titre)
        self.setNom(titre[:-4])
        df["documents"].apply(self.addDocument)
        df["auteurs"].apply(self.addAuthor)
        
    def __repr__(self):
        return "nom du corpus: {}, son nombre de document: {}, le nombre d'auteurs: {}"\
            .format(self._nom, self._ndoc, self._naut)
    
    #permet de rechercher un mot dans le corpus
    def search(self, mot):
        compiler= re.compile(r'\b{}\b'.format(str(mot)), re.IGNORECASE)
        iteration= compiler.finditer(self._all)
        result=[]
        for i in iteration:
            sp=i.span()
            result.append(self._all[sp[0]-20: sp[1]+20])
        return result
    
    #reprend la fonction search en retournant un dataframe
    def concorde(self, mot):
        liste= self.search(mot)
        dic={"contexte gauche":[], "motif trouvé":[], "contexte droit":[]}
        for el in liste:
            dic["contexte gauche"].append("..."+el[:20])
            dic["motif trouvé"].append(el[20:-20])
            dic["contexte droit"].append(el[-20:]+"...")
        df= pd.DataFrame.from_dict(dic)
        return df
    
    #nettoyer un texte passé en paramètre
    def nettoyer_texte(self, texte):
        compiler= re.compile("[%s]"%re.escape(string.punctuation))
        #mettre tout sur la même ligne et mettre en minuscule
        texte= texte.lower().replace("\n", " ")
        #enlever les ponctuations su texte
        texte= compiler.sub(" ", texte)
        #retirer les espacements inutile
        texte.replace("\t", " ")
        token=[t for t in texte.split() if t.isalpha()]
        #raciniser les mots
        stemmer=SnowballStemmer("english")
        token=[stemmer.stem(mot) for mot in token]
        texte=" ".join(token)
        return texte
    
    #permet de retourner le vocabulaire de chaque document
    def vocabulary(self):
        voc={k: list(set(self.nettoyer_texte(v.getText()).split())) for k,v in self._id2doc.items()}
        return voc
    
    #occurence des mots dans le corpu entier
    def occurence(self):
        tout=self.nettoyer_texte(self._all).split()
        voc= list(set(tout))
        occ= {mot: tout.count(mot) for mot in voc}
        return occ
        
    #donne des stats à propos des docs
    def stats(self):
        nred=0
        narx= self._ndoc
        words1=0
        words2=len(self._all)
        for i in range(self._ndoc):
            doc=self._id2doc[i]
            text=doc.getText()
            if doc.getType()=="Reddit":
                nred +=1
                words1 += len(text.split())
                narx-=1
                words2-=words1
        res= f"\nLes documents de type reddit sont {nred} et ont en moyenne {words1} mots " \
            +f"\nLes documents de type arxiv sont {narx} et ont en moyenne {words2} mots "
        return res
        
    
    #matrice document mot
    def matDocMot(self):
        mots=self._mots
        n=len(self._id2doc)
        m=len(mots)
        voc=self.vocabulary()
        mat= np.zeros((n, m))
        for l in range(n):
            document= voc[l]
            for i, c in enumerate(mots):
                mat[l,i]= document.count(c)
        return mat
    
    #expension de la fonction vocabulary
    def occurenceMot(self):
        mat= self._matdoc
        result=[]
        for i in range(len(mat)):
            nbDoc=0
            nbTot=0
            mot= self._mots[i]
            for x in mat[:,i]:
                if x!=0:
                    nbDoc+=1
                nbTot+=x
            result.append([mot, nbDoc, nbTot])
        return result
    
    #methode tfidf
    def _tf(self, i, mot, voc):
        doc= voc[i]
        nb= doc.count(mot)
        total= len(doc)
        if total==0:
            return 0
        return nb/total
    def _idf(self, mot, voc):
        D= len(voc)
        d=0
        for document in voc.values():
            if document.count(mot) > 0:
                d+=1
        return log(D/d)
    def mat_TFIDF(self):
        voc=self.vocabulary()
        n=self._ndoc
        mots=self._mots
        mat= np.zeros((n, len(mots)))
        for i in range(n):
            for j, c in enumerate(mots):
                mat[i][j]= self._tf(i, c, voc)*self._idf(c, voc)
        return mat
    
    #score obtenu avec la methode BOW
    def score(self, mots):
        #voc=self.vocabulary()
        mots= self.nettoyer_texte(mots).split()
        Q2=np.array([mots.count(m) for m in self._mots])
        if sum(Q2)==0:
            return []
        mat= self._matdoc
        #cosinus similarity
        result= mat@Q2
        result= result /(len(mat[0])*len(Q2))
        #id=np.argmax(result)
        arg=np.argsort(result)
        return arg[-3:]
    
    #score obtenu avec la méthodee BMI
    def scoreBMI(self, mots):
        voc=self.vocabulary()
        mots= self.nettoyer_texte(mots).split()
        scores=[self._score2(d, mots, voc) for d in voc.values()]
        if sum(scores)==0:
            return []
        arg=np.argsort(scores)
        return arg[:3]
    
    
    def _idf2(self, mot, voc):
        N= self._ndoc
        d=0
        for document in voc.values():
            if document.count(mot) > 0:
                d+=1
        return log((N-d+0.5)/(d+0.5))
    def _score2(self, d, Q, voc):
        s=0
        n_doc= len(d)
        m=len(self._mots)
        avgdl= m/self._ndoc
        b=0.75
        k1=1.6
        for q in Q:
            if n_doc==0:
                freq_q_in_d=0
            else:
                freq_q_in_d= d.count(q)/n_doc
            right_part= (freq_q_in_d*(k1+1))/(freq_q_in_d+k1*(1-b-b*self._ndoc/avgdl))
            s+=self._idf2(q, voc)*right_part
        return s
            
            
            
