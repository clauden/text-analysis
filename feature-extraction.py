import sys
import re
import math
import nltk
from operator import itemgetter as itemgetter
from pprint import pprint as pp
from pdb import set_trace 

DELIM = '|'
SPLITTER = re.compile('\\W')


def trace():
  if sys.__stdin__.isatty():
    pdb.set_trace()
  else:
    pass


def dbg(s, label=''):
  print("DEBUG [%s]: %s\n" % (label, s))

#
# set of unique words 
#
def words(s):
  words = [w.lower() for w in SPLITTER.split(s)]
  return dict([(w,1) for w in words])


def bigrams(s):
  sp = [w.lower() for w in SPLITTER.split(s)] if isinstance(s, basestring) else s
  return [(sp[n], sp[n+1]) for n in range(0, len(sp)-2)] if len(sp) > 1 else []


def trigrams(s):
  sp = [w.lower() for w in SPLITTER.split(s)] if isinstance(s, basestring) else s
  return [(sp[n], sp[n+1], sp[n+2]) for n in range(0, len(sp)-3)] if len(sp) > 2 else []


def ngrams(s, n=2):
  dbg(s, 'ngram-input')

  sp = [w.lower() for w in SPLITTER.split(s)] if isinstance(s, basestring) else s

  if False:
    print("foo")
    pp(sp)
    print("bar")

  return [(sp[n], sp[n+1]) for n in range(0, len(sp)-2)]


def similarity(a, b):
  return nltk.jaccard_distance(set(a), set(b))

if __name__ == '__main__':

  rules = {}
  wordfreqs = {}
  

  # while True:
  #   l = sys.stdin.readline().strip()
  #   rules += l
  
  for l in sys.stdin.readlines():
    ll = l.split(DELIM)
    if len(ll) != 3: raise "wtf" 
    rules[ll[1]] = ll[2].strip().split()

  
  for ruleid in rules:
    text = rules[ruleid]

    if False:
      print("RuleID: " + ruleid)
      pp(text)
      print("====")

    trace()

    bg = bigrams(text)
    fd = nltk.FreqDist(bg)
    for word, freq in fd.items():
        wordfreqs[word] = wordfreqs[word] + freq if word in wordfreqs else freq

  # similarity matrix
  sims = {}
  for ruleid in rules:
    t1 = rules[ruleid]
    s = {}
    for r in rules:
      if r == ruleid or r in sims: pass
      s[r] = similarity(bigrams(rules[ruleid]), bigrams(rules[r]))
    sims[ruleid] = s
  pp(sims)

  # minimum difference in similarity matrix
  mins = {}
  for ruleid in sims:
    min = 1.0
    for r in sims:
      if r != ruleid:
        if sims[ruleid][r] < min: 
          min = sims[ruleid][r] 
          mins[ruleid] = (r, min)
  pp(mins)
      

    

  # word frequency
  wfs = sorted(wordfreqs.items(), key=itemgetter(1))
  ## pp(wfs)
  # fd.plot(10, cumulative=False)
    
