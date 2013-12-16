KACAK
=====

### Turkish

http://www.galkan.net/2013/12/windows-aglarinda-domain-admin-olma.html


### English

Kacak is a tool that can enumerate users specified in the configuration file for windows based networks. It uses metasploit smb_enumusers_domain module in order to achieve this via msfrpcd service. If you are wondering what the msfrpcd service is, please look at  the https://github.com/rapid7/metasploit-framework/blob/master/documentation/msfrpc.txt . It also parse mimikatz results. 
 
At first, install the needed libraries. Please follow the instructions given below;
 
    # apt-get install msgpack-python
    # cd /tmp
    # wget https://github.com/SpiderLabs/msfrpc/archive/master.zip
    # unzip master.zip
    # cd msfrpc-master/python-msfrpc
    # python setup.py install

First step;


![Alt text](https://raw.github.com/galkan/kacak/master/images/image1.png "Install needed libraries")

Second step,

![Alt text](https://raw.github.com/galkan/kacak/master/images/image2.png "Install needed libraries")
![Alt text](https://raw.github.com/galkan/kacak/master/images/image3.png "Install needed libraries")
![Alt text](https://raw.github.com/galkan/kacak/master/images/image4.png "Install needed libraries")

Once the installation of libraries were completed, msfrpcd service must be restarted. In order to do this you can use a script which is located in the kacak files named msfrpcd.sh.  Prior  to this script, check whether the 55552 port number is open or not. Make sure that it is closed.

    # netstat -nlput | grep 55552 | grep -v grep     

There are 3 ways of using this script as shown below;
    # ./msfrpcd.sh status
      MsfRpcd: Running
 
    # ./msfrpcd.sh stop
      MsfRpcd:  Stopped
 
    #./msfrpcd.sh start
      MsfRpcd:  Starting
      ..................
      MsfRpcd:  Started

Script for managing msfrpcd service;


![Alt text](https://raw.github.com/galkan/kacak/master/images/image5.png "script for managing msfrpcd service")
  
And be sure that 55552 port number is open after that.

In order to use kacak properly, you must use 3 files. with one of the files you should specify the user credentials that can login the target ip addresses. Itis xml based file which is shown below named config_file.

    <?xml version="1.0"?>
    <domain-admin>
             <domain>
                     <name>WORKGROUP</name>
                     <username>Administrator</username>
                     <password>Test123</password>
                    <threads>10</threads>
            </domain>
            <domain>
                     <name>Sirket</name>
                     <username>Saldirgan</username>
                     <password>Aa123456</password>
                     <threads>10</threads>
          </domain>
    </domain-admin>
 
Example file which is shown above has 2 users credentials. Each user credentials must be started with <domain> and stopped with </domain>.
 
Other file named users_file  is used for the users you want to enumarate. It must be like this; "username\domain_name" and If you don’t specify the domain_name, Kacak can't enumarate the users.
 
    Sirket\YoneticiKullanici
    Workgroup\Administrator
 
And the last one is which you want to scan network named ip_file. You can also use cidr notiation.

    192.168.100.100
    192.168.100.111
 
ATTENTION: "users_file" and "ip_file" files must HAVE THE full path. Otherwise kacak can't enumarate users properly. Metasploit module needs the full path of these files.


An example screenshot for running kacak;


![Alt text](https://raw.github.com/galkan/kacak/master/images/image6.png "An extra debugging script for kacak")

Yet another one;


![Alt text](https://raw.github.com/galkan/kacak/master/images/image7.png "An extra debugging script for kacak")


If you have any problem or want to debug with an extra tool, you can use test_kacak.sh which is located in the kacak files. 

An extra debugging script for kacak;


![Alt text](https://raw.github.com/galkan/kacak/master/images/image8.png "An extra debugging script for kacak")

    # ./test_kacak.sh ../data/ip_file.txt  ../data/users.txt Sirket Aa123456 Saldirgan 5
      192.168.100.101 -> SIRKET\EtkiAlaniYoneticisi


--mimikatz options is used to parse mimikatz results. 

    # ./kacak.py --mimikatz /root/sld_kacak/kacak/data/mimikatz.txt 
        Kadi: galkan Parola: galkan's password
        Kadi: gokhan Parola: gokhan's password

ATTENTION: It was tested on Kali Linux distribution.
 
