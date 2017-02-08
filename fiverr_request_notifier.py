import cookielib 
import urllib2 
import re
import mechanize 	
import json
import time
from bs4 import BeautifulSoup
import sys

id = ""
retryTime = 300

def work(username):
	try:
		global id
		logincheck = br.open('https://www.fiverr.com/users/' + username + '/requests')
		soup = BeautifulSoup(logincheck, 'lxml')
		sc = soup.find_all('script')
		data = sc[4].string.encode('utf-8')
		indx = data.index('{')
		data = data[25:]
		jdata =json.loads(data)
		temp_id = jdata["results"]["rows"][0]["identifier"].encode('utf-8')
		if temp_id != id:
			print "New Data Found\n\n"
			print "Message : ",jdata["results"]["rows"][0]["cells"][1]["text"].encode('utf-8')
			print "Tags : ",jdata["results"]["rows"][0]["cells"][1]["tags"]
			print "Duration : ",jdata["results"]["rows"][0]["cells"][3]["text"].encode('utf-8')
			print "identifier : ",jdata["results"]["rows"][0]["identifier"].encode('utf-8')
			id = temp_id
		return True
	except:
		return False

br = mechanize.Browser() 
cookiejar = cookielib.LWPCookieJar() 
br.set_cookiejar( cookiejar ) 

br.set_handle_robots(False)
br.set_handle_equiv( True ) 
# br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True )

br.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]

logout = br.open("https://www.fiverr.com/logout") 
sign_in = br.open("https://www.fiverr.com/login") 
 
for form in br.forms():
	if form.attrs['id'] == 'session_form':
		br.form = form
		break 

br.form.controls[4].value = sys.argv[1]
br.form.controls[6].value = sys.argv[2]

logged_in = br.submit() 
logincheck = logged_in.read()

soup = BeautifulSoup(logincheck, 'lxml')
while True:
	flag = work(sys.argv[1])
	if flag:
		print "success"
	else:
		print "error"
	time.sleep(retryTime)
