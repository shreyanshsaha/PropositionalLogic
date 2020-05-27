import re
import nltk
from nltk.sem.logic import *


read_expr = Expression.fromstring

class Symbol:
  def __init__(self):
    self.symbols = dict({})
    self.currSymbol = 'A'

  def addSymbol(self, string: str):
    string = string.lower()
    if string not in self.symbols.keys():
      self.symbols[string] = self.currSymbol
      self.currSymbol= chr(ord(self.currSymbol)+1)
  
  def getSymbol(self, string: str):
    if string not in self.symbols.keys():
      return None
    return self.symbols[string]

class Extractor:
  def __init__(self):
    self.firstPartPattern = re.compile(r"(?<=if)[\w ]+(?=then)", re.IGNORECASE)
    self.secondPartPattern = re.compile(r"(?<=then)[\w ]+$", re.IGNORECASE)
    self.checkPattern = re.compile(r"(if)[\w ]+(then)\s?[\w ]+", re.IGNORECASE)
    self.symbolHandler = Symbol()
  
  def extract(self, sentence):
    if type(sentence) != str:
      raise "Sentence should be of type string!"
    if not re.match(self.checkPattern, sentence):
      raise "Sentence doesn't match the pattern if<s1>then<s2>!"
    
    firstPart = re.search(self.firstPartPattern, sentence).group(0).strip()
    secondPart = re.search(self.secondPartPattern, sentence).group(0).strip()

    self.symbolHandler.addSymbol(firstPart)
    self.symbolHandler.addSymbol(secondPart)
    print(self.symbolHandler.symbols)
    return [firstPart, secondPart]

class Prover:
  def __init__(self):
    self.logicProver = Expression.fromstring



if __name__ == "__main__":
  extractor  = Extractor()
  print(extractor.extract("If there is smoke then there is fire"))
  prover = Prover()
  lp = nltk.sem.Expression.fromstring
  SnF = read_expr('SnF')
  NotFnS = read_expr('-FnS')
  R = read_expr('SnF -> -FnS')
  prover = nltk.Prover9()
  prover.prove(NotFnS, [SnF, R])


