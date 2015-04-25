#!/usr/bin/env python

import unittest
import warnings
import numpy as np
from ugaudio.signal import normalize
from ugaudio.signal import clip_at_third, my_taper, timearray
#from ugaudio.signal import speed_scale, stretch, pitch_shift
from ugaudio.create import AlternateIntegers

class SignalTestCase(unittest.TestCase):
    """
    Test suite for ugaudio.signal.
    """

    def setUp(self):
        """
        Get set up for tests.
        """        
        # create simple test signals
        self.unnormalized_object = AlternateIntegers(value=9, numpts=5)
        self.untapered_objects = [ AlternateIntegers(value=100, numpts=N) for N in range(30, 92) ]

    def test_normalize(self):
        """
        Tests the normalize function.
        """
        unnormalized = self.unnormalized_object.signal
        normalized = normalize( unnormalized )
        
        # if normalized, then max abs value is 1 (true in general)
        self.assertTrue( max(abs(normalized)) == 1 )
        
        # compare extremes (these are true for our special test signal)
        self.assertEqual(-1, np.min(normalized))
        self.assertEqual(+1, np.max(normalized))
        self.assertEqual(-9, np.min(unnormalized))
        self.assertEqual(+9, np.max(unnormalized))

    def test_clip_at_third(self):
        """
        Tests the clip_at_third function.
        """
        # test warning regarding tapering too many pts
        with warnings.catch_warnings(record=True) as w:
            # cause all warnings to always be triggered
            warnings.simplefilter("always")
            # trigger warning with signal too short for desired taper params
            N = clip_at_third(range(5), 1, 99)
            # verify a few key aspects of warning
            assert len(w) == 1
            assert issubclass(w[-1].category, RuntimeWarning)
            assert "tapering a third" in str(w[-1].message)
            self.assertEqual(N, 1)
        
        # this signal should now just make the cut
        numpts = clip_at_third( range(33), 1, 11)
        self.assertEqual(numpts, 11)

    def test_timearray(self):
        """
        Tests the timearray function.
        """
        fs = 1
        for i in range(2, 102):
            sig = range(i)
            t = timearray(sig, fs)
            self.assertEqual(len(t), len(sig))
            self.assertEqual(t[0], 0)
            self.assertEqual(t[-1], (len(t) - 1) / fs) 

    def test_my_taper(self):
        """
        Tests the my_taper function.
        """
        fs, t = 1, 10
        for i in self.untapered_objects:
            not_tapered = i.signal
            tapered = my_taper(not_tapered, fs, t)
            Nactual = clip_at_third(not_tapered, fs, t)
            Nmidtaper = Nactual // 2
            
            # compare endpts (true in general)
            self.assertEqual(tapered[0],  0)
            self.assertEqual(tapered[-1], 0)
            
            # compare midpt(s) (true in general)
            for idx in i.idx_midpts:
                self.assertEqual(tapered[idx], not_tapered[idx])
                self.assertEqual(np.abs(tapered[idx]), 100)
            
            # compare taper regions (probably not all true in general)
            self.assertEqual( np.abs(not_tapered[ Nmidtaper]), 100 )
            self.assertEqual( np.abs(not_tapered[-Nmidtaper]), 100 )      
            self.assertLess( np.abs(tapered[ Nmidtaper]),       51 )
            self.assertLess( np.abs(tapered[-Nmidtaper]),       51 )

    @unittest.skip("not implemented yet")
    def test_spectrogram(self):
        """
        Tests spectrogram method if matplotlib is installed.
        """
        # FIXME model after obspy testing?
        try:
            import matplotlibADDEDTHISFORBADPART  # @UnusedImport
        except ImportError:
            return
        self.mseed_stream.spectrogram(show=False)

def suite():
    return unittest.makeSuite(SignalTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=2)