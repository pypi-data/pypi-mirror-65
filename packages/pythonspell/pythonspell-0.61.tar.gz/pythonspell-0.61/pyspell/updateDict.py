import os
from pyspell.bktree import makeSearch,Node,setDictionary,fillTree
import pickle


def repickle(newDictpath,treename): #Deletes the current cached BKtree & rewrites it with the dict.
    if os.path.exists(treename):
        os.remove(treename)
    with open(newDictpath,'r') as wordlist:
            dictionary=list(filter(lambda x: len(x)>1,map(lambda x: x.strip(),wordlist.readlines())));
    root=Node()
    fillTree(root,dictionary)
    with open(treename, 'wb') as pickle_handle:
            pickle.dump(root, pickle_handle)
            
def addWord(word,dictPath,priority=-1): #adds a word, list, or dict to the given dictionary.
    file = open(dictPath, "r")
    content=file.readlines();
    file.close()
    print(word+"\n" in content)
    print(content[3],word)
    if (type(word)==list):
        for item in word:
            if item+"\n" not in content:
                if(priority<0):
                    content.insert(len(content),item+"\n")
                content.insert(priority,item)
    elif type(word)==dict:
        for key in word.keys():
            if key+"\n" not in content:
                if(type(key.location)==int):
                    content.insert(key.location,key+"\n")
                elif(priority<0):
                    content.insert(len(content),key+"\n")
                else:
                    content.insert(priority,key)    
    elif type(word)==str:
        if word+"\n" not in content:
            if(priority<0):
                    content.insert(len(content),word+"\n")
            content.insert(priority,word+"\n")
    f = open(dictPath, "w")
    f.writelines(content)
    f.close()
    