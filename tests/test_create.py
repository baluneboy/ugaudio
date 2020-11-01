#!/usr/bin/env python

import unittest
import tempfile
import numpy as np
from ugaudio.load import pad_read, aiffread
from ugaudio.create import AlternateIntegers, padwrite, uncompressed_aiff2pad

# Test suite for ugaudio.create.
class CreateTestCase(unittest.TestCase):
    """
    Test suite for ugaudio.create.
    """

    def setUp(self):
        """
        Get set up for tests.
        """        
        # create simple test signals
        self.alt_ints = AlternateIntegers(value=5, numpts=10)
        self.sample_rate = 10

        # temp file to serve as AIFF file
        self.aiff_file_object = tempfile.NamedTemporaryFile(delete=False)
        self.aiff_filename = self.aiff_file_object.name

    def test_padwrite(self):
        """
        Test the padwrite function.
        """
        fs = self.sample_rate
        x = self.alt_ints.signal # alternating ints: +5, -5,...
        y = x + 2
        z = x - y
        
        # write simple pad file (and get time vector)
        self.pad_file_object = tempfile.NamedTemporaryFile(delete=False)
        self.pad_filename = self.pad_file_object.name
        t = padwrite(x, y, z, fs, self.pad_filename, return_time=True)
        self.pad_file_object.close()
        txyz = np.c_[ t, x, y, z ] # this we wrote to file
        
        # FIXME this is flimsy here because we rely on our own padread
        txyzfile = pad_read(self.pad_filename)

        # verify each column (t,x,y,z) from file closely matches expected value
        small_delta = 1e-6 # true for our simple integer case with fs = 1 sa/sec
        for i in range( txyzfile.shape[1] ):
            self.assertLess( np.max( np.abs(txyzfile[:, i] - txyz[:, i]) ), small_delta)

    def test_alternate_integers(self):
        """
        Test AlternateIntegers class.
        """
        # construct simple case
        ai = AlternateIntegers()
        self.assertEqual(ai.value, 9)
        self.assertEqual(ai.numpts, 5)
        self.assertEqual(ai.idx_midpts, [2])
        self.assertEqual(len(ai.signal), 5)
        np.testing.assert_array_equal (ai.signal, [+9, -9, +9, -9, +9])
        
        # construct case with even numpts to verify idx_midpts
        ai = AlternateIntegers(value=2, numpts=6)
        self.assertEqual(ai.idx_midpts, [2, 3])
        np.testing.assert_array_equal(ai.signal, [+2, -2, +2, -2, +2, -2])

    def test_alternate_integers_aiffwrite(self):
        """
        Test aiffwrite method of AlternateIntegers class.
        """        
        # construct simple case
        ai = AlternateIntegers(numpts=22050) # gives one-second of "sound"
        ai.aiffwrite(self.aiff_filename)

        # read AIFF file
        arr, params = aiffread(self.aiff_filename)
        self.assertEqual(len(arr), 22050)
        self.assertEqual(arr[0], 32000)
        self.assertEqual(min(arr), -32000)
        self.assertEqual(max(arr),  32000)

    def test_uncompressed_aiff2pad(self):
        """
        Test uncompressed_aiff2pad function.
        """
        # write simple AIFF file
        ai = AlternateIntegers(numpts=11025) # gives half-second of "sound"
        ai.aiffwrite(self.aiff_filename)
        
        # convert uncompressed AIFF to PAD format
        uncompressed_aiff2pad(self.aiff_filename)
        
        # read PAD file
        pad_file = self.aiff_filename + '.pad'
        arr = pad_read(pad_file)
        
        # verify sample rate
        fs = 1.0 / arr[1, 0]
        self.assertAlmostEqual(fs, 22050.0, places=3)
        
        # verify first 2 rows of values and length of array
        np.testing.assert_array_equal (arr[0, :], [0.0, 32000.0, -16000.0, -16000.0])
        np.testing.assert_array_equal (arr[1, 1:], [-32000.0, 16000.0, 16000.0])
        self.assertEqual(arr.shape[0], 11025)
                
def suite():
    return unittest.makeSuite(CreateTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=2)
