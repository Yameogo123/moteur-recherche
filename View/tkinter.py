from tkinter import *
from tkinter.messagebox import askokcancel
from Model.Menu import Menu
from Model.Corpus import Corpus
import json
import pickle
from random import randint
from datetime import datetime
from Controller.controller import *

#from matplotlib.figure import Figure
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#load questions
quest=json.loads(open('file/questions.json', encoding="utf-8").read())["questions"][:]
#load answers
ans=json.loads(open('file/answers.json', encoding="utf-8").read())["answers"]
#convert into lists
questions={i:list(q.values())[0] for i,q in enumerate(quest)}
answers={j:list(q.values())[0] for j,q in enumerate(ans)}
#load id2doc
with open('file/doc.pkl', 'rb') as t:
    id2doc = pickle.load(t)
    t.close()
#load id2aut
with open('file/aut.pkl', 'rb') as f: 
    id2aut = pickle.load(f)
    f.close()
 

def View():
    LARGEUR = 1100
    HAUTEUR = 530
    #window
    fenetre= Tk()
    fenetre.geometry("1200x600")
    fenetre.title("search Engine AYMAX")
    fenetre.resizable(width=TRUE, height=TRUE)
    #canvas
    canvas = Canvas(fenetre, width = LARGEUR, height = HAUTEUR, bg = 'white')
    canvas.pack(padx =5, pady =5)
    #initialise corpus
    corpus= Corpus("test", id2aut, id2doc, len(id2doc), len(id2aut))
    
    #fonction pour fermer la fenètre.
    def quitter():
        res = askokcancel("Quit the application", "Are you sure ?")
        if res:
            fenetre.quit()
            fenetre.destroy()
    #fonction qui retourne les input et output  
    def saisie():
        name=champ.get("1.0", 'end-1c').strip()
        champ.delete("0.0", END)
        if name != '':
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + name + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 12))
            menu= Menu(questions, answers, name)
            i=menu.score()
            j= corpus.score(name)
            do= corpus.getDocByTitle(name)
            if len(do)==0:
                if i==5 or i==4:
                    res= f"\n3 top documents result : \n\n"
                    for k in j[::-1]:
                        doc= id2doc[k]
                        texte= doc.getText()
                        auteurs= doc.getAuteur()
                        titre= doc.getTitre()
                        date= doc.getDate()
                        res+= "title: "+ titre+ "\nauthor(s): "+ auteurs+ "\ndate: "+ date +\
                            "\ncontent: "+texte[:200]+ "... \n ------------- \n"
                    stat= statistic(name, id2doc, id2aut)
                    if stat ==-1:
                        if len(j)==0:
                            res=menu.response(2)
                            '''fig= Figure(figsize= (3,3), dpi=100)
                            y= [i**2 for i in range(101)]
                            plot= fig.add_subplot(111)
                            plot.plot(y)
                            ca= FigureCanvasTkAgg(fig, master= ChatLog)
                            ca.draw()
                            ca.get_tk_widget().pack()'''
                    else:
                        res= stat
                else:
                    if i==0:
                        greetings= menu.response(i).split(",")
                        res= greetings[randint(0,len(greetings)-1)]
                    elif i==1:
                        res= menu.response(i)
                    elif i==2:
                        res= "the current time is "+ str(datetime.now())
                    elif i==3:
                        res= "\nthe corpus authors List: \n " + allAuteur(id2aut)
                    elif i==6:
                        res= corpus.stats()
                    else:
                        res="the id index is "+str(i)
            else:
                doc= do[0]
                texte= doc.getText()
                auteurs= doc.getAuteur()
                titre= doc.getTitre()
                date= doc.getDate()
                res= "\ntitle: "+ titre+ "\nauthor(s): "+ auteurs+ "\ndate: "+ date +\
                    "\ncontent: "+texte +"\n"
            #chat log to insert bot answer
            ChatLog.insert(END, "Bot: " + res + '\n\n')
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)
    
    # input field
    champ = Text(fenetre, bd=0, bg="white", width="100", height="10", font="Arial")
    champ.place(x=50, y=545, height=30, width=400)
    #Create Chat window
    ChatLog = Text(canvas, bd=0, bg="white", height="530", width="800", font="Arial", wrap=WORD)
    ChatLog.config(state=DISABLED)
    
    #Bind scrollbar to Chat window
    scrollbar = Scrollbar(canvas, command=ChatLog.yview, cursor="heart")
    ChatLog['yscrollcommand'] = scrollbar.set
    scrollbar.place(x=1080, y=6, height=500)
    ChatLog.place(x=15, y=8, height=HAUTEUR, width=LARGEUR)
    # search button
    recherche = Button(fenetre, text="Search", command=saisie, bd=0, bg="#32de97", activebackground="#3c9d9b", fg='black')
    recherche.place(x = 700 , y = 550 , width = 150)
    # Quit button
    quitte = Button(fenetre, text = 'Quit', bd=0, bg="red", activebackground="#3c9d9b", fg='black',command = quitter)
    quitte.place(x = 900 , y = 550 , width = 150)
    # launch all
    fenetre.mainloop()
    
