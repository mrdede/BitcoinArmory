################################################################################
#                                                                              #
# Copyright (C) 2011-2013, Armory Technologies, Inc.                           #
# Distributed under the GNU Affero General Public License (AGPL v3)            #
# See LICENSE or http://www.gnu.org/licenses/agpl.html                         #
#                                                                              #
################################################################################
import sys
from utilities.ArmoryUtils import SplitSecret, binary_to_hex, ReconstructSecret,\
   FiniteFieldError
import itertools
sys.argv.append('--nologging')
import unittest


SECRET = '\x00\x01\x02\x03\x04\x05\x06\x07'

BAD_SECRET = '\xff\xff\xff\xff\xff\xff\xff\xff'

# Fragment combination to String abreviated name for debugging purposes
def c2s(combinationMap):
   return '\n'.join([' '.join([str(k), binary_to_hex(v[0]), binary_to_hex(v[1])]) \
                      for k,v in combinationMap.iteritems()])
   
def splitSecretToFragmentMap(splitSecret):
   fragMap = {}
   for i,frag in enumerate(splitSecret):
      fragMap[i] = frag
   return fragMap


class Test(unittest.TestCase):

   def setUp(self):
      pass
      
   def tearDown(self):
      pass

   def getNextCombination(self, fragmentMap, m):
      combinationIterator = itertools.combinations(fragmentMap.iterkeys(), m)
      for keyList in combinationIterator:
         combinationMap = {}
         for key in keyList:
            combinationMap[key] = fragmentMap[key] 
         yield combinationMap
   
   
   def subtestAllFragmentedBackups(self, secret, m, n):
      fragmentMap = splitSecretToFragmentMap(SplitSecret(secret, m, n))
      for combinationMap in self.getNextCombination(fragmentMap, m):
         print c2s(combinationMap)
         print
         fragmentList = [value for value in combinationMap.itervalues()]
         reconSecret = ReconstructSecret(fragmentList, m, len(secret))
         self.assertEqual(reconSecret, secret)
         

   def testFragmentedBackup(self):

      self.subtestAllFragmentedBackups(SECRET, 2, 3)
      self.subtestAllFragmentedBackups(SECRET, 5, 7)
      self.subtestAllFragmentedBackups(SECRET, 2, 12)

      # Secret Too big test
      self.assertRaises(FiniteFieldError, SplitSecret, BAD_SECRET, 2,3)

      # More needed than pieces
      self.assertRaises(FiniteFieldError, SplitSecret, SECRET, 4,3)
      
      # Secret Too many needed needed
      fragmentList = SplitSecret(SECRET, 9, 12)
      self.assertEqual(len(fragmentList), 0)

      # Too few pieces needed
      fragmentList = SplitSecret(SECRET, 1, 12)
      self.assertEqual(len(fragmentList), 0)
      
if __name__ == "__main__":
   unittest.main()