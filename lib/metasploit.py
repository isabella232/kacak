__VERSION__ = '2.0'
__AUTHOR__ = 'Galkan'
__DATE__ = '2014'

 
try:
    	import sys
    	import time
    	import msfrpc
    	import re
    	import os
    	import tempfile 	
	import socket
	from xml.etree.cElementTree import parse, iterparse, ElementTree
	from lib.common import *
except ImportError,e:
   	import sys
    	sys.stdout.write("%s" %e)
    	sys.exit(1)


class MetaSploit:
	def verbose(self, description,string):
                print >> sys.stderr, bcolors.WARNING + "[ - ]  %s -->  "% (description) + bcolors.ENDC + bcolors.OKBLUE + "%s"% (string) + bcolors.ENDC


	def __init__(self, ip_file, verbose):
		self.ip_file = ip_file
		self.result_reg = re.compile("\[\*\]\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\s:\s(.*)")
		self.verbose_opt = verbose
		
		self.client = msfrpc.Msfrpc({'port':55552, 'host':'127.0.0.1'})
		try:
        		self.client.login('msf','msf')
		except socket.error:
			print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + "Can't Connect to MSFRPC Service, Please Checck this using this command netstat -nlput | grep '55552'" + bcolors.ENDC
			sys.exit(2)

        	self.resource = self.client.call('console.create')
        	self.console_id = self.resource['id']
	
		if self.verbose_opt >= 3:
			self.verbose("Console Id", self.console_id)
			self.verbose("Resource", self.resource)
	

	def parse_config_file(self, config_file):
		result = []
		try:	
			xml_element = parse(config_file).getroot()
		except:
			print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + "It isn't a valid xml File !!!" + bcolors.ENDC
			sys.exit(3)

		for menu in xml_element:
		
			result_list = {}
			for sub_menu in menu:
				if sub_menu.tag == "name":
					domain_name = sub_menu.text
					result_list["domain_name"] = sub_menu.text
				elif sub_menu.tag == "username":
					user_name = sub_menu.text
					result_list["user_name"] = sub_menu.text
				elif sub_menu.tag == "password":
                                        password = sub_menu.text
					result_list["password"] = sub_menu.text
				elif sub_menu.tag == "threads":
                                        threads = sub_menu.text
					result_list["threads"] = sub_menu.text
			result.append(result_list)

		return result	


	def create_command_and_console_file(self, user_cred):
		ip_file = self.ip_file
                console_file = tempfile.NamedTemporaryFile(mode='w+t')

                console_file.write("use auxiliary/scanner/smb/smb_enumusers_domain\n")
                console_file.write("set RHOSTS file:%s\n"% (ip_file))

                for user_info in user_cred.keys():
                        if user_info == "domain_name":
                                console_file.write("set SMBDomain %s\n"% user_cred[user_info])
                        elif user_info == "password":
                                console_file.write("set SMBPass %s\n"% user_cred[user_info])
                        elif user_info == "threads":
                                console_file.write("set THREADS %s\n"% user_cred[user_info])
                        elif user_info == "user_name":
                                console_file.write("set SMBUser %s\n"% user_cred[user_info])

                console_file.write("run\n")
                console_file.seek(0)
                commands = console_file.readlines()
                console_file.close()

                return commands


	def parse_msf_output(self, msf_output_file, domain_users_file):
		msf_output_file.seek(0)

		result = {}
		for result_line in msf_output_file:
			ip_addr = result_line.split(":")[0]
			username_infos = result_line.split(":")[1]

			for _user_file_line in open(domain_users_file, "r"):
				if _user_file_line:
					user_file_line = _user_file_line.split("\n")[0]
					substitue_line = re.sub("\\\\", "\\\\\\\\", user_file_line)

					subs_reg = re.compile("(%s)(,|$)"% substitue_line, re.IGNORECASE)

					full_user_name = ''
					for line in username_infos:
						if (not ord(line) == 0) and (not ord(line) == 10):
							full_user_name = full_user_name + line
						
					for user in full_user_name.split(" "):
						if re.search(subs_reg, user):
							user_name = re.search(subs_reg,user).groups(1)[0]
							if not ip_addr in result.keys():
								result[ip_addr] = user_name
							else:
								if not result[ip_addr] == user_name:
									result[ip_addr] = result[ip_addr] + ", " + user_name


		if result.keys():
			for ip_list in result.keys():
                		print bcolors.OKGREEN + "   [+] %s -> %s"% (ip_list, result[ip_list]) + bcolors.ENDC
		else:
			print bcolors.OKGREEN + " -- Empty --" + bcolors.ENDC

		msf_output_file.close()		
	


	def run_msf(self, domain_users_file, commands):
		output_file = tempfile.NamedTemporaryFile(mode='w+t')

		if self.verbose_opt >= 2:
			self.verbose("Output File Name", output_file.name)

		for cmd in commands:
			if self.verbose_opt >= 3:
				self.verbose("Command", cmd)

			self.resource = self.client.call('console.write',[self.console_id, cmd]) 

                        time.sleep(1)
                        while True:
				self.resource = self.client.call('console.read',[self.console_id])

				if self.verbose_opt >= 3:
					self.verbose("Resource", self.resource)

                                if len(self.resource['data']) > 1:
					if self.verbose_opt >= 2:
                                        	self.verbose("Resource Data", self.resource['data'])
				
                                        if re.search(self.result_reg, self.resource["data"]):
                                               result = ""
                                               for line in self.resource["data"]:
                                                       if not line == "\n":
                                                               result = result + line
                                                       else:
                                                               if re.match(self.result_reg, result):
                                                               		ip_address = re.match(self.result_reg, result).groups(1)[0]
                                                                      	username_info = re.search(self.result_reg, result).groups(1)[1]
                                        
                                                                       	result = ip_address + ":" + username_info + "\n"
									
									if self.verbose_opt >= 3:
										self.verbose("Result", result)										
                                                                       	output_file.write(result)
                                                               result = ""

                                if self.resource['busy'] == True:
                                        time.sleep(1)
                                        continue
                                break

                self.parse_msf_output(output_file, domain_users_file)
