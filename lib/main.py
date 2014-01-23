__VERSION__ = '2.0'
__AUTHOR__ = 'Galkan'
__DATE__ = '2014'

 
try:
    	import sys
	import argparse
	import os
	import re
	from nmap import Nmap
	from common import *
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
                
		if args.domain:
                	self.is_file_exists(args.options)



class Main:
	"""
	  Main Class for Kacak
	"""
  
	def __init__(self):
	  
		description = "Enumerate Users for windows based networks"
		parser = argparse.ArgumentParser(description = description)
		group_parser = parser.add_mutually_exclusive_group(required=True)

		group_parser.add_argument('--domain', dest = 'domain', action = 'store_const', const = 'domain', help = "Road to Domain Admin ")
                group_parser.add_argument('--mimikatz', dest = 'mimikatz', action = 'store_const', const = 'mimikatz', help = "Parse Mimikatz Results")
                group_parser.add_argument('--08_067', dest = 'smbvuln', action = 'store', nargs = 1, help = "Discover the 08_067")
		parser.add_argument('--thread', '-t', dest = 'thread', action = 'store', help = "Thread Number")
		parser.add_argument('--output', '-o', dest = 'output_file', action = 'store', help = "File to Save Results")

                parser.add_argument('options', nargs='*', action = AddressAction)
                parser.add_argument('--verbose', '-v', action = 'store', dest = 'verbose', type = int)
                self.args = parser.parse_args()

		if self.args.smbvuln and not self.args.thread:
		     print >> sys.stderr, bcolors.OKBLUE + "Usage Error:" + bcolors.ENDC + bcolors.FAIL + "-t expects one argument" + bcolors.ENDC
		     sys.exit(4)
		elif self.args.smbvuln and not self.args.output_file:
		     print >> sys.stderr, bcolors.OKBLUE + "Usage Error:" + bcolors.ENDC + bcolors.FAIL + "-o expects one argument" + bcolors.ENDC
		     sys.exit(5)
	 
		if ( self.args.verbose ) and ( self.args.verbose < 0 or self.args.verbose > 3 ):
		    print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + "Verbose value must be between 1 and 3" + bcolors.ENDC
		    sys.exit(6)



	def run_domain(self):
		"""
		    Run smb_enum_domain_users metasploit module
		"""
	
                from domain import DoMain
		verbose = self.args.verbose
                
                domain_users_file = self.args.options[0]
                config_file = self.args.options[1]
                ip_file = self.args.options[2]

		domain = DoMain(domain_users_file, config_file, ip_file, verbose)
		
		try:
		    domain.run()
		except Exception, err:
		    print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + str(err) + bcolors.ENDC
		    sys.exit(7)



	def run_mimikatz(self):
		"""
		    Parse mimikatz results
		"""
	  
               	from lib.mimikatz import Mimikatz
		verbose = self.args.verbose
		
                mimikatz_file = self.args.options[0]
                mimikatz = Mimikatz(mimikatz_file)
                
                try:
		    mimikatz.run()
		except Exception, err:
		    print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + str(err) + bcolors.ENDC
		    sys.exit(8)
		
	
	
	def run_smbvuln(self):
		"""
		    Discover 08_067 
		"""
		
		verbose = self.args.verbose
		try:
		      nmap = Nmap(self.args.output_file)
		      nmap.run(self.args.smbvuln[0], self.args.thread)
		except Exception, err:
		    print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + str(err) + bcolors.ENDC
		    sys.exit(9)
		


        def run(self):
		"""
		    Select which function to run
		"""
	  
		if self.args.domain:
			self.run_domain()
		elif self.args.mimikatz:
			self.run_mimikatz()
		elif self.args.smbvuln:
			self.run_smbvuln()
