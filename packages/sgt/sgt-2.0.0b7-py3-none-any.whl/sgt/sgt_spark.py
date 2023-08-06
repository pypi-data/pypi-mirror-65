import numpy as np
import pandas as pd
from itertools import chain
import warnings
    
def sgt_spark(sequence, alphabets, kappa, flatten, lengthsensitive):
  '''
  Extract Sequence Graph Transform features using Algorithm-2.

        sequence            An array of discrete elements. For example,
                            np.array(["B","B","A","C","A","C","A","A","B","A"].

        return: sgt matrix or vector (depending on Flatten==False or True)

  '''

  def getpositions(sequence, alphabets):
    '''
        Compute index position elements in the sequence
        given alphabets set.

        Return list of tuples [(value, position)]
    '''
    positions = [(v, np.where(sequence == v))
                     for v in alphabets if v in sequence]

    return positions
      
  sequence = np.array(sequence)
    
  size = len(alphabets)
  l = 0
  W0, Wk = np.zeros((size, size)), np.zeros((size, size))
  positions = getpositions(sequence, alphabets)

  alphabets_in_sequence = np.unique(sequence)

  for i, u in enumerate(alphabets_in_sequence):
    index = [p[0] for p in positions].index(u)

    U = np.array(positions[index][1]).ravel()

    for j, v in enumerate(alphabets_in_sequence):
      index = [p[0] for p in positions].index(v)

      V2 = np.array(positions[index][1]).ravel()

      C = [(i, j) for i in U for j in V2 if j > i]

      cu = np.array([ic[0] for ic in C])
      cv = np.array([ic[1] for ic in C])

      # Insertion positions
      pos_i = alphabets.index(u)
      pos_j = alphabets.index(v)

      W0[pos_i, pos_j] = len(C)

      Wk[pos_i, pos_j] = np.sum(np.exp(-kappa * np.abs(cu - cv)))

    l += U.shape[0]

  if lengthsensitive:
    W0 /= l

  W0[np.where(W0 == 0)] = 1e7  # avoid divide by 0

  sgt = np.power(np.divide(Wk, W0), 1/kappa)

  if(flatten):
    sgt = sgt.flatten()
  else:
    sgt = pd.DataFrame(sgt)
    sgt.columns = alphabets
    sgt.index = alphabets

  return sgt