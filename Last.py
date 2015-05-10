#coding=utf8
#!/usr/bin/python
import urllib
import urllib2
import cookielib
import re
import os
import getpass

def getVIEW(Page):          # Get viewststes for login page
	view = r'name="__VIEWSTATE" value="(.+)" '
	view = re.compile(view)
	return view.findall(Page)[0]

def Print(Score_html):		# print the result
	str = r"<td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.?)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.?)</td><td>(.?)</td>"
	str = re.compile(str)
	result = {}
	subject = []
	a = str.findall(Score_html)
	for i in a:
    		for j in range(15):
        			subject.append(i[j])
    		result[subject[3]] = subject
   		subject = []

	for i in result.keys():
    		j = result[i]
    		# print j
    		print '%-10s%-2s%-10s%-8s%6s%8s%10s%6s%6s%5s%10s%-10s%-15s%s%s' % tuple(j)
    		print " "

def getName(loginPage):		# get the name
           Sname = r'<span id="xhxm">(.+)同学</span>'
           Sname = re.compile(Sname)
           try:
		return Sname.findall(loginPage)[0]
           except IndexError, e:
		raise e
		print "User-name or password error, try again!"
		main()


def main():
	loginURL = 'http://222.24.19.201/default6.aspx'		#this is the login page for xupt
	ID = raw_input("Please input your student ID:")
	Password =  getpass.getpass("Please input your password:")
	print 'Loading........'
	page = urllib2.urlopen(loginURL).read()
	postdata = urllib.urlencode({
      		'__VIEWSTATE':getVIEW(page),   		
      		'txtYhm':ID,				#std ID
     		'txtMm':Password,			#password
            	'rblJs':'学生',
            	'btnDl':' 登录'})			
	headers = {
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
	}
	cookie = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	myRequest = urllib2.Request(loginURL, postdata,headers)
	loginPage = opener.open(myRequest).read()
	page =  unicode(loginPage, 'gb2312').encode("utf-8")		#get the cookie 
	# print page
	try:
		name = getName(page)
	except IndexError, e:
		print "User-name or password error, try again!"		#if name is not found, this is the reason 
		main()
		exit()
	else:
		pass
	
	# print cookie
	for i in cookie:
		Cookie = i.name+"="+i.value
	# print Cookie
	
	head = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Cache-Control':'no-cache',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded',
	'Host':'222.24.19.201',
	'Cookie':Cookie,
	'Origin':'http://222.24.19.201',
	'Pragma':'no-cache',
	'Referer':'http://222.24.19.201/xs_main.aspx?xh='+ID,
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
	}

	getdata = urllib.urlencode({
		'xh':ID,
		'xm':name,
		'gnmkdm': 'N121605'

		})
	MyRequest= urllib2.Request('http://222.24.19.201/xscjcx.aspx?'+getdata,None, head)		#According to this page ,we can get the viewstats
	loginPage=unicode(opener.open(MyRequest).read(), 'gb2312').encode("utf-8")
	data = urllib.urlencode({
		"__VIEWSTATE":getVIEW(loginPage),
		"btn_zcj":"历年成绩"
		})
	MyRequest= urllib2.Request('http://222.24.19.201/xscjcx.aspx?'+getdata,data, head)		#Score's page
	html = opener.open(MyRequest)
	result =  unicode(html.read(), 'gb2312').encode("utf-8")
	Print (result)												# Score
if __name__ == '__main__':
	main()