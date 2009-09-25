import socket
import re
#from mechanize import Browser
import mechanize
import md5
import os, sys
import time

# Expressoes regulares para capturar areas de interesse
er_apl = re.compile('itautec-possbr-5.(?P<versao>[0-9]*).(?P<release>[0-9]*)-.*.rpm')
er_dg = re.compile('.*id="(?P<dg>DataGrid__ctl[^\"]*)\".*')
er_libteste = re.compile('.*<td><font color="#003399" size="2">SiacBr</font></td><td><font color="#003399" size="2">(?P<module>[^<]*)</font>.*')
er_prj = re.compile('</font></td><td><font color="#003399" size="1">(?P<versao>.*)</font></td><td><font color="#003399" size="1">(?P<release>.*)</font></td><td><font color="#003399" size="1">(?P<projeto>.*)</font></td><td><font color="#003399" size="1">(?P<tpprj>.*)</font></td><td><font color="#003399" size="1">(?P<nomeprj>.*)</font></td><td><font color="#003399" size="1">&nbsp;</font></td><td><font color="#003399" size="1">&nbsp;</font></td><td><font color="#003399" size="1">&nbsp;</font></td><td><font color="#003399" size="1">&nbsp;</font></td><td><font color="#003399" size="1"></font></td>')

# Se vc esta em um ambiente onde nao eh possivel acessar o orkut direto , deixe PROXY=1

# URL
SIACLIB_URL = 'http://siaclib/siaclib/Login.aspx'
MODULO_URL  = 'http://siaclib/Siaclib/modulo.aspx'
PROJETO_URL = 'http://siaclib/Siaclib/GerenciamentoProjeto.aspx'
PROJETOMODULO_URL = 'http://siaclib/Siaclib/AlteracaoModulo.aspx'

USER = 'fabriciols'
PASS = 'fernanda'

md5_list = {}

def do_all():

	user_name = ""

	module_name = sys.argv[1]

	if len(sys.argv) == 3:
		user_name = sys.argv[2]

	if len(user_name) is 0:
		user_name = "fabriciols"

	# Define qual a versao/release do aplicativo
	if er_apl.match(module_name):
		t = er_apl.search(module_name)
		versao  = "V5%s" %t.group('versao')
		release = "R%s"  %t.group('release')
	else:
		versao  = raw_input("Versao do projeto  (Exemplo: 551/570) : ")
		release = raw_input("Release do Projeto (Exemplo: R47/R324): ")

		if not versao.startswith('V'):
			versao = "V%s" %versao

		if not versao.startswith('R'):
			release = "R%s" %release
	# --------------------------------------

	br = browser_start()
	do_login(br)

	insert_module(br, versao, release, module_name, user_name)

	project_name = find_project (br, versao, release, module_name, user_name)

	lines = br.open(PROJETOMODULO_URL)

	insert_module_on_project(br, module_name, user_name)

	#find_project (br, versao, release, module_name, user_name, project=project_name)
	#send_module(br, module_name)


def send_module(br, module_name):

	lines = br.reload()
	find_module = False

	for i in lines.readlines():
		if find_module is False:
			if er_libteste.match(i):
				#print i,
				t = er_libteste.search(i)
				module = t.group('module')
				if module == module_name:
					find_module = True

		else:

			if er_dg.match(i):
				if i.find('alt="Liberar"') is not -1:
					break

	t = er_dg.search(i)
	grid_tmp = t.group('dg')
	grid = grid_tmp.replace("__",":_").replace("_Image",":Image");

	print grid

	for i in br.forms():
		print i

	br.select_form(nr=find_form_by_control(grid, br))
	lines = br.open(br.form.click(name=grid.split(':')[-1]))

	for i in lines.readlines():
		print i

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

	print "---> Iniciando o Browser"

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

def do_login(br):

	print "---> Efetuando login"

	lines = br.open(SIACLIB_URL)
	br.select_form(nr=find_form_by_control("txtUsers", br))
	br["txtUsers"]    = USER
	br["txtPassword"] = PASS

	print("--> Usuario %s" %USER )

	br.submit()

	print "---> Login efetuado"

def find_project(br, versao, release, module_name, user_name, project=False):

	find = False
	input_name = False

	lines = br.open(PROJETO_URL)
	br.select_form(nr=0)

	try:
		br["FiltroVersaoReleaseProjeto:cmbVersao"] = [ versao ]
		br["FiltroVersaoReleaseProjeto:cmbProduto"] = [ "SiacBr" ]
	except:
		print "Nao existe nenhum item com versao = %s" %versao
		os._exit(0)

	lines = br.open(br.form.click(name="ToolBar1:ImageButton2"))

	print("--> Filtrando por versao: %s" %versao)

	br.select_form(nr=0)
	try:
		br["FiltroVersaoReleaseProjeto:cmbRelease"] = [ release ] 
	except:
		print "Nao existe nenhum item com release = %s" %release
		os._exit(0)

	lines = br.open(br.form.click(name="ToolBar1:ImageButton2"))

	print("--> Filtrando por release: %s" %release)

	br.select_form(nr=0)
	try:
		br["FiltroVersaoReleaseProjeto:cmbUsuario"] = [ user_name ]
	except:
		print "Nao existe nenhum item com usuario = %s" %user_name
		os._exit(0)

	lines = br.open(br.form.click(name="ToolBar1:ImageButton2"))

	print("--> Filtrando por usuario: %s" %user_name)

	list = []
	find_grid = False

	for i in lines.readlines():
		if find_grid is False:
			if er_dg.match(i):
				t = er_dg.search(i)
				grid_tmp = t.group('dg')
				grid = grid_tmp.replace("__",":_").replace("_Image",":Image");
				find_grid = True
		else:
			t = er_prj.search(i)
			versao  = t.group('versao')
			release = t.group('release')
			projeto = t.group('projeto')
			tpprj   = t.group('tpprj')
			nomeprj = t.group('nomeprj')
			nome_item = "| %s | %s | %s | %s | %s |" %(versao, release, projeto, tpprj, nomeprj)
			list.append([grid, nome_item])
			find_grid = False


			if project is not False:

				if project.find(projeto) is not -1:
					print "Projeto Selecionado:"
					print nome_item
					find = True
					n = len(list)

	if find is False:
		print("--> Projetos encontrados: %d" %len(list))
					
		if len(list) > 1:
			print "Mais de um projeto encontrado"

		if len(list) is 0:
			print "Nenhum projeto encontrado"
			os._exit(0)

		print "Digite o numero do projeto desejado:"
		i = 0
		for grid, nome_item in list:
			i = i + 1
			print "%d - %s" %(i, nome_item)

		n = int(raw_input("Numero do Projeto : "))

	input_name = list[n-1][0]

	br.select_form(nr=find_form_by_control(input_name, br))
	lines = br.open(br.form.click(name=input_name))


	return list[n-1][1].split('|')[3]


def insert_module(br, versao, release, module_name, user_name):

	print "---> Adicionando modulo"

	lines = br.open(MODULO_URL)
	br.select_form(nr=find_form_by_control("btnAdd", br))
	lines = br.open(br.form.click(name="btnAdd"))
	br.select_form(nr=find_form_by_control("cmbProduct", br))

	br["cmbProduct"]    = [ "SiacBr" ]
	br["txtModule"]     = module_name
	br["txtDesc"]       = "Aplicativo Linux"
	br["cmbModuleType"] = [ "frente" ]
	br["txtPathVss"]    = "siac/carga_pdv_linux/install_rpm"

	lines = br.open(br.form.click(name="btnOk"))

	print "---> Modulo inserido"

def insert_module_on_project(br, module_name, user_name):
	print "---> Adicionando modulo ao projeto"

	br.select_form(nr=find_form_by_control("btnAdd", br))
	lines = br.open(br.form.click(name="btnAdd"))

	br.select_form(nr=0)
	br["cmbProduto"]    = [ "SiacBr" ]

	print "--> Enviando Solicitacao"

	br.submit()

	br.select_form(nr=0)
	br["cmbModulo" ]    = [ module_name ]
	br["txtDescricao" ] = "Aplicativo Linux PDV"

	print "--> Finalizando Insercao"

	lines = br.open(br.form.click(name="btnOk"))

	return

# --- MAIN ---

#module_name = 'itautec-possbr-5.51.323-R00.P01.SL.i386.rpm'
if __name__ == '__main__':

	if len(sys.argv) > 1:
		do_all()
