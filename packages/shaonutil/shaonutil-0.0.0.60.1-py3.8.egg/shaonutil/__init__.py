#from shaonutil.stats import ClassA
from os.path import dirname, basename, isfile, join
import glob
import shaonutil

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
#print('\n'.join(['- '+a for a in __all__]))

for module_name in __all__:
	__import__('shaonutil'+'.'+module_name)
	getattr(shaonutil, module_name)