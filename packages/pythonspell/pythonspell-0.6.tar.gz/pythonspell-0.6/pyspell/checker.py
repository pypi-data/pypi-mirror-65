from pyspell.bktree import makeSearch,Node,setDictionary
from pyspell.updateDict import addWord,repickle
import os,time,pickle
class Checker:
    def __init__(self, path_to_wordlist,treename="bktree.pickle"):
        self.dictionaryPath=path_to_wordlist
        self.treename=treename
        if not os.path.exists(treename):
            repickle(self.dictionaryPath,self.treename);
    def load(self): #Initialize the cached BK tree and the dictionary
        with open(self.dictionaryPath,'r') as wordlist:
            self.dictionary=list(filter(lambda x: len(x)>1,map(lambda x: x.strip(),wordlist.readlines())));
        file = open(self.treename, 'rb')
        self.root = pickle.load(file)
        file.close()
    def repickle(self): #repickle the dictionary after modifications
        repickle(self.dictionaryPath,self.treename)
        file = open(self.treename, 'rb')
        self.root = pickle.load(file)
        file.close()
    def check(self,word,returnNum=1,returnType="words",repeat=True,forcePrecision=0): #Find  a word or list of words
        if (type(word)==str):
            return makeSearch(word,self.root,self.dictionary,returnNum,returnType,repeat)
        elif (type(word)==list):
            return [makeSearch(word[i],self.root,self.dictionary,returnNum,returnType,repeat) for i in range(len(word))]
    def updateDict(self,word,priority=-1,pickle=True):
        addWord(word,priority,self.dictionaryPath,pickle);
        if pickle:
            repickle(self.dictionaryPath,self.treename)
        with open(self.dictionaryPath,'r') as wordlist:
            self.dictionary=list(filter(lambda x: len(x)>1,map(lambda x: x.strip(),wordlist.readlines())));