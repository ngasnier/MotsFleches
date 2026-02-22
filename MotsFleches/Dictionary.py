import re

class Dictionary:
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
        self.indexBySize = []
        self.wordsBySize = []
        self.nbLookups = 0
        self.nbCacheMiss = 0

        with open(textFilePath, 'r', encoding=encoding) as file:
            for line in file:
                word, separators = self.cleanWord(line)  # On normalise en majuscules
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

        self.wordsBySize[wordSize].append(word)

    def allocateIndexBySize(self, size):
        start = len(self.indexBySize)
        for i in range(start, size+1):
            self.indexBySize.append({}) # Index(i)
            self.wordsBySize.append([])

    def contains(self, word):
        size = len(word)
        index = self.indexBySize[size]
        self.nbLookups += 1
        words = index.get(word, None)
        if words is None: # Lazy caching 
            self.nbCacheMiss+=1
            words = [w for w in self.wordsBySize[size]]
            index[word] = words
        return len(words)>0
            
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
            if i<len(self.indexBySize):
                index = self.indexBySize[i]
                subPattern = pattern[:i]
                words = index.get(subPattern, None)
                if words is None: # Lazy caching of searches
                    self.nbCacheMiss+=1
                    regexp = re.compile(f'^{subPattern}$')
                    #words = [w for w in self.wordsBySize[i] if regexp.match(w)]
                    words = list(filter(regexp.match, self.wordsBySize[i]))
                    index[subPattern] = words
                candidates = candidates + [w for w in words if w not in exclusions and w not in candidates]
        return candidates

