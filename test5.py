from autotransv2 import *

#atoms

Enoun = Word("noun","English")
#with open("Enounroot.txt") as f:#
#    input = f.readlines()#
#Enoun.root = [x.strip() for x in input]


#still must distinguish between persons and things neuters
Enoun.root = ["cat","mouse","book","table","dog","sausage","milk"]
Enoun.irreg = {}
Enoun.irreg["mouse"] = ["number","plu","mice"]

for c in case:
   for g in gender:
    Enoun.morph[("sing",g,"3rd",c)] = ""
    Enoun.morph[("plu", g,"3rd",c)] = "s"

Epronoun = Word("pronoun","English")
Epronoun.root = [""]
for g in gender:
    Epronoun.morph[("sing",g,"1st","subj")] = "I"
    Epronoun.morph[("sing",g,"2nd","subj")] = "you"
    Epronoun.morph[("plu",g,"1st","subj")] = "we"
    Epronoun.morph[("plu",g,"2nd","subj")] = "you"
    Epronoun.morph[("plu",g,"2nd","subj")] = "they"
Epronoun.morph[("sing","masc","3rd","subj")] = "he"      
Epronoun.morph[("sing","fem","3rd","subj")] = "she"
Epronoun.morph[("sing","neut","3rd","subj")] = "it"


for g in gender:
    Epronoun.morph[("sing",g,"1st","obj")] = "me"
    Epronoun.morph[("sing",g,"2nd","obj")] = "you"
    Epronoun.morph[("plu",g,"1st","obj")] = "us"
    Epronoun.morph[("plu",g,"2nd","obj")] = "you"
    Epronoun.morph[("plu",g,"3rd","obj")] = "them"

Epronoun.morph[("sing","masc","3rd","obj")] = "him"      
Epronoun.morph[("sing","fem","3rd","obj")] = "her"
Epronoun.morph[("sing","neut","3rd","obj")] = "it"

  
Earticle = Word("article","English")
Earticle.root = ["the"]
for c in case:
   for g in gender:
     Earticle.morph[("sing",g,"3rd",c)] =""
     Earticle.morph[("plu",g,"3rd",c)] = ""

  
EIarticle = Word("indarticle","English")
EIarticle.root = [""]
for c in case:
   for g in gender:
     EIarticle.morph[("sing",g,"3rd",c)] ="a"
     EIarticle.morph[("plu",g,"3rd",c)] = ""






verb0 = Word("verb","English")
verb0.root = ["run","eat","play","talk"]
for c in case:
   for g in gender:
     verb0.morph[("sing",g,"1st",c)] =""
     verb0.morph[("sing",g,"2nd",c)] =""
     verb0.morph[("sing",g,"3rd",c)] ="s"
     verb0.morph[("plu",g,"1st",c)] =""
     verb0.morph[("plu",g,"2nd",c)] =""
     verb0.morph[("plu",g,"3rd",c)] =""


verb1 = Word("verb","English")
verb1.root = ["like","take","drop"]
for c in case:
   for g in gender:
     verb1.morph[("sing",g,"1st",c)] =""
     verb1.morph[("sing",g,"2nd",c)] =""
     verb1.morph[("sing",g,"3rd",c)] ="s"
     verb1.morph[("plu",g,"1st",c)] =""
     verb1.morph[("plu",g,"2nd",c)] =""
     verb1.morph[("plu",g,"3rd",c)] =""

Art = OSynt("article","English")
Art.alter =[Earticle,EIarticle]

NounPhrase = ASynt("noun phrase","English")
NounPhrase.twolist = [Art, Enoun]
NounPhrase.constraint = ["number","gender","person"]

Subject = OSynt("subject","English")
Subject.alter = [Epronoun,NounPhrase]
Subject.impose = ["case","subj"]

Object = OSynt("subject","English")
Object.alter = [Epronoun,NounPhrase]
Object.impose = ["case","obj"]




S3 = ASynt("S3","English")
S3.twolist = [Subject,verb1]
S3.constraint = ["number","person"]

S2 = ASynt("S2","English")
S2.twolist = [S3,Object]

S1 = ASynt("S1","English")
S1.twolist = [Subject,verb0]
S1.constraint = ["number","person"]

Sen = OSynt("sentence","English")
Sen.alter = [S1,S2]

def P(s):
 return Sen.parse(s)


Pfnoun = Word("fem-noun","Portuguese")
Pfnoun.root = ["mesa"]
for c in case:
    Pfnoun.morph[("sing","fem","3rd",c)] = ""
    Pfnoun.morph[("plu", "fem","3rd",c)] = "s"



Pmnoun = Word("masc-noun","Portuguese")
Pmnoun.root = ["gato","rato","livro"]
for c in case:
    Pmnoun.morph[("sing","masc","3rd",c)] = ""
    Pmnoun.morph[("plu", "masc","3rd",c)] = "s"

Pnoun = OSynt("noun","Portuguese")
Pnoun.alter =[Pmnoun,Pfnoun]

Averb = Word("a-verb","Portuguese")
Averb.root = ["jog","fal"]
for c in case:
   for g in gender:
    Averb.morph[("sing",g,"1st",c)] ="o"
    Averb.morph[("sing",g,"2nd",c)] ="as"
    Averb.morph[("sing",g,"3rd",c)] ="a"
    Averb.morph[("plu",g,"1st",c)] ="amos"
    Averb.morph[("plu",g,"2nd",c)] ="ais"
    Averb.morph[("plu",g,"3rd",c)] ="am"

Everb = Word("e-verb","Portuguese")
Everb.root = ["corr","com"]
for c in case:
   for g in gender:
    Everb.morph[("sing",g,"1st",c)] ="o"
    Everb.morph[("sing",g,"2nd",c)] ="es"
    Everb.morph[("sing",g,"3rd",c)] ="e"
    Everb.morph[("plu",g,"1st",c)] ="emos"
    Everb.morph[("plu",g,"2nd",c)] ="eis"
    Everb.morph[("plu",g,"3rd",c)] ="em"


Pverb = OSynt("verb","Portuguese")
Pverb.alter = [Averb,Everb]

PSen = ASynt("sentence","Portuguese")
PSen.twolist = [Pnoun,Pverb]
PSen.constraint = ["number","person"]

dictionary = Dictionary("english","portuguese")

dictionary.dictionary = {"cat":"gato","mouse":"rato","book":"livro","table":"mesa","run":"corr","talk":"fal","play":"jog"}
dictionary.word = {"noun":Pnoun, "verb":Pverb}
dictionary.switchlist = {PSen:"*",Pnoun:"",Pverb:"",Pmnoun:"",Pfnoun:"",Everb:"",Averb:""}

