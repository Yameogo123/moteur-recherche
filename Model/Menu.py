import string 
from nltk.stem.snowball import SnowballStemmer
#from nltk.corpus import stopwords
import re
import numpy as np
from math import log


class Menu: 
    
    def __init__(self, questions={}, answers={}, recherche=""):
        self._quest=questions
        self._ans= answers
        self.recherche=recherche
        self.all_words= self._nettoyer(" ".join(list(set(questions.values()))))
        self._ndoc= len(questions)
        
    def _nettoyer(self, text):
        ponctuation= string.punctuation
        compiler=re.compile("[%s]" % re.escape(ponctuation))
        text= compiler.sub(" ", text)
        text= text.replace("\n", " ").replace("\t", " ")
        #st= stopwords.words("english")
        texte= text.lower()
        token= texte.split()
        token= list(set([tk for tk in token if tk.isalpha() and len(tk)>1]))
        #token= [tk for tk in token if tk not in st]
        #Pour raciniser les mots
        stemmer=SnowballStemmer("english")
        token=[stemmer.stem(mot) for mot in token]
        return token
    
    def vocabulary(self):
        voc={k: self._nettoyer(v) for k,v in self._quest.items()}
        return voc
    
    #matrice methode BOW
    def matDocMot(self, mots):
        voc= self.vocabulary()
        n=len(voc)
        m= len(mots)
        mat= np.zeros((n, m))
        for i in range(n):
            doc=voc[i]
            for j in range(m):
                mat[i][j]= doc.count(mots[j])
        return mat
    
    #methode tfidf
    def _tf(self, doc, mot):
        n= doc.count(mot)
        N= len(doc)
        if N==0:
            return 0
        return n/N
    def _idf(self, mot, voc):
        n=0
        for v in voc.values():
            if v.count(mot)>0:
                n+=1
        if n==0:
            return 0
        return log(self._ndoc/n)
    def _matTfIdf(self, mots):
        voc= self.vocabulary()
        n=len(voc)
        m= len(mots)
        mat= np.zeros((n, m))
        for i in range(n):
            doc=voc[i]
            for j in range(m):
                mot=mots[j]
                mat[i][j]= self._tf(doc, mot)*self._idf(mot, voc)
        return mat
    
    #score with tf idf
    def score(self):
        mots= self.all_words
        p= self._nettoyer(self.recherche)
        mat=self._matTfIdf(mots)
        entrer=np.array([p.count(m) for m in mots])
        result= mat@entrer
        if sum(result)==0:
            return 5
        return np.argmax(result)
    
    def response(self, i):
        return self._ans[i]
        
        
    
    
    
    
    
    
    
    
    
    
    
    