import sys
import math
import os
   
def load(wordsfile):
   wordlist = []
   with open(wordsfile, encoding="utf-8") as f:
        for line in f:
            wordlist.append(line.split("\n")[0])
   return wordlist


def getword(wordlist,maxlen,minlen):
  while True:
    byte = math.ceil(math.log2(len(wordlist)) / 8)
    random = os.urandom(byte)
    number = int.from_bytes(random, byteorder=sys.byteorder) % len(wordlist)
    word = wordlist[number]
    if (len(word) <= maxlen and len(word) >= minlen):
      return word

if __name__ == '__main__':
  words = 4
  min = 5
  max = 12  
  if len(sys.argv) > 1:
    words = int(sys.argv[1])
  if len(sys.argv) > 2:
    min = int(sys.argv[2])
  if len(sys.argv) > 3:
    max = int(sys.argv[3])
  wordlist = load("germanwords-typical.txt")
  
  phrase = ""
  for i in range(0,words):
    phrase = phrase + (getword(wordlist,max,min)) + " "    
  print(phrase)