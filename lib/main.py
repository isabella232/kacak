__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '10.10.2013'

 
try:
    	import sys
	import argparse
	import os
	import re
	from lib.common import *
except ImportError,e:
   	import sys
    	sys.stdout.write("%s\n" %e)
	sys.exit(1)

 

class AddressAction(argparse.Action):
        def is_file_exists(self, file_list):
		for file in file_list[0],file_list[2]:
			if not re.match("/", file):		
				print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + "%s: Full Path Must Be Used </usr/local/data/data.txt>"% (file) + bcolors.ENDC
				sys.exit(2)				

		for file in file_list:
                        if not os.path.exists(file):
                                print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + "The file \"%s\" doesn't Exists On The System !!!"% (file) + bcolors.ENDC
                                sys.exit(3)



        def __call__(self, parser, args, values, option = None):
                args.options = values
                if args.domain and not len(args.options) == 3:
                        parser.error("Usage --domain <users_file> <config_file> <ip_file>")
                elif args.mimikatz and not len(args.options) == 1:
                        parser.error("Usage --mimikatz <mimikatz_result_file>")
                #elif args.smbvuln and not len(args.options) == 1:
                #        parser.error("Usage --smb-vuln <ip_file>")

		if args.domain:
                	self.is_file_exists(args.options)



class Main:
	def __init__(self):
		parser = argparse.ArgumentParser()
		group_parser = parser.add_mutually_exclusive_group(required=True)

		group_parser.add_argument('--domain', dest='domain', action='store_const', const='domain', help="Road to Domain Admin ")
                group_parser.add_argument('--mimikatz', dest='mimikatz', action='store_const', const='mimikatz', help="Parse Mimikatz Results")
                #group_parser.add_argument('--smb-vuln', dest='smbvuln', action='store_const',     const='smbvuln', help="Discover the vulnerabily ip which has 08_067")

                parser.add_argument('options', nargs='*', action = AddressAction)
                parser.add_argument('--verbose', '-v', action = 'store', dest = 'verbose', type=int)
                self.args = parser.parse_args()

		if (self.args.verbose) and (self.args.verbose < 0 or self.args.verbose >3):
			print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + "Verbose value must be between 1 and 3" + bcolors.ENDC
			sys.exit(4)


	def run_domain(self):
		try:
                	from lib.domain import DoMain
                except ImportError,e:
                        sys.stdout.write("%s\n" %e)
                        sys.exit(5)

                domain_users_file = self.args.options[0]
                config_file = self.args.options[1]
                ip_file = self.args.options[2]

		verbose = self.args.verbose
                domain = DoMain(domain_users_file, config_file, ip_file, verbose)
                domain.run()


	def run_mimikatz(self):
		try:
                	from lib.mimikatz import Mimikatz
                except ImportError,e:
                        sys.stdout.write("%s\n" %e)
                        sys.exit(6)

		verbose = self.args.verbose
                mimikatz_file = self.args.options[0]

                mimikatz = Mimikatz(mimikatz_file)
                mimikatz.run()

		
	def run_smbvuln(self):
		verbose = self.args.verbose
		print "Smb Vuln"


        def run(self):
		if self.args.domain:
			self.run_domain()
		elif self.args.mimikatz:
			self.run_mimikatz()
		#elif self.args.smbvuln:
		#	self.run_smbvuln()
