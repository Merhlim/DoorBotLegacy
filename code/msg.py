#!/usr/bin/env python
try:
	import info
	import messages
	from time import sleep
	#Begin
	def fullprog(info):
		messg = info.getlatestmessage()
		while True:
			if(messg != False):
				messages.TextData(messg,info)
			info.timecheck()
			info.temp()
 			sleep(1)
			url = str(info.browser.current_url)
			if ("index.html" in url):
				info = messages.Index(info)
			if ("msg.html" in url):
				messg = info.getlatestmessage()
				info = messages.msg(info)
			if ("vis.html" in url):
				messg = info.getlatestmessage()
				info = messages.vis(info)
        	        continue
	fullprog(info)
except Exception as err:
       info.dbgmsg("Oops i have run into an err\n" + str(err))
