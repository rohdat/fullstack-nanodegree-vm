import os
os.remove(os.getcwd()+'/'+'puppyshelter.db')
import code
execfile("puppies.py")
execfile("puppypopulator.py")
code.interact(local=locals())

