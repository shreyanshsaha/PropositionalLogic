import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

import string


class Preprocessing:
  def __init__(self):
    pass

  def preprocess(self, inputStr: str):
    inputStr = inputStr.lower()
    inputStr = inputStr.translate(str.maketrans('', '', string.punctuation))
    inputStr = inputStr.strip()
    stopWords = set(stopwords.words('english'))
    stopWords.difference_update(set({'if', 'then', 'is', 'only'}))
    tokens = word_tokenize(inputStr)
    inputStr = " ".join([i for i in tokens if i not in stopWords])

    stemmer = PorterStemmer()
    tokens = word_tokenize(inputStr)
    inputStr = " ".join([stemmer.stem(i) for i in tokens])
    return inputStr

if __name__ == "__main__":
  preprocessor = Preprocessing()
  print(preprocessor.preprocess("It is raining"))

