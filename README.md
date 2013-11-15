KACAK
=====

Kacak sızma testleri esnasında windows ağları için belirli yeteneklere sahip bir araçtır. Geliştirilmesi devam etmekte
olan bu sürüm yetenekleri olarak;
 - Kurum domain yapısı üzerinde belirtilen kullanıcıların oturum bilgisinin tespit edilebilmesi
 - Mimikatz sonuçlarının raporlanabilmesi


### Kullanıcı Oturum Bilgilerinin Tespit Edilmesi

Kurulum öncesi gerekli paketlerin sisteme kurulması gerekmektedir. Bunun için aşağıdaki adımlar takip edilmelidir.

     # apt-get install msgpack-python

Duruma ait örnek ekran görüntüsü belirtildiği şekilde olmaktadır.     
![alt tag](https://raw.github.com/galkan/kacak/master/images/image1.png)

İndirilen dosya (master.zip) zip dosyasından çıkarılır

     # cd /tmp
     # wget https://github.com/SpiderLabs/msfrpc/archive/master.zip

Duruma ait örnek ekran görüntüsü belirtildiği şekilde olmaktadır.    
![alt tag](https://raw.github.com/galkan/kacak/master/images/image2.png)

     # unzip master.zip
     # cd msfrpc-master/python-msfrpc
     # python setup.py install

Duruma ait örnek ekran görüntüleri belirtildiği şekilde olmaktadır.         
![alt tag](https://raw.github.com/galkan/kacak/master/images/image3.png)
![alt tag](https://raw.github.com/galkan/kacak/master/images/image4.png)
 
Gerekli paketlerin sisteme kurulmasının ardından "msfrpc" servisinin başlatılması gereklidir. Bunun için paket ile 
birlikte gelen "msfrpcd.sh" betiği kullanılabilir. Msfrpc servisinin başlatılması için betik aşğıda belirtildiği şekilde 
çalıştırılmalıdır. Bu betik 55552 portunda msfrpc servisinin çalıştırılmasını betik içerisindeki gömülü kullanıcı adı
parola bilgisi ile başlatmaktadır. Daha önceden bu servisin farklı bir kullanıcı adı/parola bilgisi ile çalıştırılması 
olasılığına karşın kontrol edilmelidir. Bu işlem netstat komutu yardımı ile belirtilen şekilde kontrol edilebilmektedir.
     
      # netstat -nlput | grep 55552 | grep -v grep     

Bu adım doğrulandıktan sonra betik aşağıda belirtildiği şekilde yönetilebilmektedir.

      # ./msfrpcd.sh status
      MsfRpcd: Running

      # ./msfrpcd.sh stop
      MsfRpcd:  Stopped

      #./msfrpcd.sh start
      MsfRpcd:  Starting
      ..................
      MsfRpcd:  Started

Duruma ait örnek ekran görüntüsü belirtildiği şekilde olmaktadır.    
![alt tag](https://raw.github.com/galkan/kacak/master/images/image5.png)

Kullanım için parametre olarak 3 adet dosya kullanılmaktadır. 1. parametre olarak hangi kullanıcıların sisteme oturum 
açtığı bilgisinin sorgulanacağı dosya, 2. parametre olarak hangi kullanıcı bilgileri ile belirtilen sistemlerde oturum 
açılıp açılmadığı bilgisinin alınacağı "xml" tabanlı yapılandırma dosyası, 3. parametre ilede hangi ip adresleri için 
sorgulamanın gerçekleştirileceği dosya kullanılmaktadır.

     - <user_file>: Bu dosya içerisinde hangi kullanıcıların aranacağı bilgisi yer almalıdır. Her bir satırda 
     "Domain\Kullanıcı_Adı" şeklinde  belirtim gerçekleştirilebilir. Örnek bir içerik aşağıda gösterilmiştir.
     
     Sirket\YoneticiKullanici
     Workgroup\Administrator

     - <ip_file>: Bu dosya içerisinde hangi ip adreslerinin aranacağı belirtilmektedir. Metasploit formatında kabul 
     edilen tüm ip adres yazım formatı geçerli olmaktadır. Örnek bir içerik aşağıda gösterilmiştir.
     
     192.168.100.100
     192.168.100.111

     - <config_file>: Bu dosya içerisinde hangi kullanıcı bilgileri ile belirtilen sistemlere oturum açılıp açılmayacağı
     bilgisi bulunmaktadır. İstenilen sayıda kullanıcı bilgileri için belirtimler gerçekleştirilebilir. Domain Adı, 
     Kullanıcı Adı, Kullanıcı Parola bilgisi ve kullanılmak istenen "thread" sayısının belirtimleri kullanılmaktadır.
     Örnek bir içerik aşağıda gösterilmiştir.

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


NOT: Belirtilen dosyalar içerisinde "users_file" ve "ip_file" dosyaları için  tam yol belirtilmelidir. Aksi halde hata 
mesaji alıacaktır. Bu durum yapılandırma dosyası için geçerli değildir. Örneğin "/usr/local/data/users.txt" gibi.
Kullanıcı oturum açma tespit etme özelliği için "--domain" opsiyonu ile çalıştırılmalıdır. Örnek bir kullanım aşağıda gösterildiği gibi 
olmaktadır.

     # ./kacak.py --domain /root/sld_kacak/kacak/data/users.txt config/config.xml /root/sld_kacak/kacak/data/ip_file.txt

     [+] Domain: WORKGROUP
     -- Empty --

     [+] Domain: Sirket
          [+] 192.168.100.101 -> SIRKET\EtkiAlaniYoneticisi

Duruma ait örnek ekran görüntüsü belirtildiği şekilde olmaktadır.    
![alt tag](https://raw.github.com/galkan/kacak/master/images/image6.png)

NOT: Betik hata ayıklama seçeneği amaçlı "-v" opsiyonu ile çaıştırılarak debug mesajları verebilmektedir. Hata ayıklama 
modu olarak 3 seviye bulunmaktadır. 1 en düşük 3 ise en yüksek seviye olarak belirtilmektedir. Örnek bir kullanım 
aşağıda gösterildiği gibi olmaktadır. [-] ile başlayan satırlar hata ayıklama mesajlarına ilişkin satırlardır.

     # ./kacak.py --domain /root/sld_kacak/kacak/data/users.txt /root/sld_kacak/kacak/config/config.xml /root/sld_kacak/kacak/data/ip_file.txt

     [+] Domain: WORKGROUP
     -- Empty --

     [+] Domain: Sirket
          [+] 192.168.100.101 -> SIRKET\EtkiAlaniYoneticisi


     # ./kacak.py --domain /root/sld_kacak/kacak/data/users.txt /root/sld_kacak/kacak/config/config.xml /root/sld_kacak/kacak/data/ip_file.txt -v 1
     [ - ]  Config File's Options -->  [{'threads': '10', 'password': 'Test123', 'user_name': 'Administrator', 'domain_name': 'WORKGROUP'}, {'threads': '10', 'password': 'Aa123456', 'user_name': 'Saldirgan', 'domain_name': 'Sirket'}]

     [+] Domain: WORKGROUP
     [ - ]  Commands -->  ['use auxiliary/scanner/smb/smb_enumusers_domain\n', 'set RHOSTS file:/root/sld_kacak/kacak/data/ip_file.txt\n', 'set THREADS 10\n', 'set SMBPass Test123\n', 'set SMBUser Administrator\n', 'set SMBDomain WORKGROUP\n', 'run\n']
     -- Empty --

     [+] Domain: Sirket
     [ - ]  Commands -->  ['use auxiliary/scanner/smb/smb_enumusers_domain\n', 'set RHOSTS file:/root/sld_kacak/kacak/data/ip_file.txt\n', 'set THREADS 10\n', 'set SMBPass Aa123456\n', 'set SMBUser Saldirgan\n', 'set SMBDomain Sirket\n', 'run\n']
          [+] 192.168.100.101 -> SIRKET\EtkiAlaniYoneticisi

Duruma ait örnek ekran görüntüsü belirtildiği şekilde olmaktadır.           
![alt tag](https://raw.github.com/galkan/kacak/master/images/image7.png)

NOT: test dizini altında hata ayıklama ve kontrol amaçli olarak "bash script" ile geliştirilmiş aynı işi gerçekleştirien
bir betik bulunmaktadır. Olası durumlarda bu betik yardımı ilede aynı işlem gerçekleştirilebilmektedir.
     
     # ./test_kacak.sh ../data/ip_file.txt  ../data/users.txt Sirket Aa123456 Saldirgan 5
     192.168.100.101 -> SIRKET\EtkiAlaniYoneticisi

Duruma ait örnek ekran görüntüsü belirtildiği şekilde olmaktadır.    
![alt tag](https://raw.github.com/galkan/kacak/master/images/image8.png)

### Mimikatz Sonuçlarının Raporlanması

Mimikatz sonuçlarının ayrıştırılabilmesi için "--mimikatz" seçeneği kullanılmaktadır. Bu seçenek yardımı ile sonuçlar
kolayca raporlanabilmektedir. Mimikatz ile elde edilen örnek bir çıktının raporlanmasına dair örnek bir kullanım ve
çıktı aşağıda gösterildiği gibi olmaktadır.

     # ./kacak.py --mimikatz /root/sld_kacak/kacak/data/mimikatz.txt 
     Kadi: galkan Parola: galkan Sifresi
     Kadi: alkan Parola: alkan Sifresi
     
### To Do

- MS_08_067 açıklığını taşıyan ip adreslerinin tespit edilebilmesi
- Windows ağları üzerinde kullanıcıların "nmap" betikleri yardımı ile tespit edilebilmesi 

