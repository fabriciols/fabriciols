# coding: utf-8 

#from mechanize import Browser
import mechanize
import winsound
import socket
import re
import time

#er_websense = re.compile('.*Websense.*');
#er_sold     = re.compile('.*sendo oferecido para a venda.*');
#er_sold_2   = re.compile('.*This page has been moved.*');
re_build_level = re.compile('alt="" /> (?P<buidl>[^<]*).*\(N.*vel.* (?P<level>[0-9]*)\).*')

#TRIBAL_ROOT_URL = 'http://tribalwars.com.br'
TRIBAL_ROOT_URL =  'http://tribalwars.com.br/index.php?action=login'
#TRIBAL_ROOT_URL = 'http://br21.tribalwars.com.br/game.php?screen=overview&'
#PROXY_URL       = 'http://www.usxs.info'
PROXY_URL       = 'http://ipfound.info/'
USERNAME = "tribalwbot"
PASSWORD = "123456"
WORLD = "21"


def start_browser():
	br = mechanize.Browser(factory=mechanize.RobustFactory())

	# Se precisar de proxy , descomentar e preencher esta linha
	br.set_proxies({"http": "net\\fabriciols:rootroot123456@proxy.intranet:80" })

	socket.setdefaulttimeout(60)

	br.set_debug_redirects(True)
	br.set_debug_responses(True)
	br.set_debug_http(True)
	br.set_handle_equiv(False)

	br.set_handle_robots(False)

	# Don't add Referer (sic) header
	br.set_handle_referer(False)
	# Don't handle Refresh redirections
	br.set_handle_refresh(False)

# Simula um IE 7.0
	br.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)')]

	return br


def open_tribal(br, proxy=False):

	if proxy is not False:
		response = br.open(proxy)

		br.select_form(nr=2)

		for i in br.forms():
			print i,

		br["u"] = TRIBAL_ROOT_URL

		response = br.submit()

		for i in response.readlines():
			print i,

	else:
		response = br.open(TRIBAL_ROOT_URL)

	br.select_form(nr=0)

	for i in br.forms():
		print i,

	br["user"]     = USERNAME
	br["password"] = PASSWORD
	br["server"] = [ "br%s" %WORLD ]

	response = br.submit()

	for i in br.links():
		response = br.follow_link(i)
		break

	try:
		link = br.find_link(text_regex=re.compile("visualiza.*ssica"))
		response = br.follow_link(link)
	except:
		pass

	for i in response.readlines():
		if re_build_level.match(i):
			t = re_build_level.search(i)
			build = t.group("build")
			level = t.group("level")
			print "+", i,
			print build, level
		else:
			print "-", i,

	return br

def	create_user(username, mail):

	result = br.open(url)
	br.select_form(nr=0)

	response = br.submit()

	br.select_form(nr=1)

	for i in br.forms():
		print i

	br["name"] = username
	br["password"] = "12345678"
	br["password_confirm"] = "12345678"
	br["email"] = mail
	br.form.find_control("agb").items[0].selected = True

	response = br.submit()

#mail = "tw_123+tw_123_1@gmail.com"
#create_user("tw_123_1", mail) 

br = start_browser()
br = open_tribal(br, proxy=PROXY_URL)

print dir(br)
