import random

def getRandomWord(maxLen):
  """
  Return random word from dictionary, must match global varable for max word len.
  maxLen is to prevent annoyingly long/obscure words from making it into pwds

  Takes:
    maxLen - maximum length of the returned word
  """
  with open("pswdFactory/words.txt") as src:
    dicList = src.readlines()
    while True:
      word = dicList[random.randrange(0, len(dicList))][:-1]

      if len(word) < maxLen:
        return word[0].capitalize() + word[1:]

def getPwd(maxLen, nWords, dChance):
  """
  Return pswd consisting of nWords words of maxLen or less charcaters, with a nChance chance that there will be a random 1 digit number after each word

  Takes:
    maxLen - maximum length of the individual words
    nWords - number of random words in returned pwList
    dChance - chnace there will be a single digit after each individual word
  """
  pwd =  ""
  for _ in range(nWords):
    pwd += getRandomWord(maxLen)

    if random.randrange(0,100) < dChance:
      pwd += str(random.randrange(0,10))

  return(pwd)

def pswdList(amount=50, maxLen=6, nWords=3, dChance=33):
  """
  Return pswd list consisting of amount pwds, consisting of nWords words of maxLen or less charcaters, with a nChance chance that there will be a random 1 digit number after each word.

  If amount is greater than 1 the list will be formatted as below:
    Pass2WordExample
    CorrectHorseBattery
  
  else the password will be returned with no extra characters

  Takes:
    amount - number of pwds to generate.
    maxLen - maximum length of the individual words
    nWords - number of random words in returned pwList
    dChance - chnace there will be a single digit after each individual word
  """
  
  ret = ""
  ret += getPwd(maxLen, nWords, dChance) #avoid \n on first pswd
  for _ in range(1, amount):
    ret += '\n' + getPwd(maxLen, nWords, dChance) 
  return ret


def getPswdList(amount=50, maxLen=6, nWords=3, dChance=33):
  """
  helper function which is meant to abstract the password creation process.
  Simply calles pswdList with given perams

  If amount is greater than 1 the list will be formatted as below:
    Pass2WordExample
    CorrectHorseBattery
  
  else the password will be returned with no extra characters

  Takes:
    amount - number of pwds to generate.
    maxLen - maximum length of the individual words
    nWords - number of random words in returned pwList
    dChance - chnace there will be a single digit after each individual word
  """
  return pswdList(amount, maxLen, nWords, dChance)