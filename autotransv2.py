
number = ["sing","plu"]
gender = ["fem","masc","neut"]
person = ["1st","2nd","3rd"]
case =   ["subj","gen","obj"]


categories = [] 
for n in number:
 for g in gender:
  for p in person:
   for c in case:
     categories.append((n,g,p,c))


type={}
type["number"] = [cat[0] for cat in categories]
type["gender"] = [cat[1] for cat in categories]
type["person"] = [cat[2] for cat in categories]
type["case"] = [cat[3] for cat in categories]

sym = {"number":0,"gender":1,"person":2,"case":3}

def intersection(a,b):
 val = []
 for x in a:
  if x in b:
   val.append(x)
 return val

def intersection3(a,b,c):
  return intersection(intersection(a,b),c)

def intersection4(a,b,c,d):
  return intersection(intersection3(a,b,c),d)


def listproj1(list, constraint1):
 return [lex[sym[constraint1]] for lex in list]

def listproj2(list, constraint2):
 return [(lex[sym[constraint2[0]]], lex[sym[constraint2[1]]]) for lex in list]

def comp2(element, constraint2):
 return (element[sym[constraint2[0]]], element[sym[constraint2[1]]])

  

class Word:
  def __init__(self,data,lang):
   self.name = data
   self.lang = lang
   self.root = []
   self.morph= {}
   self.irreg = {}
 
   for cat in categories:
    self.morph[cat] = "*"
 
  def flex(self,root,cat):
   if self.morph[cat]!="*" and root in self.irreg.keys() and cat[sym[self.irreg[root][0]]] == self.irreg[root][1]:
    return self.irreg[root][2] 
   else:
    if self.morph[cat]!="*":
     return root + self.morph[cat]
    else:
     return "*"
 #will need another flex for translation that returns ""#
  def flexcheck(self,string,root,cat):
   if string == self.flex(root,cat):
     return True
   else:
     return False
 

  def parse(self,s):
      val = []
      for lex in self.root:
       for cat in categories:
        if s == self.flex(lex,cat):
         val.append((self.name,lex,cat))
      return val 
 
  def parsecat(self,s):
   return [par[2] for par in self.parse(s)]

  def parsecheck(self,s):
   if self.parse(s)!=[]:
    return True
   else:
    return False

  def permuparse(self,s,dictionary):
   return s

Nullword = Word("false","none")



class ASynt:
 def __init__(self, data, language):
  self.name =data
  self.language = language
  self.twolist = []
  self.constraint = []
  self.impose = []
  self.switch = "off"
 
 def parse(self,s):
  s= s.replace(" ","")
  l = len(s)
  val = [n for n in range(l) if self.twolist[0].parsecheck(s[0:n]) and self.twolist[1].parsecheck(s[n:l])]
  if val!=[]:
   m = val[0]
   v = self.twolist[0].parse(s[0:m]) + self.twolist[1].parse(s[m:l])
   if self.constraint!=[]:
    con =  intersection( listproj2(self.twolist[0].parsecat(s[0:m]), self.constraint),  listproj2(self.twolist[1].parsecat(s[m:l]),self.constraint))
    if con!=[]:
     v = [a for a in self.twolist[0].parse(s[0:m])+ self.twolist[1].parse(s[m:l]) if comp2(a[2],self.constraint) in con]
    else:
     v = []
   if self.impose!=[] and v!=[]:
     v = [a for a in v if a[2][sym[self.impose[0]]] == self.impose[1]]
   return v
  return []
 def parsecheck(self,s):
  val = self.parse(s)
  if val!=[]:
   return True
  else:
   return False
 def parsecat(self,s):
  val = []
  list = self.parse(s)
  for lex in list:
     val.append(lex[2])
  return val
 
 def parsefilter(self,s, con):
  return list(set(listproj2(self.parsecat(s),con)))

 def permuparse(self,s,switchlist):
  s= s.replace(" ","")
  l = len(s)
  val = [n for n in range(l) if self.twolist[0].parse(s[0:n]) and self.twolist[1].parse(s[n:l])]
  if val!=[]:
   m = val[0]
   if switchlist[self]=="":
    return self.twolist[0].permuparse(s[0:m],switchlist)+" "+ self.twolist[1].permuparse(s[m:l],switchlist)
   else:
    return self.twolist[1].permuparse(s[m:l],switchlist)+" "+ self.twolist[0].permuparse(s[0:m],switchlist)


class OSynt:
 def __init__(self, data, language):
  self.name =data
  self.language = language
  self.alter = []
  self.impose =[]
 
 def parse(self,s):
  a =[]
  if self.alter[0].parsecheck(s) == True: 
   a = self.alter[0].parse(s)
  if self.alter[1].parsecheck(s) == True: 
   a = self.alter[1].parse(s)
  w = a
  if self.impose!=[] and a is not None and a!=[]:
    w = [x for x in a if x[2][sym[self.impose[0]]] == self.impose[1]]
  return w


 def parsecheck(self,s):
  if self.parse(s)!=[]:
   return True
  else:
   return False





 def parsecat(self,s):
  val = []
  list = self.parse(s)
  for lex in list:
     val.append(lex[2])
  return val

 def flex(self,root,cat):
   if root in self.alter[0].root:
    return self.alter[0].flex(root,cat)
   if root in self.alter[1].root:
    return self.alter[1].flex(root,cat)

 def permuparse(self,s,switchlist):
  if self.alter[0].parsecheck(s) == True: 
    return self.alter[0].permuparse(s,switchlist)
  if self.alter[1].parsecheck(s) == True: 
   return self.alter[1].permuparse(s,switchlist)
 
 def parsefilter(self,s, con):
  return list(set(listproj2(self.parsecat(s),con)))



 
class Dictionary:
 def __init__(self,language1,language2):
   self.language1 = language1
   self.language2 = language2
   self.dictionary = {}
   self.word ={}
   self.switchlist = {}
#i.e. {"prenoun":"switch",}

def organize1(list,keys):
 col = {}
 for typ in keys:
  col[typ] = []
  for lex in list:
   if lex[0] == typ:
    col[typ].append(lex)
 return col



def translation(sparser,dparser, dictionary,s):
 
 list = sparser.parse(s) 
 tr = []
 if list is None:
  return "syntax error"
 for lex in list:
  add = dictionary.word[lex[0]].flex(dictionary.dictionary[lex[1]], lex[2])
  tr.append(add)
 trans = tr[0]
 l = len(tr)
 for i in range(1,l):
  if tr[i]!=tr[i-1]:
   trans = trans+ " "+tr[i]
 return trans[1:]

