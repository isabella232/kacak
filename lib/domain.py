#!/usr/bin/env python
# -*- coding: utf-8 -*-

__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '10.10.2013'

try:
	import os
	import sys
	from lib.metasploit import MetaSploit
	from lib.common import *
except ImportError,e:
        import sys
        sys.stdout.write("%s" %e)
        sys.exit(1)



class DoMain:
	def __init__(self, domain_users_file, config_file, ip_file, verbose):
		self.domain_users_file = domain_users_file
		self.config_file = config_file
		self.ip_file = ip_file
		self.verbose_opt = verbose


	def run(self):
		for check_file in self.domain_users_file, self.config_file, self.ip_file:
                	if not os.path.exists(check_file):
                        	print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + "%s : File Doesn't Exists on System !!!\n"% (check_file) + bcolors.ENDC
                        	sys.exit(2)

        	msf = MetaSploit(self.ip_file, self.verbose_opt)
        	user_cred = msf.parse_config_file(self.config_file)


		if self.verbose_opt >= 1:
			msf.verbose("Config File's Options", user_cred)


        	for user_info in user_cred:
                	print bcolors.OKGREEN + "\n[+] Domain: " + bcolors.ENDC + bcolors.OKGREEN + "%s"% user_info["domain_name"] + bcolors.ENDC

                	commands = msf.create_command_and_console_file(user_info)
			if self.verbose_opt >= 1:
				msf.verbose("Commands", commands)

                	msf.run_msf(self.domain_users_file, commands)
