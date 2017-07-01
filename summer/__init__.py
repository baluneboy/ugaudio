"""A package for summer code."""

from os.path import dirname, basename, isfile
import glob

# glob *.py files
modules = glob.glob(dirname(__file__)+"/week?/*.py")
#print modules

__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]