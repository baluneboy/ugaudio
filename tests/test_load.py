#!/usr/bin/env python

import os
import unittest
import tempfile
import numpy as np
from ugaudio.pad import PadFile
from ugaudio.load import padread, aiffread
from ugaudio.create import AlternateIntegers, padwrite

# Test suite for ugaudio.create.
class LoadTestCase(unittest.TestCase):
    """
    Test suite for ugaudio.load.
    """

    def setUp(self):
        """
        Get set up for tests.
        """        
        # create simple test signals
        tests_dir = os.path.dirname(__file__)
        examples_dir = os.path.join(os.path.dirname(tests_dir), 'examples')
        self.pad_file = os.path.join(examples_dir, '2014_10_17_06_31_15.515+2014_10_17_06_41_15.528.121f02')

    def test_padread(self):
        """
        Test padread function with actual PAD file sample.
        """
        arr = padread(self.pad_file)
        
        # verify sample rate
        fs = 1.0 / arr[1, 0]
        self.assertAlmostEqual(fs, 500.0, places=3)
        
        # verify length of array
        self.assertEqual(arr.shape[0], 300003)
        
        # verify first and last row of values
        np.testing.assert_almost_equal(arr[ 0, :],
                                        [0.00000000e+00, 4.64045570e-06,
                                        4.52020868e-05, -3.04387271e-04],
                                        decimal=6)
        np.testing.assert_almost_equal(arr[-1, :],
                                        [6.00013367e+02, -2.88429856e-03,
                                        1.06823947e-02, -4.05408442e-03],
                                        decimal=6) 

    def test_aiffread(self):
        """
        Test aiffread function.
        """
        pf = PadFile(self.pad_file)
        pf.convert()
        aiff_file = self.pad_file + 's.aiff'
        arr, params = aiffread(aiff_file)

        # verify sample rate
        fs = params[2]
        self.assertAlmostEqual(fs, 500.0, places=3)
        
        # verify length of array
        self.assertEqual(arr.shape[0], 300003)
        
        # verify first and last row of values
        np.testing.assert_array_equal(arr[0:3], [-323, -147,  328])  
        np.testing.assert_array_equal(arr[-3:], [  18, 1033, 3690]) 

def suite():
    return unittest.makeSuite(LoadTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=2)
