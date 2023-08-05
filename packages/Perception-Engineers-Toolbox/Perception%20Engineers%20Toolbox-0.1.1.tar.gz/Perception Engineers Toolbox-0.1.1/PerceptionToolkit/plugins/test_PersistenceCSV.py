from unittest import TestCase
from plugins.PersistenceCSV import *
import numpy as np


class TestPersistenceCSV(TestCase):
    def test_str_arr2float_arr(self):
        self.assertTrue(np.alltrue(PersistenceCSV.strArr2floatArr(['1', '2']) == [1, 2]))
        self.assertTrue(np.alltrue(PersistenceCSV.strArr2floatArr(['1', '2', 'somestring']) == [1, 2, -1]))
        self.assertTrue(PersistenceCSV.strArr2floatArr([]) == [])
