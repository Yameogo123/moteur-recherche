import praw
import xmltodict
import urllib.request as ur
from datetime import datetime
import pickle


from Model.DocumentGenerator import DocumentGenerator
from Model.Author import Author

def statistic(name, id2doc, id2aut):
    Lmot= [len(doc.getText().split(" ")) for doc in id2doc.values() if doc.getAuteur() == name]
    if len(Lmot) !=0:
        moy= sum(Lmot)/ len(Lmot)
    try:
        return f"\n Le nombre d'ouvrage écrit par {name}: "+ str(id2aut[name].getNdoc()) +"\n" \
        +" Nombre de mot moyen écrit est: "+ str(moy)
    except:
        return -1

def allAuteur(id2aut):
    auteurs= id2aut.keys()
    aut= "\n".join(auteurs)
    return aut
    

def refreshDoc(redditSubject='Coronavirus', arxivSubject='covid'):
    id2doc={}
    id2aut={}
    id=0
    #reddit
    reddit = praw.Reddit(client_id='PqiWHPjbGjiAkYAYCJbtiQ', 
        client_secret='ZyC2vijMHoj1itwZmz-vzr1DyBY2Cw', user_agent='td3', check_for_async=False)
    subr =  reddit.subreddit(redditSubject)
    for post in subr.hot(limit=100):
        titre = post.title
        titre = titre.replace("\n", " ")
        nom= str(post.author)
        date=datetime.fromtimestamp(post.created).strftime("%Y-%m-%d")
        d= DocumentGenerator.factory("Reddit", titre, post.author.name, date, post.url, post.selftext.replace("\n"," "))
        if nom not in id2aut.keys():
            auteur= Author(nom, 1, {0:d})
            id2aut[nom]=auteur
        else:
            id2aut[nom].addProd(d)
        id2doc[id]=d
        id+=1
    #Arxiv
    url = 'http://export.arxiv.org/api/query?search_query=all:' + arxivSubject + '&start=0&max_results=100'
    url_read = ur.urlopen(url).read()
    # url_read est un "byte stream" qui a besoin d'être décodé
    data =  url_read.decode()
    dico = xmltodict.parse(data) 
    docs = dico['feed']['entry']
    for d in docs:
        titre = d['title']
        titre = titre.replace("\n", " ")
        date=d["published"]
        authors= d["author"]
        try:
            auth = ", ".join([a["name"] for a in authors])  # On fait une liste d'auteurs, séparés par une virgule
        except:
            auth = authors["name"] 
        arxiv=DocumentGenerator.factory("Arxiv", titre, auth, date[:10], d["link"], d["summary"].replace("\n", " "))
        auteur= Author(auth, 1, {0:arxiv})
        if auth not in id2doc.keys():
            id2aut[auth]=auteur
        else:
            id2aut[auth].addProd(arxiv)
        id2doc[id]=arxiv
        id+=1
    with open("./file/doc.pkl", "wb") as t:
        pickle.dump(id2doc,t)
    t.close()
    with open("./file/aut.pkl", "wb") as f:
        pickle.dump(id2aut,f)
    f.close()
    
    
    
    
    
    
    
    
