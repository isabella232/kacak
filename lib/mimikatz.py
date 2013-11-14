#!/usr/bin/env python
# -*- coding: utf-8 -*-

__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '10.10.2013'


try:
    	import sys
	import re
	from lib.common import *
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


class Mimikatz:
	def __init__(self, mimikatz_file):
		self.mimikatz_file = mimikatz_file
		self.mimikatz_start = re.compile("kerberos")
		self.mimikatz_info = re.compile("\*\s([^\s]+)\s*:\s([^$]+$)")


	def run(self):
		read_file = open(self.mimikatz_file, "r").read().splitlines()
		result = {}
		username = ""
		password = ""		

		control = 0
     		for line in read_file:
          		if re.search(self.mimikatz_start, line):
				control = 1

			elif (control == 1) and (re.search(self.mimikatz_info, line)):
				user_info = re.search(self.mimikatz_info, line).groups(0)
				if user_info[0] == "Username":
					username = user_info[1]
					if username and not username == "(null)" and not username in result.keys():
						result[username] = ""

				elif user_info[0] == "Password":
					password = user_info[1]
					if password and username and not password == "(null)":
                                                result[username] = password
						username = ""
						password = ""

			elif (control == 1) and (not re.search(self.mimikatz_info, line)):
				control = 0

		for user in sorted(result, key=result.get, reverse=False):
  			print bcolors.OKBLUE + "Kadi: " + bcolors.ENDC + bcolors.OKGREEN + "%s"% (user) + bcolors.ENDC + bcolors.OKBLUE + " Parola: " + bcolors.ENDC + bcolors.OKGREEN + "%s"% (result[user]) + bcolors.ENDC
