from __future__ import annotations # Urk... why is that necessary... Python is a strange language...
from MotsFleches import Dictionary, Charset
from MotsFleches import Interval

from abc import ABC, abstractmethod


class IPossible(Interval, ABC):
    def makeChoice(self) -> list[IPossible]:
        pass

    @property
    def count(self) -> int:
        pass

    @property
    def isSet(self) -> bool:
        pass

    def filter(self, content:list[Charset]):
        pass

class AllWords(IPossible):
    def __init__(self, interval:Interval, dict:Dictionary):
        Interval.__init__(self, interval.grid, interval.offset, interval.start, interval.end, interval.direction)
        self.size = interval.cellCount
        self.dictionary = dict
        self.words = None

    def queryDictionary(self):
        self.words = self.dictionary.query(self.content, self.grid.usedWords)

    def makeChoice(self) -> list[IPossible]:
        if self.words is None:
            self.queryDictionary()
        return None
    
    @property
    def count(self) -> int:
        return len(self.words)
    
    @property
    def isSet(self) -> bool:
        return False

    def filter(self, content:list[Charset]):
        return

    def __str__(self):
        return f"Allwords({self.size})"

class SetWord(IPossible):
    def __init__(self, interval:Interval, word:str):
        Interval.__init__(self, interval.grid, interval.offset, interval.start, interval.end, interval.direction)
        self.size = interval.cellCount
        self.word = word
        # TODO : penser à mettre à jour le charset/contenu de la grille dans l'algo qque part...
        #interval.grid.placeWord(interval, word, False)
        
    def makeChoice(self) -> list[IPossible]:
        return None
    
    @property
    def count(self) -> int:
        return 1
    
    @property
    def isSet(self) -> bool:
        return True

    def filter(self, content:list[Charset]):
        return

    def __str__(self):
        return f"SetWord({self.word})"

    
class SplitInterval(IPossible):
    
    def __init__(self, interval:Interval, pos:int, dict:Dictionary):
        Interval.__init__(self, interval.grid, interval.offset, interval.start, interval.end, interval.direction)
        if pos<0:
            raise ValueError("pos must be positive.")
        if pos>interval.cellCount-1:
            raise ValueError(f"pos must between 0 and {interval.cellCount}.")

        self.pos = pos
        self.before = None
        self.after = None

        split = interval.split(interval.start+pos)

        for newInterval in split:
            if newInterval.start<pos:
                self.before = AllWords(newInterval, dict) 
            else:
                if newInterval.cellCount>0:
                    self.after = PossibleSet(newInterval, dict)

    def makeChoice(self):
        return None
    
    @property
    def count(self)  -> int:
        return 0

    @property
    def isSet(self) -> bool:
        return False
    
    def filter(self, content:list[Charset]):
        return    
    
    def __str__(self):
        return f"SplitInterval({self.pos}, {self.before}, {self.after})"
    
class PossibleSet(IPossible):
    def __init__(self, interval:Interval, dict:Dictionary):
        Interval.__init__(self, interval.grid, interval.offset, interval.start, interval.end, interval.direction)
        self.possibles = []
        self.possibles.append(AllWords(interval, dict))
        for i in range(interval.cellCount):
            self.possibles.append(SplitInterval(interval, i, dict))

    def makeChoice(self):
        return None
    
    @property
    def count(self)  -> int:
        return len(self.possibles)

    @property
    def isSet(self) -> bool:
        return False
    
    def filter(self, content:list[Charset]):
        for p in self.possibles:
            p.filter(content)
        
        self.possibles = filter(lambda p: p.count>0, self.possibles)

    def __str__(self):
        str = "["
        for p in self.possibles:
            str+=f"{p}"
        str += "]"
        return str
    
    def __repr__(self):
        return self.__str__()