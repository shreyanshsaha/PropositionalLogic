import re
import nltk
from nltk.sem.logic import *
from preprocessing import Preprocessing

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
      self.addSymbol(string)
      return self.symbols[string]
    return self.symbols[string]

class Prover:
  def __init__(self):
    self.logicProver = nltk.Prover9()
    self.statements = []
  
  def addStatement(self, expression):
    expr = read_expr(expression)
    if expr not in self.statements:
      self.statements.append(expr)
    return expr

class Extractor(Prover):
  def __init__(self):
    super(Extractor, self).__init__()
    self.firstPartPattern = re.compile(r"(?<=if)[\w ]+(?=then)", re.IGNORECASE)
    self.secondPartPattern = re.compile(r"(?<=then)[\w ]+$", re.IGNORECASE)
    self.implicationPattern = re.compile(r"(if)[\w ]+(then)\s?[\w ]+", re.IGNORECASE)
    self.implicationPattern2 = re.compile(r"^when\s\w+[\w\s]*(then)\s?[\w]+[\w\s]*", re.IGNORECASE)
    self.andPattern = re.compile(r".+(and)\s\w+", re.IGNORECASE)
    self.orPattern = re.compile(r".+(or)\s\w+", re.IGNORECASE)
    self.doubleImplyPattern = re.compile(r"[\w\s]+(only if)\s\w+.*", re.IGNORECASE)

    self.symbolHandler = Symbol()
    self.preprocessing = Preprocessing()
  
  def isImplication(self, sentence: str):
    self.implicationPattern2 = re.compile(r"^when\s\w+[\w\s]*,\s?[\w]+[\w\s]*", re.IGNORECASE)
    if re.match(self.implicationPattern, sentence) or re.match(self.implicationPattern2, sentence):
      return True
    return False

  def __extractOr(self, sentence):
    if not re.match(self.orPattern, sentence):
      raise "Sentence doesn't match the pattern <s1>and<s2>!"

    firstPart, secondPart = list(map(str.strip, sentence.lower.split('or')))
    return self.addStatement(self.symbolHandler.getSymbol(firstPart)+" v "+self.symbolHandler.getSymbol(secondPart))

  def __extractAnd(self, sentence):
    if not re.match(self.andPattern, sentence):
      raise "Sentence doesn't match the pattern <s1>and<s2>!"

    firstPart, secondPart = list(map(str.strip, sentence.lower.split('and')))

    return self.addStatement(self.symbolHandler.getSymbol(firstPart)+" ^ "+self.symbolHandler.getSymbol(secondPart))

  def __extractStatement(self, sentence):
    print(sentence)
    isPattern = re.compile(r"[\w\s]+\s(is)\s[\w\s]+", re.IGNORECASE)
    isNotPattern = re.compile(r"[\w\s]+\s(is not)\s[\w\s]+", re.IGNORECASE)

    if re.match(isPattern, sentence):
      if re.match(isNotPattern, sentence):
        parts = sentence.split('is not')
        sym1 = self.symbolHandler.getSymbol(parts[0])
        sym2 = self.symbolHandler.getSymbol(parts[1])
        print("Symbol for statement: ", sym1, sym2)
        return self.addStatement(sym1+" -> ~"+sym2)
      else:
        parts = sentence.split('is')
        sym1 = self.symbolHandler.getSymbol(parts[0])
        sym2 = self.symbolHandler.getSymbol(parts[1])
        print("Symbol for statement: ", sym1, sym2)
        return self.addStatement(sym1+" -> "+sym2)

    if 'not' in sentence.split(' '):
      sentence = sentence.replace('not', '').strip()
      print("Symbol for statement: ", self.symbolHandler.getSymbol(sentence))
      return self.addStatement("~"+self.symbolHandler.getSymbol(sentence))
    else:
      print("Symbol for statement: ", self.symbolHandler.getSymbol(sentence))
      return self.addStatement(self.symbolHandler.getSymbol(sentence))
    
  def __extractImplication(self, sentence):
    if not re.match(self.implicationPattern, sentence):
      raise "Sentence doesn't match the pattern if<s1>then<s2>!"
    firstPart = re.search(self.firstPartPattern, sentence).group(0).strip()
    secondPart = re.search(self.secondPartPattern, sentence).group(0).strip()

    self.symbolHandler.addSymbol(firstPart)
    self.symbolHandler.addSymbol(secondPart)
    print(self.symbolHandler.symbols)
    return self.addStatement(self.symbolHandler.getSymbol(firstPart)+" -> "+self.symbolHandler.getSymbol(secondPart))

  def __extractDoubleImplt(self, sentence):
    parts = list(map(str.strip, sentence.split('only if')))
    return self.addStatement(self.symbolHandler.getSymbol(parts[0])+" <-> "+self.symbolHandler.getSymbol(parts[1]))

  def extract(self, sentence: str):
    if type(sentence) != str:
      raise "Sentence should be of type string!"
    if len(sentence)<=0:
      raise "input len should be > 0!"

    if self.isImplication(sentence):
      sentence.replace(",", "then")
      sentence = self.preprocessing.preprocess(sentence)
      return self.__extractImplication(sentence)
    
    sentence = self.preprocessing.preprocess(sentence)
    if re.match(self.andPattern, sentence):
      # print("Extracting and")
      return self.__extractAnd(sentence)
    elif re.match(self.doubleImplyPattern, sentence):
      return __extractDoubleImply(sentence)
    else:
      # print("Extracting statement")
      return self.__extractStatement(sentence)

  def prove(self, expression):
    expression = self.preprocessing.preprocess(expression)
    # symbol = self.symbolHandler.getSymbol(expression)
    stmt = str(self.extract(expression))
    print("Statement to prove:", stmt)
    print("Statements: ")
    print([str(i) for i in self.statements])
    return self.logicProver.prove(read_expr(stmt), self.statements)


if __name__ == "__main__":
  extractor  = Extractor()
  print("Enter statements(0 to exit)..")
  while True:
    print("Enter: ", end='')
    answer = input().rstrip()
    if answer=='0':
      break
    extractor.extract(answer)
  print("Enter the statement to verify: ", end='')
  statement = input().rstrip()
  print(extractor.prove(statement))

  # print(extractor.extract("If there is smoke then there is fire"))
  # print(extractor.extract("there is smoke"))
  # print(extractor.prove("there is fire"))
  # prover = Prover()
  # # lp = nltk.sem.Expression.fromstring
  # SnF = read_expr('SnF')
  # NotFnS = read_expr('-FnS')
  # R = read_expr('SnF -> -FnS')
  # prover = nltk.Prover9()
  # prover.prove(NotFnS, [SnF, R])


