#!/usr/bin/env python

__VERSION__ = '2.0'
__AUTHOR__ = 'Galkan'
__DATE__ = '2014'


try:
	import sys
	from lib.version import *
	from lib.main import Main
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)
 
##
### Main go go go ...
##

if __name__ == "__main__":
	try:
	    main = Main()
	    main.run()
	except KeyboardInterrupt:
            print message
            sys.exit(2)

	    