import os

def TextData(msg,info):
        fileop = open('/home/pi/web/imsg.html', 'w')
        main = """<!DOCTYPE html>
<html lang='en-us'>
<head>
<meta charset='utf-8' http-equiv='refresh' content='2'>
<title></title>
</head>
<body>
<font color='white' size=6>
<p>"""+msg+"""</p>
</font>
</body>
</html>"""
        fileop.write(main)
        fileop.close()
        
def vis(info):
        if (info.visd == 0):
		TextData("...",info)
                if (info.debug == True):
                        print '\nVISD'
                        info.slack.chat.post_message('#doorbot', cdn +' Screen location: Visitor\'s page', as_user=True)
                else:
                        send(info,"There is a visitor at: "+ info.cdn)
                        TextData("",info)
                        info.visd = 1
                        info.ind = 0
        return info

def msg(info):
        if (info.deld == 0):
		TextData("...",info)
                if (info.debug == True):
                        print '\nDELD'
                        info.slack.chat.post_message('#doorbot', cdn +' Screen location: Delivery\'s page', as_user=True)
                else:
                        send(info,"There is a delivery at: "+ info.cdn)
                        TextData("",info)
                        info.deld = 1
                        info.ind = 0
        return info
                        
def Index(info):
        if (info.ind == 0):
                getrec = info.getlatestmessage()
                if getrec == '...':
                        TextData(info.rs,info)
                        info.log(info.debug,'\nScreen location: home page')
                        info.ind = 1
                        info.deld = 0
                        info.visd = 0
                if getrec != "...":
                        info.slack.chat.post_message('#doorbot', '...', as_user=True) 
                        TextData(info.rs,info)
                        info.log(info.debug,'\nScreen location: home page')
                        info.ind = 1
                        info.deld = 0
                        info.visd = 0
        return info
                
def send(info,message):
        info.slack.chat.post_message('#doorbot', message, as_user=True)
        if bool(info.parser.get("config","ring_doorbell")) == True:
                print 'curl -POST https://api.particle.io/v1/devices/'+info.parser.get("config","doorbell1")+'/doorbell -d access_token='+info.parser.get("config","door_bell_key")
                os.system('curl -POST https://api.particle.io/v1/devices/'+info.parser.get("config","doorbell1")+'/doorbell -d access_token='+info.parser.get("config","door_bell_key"))
                os.system('curl -POST https://api.particle.io/v1/devices/'+info.parser.get("config","doorbell2")+'/doorbell -d access_token='+info.parser.get("config","door_bell_key"))
                os.system('curl -POST https://api.particle.io/v1/devices/'+info.parser.get("config","doorbell3")+'/doorbell -d access_token='+info.parser.get("config","door_bell_key"))
                os.system('curl -POST https://api.particle.io/v1/devices/'+info.parser.get("config","doorbell4")+'/doorbell -d access_token='+info.parser.get("config","door_bell_key"))
                os.system('curl -POST https://api.particle.io/v1/devices/'+info.parser.get("config","doorbell5")+'/doorbell -d access_token='+info.parser.get("config","door_bell_key"))
        if info.CheckCamera() == True:
                info.cam.hflip = True
                info.cam.capture('/home/pi/code/temp.png')
                info.slack.files.upload('/home/pi/code/temp.png', filename='temp.png',title='Photo of user' ,channels='C1TTTL924')

	info.slack.chat.post_message('#doorbot', info.wa, as_user=True)

        
