import socket
import mechanize
from unicodedata import normalize

PROXY_USERNAME = 'fabriciols'
PROXY_PASSWORD = 'rootroot12345'

BUGZILLA_USERNAME = 'fabriciols'
BUGZILLA_PASSWORD = '171086'

BUGZILLA_ROOT_URL  = 'http://bugzilla-cmmi.itautec.com'
BUGZILLA_LOGIN_RUL = '%s/index.cgi?GoAheadAndLogIn=1' %BUGZILLA_ROOT_URL
BUGZILLA_BUG_URL   = '%s/show_bug.cgi?id='            %BUGZILLA_ROOT_URL
BUGZILLA_ATTACH_URL= "%s/attachment.cgi?bugid=%s&action=enter" %BUGZILLA_ROOT_URL

def remover_acentos(txt, codif='utf-8'):
	return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

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

	br.set_handle_robots(False)
	br.set_proxy_password_manager(None)

	# Desabilita o proxy
	br._set_handler("_proxy",  obj=None);
   
	socket.setdefaulttimeout(30)

	return br

def do_login(br, username, password):

	lines = br.open(BUGZILLA_LOGIN_RUL)

	br.select_form("login")
	br["Bugzilla_login"]    = "%s@itautec.com" %username
	br["Bugzilla_password"] = password

	response = br.submit()

def get_bug_fields(br, bug):

	bug_url = "%s%s" %(BUGZILLA_BUG_URL, bug)

	lines = br.open(bug_url)

	br.select_form("changeform")

	bug_fields = { 
		'produto'   : remover_acentos(br["product"][0]),
		'componente': remover_acentos(br["component"][0]),
		'plataforma': remover_acentos(br["rep_platform"][0]),
		'os'        : remover_acentos(br["op_sys"][0]),
		'versao'    : remover_acentos(br["version"][0]),
		'prioridade': remover_acentos(br["priority"][0]),
		'severidade': remover_acentos(br["bug_severity"][0]),
		'tr'        : remover_acentos(br["cf_transicao"][0]),
		'pacote'    : remover_acentos(br["cf_pacote"][0]),
		'fornecedor': remover_acentos(br["cf_fornecedor"][0]),
		'resolucao' : remover_acentos(br["resolution"][0]),
	}

	return bug_fields

def get_desc_by_tr(tr):
	if tr   == "10":
		return "Finalizar Analize"
	elif tr == "7":
		return "Solicitar esclarecimento"
	elif tr == "19":
		return "Finalizar Desenvolvimento"
	else:
		return "TR INVALIDO"

def attach_file(br, filename_cy):
	pass



# --- MAIN ---
#br = browser_start()

#do_login(br)

#fields = get_bug_fields('133')

#do_all_job(br, fields)
