__VERSION__ = '2.0'
__AUTHOR__ = 'Galkan'
__DATE__ = '2014'

 
try:
    	import sys
	import re
	import os
	import subprocess
	import tempfile
	#import threading
	from Queue import Queue
	from threading import Thread
	from common import *
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)



class Worker(Thread):    
  
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
  
  
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
		func(*args, **kargs)
            except Exception, e:
		print e
		
            self.tasks.task_done()


class ThreadPool:    
  
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): 
	  Worker(self.tasks)


    def add_task(self, func, *args, **kargs):        
	self.tasks.put((func, args, kargs))
	
	
    def wait_completion(self):        
	self.tasks.join()



class Nmap:
	"""
	    Nmap Class ...
	"""
  
	def __init__(self, output_file):
		self.nmap = "/usr/bin/nmap"
		self.nmap_08067_script = "./scripts/smb-check-vulns.nse"
		self.opened_port_pattern = "Ports: 445/open/tcp//"
		
		if not os.path.exists(self.nmap):
		    print bcolors.OKBLUE + "Error: " + bcolors.ENDC + bcolors.FAIL + "%s: File Doesn\'t Exists on The System !!!"% (self.nmap) + bcolors.ENDC
		    sys.exit(2)
  
		try:
		    self.result_file = open(output_file, "w")  
		except Exception, err:
		    print bcolors.OKBLUE + "Error: " + bcolors.ENDC + bcolors.FAIL + str(err) + bcolors.ENDC
		    sys.exit(3)
	
	
	
	def run_08_067(self, ip):
		nmap_smb = "-n -Pn -sS -p 445 -T4  --script=%s --script-args=unsafe=1 %s "% (self.nmap_08067_script, ip)
		nmap_smb_command = "%s %s"% (self.nmap, nmap_smb)

		proc = subprocess.Popen([nmap_smb_command],
                        shell=True,
                        stdout=subprocess.PIPE,
		)
		
		stdout_value = str(proc.communicate())
	
		if stdout_value.find("MS08-067: VULNERABLE") > 0:
		    self.result_file.write("VULNERABLE : %s\n"% ip)  
		    print "VULNERABLE : %s"% ip
  
              
              
	def run(self, ip_list, thread_number):
		"""
		    08_067
		"""
		
		pool = ThreadPool(int(thread_number))
     	    
		try:
		      nmap_445_file = tempfile.NamedTemporaryFile(mode='w+t')
		      nmap_445_file_name = nmap_445_file.name
		except Exception, err:
                      print bcolors.OKBLUE + "Error: " + bcolors.ENDC + bcolors.FAIL + err + bcolors.ENDC
                      sys.exit(3)  
  
  
                nmap_445 = "-n -Pn -sS -T4 --open -p 445 --host-timeout=10m --max-rtt-timeout=600ms --initial-rtt-timeout=300ms --min-rtt-timeout=300ms --max-retries=2 --min-rate=150 %s -oG %s"% (ip_list, nmap_445_file_name)
                nmap_445_command = "%s %s"% (self.nmap, nmap_445)

                proc = subprocess.Popen([nmap_445_command],
                        shell=True,
                        stdout=subprocess.PIPE,
                        )

                stdout_value = str(proc.communicate())
                nmap_445_file.seek(0)
                for result in nmap_445_file:
		    if result.find(self.opened_port_pattern) > 0:
			ip = result.split(" ")[1]
			pool.add_task(self.run_08_067, ip)
			
		pool.wait_completion()
			
		
	  
		




