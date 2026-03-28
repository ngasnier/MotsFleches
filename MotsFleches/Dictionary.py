from __future__ import annotations # Urk... why is that necessary... Python is a strange language...
import re

class Charset:
    ALL_LETTERS = 0b11111111111111111111111111
    A = 0b00000000000000000000000001
    B = 0b00000000000000000000000010
    C = 0b00000000000000000000000100
    D = 0b00000000000000000000001000
    E = 0b00000000000000000000010000
    F = 0b00000000000000000000100000
    G = 0b00000000000000000001000000
    H = 0b00000000000000000010000000
    I = 0b00000000000000000100000000
    J = 0b00000000000000001000000000
    K = 0b00000000000000010000000000
    L = 0b00000000000000100000000000
    M = 0b00000000000001000000000000
    N = 0b00000000000010000000000000
    O = 0b00000000000100000000000000
    P = 0b00000000001000000000000000
    Q = 0b00000000010000000000000000
    R = 0b00000000100000000000000000
    S = 0b00000001000000000000000000
    T = 0b00000010000000000000000000
    U = 0b00000100000000000000000000
    V = 0b00001000000000000000000000
    W = 0b00010000000000000000000000
    X = 0b00100000000000000000000000
    Y = 0b01000000000000000000000000
    Z = 0b10000000000000000000000000
    
    def __init__(self, value:int = ALL_LETTERS):
       self.chars =  value
    
    def intersect(self, other:Charset):
        self.chars = self.chars & other.chars

    def empty(self):
        self.chars = 0

    def setLetter(self, letter:str):
        self.chars = 0
        self.addLetter(letter)

    def setAllLetters(self):
        self.chars = Charset.ALL_LETTERS

    def addLetter(self, letter:str):
        if len(letter)!=1:
            raise ValueError("setLetter : only strings of one character allowed.")
        self.chars = self.chars | (Charset.A if letter=="A" else 0)
        self.chars = self.chars | (Charset.B if letter=="B" else 0)
        self.chars = self.chars | (Charset.C if letter=="C" else 0)
        self.chars = self.chars | (Charset.D if letter=="D" else 0)
        self.chars = self.chars | (Charset.E if letter=="E" else 0)
        self.chars = self.chars | (Charset.F if letter=="F" else 0)
        self.chars = self.chars | (Charset.G if letter=="G" else 0)
        self.chars = self.chars | (Charset.H if letter=="H" else 0)
        self.chars = self.chars | (Charset.I if letter=="I" else 0)
        self.chars = self.chars | (Charset.J if letter=="J" else 0)
        self.chars = self.chars | (Charset.K if letter=="K" else 0)
        self.chars = self.chars | (Charset.L if letter=="L" else 0)
        self.chars = self.chars | (Charset.M if letter=="M" else 0)
        self.chars = self.chars | (Charset.N if letter=="N" else 0)
        self.chars = self.chars | (Charset.O if letter=="O" else 0)
        self.chars = self.chars | (Charset.P if letter=="P" else 0)
        self.chars = self.chars | (Charset.Q if letter=="Q" else 0)
        self.chars = self.chars | (Charset.R if letter=="R" else 0)
        self.chars = self.chars | (Charset.S if letter=="S" else 0)
        self.chars = self.chars | (Charset.T if letter=="T" else 0)
        self.chars = self.chars | (Charset.U if letter=="U" else 0)
        self.chars = self.chars | (Charset.V if letter=="V" else 0)
        self.chars = self.chars | (Charset.W if letter=="W" else 0)
        self.chars = self.chars | (Charset.X if letter=="X" else 0)
        self.chars = self.chars | (Charset.Y if letter=="Y" else 0)
        self.chars = self.chars | (Charset.Z if letter=="Z" else 0)

    def add(self, other:Charset):
        self.chars = self.chars | other.chars

    def remove(self, other:Charset):
        self.chars = self.chars & ( other.chars ^ Charset.ALL_LETTERS )

    def count(self):
        # if too slow : use gmpy popcount()
        i:int = self.chars
        i = i - ((i >> 1) & 0x55555555)                 # add pairs of bits
        i = (i & 0x33333333) + ((i >> 2) & 0x33333333)  # quads
        i = (i + (i >> 4)) & 0x0F0F0F0F                 # groups of 8
        i = (i * 0x01010101) & 0xffffffff               # horizontal sum of bytes
        return  i >> 24; 

    @property
    def letters(self):
        str = ""
        str += "A" if (self.chars & Charset.A)>0 else ""
        str += "B" if (self.chars & Charset.B)>0 else ""
        str += "C" if (self.chars & Charset.C)>0 else ""
        str += "D" if (self.chars & Charset.D)>0 else ""
        str += "E" if (self.chars & Charset.E)>0 else ""
        str += "F" if (self.chars & Charset.F)>0 else ""
        str += "G" if (self.chars & Charset.G)>0 else ""
        str += "H" if (self.chars & Charset.H)>0 else ""
        str += "I" if (self.chars & Charset.I)>0 else ""
        str += "J" if (self.chars & Charset.J)>0 else ""
        str += "K" if (self.chars & Charset.K)>0 else ""
        str += "L" if (self.chars & Charset.L)>0 else ""
        str += "M" if (self.chars & Charset.M)>0 else ""
        str += "N" if (self.chars & Charset.N)>0 else ""
        str += "O" if (self.chars & Charset.O)>0 else ""
        str += "P" if (self.chars & Charset.P)>0 else ""
        str += "Q" if (self.chars & Charset.Q)>0 else ""
        str += "R" if (self.chars & Charset.R)>0 else ""
        str += "S" if (self.chars & Charset.S)>0 else ""
        str += "T" if (self.chars & Charset.T)>0 else ""
        str += "U" if (self.chars & Charset.U)>0 else ""
        str += "V" if (self.chars & Charset.V)>0 else ""
        str += "W" if (self.chars & Charset.W)>0 else ""
        str += "X" if (self.chars & Charset.X)>0 else ""
        str += "Y" if (self.chars & Charset.Y)>0 else ""
        str += "Z" if (self.chars & Charset.Z)>0 else ""
        return str
    
    def __str__(self):
        if self.chars==0:
            return "*"
        if self.chars==Charset.ALL_LETTERS:
            return " "
        return self.letters
    
    def __repr__(self):
        return self.__str__()

class Index:
    def __init__(self, size):
        self.size = size
        self.words = []
        self.index = [ {} for i in range(size)]

    def put(self, word):
        if len(word)!=self.size:
            raise Exception(f"try to add word '{word}' in an index of size {self.size}")
        
        self.words.append(word)

        for i in range(self.size):
            idxBySize = self.index[i]
            letter = word[i]
            idxByLetter = idxBySize.get(letter, [])
            idxByLetter.append(word)
            idxBySize[letter] = idxByLetter

    def query(self, pos, letter):
        return self.index[pos].get(letter, [])
    
    def queryAllWords(self):
        return self.words
    

class Dictionary:
    instance:Dictionary

    def __init__(self, textFilePath:str, encoding='utf-8'):
        """
        Initialise le dictionnaire en chargeant les mots depuis un fichier texte.
        :param chemin_fichier: Chemin vers le fichier texte (un mot par ligne).
        """
        self. accents = {
            'à': 'a', 'â': 'a', 'ä': 'a',
            'ç': 'c',
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'î': 'i', 'ï': 'i',
            'ô': 'o', 'ö': 'o',
            'ù': 'u', 'û': 'u', 'ü': 'u',
            'ÿ': 'y',
            'À': 'A', 'Â': 'A', 'Ä': 'A',
            'Ç': 'C',
            'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
            'Î': 'I', 'Ï': 'I',
            'Ô': 'O', 'Ö': 'O',
            'Ù': 'U', 'Û': 'U', 'Ü': 'U'
        }
        self.cacheBySize = []
        self.indexBySize = []
        self.nbLookups = 0
        self.nbCacheMiss = 0

        with open(textFilePath, 'r', encoding=encoding) as file:
            for line in file:
                word, separators = self.cleanWord(line)  
                if word:  
                    self.addWord(word)

    def cleanWord(self, word): 
        # Liste des caractères à supprimer
        separators = {' ', '-', "'", "."}
        positions = []
        cleanWord = []

        for index, char in enumerate(word.strip().upper()):
            if char in separators:
                positions.append(index)
            else:
                # Remplacer les accents si nécessaire
                clean_char = self.accents.get(char, char)
                cleanWord.append(clean_char)

        return ''.join(cleanWord), positions
    
    def addWord(self, word):
        wordSize = len(word)

        # Allocate index if needed
        self.allocateIndexBySize(wordSize)

        self.indexBySize[wordSize].put(word)

    def allocateIndexBySize(self, size):
        start = len(self.cacheBySize)
        for i in range(start, size+1):
            self.cacheBySize.append({}) # Index(i)
            self.indexBySize.append(Index(i))

    def contains(self, word):
        size = len(word)
        index = self.cacheBySize[size]
        self.nbLookups += 1
        words = index.get(word, None)
        if words is None: # Lazy caching 
            self.nbCacheMiss+=1
            words = [w for w in self.indexBySize[size].queryAllWords()]
            index[word] = words
        return len(words)>0
    
    def query(self, charset:list[Charset], exclusions=[]):
        self.nbLookups += 1
        patSize = len(charset)
        pattern = ''.join([f"[{cs.letters}]" for cs in charset])
        cache = self.cacheBySize[patSize]
        words = cache.get(pattern, None)
        if words is None: # Lazy caching of searches
            self.nbCacheMiss+=1

            index = self.indexBySize[patSize]
            bestResult = index.queryAllWords()
            bestResultCount = 1000000
            for pos in range(patSize):
                if charset[pos].count()==1:
                    result = index.query(pos, charset[pos].__str__())
                    if len(result)<bestResultCount:
                        bestResult = result
                        bestResultCount = len(result)

            regexp = re.compile(f'^{pattern}$')
            words = list(filter(regexp.match, bestResult))
            cache[pattern] = words
        return [w for w in words if w not in exclusions]

    def findCandidates(self, placeholder:str, exclusions=[], exactLength:bool=False):
        """
        Return candidates of length between 2 and len(placeholder)
        """
        candidates = []
        if len(placeholder)<2:
            return candidates        
        pattern = placeholder.replace(" ", ".")
        lenMax = pattern.find("*")
        if lenMax<0:
            lenMax = len(pattern)+1
        else:
            lenMax = lenMax+1

        # Don't try to fit words smaller than partial words
        lenMin = 2
        i = 0
        # All length ok if pattern is empty...
        while i<lenMax-1 and pattern[i]==".":
            i+=1
        # If letters, can only fit at least this size...
        while i<lenMax-1 and pattern[i]!=".":
            if i+1>lenMin:
                lenMin = i+1
            i+=1

        if exactLength:
            lenMin = lenMax-1

        index = None
        for i in range(lenMin, lenMax):
            self.nbLookups += 1
            if i<len(self.cacheBySize):
                cache = self.cacheBySize[i]
                subPattern = pattern[:i]
                words = cache.get(subPattern, None)
                if words is None: # Lazy caching of searches
                    self.nbCacheMiss+=1

                    index = self.indexBySize[i]
                    bestResult = index.queryAllWords()
                    bestResultCount = 1000000
                    for pos in range(i):
                        if subPattern[pos]!='.':
                            result = index.query(pos, subPattern[pos])
                            if len(result)<bestResultCount:
                                bestResult = result
                                bestResultCount = len(result)

                    regexp = re.compile(f'^{subPattern}$')
                    #words = [w for w in self.indexBySize[i] if regexp.match(w)]
                    words = list(filter(regexp.match, bestResult))
                    cache[subPattern] = words
                candidates = candidates + [w for w in words if w not in exclusions and w not in candidates]
        return candidates

    def initInstance(inst:Dictionary):
        Dictionary.instance = inst

    def getInstance()->Dictionary:
        return Dictionary.instance

