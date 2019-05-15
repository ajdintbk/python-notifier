from selenium import webdriver
import time
import ctypes
import os,sys
import telegram
from selenium.webdriver.chrome.options import Options
import requests



#provjera konekcije
def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("")
    return False

if(check_internet()==False):
    animation = "|/-\\"
    while(check_internet()==False):
        clear = lambda: os.system('cls')
        clear()
        for i in range(50):
            time.sleep(0.1)
            sys.stdout.write("\r" +animation[i % len(animation)] + " Waiting for network " + animation[i % len(animation)])
            sys.stdout.flush()
    clear()
    print("Connected!\n")



print("                _______ _______ _______      _______ _______ _______ _______ _______ _______ _______ ______                                                                                                                      ")
print("               |    ___|_     _|_     _|    |    |  |       |_     _|_     _|    ___|_     _|    ___|   __ \                                                                                                                    ")
print("               |    ___|_|   |_  |   |      |       |   -   | |   |  _|   |_|    ___|_|   |_|    ___|      <                                                                                                                     ")
print("               |___|   |_______| |___|      |__|____|_______| |___| |_______|___|   |_______|_______|___|__|                                                                                                                     ")

#login
index= input("Unesi index: ")
pw = input("Unesi password: ")
my_token='672622858:AAGIZmi_Id0KbNoR5I7kWxIZHeXR_Wj9QPE' #telegram token

#url DLWMS-a
url = 'https://www.fit.ba/student/login.aspx'

#chrome driver options
options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized') # 
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options, executable_path='C:/Users/Ajdin Tabak/Documents/chromedriver')

#chrome web driver skinuti i raspakovati - onda navesti full path do chromedriver-a

driver.get (url)

#login automated
driver.find_element_by_id('txtBrojDosijea').send_keys(index) 
driver.find_element_by_id('txtLozinka').send_keys(pw)
driver.find_element_by_id('btnPrijava').click()

#trazi zadnju obavijest i uzima njeno vrijeme
getVrijeme = driver.find_element_by_id('lblDatum')
vrijeme = getVrijeme.text[11:16]
#petlja koja ce loop forever
while True:
    #trazi ponovo datum i provjerava sa onim izvan petlje, ako vidi da su razliciti salje obavijest na telegram
    tempGetVrijeme = driver.find_element_by_id('lblDatum')
    vrijemDatum=driver.find_element_by_id('lblDatum')
    vrijemeDatum=vrijemDatum.text
    tempGetVrijeme = tempGetVrijeme.text[11:16]
    
    if tempGetVrijeme != vrijeme:
        vrijeme = tempGetVrijeme
        subject = driver.find_element_by_id('lnkNaslov')
        full = "["+ subject.text + "]"
        driver.find_element_by_id('lnkNaslov').click()
        panel = driver.find_element_by_id('Panel1')
        if len(panel.text) > 140:
            full=full + "\n\n" + panel.text[0:100]+ " [...]"
        elif len(panel.text) < 140:
            full = full + "\n\n" + panel.text   
        #token message send
        def send(msg, chat_id, token=my_token):
            bot = telegram.Bot(token=token)
            bot.sendMessage(chat_id=chat_id, text=msg)
        send(full, 'chatID', 'token') #telegram chat id i Bot token 
        
        driver.execute_script("window.history.go(-1)")
        
        print ("Telegram message sent succesfully.")
        #end of telegram send
    #svako koliko ce provjeravati DLWMS (u sekundama)
    time.sleep(20)
    driver.refresh()
