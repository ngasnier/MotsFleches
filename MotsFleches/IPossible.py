from __future__ import annotations # Urk... why is that necessary... Python is a strange language...
from MotsFleches import Dictionary, Charset
from MotsFleches import Interval

from abc import ABC, abstractmethod
import random

class IPossible(Interval, ABC):
    def makeChoice(self) -> list[IPossible]:
        pass

    @property
    def count(self) -> int:
        pass

    @property
    def isSet(self) -> bool:
        pass

    def filter(self):
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
        if len(self.words)==0:
            return []
        word = random.choices(self.words, k=1)[0]
        self.words.remove(word)
        return [SetWord(self, word)]
    
    @property
    def count(self) -> int:
        if self.words is None:
            self.queryDictionary()
        return len(self.words)
    
    @property
    def isSet(self) -> bool:
        return False

    def filter(self):
        self.queryDictionary()

    def __str__(self):
        content = ""
        if self.count<10:
            content = ','.join(self.words)
        else:
            content = "{self.count} words"
        return f"Allwords({self.size}, [{content}])"

class SetWord(IPossible):
    def __init__(self, interval:Interval, word:str):
        Interval.__init__(self, interval.grid, interval.offset, interval.start, interval.end, interval.direction)
        self.size = interval.cellCount
        self.word = word
        
    def makeChoice(self) -> list[IPossible]:
        return [self]
    
    @property
    def count(self) -> int:
        return 1
    
    @property
    def isSet(self) -> bool:
        return True

    def filter(self):
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
        choice = []
        if self.before is not None:
            choice.append(self.before)
        if self.after is not None:
            choice.append(self.after)
        return choice
    
    @property
    def count(self)  -> int:
        if (self.before is not None and self.before.count==0) or (self.after is not None and self.after.count==0):
            return 0
        else:
            return 1

    @property
    def isSet(self) -> bool:
        return False
    
    def filter(self):
        if self.before is not None:
            self.before.filter()
        if self.after is not None:
            self.after.filter()
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
        if len(self.possibles)==0:
            return []
        choice = random.choices(self.possibles, k=1)[0]
        self.words.remove(choice[0])
        return choice
    
    @property
    def count(self)  -> int:
        return len(self.possibles)

    @property
    def isSet(self) -> bool:
        return False
    
    def filter(self):
        for p in self.possibles:
            p.filter()
        
        self.possibles = list(filter(lambda p: p.count>0, self.possibles))

    def __str__(self):
        str = "["
        for p in self.possibles:
            if isinstance(p, PossibleSet):
                str+=f"PossibleSet({p.count}), "
            else:
                str+=f"{p}, "
        str += "]"
        return str
    
    def __repr__(self):
        return self.__str__()