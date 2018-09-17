import sys
import re
import math
import nltk
from operator import itemgetter as itemgetter
from pprint import pprint as pp
from pdb import set_trace 
import codecs


DELIM = '|'
SPLITTER = re.compile('\\W')

# cluster threshold
MIN=0.75

def trace():
  # if sys.__stdin__.isatty():
  #   return set_trace()
  #else:
    return None


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


def k_cluster(nodeid, k, distances):
  cl = []
  min = 1.0
  max = 0.0

  # one pass
  for node in distances:
    if node != nodeid and node not in cl and distances[node] <= min:
      min = distances[node]
      cl.append(node)
  
  # remember the closest we got
  max = min

  return cl, min


if __name__ == '__main__':

  rules = {}
  wordfreqs = {}
  


  fd = codecs.open('data', 'r', 'utf-8') if sys.__stdin__.isatty() else sys.stdin
  for l in fd.readlines():
  # for l in open('data').readlines() if sys.__stdin__.isatty() else sys.stdin.readlines():
    pp(l)
    print(type(l))

    u = l
    u = l.decode('utf-8')
    pp(u)
    
    # substitute reasonable ASCII approximations to normalize across datasets...
    # should be abstracted someplace!
    s = u''
    for c in u:
      if c == unichr(0x201c) or c == unichr(0x201d) :
      # if c == u'\u201c' or c == u'\u201d' :
        s += '"'
      elif c == unichr(0x2019):
        s += "'"
      else:
        s += c
    u = s
      

    ll = u.split(DELIM)
    if len(ll) != 3: raise "wtf" 
    rules[ll[1]] = ll[2].strip().split()

    print "validating"
    pp(rules[ll[1]])

    # lose this block...
    """
    for r in rules[ll[1]]: 
      pp("asserting: %s" % r)
      try:
        assert(type(r) == 'unicode')
      except AssertionError:
        print("apparently it's a %s..." % type(rules[ll[1]]))
      exit(1)
    """

  for ruleid in rules:
    text = rules[ruleid]

    if False:
      print("RuleID: " + ruleid)
      pp(text)
      print("====")

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
    
  for ruleid in rules:
    print("building cluster around %s..." % ruleid)
    c, m = k_cluster(ruleid, 1, sims[ruleid])
    print("min distance: %f" % m)
    if m <= MIN: 
      print("Cluster found: [%s] %s" % (ruleid, rules[ruleid]))
      ## print("Cluster found: [%s] %s" % (ruleid, u' '.join(rules[ruleid])))

      rule_text = u' '.join(rules[ruleid])
      pp(rule_text)
      print type(rule_text)

      msg = u'Cluster found: ['
      msg += ruleid
      msg += u']: '
      msg += (rule_text)
      print (msg)

      print(u"Cluster found: [%s] %s" % (ruleid, rule_text))
      print([(r, ' '.join(rules[r])) for r in c]) 
    # else: print("no strong cluster found")

