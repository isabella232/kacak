kacak
=====

# USER ENUMARATION

Kurulum oncesi gerekli paketlerin sisteme kurulmasi gerekmektedir. Bunun icin asagidaki adimlar takip edilmelidir.

apt-get install msgpack-python

wget https://github.com/SpiderLabs/msfrpc/archive/master.zip
 
İndirilen dosya (master.zip) zip dosyasından çıkarılır
cd msfrpc-master/python-msfrpc

python setup.py install
 

Gerekli paketlerin sisteme kurulmasinin ardindan msfrpc servisinin baslatilmasi gereklidir. Bunun icin paket ile birlikte gelen msfrpcd.sh betigi kullanilabilir. Msfrpc servisinin baslatilmasi icin betik asagida belirtildigi sekilde calistirilmalidir.

      # ./msfrpcd.sh status

      MsfRpcd: Running

      ./msfrpcd.sh stop

      MsfRpcd:  Stopped

      ./msfrpcd.sh start

      MsfRpcd:  Starting

      ........................

      MsfRpcd:  Started


Betik parametre olarak 3 adet dosya almaktadir. 1. olarak hangi kullanicilarin sisteme oturum acmadigi bilgisinin sorgulandigi, 2. olarak hangi kullanici bilgileri ile belirtilen sistemlerde oturum acilip acilmadigi bilgisinin alinacagi xml tabanli yapilandirma dosyasi, 3. ve son olarak ise hangi ip adresleri icin sorgulamalarin gerceklestirilecegi dosya.

- <user_file>: Bu dosya icerisinde hangi kullanicilarin aranacagi bilgisi yer almalidir. Her bir satirda Domain\Kullanici_Adi seklinde  belirtim gerceklestirilmelidir. Ornegin;
Sirket\YoneticiKullanici
Workgroup\Administrator

- <ip_file>: Bu dosya icerisinde hangi ip adreslerinin aranacagi belirtilmektedir. Metasploit formatinda kabul edilen tum ip adres yazilis bicimleri gecerli olmaktadir. Ornegin
192.168.100.100
192.168.100.111

- <config_file>: Bu dosya icerisinde hangi kullanici bilgileri ile belirtilen sistemlere oturum acilip acilmayacagi bilgisi bulunmaktadir. Istenilen sayida kullanici bilgileri icin belirtimler gerceklestirilebilir. Domain adi, Kullanici adi, Kullanici parolasi ve acilacak thread sayisi asagida gosterildigi sekilde belirtilmelidir.

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


Not: Belirtilen dosyalar icerisinde users_file ve ip_file dosyalari icin  tam yol belirtilmelidir. Aksi halde hata mesaji alinacaktir. Bu durum yapilandirma dosyasi icin gecerli degildir. Ornegin /usr/local/data/users.txt gibi.

User enumaration ozelligi icin betik --domain opsiyonu ile calistirilmalidir. Ornek bir kullanim asagida gosterildigi gibi olmaktadir.

./kacak.py --domain /root/sld_kacak/kacak/data/users.txt config/config.xml /root/sld_kacak/kacak/data/ip_file.txt

[+] Domain: WORKGROUP
 -- Empty --

[+] Domain: Sirket
   [+] 192.168.100.101 -> SIRKET\EtkiAlaniYoneticisi

Not: Betik hata ayiklama secenegi amacli -v opsiyonu ile calistirilarak debug mesajlari verebilmektedir. Hata ayiklama modu olarak 3 seviye bulunmaktadir. 1 en dusuk 3 ise en yuksek seviye olarak goze carpmaktadir. Ornek bir kullanim asagida gosterildigi gibi olmaktadir. [-] ile baslayan satirlar hata ayiklama mesajlarina iliskin satirlardir.

./kacak.py --domain /root/sld_kacak/kacak/data/users.txt /root/sld_kacak/kacak/config/config.xml /root/sld_kacak/kacak/data/ip_file.txt

[+] Domain: WORKGROUP
 -- Empty --

[+] Domain: Sirket
   [+] 192.168.100.101 -> SIRKET\EtkiAlaniYoneticisi


./kacak.py --domain /root/sld_kacak/kacak/data/users.txt /root/sld_kacak/kacak/config/config.xml /root/sld_kacak/kacak/data/ip_file.txt -v 1
[ - ]  Config File's Options -->  [{'threads': '10', 'password': 'Test123', 'user_name': 'Administrator', 'domain_name': 'WORKGROUP'}, {'threads': '10', 'password': 'Aa123456', 'user_name': 'Saldirgan', 'domain_name': 'Sirket'}]

[+] Domain: WORKGROUP
[ - ]  Commands -->  ['use auxiliary/scanner/smb/smb_enumusers_domain\n', 'set RHOSTS file:/root/sld_kacak/kacak/data/ip_file.txt\n', 'set THREADS 10\n', 'set SMBPass Test123\n', 'set SMBUser Administrator\n', 'set SMBDomain WORKGROUP\n', 'run\n']
 -- Empty --

[+] Domain: Sirket
[ - ]  Commands -->  ['use auxiliary/scanner/smb/smb_enumusers_domain\n', 'set RHOSTS file:/root/sld_kacak/kacak/data/ip_file.txt\n', 'set THREADS 10\n', 'set SMBPass Aa123456\n', 'set SMBUser Saldirgan\n', 'set SMBDomain Sirket\n', 'run\n']
   [+] 192.168.100.101 -> SIRKET\EtkiAlaniYoneticisi

Not: test dizini altinda hata ayiklama ve kontrol amacli olarak bash scrripting ile gelistirilmis ayni ise yapan bir betik bulunmaktadir. Bu betik yardimi ilede ayni islem gerceklestirilebilmektedir.

./test_kacak.sh ../data/ip_file.txt  ../data/users.txt Sirket Aa123456 Saldirgan 5

192.168.100.101 -> SIRKET\EtkiAlaniYoneticisi

# MIMIKATZ PARSER 

Mimikatz sonuclarinin parse edilebilmesi icin --mimikatz secenegi aktive edilmistir. Bu seenek yardimi ile sonuclar asagida gosterildigi sekilde parse edilebilmektedir.

./kacak.py --mimikatz /root/sld_kacak/kacak/data/mimikatz.txt 

Kadi: bayram Parola: bayramSifresi

Kadi: h.unay Parola: h.unaySifresi

Kadi: serkan Parola: serkanSifresi




