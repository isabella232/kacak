KACAK
=====

ATTENTION: Most updated version can be accessed using this link http://www.galkan.net/2014/01/enumerate-users-for-windows-based-networks.html

Kacak is a tool that can enumerate users specified in the configuration file for windows based networks. It uses metasploit *smb_enumusers_domain* module in order to achieve this via msfrpcd service. 
 Details about msfrpcd service can be seen from metasploit documentation at  https://github.com/rapid7/metasploit-framework/blob/master/documentation/msfrpc.txt . Kacak also parses mimikatz results.

### Installation 

First install the needed libraries. Please follow the instructions given below;

```
 # apt-get install msgpack-python  
 # cd /tmp  
 # wget https://github.com/SpiderLabs/msfrpc/archive/master.zip  
 # unzip master.zip  
 # cd msfrpc-master/python-msfrpc  
 # python setup.py install  
```


Once the installation of libraries were completed, msfrpcd service must be restarted. In order to do this you can use a script which is located in the kacak files named **msfrpcd.sh**. Prior to this script, check whether if port 55552 is open.  
```
 # netstat -nlput | grep 55552 | grep -v grep     
```
There are 3 ways of using this script as shown below;
```
  # ./msfrpcd.sh status
  MsfRpcd: Running
```
```
 # ./msfrpcd.sh stop
  MsfRpcd:  Stopped
```

```
 #./msfrpcd.sh start
  MsfRpcd:  Starting
  ..................
  MsfRpcd:  Started
```
Script for managing msfrpcd service;

And be sure that 55552 port number is open after that. 

Download latest kacak version from github.  
**https://github.com/galkan/kacak.**  

```
 # wget https://github.com/galkan/kacak/archive/master.zip
 # unzip master.zip
```
In order to use kacak properly, 3 config files should be specified.

First file is used to specify credentials used to login to target machines. 
with one of the files you should specify the user credentials that can login the target ip addresses. It is xml based file named **config_file** with following syntax:  
```xml
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
```

Example file which is shown above has 2 users credentials.  

Seconf config file is **users_file** . It is used to specify users we want to search on target machines. Common use is to search for domain admin users or DB admin users. Syntax is as follows : "**domain_name\username**". Users will not be enumerated if domain_name is not specified.  Example usernames are as follows:  
```
Sirket\YoneticiKullanici  
Workgroup\Administrator  
```

Third config files is ip_file . It is used to specify target IP addresses in CIDR notation.   
```
192.168.100.100  
192.168.100.111  
```

ATTENTION: "**users_file**" and "**ip_file**" files must HAVE THE full path. Otherwise kacak can't enumarate users properly.  

An example kacak output:  
**Resim**  

If you have any problem or want to debug with an extra tool, you can use test_kacak.sh which is located in the kacak files.

An extra debugging script for kacak;
**Resim**  

```
 # ./test_kacak.sh ../data/ip_file.txt  ../data/users.txt Sirket Aa123456 Saldirgan 5  
  192.168.100.101 -> SIRKET\EtkiAlaniYoneticisi  
```
**--mimikatz** option can be used to parse mimikatz results.
```
 # ./kacak.py --mimikatz /root/sld_kacak/kacak/data/mimikatz.txt  
    Kadi: galkan Parola: galkan's password  
    Kadi: gokhan Parola: gokhan's password  
```

Kacak was developed and tested on Kali Linux distribution.
