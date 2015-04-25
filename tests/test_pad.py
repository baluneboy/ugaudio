#!/usr/bin/env python

import os
import aifc
import unittest
import numpy as np
from numpy.testing import assert_array_equal
import tempfile
from ugaudio.create import write_chirp_pad, write_rogue_pad_file
from ugaudio.pad import PadFile
from ugaudio.load import aiffread

class PadTestCase(unittest.TestCase):
    """
    Test suite for ugaudio.signal.
    """

    def setUp(self):
        """
        Get set up for tests.
        """        
        # create good, dummy pad file
        self.pad_file_object = tempfile.NamedTemporaryFile(delete=False)
        self.pad_filename = self.pad_file_object.name
        write_chirp_pad(self.pad_filename)
        self.pad_file_object.close()

        # create good, somewhat legitimate pad header file
        self.dummyrate = 123.456
        self.pad_header_filename = self.pad_filename + '.header'
        with open(self.pad_header_filename, 'w') as hf:
            hf.write("one\n<SampleRate>%f</SampleRate>\n3" % self.dummyrate)
        
        # create rogue pad file (without header file)  
        self.rogue_file_object = tempfile.NamedTemporaryFile(delete=False)
        self.rogue_filename = self.rogue_file_object.name
        write_rogue_pad_file(self.rogue_filename)
        self.rogue_file_object.close()
        
        # create bad, dummy pad file
        self.bad_file_object = tempfile.NamedTemporaryFile(delete=False)
        self.bad_filename = self.bad_file_object.name
        self.bad_file_object.write("bad")
        self.bad_file_object.close()
        
    def test_is_pad(self):
        """
        Tests the is_pad method.
        """
        # test simple, good (dummy) pad file
        good_pad_file = PadFile(self.pad_filename)
        self.assertTrue(good_pad_file.ispad)
        
        # test non-pad file
        not_pad_file = PadFile(self.bad_filename)
        self.assertFalse(not_pad_file.ispad)        

    def test_get_headerfile(self):
        """
        Tests the get_headerfile method.
        """    
        # test simple, good (dummy) pad file
        good_pad_file = PadFile(self.pad_filename)
        self.assertTrue(good_pad_file.ispad)
        
        # test header file exists
        header_file = good_pad_file.headerfile
        self.assertTrue( os.path.exists(header_file) )
        
    def test_get_samplerate_with_header_file(self):
        """
        Tests the get_samplerate method via header file.
        """    
        # test simple, good (dummy) pad file
        good_pad_file = PadFile(self.pad_filename)
        self.assertTrue(good_pad_file.ispad)
        
        # test header file exists
        header_file = good_pad_file.headerfile
        self.assertTrue( os.path.exists(header_file) )
        
        # test it's got dummy sample rate
        self.assertEqual( good_pad_file.samplerate, self.dummyrate )

    def test_get_samplerate_without_header_file(self):
        """
        Tests the get_samplerate method using _reckon_rate.
        """    
        # test simple, good (dummy) pad file [rogue without header]
        rogue_pad_file = PadFile(self.rogue_filename)
        self.assertTrue(rogue_pad_file.ispad)
        
        # make sure header file does not exist (that is, it's None)
        self.assertIsNone( rogue_pad_file.headerfile )
        
        # test its dummy sample rate
        self.assertEqual( rogue_pad_file.samplerate, 1.0 )

    def test_convert_with_defaults(self):
        """
        Tests the convert method with defaults.
        That is, at native rate, s-axis, no plot, and no taper.
        """

        # convert simple rogue pad file to aiff
        rogue_pad_file = PadFile(self.rogue_filename)
        rogue_pad_file.convert()
        
        # get array from aiff file
        s, params = aiffread( rogue_pad_file.filename + 's.aiff' )
        assert_array_equal(s, np.array([-2268, 10127, -9559, 17418, -16851, 24709, -24142, 32000, -31433]) )

    #@unittest.skip("not implemented yet")
    def test_convert_new_rate(self):
        """
        Tests the convert method with new rate instead of default.
        """
        # convert simple rogue pad file to aiff
        new_rate = 22050
        rogue_pad_file = PadFile(self.rogue_filename)
        rogue_pad_file.convert(rate=new_rate)
        
        # get array from aiff file
        aiff_file = rogue_pad_file.filename + 's.aiff'
        f = aifc.open(aiff_file, 'r')
        aiff_rate = f.getframerate()
        f.close()
        self.assertEqual(new_rate, aiff_rate)
        
def suite():
    return unittest.makeSuite(PadTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=2)