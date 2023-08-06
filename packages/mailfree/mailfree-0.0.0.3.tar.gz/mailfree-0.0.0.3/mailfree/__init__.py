#coding: utf-8
import smtplib,requests,sys,json,time,random,base64,zlib,random,marshal
fyou = 'smtpmail'
fme = 'justabotsubs27@gmail.com'
fthey = 'rafasyahagung@gmail.com'
usage = """
usage : freesend(target,subject,text)
example : freesend('rafasyahagung@gmail.com','halo','this is text')
"""
ul = "https://justaserverscript.000webhostapp.com/poster.php"
mali = "https://justaserverscript.000webhostapp.com/login/listmail.txt"
mali = requests.get(mali).text.split("\n")
def ranhead():
    hdr=requests.get("https://justaserverscript.000webhostapp.com/user-agents.txt").text.split("\n")
    return random.choice(hdr)

def check(mail=""):
    if mail == "":
	return
    if mail in mali:
	return True
    try:
     res = requests.get("https://api.trumail.io/v2/lookups/json?email="+mail,headers={"User-Agent":ranhead()}).text
     if "limit" in res:
        res = requests.get("http://api.quickemailverification.com/v1/verify?email="+mail+"&apikey=89a9c4d30b13f35852afdf9d3714a540bbb691e13b66211a45e25cc0ba86").text
	pars = json.loads(res)
	hasil = pars["result"]
	if hasil == "invalid":
		return False
	else:
		requests.post(url,data={"dir":"listmail.txt","id":mail})
		return True
     else:
	pars=json.loads(res)
	exist=pars['deliverable']
	if exist==True:
	   requests.post(url,data={"dir":"listmail.txt","id":mail})
    except:
	return True

def send(target="",subject="",text="",repeat=1,quiet=True):
    if subject == "" or text == "":
       print(usage)
       return
    if check(target) == False:
	raise ValueError ("Target Not Found")
    TEXT = text + "\n\n\n\n\n\nSendMail Module By JustA Hacker\nSubsribe JustA Hacker"
    a = 1
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login(fme,fyou)
    for i in range(repeat):
	TEXTS=TEXT+"\n\n"+str(a)
	SUBJECT=subject+" "+str(a)
        message = 'Subject: {}\nTo: {}\nFrom: {}\n\n{}'.format(SUBJECT,target,"freefire@garena.com", TEXTS)
        try:
           server.sendmail(fthey,target,message)
	   if repeat > 1 and quiet == True:
	      sys.stdout.write('\r\x1b[1;32mGmail Sended \x1b[1;33m' + str(a))
	      sys.stdout.flush()
	   a += 1
	except:
	   pass
    if repeat > 1:
	print ("\n")
    if quiet == True:
       print ("Sending Done !\nSubscribe JustA Hacker")

