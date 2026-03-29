from __future__ import annotations
from MotsFleches import Dictionary, Charset

from abc import ABC, abstractmethod
import random
 
class Interval:
    def __init__(self, offset:int, start:int, end:int, direction:bool):
        """
        Parameters
        ----------
        offset : int
            grid or row index of the interval relative to the grid.
        start : int
            start index of the interval in the row or column indicated by offset
        end : int
            end index of the interval in the row or column indicated by offset.
            convention is that the interval stop at index end-1.
        """
        self.offset = offset
        self.start = start
        self.end = end
        self.direction = direction
   
    def split(self, pos:int):
        """
        Split interval by a definition cell.

        Parameters
        ---------
        pos : the position of the definition cell, relative to the grid.

        Returns
        -------
        array of Interval. Only intervals of at least one cell are returned.
        """
        newStart = pos+1
        newInter1 = Interval(self.offset, self.start, pos, self.direction)
        newInter2 = Interval(self.offset, newStart, self.end, self.direction)
        intervals = [  ]
        if pos-self.start>0:
            intervals.append(newInter1)
        if self.end-newStart>0:
            intervals.append(newInter2)
        return intervals
    
    @property
    def cellCount(self):
        return self.end-self.start
    
    def __str__(self):
        return f"[{self.offset, self.start, self.end, self.direction}]"
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, value):
        return  value.offset==self.offset and value.start==self.start and value.end==self.end and value.direction==self.direction
    
    def getIntervalCharset(self, content:list[list[Charset]]):
        if self.direction:
            return content[self.offset][self.start:self.end]
        else:
            contenu = []
            for j in range(self.start, self.end):
                contenu.append(content[j][self.offset])
            return contenu

    
class IPossible(Interval, ABC):
    def makeChoice(self) -> list[IPossible]:
        pass

    @property
    def count(self) -> int:
        pass

    @property
    def isSet(self) -> bool:
        pass

    @property
    def theSetContent(self) -> str:
        pass

    def filter(self, content:list[list[Charset]], usedWords:list[str]):
        pass

class AllWords(IPossible):
    def __init__(self, interval:Interval):
        Interval.__init__(self, interval.offset, interval.start, interval.end, interval.direction)
        self.size = interval.cellCount
        self.words = None

    def queryDictionary(self, content:list[Charset], usedWords:list[str]):
        self.words = Dictionary.getInstance().query(content, usedWords)

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
        return len(self.words)
    
    @property
    def isSet(self) -> bool:
        return False

    @property
    def theSetContent(self) -> str:
        return ""

    def filter(self, content:list[list[Charset]], usedWords:list[str]):
        subcontent = self.getIntervalCharset(content)
        self.queryDictionary(subcontent, usedWords)

    def __str__(self):
        content = ""
        if self.count<10:
            content = ','.join(self.words)
        else:
            content = "{self.count} words"
        return f"Allwords({self.size}, [{content}])"

class SetWord(IPossible):
    def __init__(self, interval:Interval, word:str):
        Interval.__init__(self, interval.offset, interval.start, interval.end, interval.direction)
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
    
    @property
    def theSetContent(self) -> str:
        return self.word
  
    def filter(self, content:list[list[Charset]], usedWords:list[str]):
        return

    def __str__(self):
        return f"SetWord({self.word})"

    
class SplitInterval(IPossible):
    
    def __init__(self, interval:Interval, pos:int):
        Interval.__init__(self, interval.offset, interval.start, interval.end, interval.direction)
        if pos<0:
            raise ValueError("pos must be positive.")
        if pos>interval.cellCount-1:
            raise ValueError(f"pos must between 0 and {interval.cellCount}.")

        self.pos = pos
        self.before = None
        self.after = None
        self.canMakeChoice = False

        split = interval.split(interval.start+pos)

        for newInterval in split:
            if newInterval.start<pos:
                self.before = AllWords(newInterval) 
            else:
                if newInterval.cellCount>0:
                    self.after = PossibleSet(newInterval)

    def makeChoice(self):
        choice = []
        if self.canMakeChoice:
            if self.before is not None:
                choice.append(self.before)
            if self.after is not None:
                choice.append(self.after)
        self.canMakeChoice = False
        return choice
    
    @property
    def count(self)  -> int:
        if self.canMakeChoice:
            return 1
        else:
            return 0

    @property
    def isSet(self) -> bool:
        return False
    
    @property
    def theSetContent(self) -> str:
        return ""

    def filter(self, content:list[Charset], usedWords:list[str]):
        canPlaceDefinition = False
        if self.direction:
            canPlaceDefinition = content[self.offset][self.pos].count>0
        else:
            canPlaceDefinition = content[self.pos][self.offset].count>0

        if self.before is not None:
            self.before.filter(content, usedWords)
        if self.after is not None:
            self.after.filter(content, usedWords)

        self.canMakeChoice = canPlaceDefinition and ((self.before is not None and self.before.count!=0) or (self.after is not None and self.after.count!=0))
        return    
    
    def __str__(self):
        strint=Interval.__str__(self)
        return f"SplitInterval({strint}, {self.pos})"
    
class PossibleSet(IPossible):
    def __init__(self, interval:Interval):
        Interval.__init__(self, interval.offset, interval.start, interval.end, interval.direction)
        self.possibles = []
        self.possibles.append(AllWords(interval))
        for i in range(interval.cellCount):
            self.possibles.append(SplitInterval(interval, i))

    def makeChoice(self):
        if len(self.possibles)==0:
            return []
        choice = random.choices(self.possibles, k=1)[0]
        self.possibles.remove(choice)
        return [ choice ]
    
    @property
    def count(self)  -> int:
        return len(self.possibles)

    @property
    def isSet(self) -> bool:
        return False
    
    @property
    def theSetContent(self) -> str:
        return ""

    def filter(self, content:list[list[Charset]], usedWords:list[str]):
        for p in self.possibles:
            p.filter(content, usedWords)
        
        self.possibles = list(filter(lambda p: p.count>0, self.possibles))

    def __str__(self):
        strint=Interval.__str__(self)
        # str = "["
        # for p in self.possibles:
        #     if isinstance(p, PossibleSet):
        #         str+=f"PossibleSet({strint}, {p.count}), "
        #     else:
        #         str+=f"{p}, "
        # str += "]"
        return f"PossibleSet({strint})"
    
    def __repr__(self):
        return self.__str__()