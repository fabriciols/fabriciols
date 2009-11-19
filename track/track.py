import re
#from mechanize import Browser
import mechanize
import os, sys
import time as time_sleep
import winsound
import socket
import smtplib

# URL
CORREIOS_URL = 'http://websro.correios.com.br/sro_bin/txect01$.Inexistente?P_LINGUA=001&P_TIPO=002&P_COD_LIS=%s'
#CORREIOS_URL = 'file:///C:/Documents%20and%20Settings/fabriciols/Desktop/python/track/url.html'

# ER
#er_tabela = re.compile('<tr><td rowspan=(?P<count>[0-9])>(?P<time>[^<]*)')
er_item = re.compile('<tr><td rowspan=(?P<count>[0-9])>(?P<time>[^<]*)</td><td>(?P<location>[^<]*).*<FONT [^>]*>(?P<status>[^<*]*)<.*');
er_subitem = re.compile('<tr><td colspan=2>(?P<comment>[^<]*)<')

# Configuracoes de email
smtpServer='smtp.itautec.com';
fromAddr='track@itautec.com';

def find_form_by_control(control, br):

	j = 0
	for i in br.forms():
		try :
			i.find_control(name=control)
		except :
			j += 1
			continue
		else :
			return( j )
	return ( -1 )

def browser_start():

	br = mechanize.Browser()

	# Debug do protocolo HTTP
	#br.set_debug_redirects(True)
	#br.set_debug_responses(True)
	#br.set_debug_http(True)

	br.set_proxies({"http": "net\\fabriciols:rootroot@proxy.intranet:80"})

	br.set_handle_robots(False)

	# Desabilita o proxy
	#br._set_handler("_proxy",  obj=None);
	#br.set_proxy_password_manager(None)
   
	socket.setdefaulttimeout(60)

	return br

def usage():
	print "%s : [TRACK_NUMBER]* [ -t SEGUNDOS] [-e EMAIL]" %os.path.basename(sys.argv[0])
	print "TRACK_NUMBER - Numero do rastreio, podendo ser N numeros separado por espaco (' ')"
	print "-t SEGUNDOS  - Intervalo de tempo entre as checagens                Default:3600 (1hr)"
	print "-e EMAIL     - Endereco de email para avisar qndo houver alteracao  Default:numm (nao manda email)"
	print "-f FILE      - Arquivo contendo os TRACK NUMBERS separado por '\n' apenas 1 por linha"


def do_sendmail(track):

	print "Enviando email. Track = ", track

	if os.path.exists("log.txt"):
		fd = open('log.txt', 'a+')
	else:
		return

	text = fd.read()

	full_text = "Subject: Status do track number: %s\nTo: %s\n\n%s" %(track, EMAIL, text)

	server = smtplib.SMTP(smtpServer)
	#server.set_debuglevel(1)
	server.sendmail(fromAddr, EMAIL, full_text)
	server.quit()

	fd.close()


def myPrint(str):
	print str
	fd = open('log.txt', 'a+')
	fd.write(str)
	fd.write("\n")
	fd.close()

#__MAIN__

if len(sys.argv) is 1:
	usage()
	os._exit(0)

TRACK_LIST   = []
BROWSER_LIST = []
i = 1
EMAIL = False
TIME  = 3600

# Trata os parametros de linha de comando
while i < len(sys.argv):
	if sys.argv[i] == '-t':
		TIME = sys.argv[i+1]
		i += 1
	elif sys.argv[i] == '-e':
		EMAIL = sys.argv[i+1]
		i += 1
	elif sys.argv[i] == '-f':
		for line in open(sys.argv[i+1]):
			comment = ""
			track   = ""

			if line.find('#') is not -1:
				track, comment = line.split('#')
			else:
				# o :-1 eh para tirar o '\n'
				track = line[:-1];

			TRACK_LIST.append([track.upper(), comment[:-1]])
		i += 1
	else:
		TRACK_LIST.append(sys.argv[i], "")

	i += 1

if len(TRACK_LIST) is 0:
	usage()
	os._exit(0)

j=0

num_lines = -1
num_lines_old = -1

# Abre um BROWSER para cada track diferente
for track, comment in TRACK_LIST:
	BROWSER_LIST.append([ track, comment, browser_start(), -1 ])
	print "Abrindo track: %s" %track,
	BROWSER_LIST[j][2].open(CORREIOS_URL %track)
	print "ok"
	j += 1

while 1:
	z=-1
	update = False

	if os.path.exists("log.txt"):
		os.remove("log.txt")

	myPrint("#####################################################################################")

	for track, comment, br, line in BROWSER_LIST:
		z += 1


		# Refresh na pagina
		while 1:
			try:
				lines = br.reload()
				break
			except:
				print "Site Bixado"
				continue

		my_time = time_sleep.strftime('%X %d/%m/%Y')

		myPrint("Atualizando Status (%s)" %my_time)
		myPrint("Track: %s" %track)
		if comment is not "":
			myPrint("Info : %s" %comment)

		myPrint("-------------------------------------------------------------------------------------")
		myPrint("|      HORARIO     |                     LOCAL                 |       STATUS       |")
		myPrint("-------------------------------------------------------------------------------------")

		num_lines_old = line
		num_lines = 0

		for i in lines.readlines():
			if er_item.match(i):
				t = er_item.search(i)
				time = t.group('time')
				count = t.group('count')
				status = t.group('status')
				location = t.group('location')

				myPrint("| %-10s | %-41s | %-18s |" %(time, location, status) )

				num_lines += 1
			elif er_subitem.match(i):
				t = er_subitem.search(i)
				comment = t.group('comment')
				myPrint("| %-16s | %-60s   |" %("  ", comment) )
				myPrint("-------------------------------------------------------------------------------------")
				num_lines+= 1
		myPrint("-------------------------------------------------------------------------------------")

		# Quando as linhas forem diferentes
		# manda email avisando
		if num_lines_old != num_lines:
			if num_lines_old is not -1 and num_lines is not -1:
				update = track
		else:
			print "Pagina nao atualizada (%d == %d)" %(num_lines, num_lines_old)


		BROWSER_LIST[z][3] = num_lines


	if update is not False:
		do_sendmail(update)

		num_bip = 10
		i = 0

		while i < num_bip:
			print "Track atualizado !!!"
			winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
			i += 1

	# 10 minutos de sleep
	i = 0
	sys.stdout.write("Atualizando em : ")
	while i <= TIME:
		sys.stdout.write("%-10d" %(TIME-i))
		print "\b" * 10,
		time_sleep.sleep(1)
		i += 1

	print




