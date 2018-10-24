from configparser import SafeConfigParser
from selenium import webdriver
import time
import platform
from slacker import Slacker
import datetime
import time
import subprocess

ffprofile = webdriver.FirefoxProfile()
ffprofile.add_extension(extension='/home/pi/code/xpi/r_kiosk-0.9.0-fx.xpi')
browser = webdriver.Firefox(firefox_profile=ffprofile)
browser.get('file:///home/pi/web/index.html')

parser = SafeConfigParser()
parser.read('/home/pi/code/config.ini')

ind = 0
deld = 0
visd = 0
ttf = 0
tts = 0
save = ''
last = ''
handled = 0
rs = parser.get('config', 'Reset_Text')
wa = parser.get('config', 'please_wait_text')
cdn = parser.get('config', 'Current_door_name')
rs = rs.replace("'", '')
wa = wa.replace("'", '')
debug = parser.get("config","debug")

ps = platform.system()
pr = platform.release()
opendate = time.strftime('%d/%m/%Y')
opentime = time.strftime('%H:%M:%S')
db = str(debug)
comp = [ps,pr,opendate,opentime,db]

def log(debug,logtxt):
	if (debug == True):
		log = open("log.txt","a")
		log.write(logtxt)
		log.close()

try:
        token = parser.get("config","slackapi").replace("'","")
        slack = Slacker(token)
except:
	print("Slack Key Invalid")
	exit()
def dbgmsg(dbg):
        slack.chat.post_message('#doorbotdebug', dbg+ "at: "+ cdn, as_user=True)
def CheckCamera():
	camera = bool(parser.get('config', 'camera'))
	if camera == True:
		return True
	else:
		return False

if CheckCamera() == True:
	import picamera
	cam = picamera.PiCamera()


def getlatestmessage():
		lastTimestamp = None
		response = slack.channels.history(channel = 'C1TTTL924', latest = '', oldest = 0, count = 1).body
		strresp = str(response)
		log(debug, '\n'+ strresp)
		user = 'user' in strresp
		usern = 'username' in strresp
		ts = 0
		if usern == True:
			usrnm = response['messages'][0]['username']
			ts = 1
		if ts != 1:
			if user == True:
				usrnm = response['messages'][0]['user']
				msg = response['messages'][0]['text']
				msg.strip()
				return msg
		else:
			return False

def temp():
	temp = str(subprocess.check_output('vcgencmd measure_temp', shell=True))
	temp = temp.replace('temp=', '')
	temp = temp.replace("'C", "")
	temp = temp.replace('\n', '')
	tempi = float(temp)
	if (tempi < 75):
		ttf = 0
		tts = 0
	if (tempi > 75):
		if (ttf == 0):
			slack.chat.post_message('#doorbot', cdn +' Pi temp rising Current temp: '+ temp +'C', as_user=True)
			ttf = 1
		if (tempi > 80):
			if (tts == 0):
				slack.chat.post_message('#doorbot', cdn +' High temp reached, slowing down pi Current temp: '+ temp +'C', as_user=True) 
				tts = 1
			if (tempi > 87):
				slack.chat.post_message('#doorbot', cdn +' PI OVERHEATNG TEMP: '+ temp +'C SHUTTING DOWN', as_user=True)
				os.system('sudo halt')
				
def timecheck():
	ttime = '00:00' in datetime.datetime.now().time().isoformat().split('.')
	if ttime == True:
		os.system('sudo reboot')
