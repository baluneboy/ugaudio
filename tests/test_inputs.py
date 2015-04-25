#!/usr/bin/env python

import os
import sys
import unittest
import tempfile
from ugaudio.inputs import parse_args

class InputsTestCase(unittest.TestCase):
    """
    Test suite for ugaudio.inputs.
    """

    def setUp(self):
        """
        Get set up for tests.
        """        
        # create temp file
        self.file_object = tempfile.NamedTemporaryFile()
        self.filename = self.file_object.name

    def test_with_empty_or_bad_args(self):
        """
        When no args, this should fail with SystemExit, sys.exit(2).
        """
        # temporarily suppress stdout and stderr
        _stderr = sys.stderr
        _stdout = sys.stdout
        with open(os.devnull, 'wb') as null:
            sys.stdout = sys.stderr = null

            # try to parse arguments with empty command line args
            with self.assertRaises(SystemExit) as cm:
                sys.argv[1:] = []                
                mode, axis, rate, taper, files = parse_args()
            # now we should get 2 as code because of sys.exit(2)
            self.assertEqual(cm.exception.code, 2)
                
            # try to parse arguments with bad axis arg "w"
            with self.assertRaises(SystemExit) as cm:
                sys.argv[1:] = ['-a', 'w', self.filename]
                mode, axis, rate, taper, files = parse_args()
            # now we should get 1 as code because of sys.exit(1)
            self.assertEqual(cm.exception.code, 1)
            
            # try to parse arguments with bad rate
            with self.assertRaises(SystemExit) as cm:
                sys.argv[1:] = ['-r', '-120', self.filename]
                mode, axis, rate, taper, files = parse_args()
            # now we should get 1 as code because of sys.exit(1)
            self.assertEqual(cm.exception.code, 1)

            # try to parse arguments with bad taper values
            for t in ['-120', '123.45']:
                with self.assertRaises(SystemExit) as cm:
                    sys.argv[1:] = ['-t', t, self.filename]
                    mode, axis, rate, taper, files = parse_args()
                # now we should get 1 as code because of sys.exit(1)
                self.assertEqual(cm.exception.code, 1)
        
        # restore stdout and stderr
        sys.stderr = _stderr
        sys.stdout = _stdout            

    def test_some_variations(self):
        """
        Test all modes (aiff, plot, and demo).
        """
        
        # change input arguments for demo mode
        sys.argv[1:] = ['-m', 'demo']
        mode, axis, rate, taper, files = parse_args()
        self.assertEqual(mode, 'demo')
        
        # change input arguments for aiff mode
        sys.argv[1:] = ['-m', 'aiff', self.filename]
        mode, axis, rate, taper, files = parse_args()
        self.assertEqual(mode, 'aiff')
        self.assertEqual(axis, 's')
        self.assertEqual(rate, 0)
        self.assertEqual(taper, 0)
        self.assertEqual(len(files), 1)
        
        # change input arguments for plot mode
        sys.argv[1:] = ['-m', 'plot', self.filename, self.filename]
        mode, axis, rate, taper, files = parse_args()
        self.assertEqual(mode, 'plot')
        self.assertEqual(axis, 's')
        self.assertEqual(rate, 0)
        self.assertEqual(taper, 0)
        self.assertEqual(len(files), 2)

        # change input arguments for axis and taper
        for ax in 'xyzs4':
            for r in [0, 100, 200]:
                for t in [0, 1234, 4567]:
                    sys.argv[1:] = ['-a', ax, '-r', str(r), '-t', str(t), self.filename]
                    mode, axis, rate, taper, files = parse_args()
                    self.assertEqual(mode, 'aiff')
                    self.assertEqual(axis, ax)
                    self.assertEqual(rate, r)
                    self.assertEqual(taper, t)
                    self.assertEqual(len(files), 1)    

def suite():
    return unittest.makeSuite(InputsTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=2)