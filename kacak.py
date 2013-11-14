#!/usr/bin/env python
# -*- coding: utf-8 -*-

__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '10.10.2013'


try:
	import sys
	from lib.main import Main
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)

##
### Main go go go ...
##

if __name__ == "__main__":
	main = Main()
	main.run()
