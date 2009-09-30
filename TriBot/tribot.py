# coding: utf-8 

#from mechanize import Browser
import mechanize
import winsound
import socket
import re
import time
from pysqlite2 import dbapi2 as sqlite3
import os

#er_websense = re.compile('.*Websense.*');
#er_sold     = re.compile('.*sendo oferecido para a venda.*');
#er_sold_2   = re.compile('.*This page has been moved.*');
re_build_level = re.compile('.*alt="" /> (?P<build>[^<]*).*\(N.*vel.* (?P<level>[0-9]*)\).*')

# ER da pagina principal
re_pr_build_name = re.compile('.*alt="" /> (?P<build>[^>]*)</a>$')
re_pr_wood       = re.compile('''.*title="Madeira" alt="" />(?P<wood>[0-9]*)</td>.*''')
re_pr_iron       = re.compile('''.*title="Ferro" alt="" />(?P<iron>[0-9]*)</td>.*''')
re_pr_stone      = re.compile('''.*title="Argila" alt="" />(?P<stone>[0-9]*)</td>.*''')
re_pr_worker     = re.compile('''.*title="Trabalhador" alt="" />(?P<worker>[0-9]*)</td>.*''')
re_pr_time       = re.compile('.*<td>(?P<time>[^<]*)</td>.*')
re_pr_last       = re.compile('.*<td>(?P<last>.*)</td>$')
re_pr_finished   = re.compile('.*<td colspan="6" align="center" class="inactive">Edif.*io totalmente constru.*do</td>.*')
re_pr_expand     = re.compile('.*Expandir para o n.*vel .*</a></td>.*')
re_pr_farm       = re.compile('.*A Fazenda .* muito pequena.*')
re_pr_make       = re.compile('.*Construir.*')
re_pr_full       = re.compile('.*Recursos suficientes.*')
re_pr_wait       = re.compile('.*Recursos dispon.*')
#re_pr_wait       = re.compile('.*Recursos dispon.*(?P<time>[0-9][0-9]:[0-9][0-9]:[0-9][0-9]).*')



#TRIBAL_ROOT_URL = 'http://tribalwars.com.br'
TRIBAL_ROOT_URL =    'http://tribalwars.com.br/index.php?action=login'
TRIVAL_VILLAGE_URL = 'http://br%s.tribalwars.com.br/game.php?screen=overview&intro&popup'
#TRIBAL_ROOT_URL = 'http://br21.tribalwars.com.br/game.php?screen=overview&'
PROXY_URL       = 'http://payp.info/'
DB_FILENAME     = 'tribot.db'
#USERNAME = "tribalwbot"
#PASSWORD = "123456"
USERNAME = "fabriciols01"
PASSWORD = "171086"
WORLD = "21"

BUILD_INFO_TABLE = 'build_info'
BUILD_LIST_TABLE = 'build_list'
BUILD_RESO_TABLE = 'build_resource'


######
# SQL 
######
BUILD_LIST_TABLE_SQL = '''
			build_id   INTEGER PRIMARY KEY AUTOINCREMENT,
			build_name VARCHAR(30)'''

BUILD_INFO_TABLE_SQL = '''
			build_id           NUMBER PRIMARY KEY,
			build_level        NUMBER,
			build_future_level NUMBER'''

BUILD_RESO_TABLE_SQL = '''
			build_id   NUMBER PRIMARY KEY,
			wood       NUMBER,
			iron       NUMBER,
			stone      NUMBER,
			time_sec   NUMBER,
			flag       NUMBER'''
         # 0 - Pronto para produzir
         # 1 - Tempo para poder fazer
         # 2 - Falta Fazenda
         # 3 - Totalmente Construido
         # 4 - Pronto para produzir porem a fila esta cheia

SQL_TABLE_LIST = [
	[ BUILD_INFO_TABLE, BUILD_INFO_TABLE_SQL ],
	[ BUILD_RESO_TABLE, BUILD_RESO_TABLE_SQL ],
	[ BUILD_LIST_TABLE, BUILD_LIST_TABLE_SQL ],
]


N_BUILD = '1'

def start_browser():
	br = mechanize.Browser(factory=mechanize.RobustFactory())

	# Se precisar de proxy , descomentar e preencher esta linha
	br.set_proxies({"http": "net\\fabriciols:rootroot123456@proxy.intranet:80" })

	socket.setdefaulttimeout(60)

	#br.set_debug_redirects(True)
	#br.set_debug_responses(True)
	#r.set_debug_http(True)
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

		br.select_form(nr=0)

		br['u'] = TRIBAL_ROOT_URL

		response = br.submit()

	else:
		response = br.open(TRIBAL_ROOT_URL)

	br.select_form(nr=2)

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

	return br


def add_build(build_name, conn):

	c = conn.cursor()

	c.execute("""insert into %s (build_name) values ('%s')""" %(BUILD_LIST_TABLE, build_name))

	conn.commit();

	return get_build_id(build_name, conn)

def get_build_id(build_name, conn):

	c = conn.cursor()

	c.execute("""select build_id from %s where build_name = '%s'""" %(BUILD_LIST_TABLE, build_name))

	ret = c.fetchall()

	if len(ret) is 0:
		return add_build(build_name, conn)
	else:
		return ret[0][0]

def sql_update_build_info(build, conn):

	c =  conn.cursor()

	build_name, build_level, build_future_level = build

	build_id = get_build_id(build_name, conn)

	c.execute("""select build_id from %s where build_id = '%s'""" %(BUILD_INFO_TABLE, build_id))

	ret = c.fetchall()

	# Se for zero, quer dizer que eh a primeira vez que essa build aparece
	# entao temos que inserir um novo registro
	if len(ret) is 0:
		c.execute("""insert into %s values ('%s', %s, %s)""" %(BUILD_INFO_TABLE, build_id, build_level, build_future_level))
	# Caso contrario, vamos soh atualizar os levels
	else:
		c.execute("""update %s set build_level = %s and build_future_level = %s
			where build_id = '%s'""" %(BUILD_INFO_TABLE, build_level, build_future_level, build_id))

	conn.commit()

def update_build_construct(br, conn)

	BUILD  = False
	WOOD   = False
	IRON   = False
	STONE  = False
	WORKER = False
	TIME   = False
	LAST   = False

	for i in br.response().readlines():
		
		#print "--", i,

		if not BUILD and re_pr_build_name.match(i):
			t = re_pr_build_name.search(i)
			BUILD = t.group("build")
			#print "build = %s" %i,

			WOOD   = False
			IRON   = False
			STONE  = False
			WORKER = False
			TIME   = False
			LAST   = False

			continue

		if BUILD and re_pr_finished.match(i):
			WOOD   = -3
			IRON   = -3
			STONE  = -3
			WORKER = -3
			TIME   = -3
			LAST   = -3

		if not WOOD and re_pr_wood.match(i):
			t = re_pr_wood.search(i)
			WOOD = t.group("wood")
			#print "wood = %s" %i,
			continue

		if not IRON and re_pr_iron.match(i):
			t = re_pr_iron.search(i)
			IRON = t.group("iron")
			#print "iron = %s" %i,
			continue

		if not STONE and re_pr_stone.match(i):
			t = re_pr_stone.search(i)
			STONE = t.group("stone")
			#print "stone = %s" %i,
			continue

		if not WORKER and re_pr_worker.match(i):
			t = re_pr_worker.search(i)
			WORKER = t.group("worker")
			#print "worker = %s" %i,
			continue

		if not TIME and re_pr_time.match(i):
			t = re_pr_time.search(i)
			TIME = t.group("time")
			#print "time = %s" %i,
			continue

		if not LAST and TIME :
			LAST = i.strip()
			#print "last = %s" %i,

		if BUILD and WOOD and IRON and STONE and WOOD and TIME and LAST:

			LAST = get_last_id(LAST)

			print "------------------"
			print BUILD
			print WOOD
			print STONE
			print IRON
			print WORKER
			print TIME
			print LAST

			BUILD  = False
			WOOD   = False
			IRON   = False
			STONE  = False
			WORKER = False
			TIME   = False
			LAST   = False
	

def update_build(br, conn):

	response = br.response()

	for i in response.readlines():
		if re_build_level.match(i):
			t = re_build_level.search(i)
			build = t.group("build").decode('utf-8')
			level = t.group("level")
			#print "+", i,
			sql_update_build_info([ build, level, 0], conn)

def db_start():

	conn = sqlite3.connect('tribal.db')
	return conn


def check_if_table_exist(table_name, cur):

	cur.execute("pragma table_info(%s)" %table_name)
	
	ret = cur.fetchall()

	print ret

	if len(ret) is 0:
		return False
	else:
		return True


def create_all_tables(conn):

	cur = conn.cursor()

	for table_name, table_sql in SQL_TABLE_LIST:
		if check_if_table_exist(table_name, cur) is False:
			sql_exec = '''CREATE TABLE %s (%s)''' %(table_name, table_sql)
			print sql_exec
			cur.execute(sql_exec)

	conn.commit()


def open_overview(br):
	try:
		#text='Aldeia de tribalwbot'
		link = br.find_link(text_regex=re.compile("Aldeia de .*"))
		print link
		response = br.follow_link(link)
	except:
		pass

	return br

def open_principal(br):
	try:
		#text='Edif\xc3\xadcio principal'
		link = br.find_link(text_regex=re.compile("Edif.*cio principal"))
		response = br.follow_link(link)
	except:
		pass

	return br

# 0 - Pronto para produzir
# 1 - Tempo para poder fazer
# 2 - Falta Fazenda
# 3 - Totalmente Construido
def get_last_id(last):

	if last is -3:
		return 3

	if re_pr_expand.match(last) or re_pr_make.match(last):
		return 0

	if re_pr_wait.match(last):
		time = t.group("time").decode('utf-8')
		print time
		return 1

	if re_pr_farm.match(last):
		return 2

	if re_pr_finished.match(last):
		return 3

	if re_pr_full.match(last):
		return 4


	print last
	raise "Error"

def create_user(username, mail):

	result = br.open(url)
	br.select_form(nr=0)

	response = br.submit()

	br.select_form(nr=1)

	br["name"] = username
	br["password"] = "12345678"
	br["password_confirm"] = "12345678"
	br["email"] = mail
	br.form.find_control("agb").items[0].selected = True

	response = br.submit()

#mail = "tw_123+tw_123_1@gmail.com"
#create_user("tw_123_1", mail) 

conn = db_start()
create_all_tables(conn)

br = start_browser()
br = open_tribal(br, proxy=PROXY_URL)
update_build(br, conn)
br = open_principal(br)
update_build_construct(br, conn)


