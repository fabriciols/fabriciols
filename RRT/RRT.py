# -*- coding: latin-1 -*-

import win32com.client
import os
import sys
import difflib
import webbrowser

# VERSAO = "0.1"
# DATA = 19/06/09
# Fabricio Lopes de Souza
# Versao inicial
# VERSAO = "0.2"
# DATA="19/06/09"
# Fabricio Lopes de Souzs
# Alteracao para corrigir a divergencia no diff de alguns arquivos
# VERSAO = "0.3"
# DATA="22/06/09"
# Fabricio Lopes de Souzs
# Remocao dos arquivos .MAK .MAP na hora de fazer o diff
# VERSAO="0.4"
# DATA="23/06/09"
# Fabricio Lopes de Souzs
# Possibilidade de procurar por projetos
# Adicionando novo parametro para isso: PROJETO
# Mudando o nome do parametro BUG para LABEL, tornando-o mais adequado
# VERSAO="0.5"
# DATA="03/07/09"
# Adicionando a possibilidade de tentar com outro usuario/senha
# VERSAO="0.6"
# DATA="07/07/09"
# Reformulada a funcao de selecionar a base
# Melhorada o esquema de troca de usuario
# Saida agora eh feita em arquivo (com o nome do label + .txt)
# VERSAO="0.7"
# DATA="07/07/09"
# Adicionada a base da R47
# VERSAO="0.8"
# DATA="08/07/09"
# Adicionada a opcao '-b' que abre um browser com o diff de cada arquivo
# e propicia ao usuário a entrada manual de linhas modificadas
# Reduzindo o tamanho das mensagens printadas no console
# Adicionando a opcao '-m' para selecionar o modulo desejado
# Por padrao temos o APL definido (por enqnto temos APL/USG
# FILE_EXCLUDE agora nao procura soh por extensão, e sim no nome todo
# VERSAO="0.9"
# DATA="14/07/09"
# Adicionado opcao -u e -p, para usuario e password
# VERSAO="0.91"
# DATA="15/07/09"
# Adicionando os modulos RETAGUARDA e SERVER
VERSAO="0.92"
DATA="15/07/09"
# Adicionando o fonte no GOOGLE CODE

FILE_EXCLUDE = [
	".MAK",
	".MAP",
	".DOC",
   ".SO",
	".A",
	"TAGS",
]


USER_LIST = [
	[ "usuario"    , "Nome Completo"              , "Tempo de experiencia",         	   "Cargo"                      ],
	[ "fabriciols" , "Fabricio Lopes de Souza"    , "Menos de 3 anos de experiencia",   "Analista/Engenheiro Junior" ],
	[ "kemmel"     , "Kemmel Scarpellini"         , "Menos de 3 anos de experiencia",   "Analista/Engenheiro Junior" ],
	[ "dpsilva"    , "Danilo Penin"               , "Menos de 3 anos de experiencia",   "Analista/Engenheiro Junior" ],
	[ "mizutani"   , "Thiago Mizutani"            , "Menos de 3 anos de experiencia",	"Analista/Engenheiro Junior" ],
	[ "mftoledo"   , "Marcelo Ferrari Toledo"     , "Entre 5 e 10 anos de experiencia", "Analista/Engenheiro Especialista" ],
	[ "fabiobs"    , "Fabio Brochado da Silva"    , "Entre 5 e 10 anos de experiencia", "Analista/Engenheiro Especialista" ],
	[ "rosanab"    , "Rosana Bergamasco Kamimura" , "Mais de 10 anos de experiencia",   "Analista/Engenheiro Especialista" ],
	[ "claudiol"   , "Claudio Ling"               , "Entre 5 e 10 anos de experiencia", "Analista/Engenheiro Especialista" ],
	[ "rmoroz"     , "Raphael Moroz Mazzaro"      , "Entre 5 e 10 anos de experiencia", "Analista/Engenheiro Senior" ],
]

APL_BASE_LIST = [
	[ "siacbrasil_R1"  , "\\\\srvti104\sh124\SWSIAC\VSS_CMMI\siacbrasil_R1"      , "$/siacbrasil/desenvolvimento" ],
	[ "siacbrasilR314" , "\\\\srvti104\sh106\VSS_CMMI\VssSIAC\SWSiacStore_CMMI"  , "$/siacbrasilR314/desenvolvimento" ],
	[ "siacbrasilR317" , "\\\\srvti104\sh106\VSS_CMMI\VssSIAC\SWSiacStore_CMMI"  , "$/siacbrasilR317/desenvolvimento" ],
	[ "siacbrasilR319" , "\\\\srvti104\sh106\VSS_CMMI\VssSIAC\SWSiacStore_CMMI"  , "$/siacbrasilR319/desenvolvimento" ],
	[ "siacbrasilR321" , "\\\\srvti104\sh106\VSS_CMMI\VssSIAC\SWSiacStore_CMMI"  , "$/siacbrasilR321/desenvolvimento" ],
	[ "R47"            , "\\\\srvti104\sh106\VSS_CMMI\VssSIAC\SWSiacBR"          , "$/siac/desenvolvimento" ],
]

APL_DIR_LIST = [ 
	'apl/bin/dos' ,
	'apl/bin/linux',
	'apl/include',
	'apl/source/comum',
	'apl/source/dos',
	'apl/source/linux',
	'sta/bin/dos' ,
	'sta/bin/linux',
	'sta/include/comum',
	'sta/include/dos',
	'sta/include/linux',
	'sta/source/comum',
	'sta/source/dos',
	'sta/source/linux' ]

APL_ROOT_DIR = "pos"

USG_BASE_LIST = [
	[ "usg" , "\\\\srvti104\sh106\VSS_CMMI\VssComum\SWSiacComum", "$/desenvolvimento" "pos/lib/gdac/usg" ]
]

USG_DIR_LIST = [
	"comum",
	"dos",
	"linux",
]

USG_ROOT_DIR = "pos/lib/gdac/usg"

SERVER_ROOT_DIR = "server"

SERVER_DIR_LIST = [
	"bin",
	"include",
	"source",
]

RET_ROOT_DIR = "retaguarda"

ALL_BASE_LIST = { "APL" : APL_BASE_LIST, "USG" : USG_BASE_LIST, "SERVER" : APL_BASE_LIST   , "RET" : APL_BASE_LIST}
ALL_DIR_LIST  = { "APL" : APL_DIR_LIST , "USG" : USG_DIR_LIST , "SERVER" : SERVER_DIR_LIST , "RET" : SERVER_DIR_LIST}
ALL_ROOT_DIR  = { "APL" : APL_ROOT_DIR , "USG" : USG_ROOT_DIR , "SERVER" : SERVER_ROOT_DIR , "RET" : RET_ROOT_DIR}

	
USERNAME = 'fabriciols'
PASSWORD = 'fabriciols'

LABEL_FINAL = -1
	

def checkActionEnd(Action, start):
	if Action.startswith('Checked in'):
		return 1

	if Action.startswith('Added'):
		return 1

	if Action.startswith('Created'):
		return 1

	if Action.startswith('Label') and LABEL_FINAL is not -1 and start is 2:
		return 1

	return 0

def fail(msg):
	out = sys.stderr.write
	out(msg + "\n\n")
	return 0

def select_base(pr=False):

	if pr is False:
		i = 0
		print "Selecione a base correspondente:"
		for base in BASE_LIST:
			print "%-2.0d| %-15s - %-20s (%s)" %(i+1, base[0], base[2], os.path.basename(base[1]))
			i += 1
		n = int(raw_input("Numero da Base: "))
		return n-1
	return -1

# open a file & return the file object; gripe and return 0 if it
# couldn't be opened
def fopen(fname):
	try:
		return open(fname, 'U')
	except IOError, detail:
		return fail("couldn't open " + fname + ": " + str(detail))

def writeLine(str):
	file_name = file_out_name
	fd = open(file_name, 'a')
	fd.write(str)
	fd.write('\n')
	fd.close()

# open two files & spray the diff to stdout; return false iff a problem
def fcompare(f1name, f2name, browser=0):

	# Se estamos comparando 2 arquivos iguais
	# Retorna o numero de linhas no arquivo
	# Isso acontece quando estamos revisando um arquivo que foi adicionado
	if f1name == f2name:
		lines = len(open(f1name).readlines())
		return lines

	f1 = fopen(f1name)
	f2 = fopen(f2name)

	if not f1 or not f2:
		return 0

	add_removed = 0
	changed = 0
	changed_2 = 0

	a = f1.readlines(); f1.close()
	b = f2.readlines(); f2.close()

#print "Diff %s - %s" %(f1name, f2name)
	for line in difflib.ndiff(a, b):
		if line.startswith("+") or line.startswith("-"):
			add_removed += 1
		elif line.startswith("?"):
			if line.find("--") is not -1:
				changed_2 += 1
			else:
				changed += 1
		#print line,

	# A cada 2 linhas com "?", temos 1 linha adiciona, mas no arqvivo aparece uma com "+" e uma com "-", por isso
	# removemos a metade
	ret_lines = add_removed - ( changed / 2 ) - changed_2

	# Se escolehu opcao de browser
	# Abre 1 de cada vez
	if browser is 1:
		d = difflib.HtmlDiff()
		diff = d.make_file(b, a, context=True)
		file_name = "%s.html" %f1name
		f3 = open(file_name, 'a')
		f3.write(diff)
		f3.close()
		webbrowser.open_new_tab(file_name)
		s = raw_input("Diff: %-20s Digite o numero de linhas (Sugestao: %.4d): " %(f1name, ret_lines))
		try:
			user_ret_line = int(s)
		except:
			pass
		else:
			ret_lines = user_ret_line

		os.remove(file_name)

	return ret_lines

# Funcao que retorna uma lista de fontes alterados
# Ela procura a partir do ROOT_DIR na base definida em SSafe
def GetFilesByBug(bug, username):

	full_changed_list = []
	user_changed_list = []
	
	for dir in DIR_LIST:

		if bug.upper() == "NULL":
			start = 1
		else:
			start = 0

		full_dir = "%s/%s/%s" %(BASE_LIST[base_num][2], ROOT_DIR, dir)
		print "|- Dir: %s" %full_dir.split('/', 3)[3]
		ss_dir = SSafe.VSSItem(full_dir)

		vers = ss_dir.Versions

		for v in vers:

			#print v.Action

			if start is 0:

				# Se nao comecei ainda, procuro pela label do meu bug
				if v.Action.startswith('Labeled'):
					#print bug, v.Action.find(bug)
					if v.Action.find(bug) is not -1:
						start = 1
				else:
					continue

			else:

				# Se ja comecei, e encontrei um label, finaliza o processo
				if v.Action.startswith('Labeled'):
					# Se foi passado o parametro de um label especifico para o intervalo
					# so para se encontrar ele
					if LABEL_FINAL is not -1:
						#print v.Action, v.Label, v.VersionNumber, start
						if v.Action.find(LABEL_FINAL) is -1:
							continue
					break


				#print v.Username.upper(), username.upper()
				if username.upper() != "NULL":
					if v.Username.upper() != username.upper():
						continue

				# Ajusta pra quando adicionou o arquivo
				if v.Action.startswith('Added'):
					full_name = "%s/%s" %(full_dir, v.Action.replace('Added ', ''))
				else:
					full_name = "%s/%s" %(full_dir, v.VSSItem.Name)

				list = [ full_name, v.Username ]

				# Se ocorreu 2 chek-in no mesmo bug, evita duplicacao
				if isOnList(full_name, full_changed_list) is 0:
					print "|-- %s" %os.path.basename(full_name)
					full_changed_list.append(list)

	return full_changed_list

def isOnList(file_name, full_changed_list):
	for file, user in full_changed_list:
		if file == file_name:
			return 1

	return 0

def get_USER(username):

	username = username.lower()

	for user in USER_LIST:
		if user[0] == username:
			return user
	print username
	return USER_LIST[0]

def do_RRT(bug, username, browser=0):


		print "|--- Procurando arquivos alterados ---|"
		print "|--- bug: %s usuario: %s" %(bug, username)
		list = GetFilesByBug(bug, username)
		file_list = list[0]
		user_list = list[1]

		if len(file_list) is 0:
			print "Sem arquivos alterados para o bug"
			os._exit(0)

		print "|--- Realizando o diff ---|"
		print "|--- Arquivo de saida: %s" %file_out_name

		if os.path.exists(file_out_name):
			os.remove(file_out_name)
	
		for full_dir, user_diff in list:
			#print "-> %s - %s" %(full_dir, user_diff)
			#full_dir = "%s/%s" %(DIR_ROOT, file)

			#print "------ Procurando arquivo : %s -----" %full_dir

			vssitem_list = []
			label = 0
			v_number = 0
			jump = 0

			if bug.upper() == "NULL":
				start = 1
			else:
				start = 0
				
			# Se o arquivo for um dos presentes na lista de excessao
			for fexclude in FILE_EXCLUDE:
				if full_dir.upper().find(fexclude) is not -1:
					jump = 1
					break

			if jump is 1:
				print "- Diff: Ignorado - %s" %os.path.basename(full_dir)
				continue

			try:
				ss_dir = SSafe.VSSItem(full_dir)
			except:
				print "Arquivo fonte: %s nao encontrado" 

			#print "%-30s -" %full_dir.replace(DIR_ROOT,""),

			vers = ss_dir.Versions
			ss_file = SSafe.VSSItem(full_dir)
			vers = ss_file.Versions
			last_v = vers[0]

			for v in vers:
				label_end = 0

				#print "|%s| - |%s| - |%s| - |%d|" %(v.VersionNumber, v.Action, v.Label, start)

				if start is 0:

					# Se nao comecei ainda, procuro pela label do meu bug
					if v.Action.startswith('Labeled'):
						#print bug, v.Action.find(bug)
						if v.Action.find(bug) is not -1:
							start = 1
					else:
						continue

				else:

					# Se ja comecei, e encontrei um label, finaliza o processo
					if v.Action.startswith('Labeled'):
						if start is 1 and LABEL_FINAL is -1:
							break
						else:
							label = 1

					if v.Action.startswith('Checked in'):
						#print "last_v = %s | %s" %(v.VersionNumber, v.Label)
						last_v = v

					# Achamos a versao alterada pelo bug
					# Salvamos o VSSITEM e o numero da versao para procurar a versao anterior
					if checkActionEnd(v.Action, start) is 1:
						if start is 1:
							vssitem_list.append(v)
							start = 2

							# Se o primeiro que achamos eh versao '1'
							# entao nao vamos achar mais
							if int(v.VersionNumber) is 1:
								vssitem_list.append(v)

							#print "Versao: %-3d (Alterada)" %v.VersionNumber,
							continue
						elif start is 2:

							# Se foi passado o parametro de um label especifico para o intervalo
							# so para se encontrar ele
							if LABEL_FINAL is not -1:
								#print "Verifica LABEL_FINAL = %d" %v.Action.find(LABEL_FINAL)
								#print v.Action, v.Label, v,VersionNumber, start
								if v.Action.find(LABEL_FINAL) is -1:
									continue
								else:
									start = 3
									continue

							#print "%-3d (Base)" %v.VersionNumber,

							if len(vssitem_list) is 2:
								vssitem_list[1] = v
							else:
								vssitem_list.append(v)

							if label is 1:
								break
							else:
								continue

						elif start is 3:

							if checkActionEnd(v.Action, start) is 1:
								if len(vssitem_list) is 2:
									vssitem_list[1] = v
								else:
									vssitem_list.append(v)

								if label is 1:
									break
								else:
									continue

			# Como temos as 2 versoes, efetuamos o get delas
			get_name = "%s_%s" %(os.path.basename(sys.argv[0]), os.path.basename(full_dir))

			full_names = []

			for get_item in vssitem_list:
				get_full_name = "%s_%s" %(get_name, get_item.VersionNumber)

				# Por garantia, remove qquer copia pre-existente
				if os.path.exists(get_full_name):
					os.chmod(get_full_name, 0777)
					os.remove(get_full_name)

				# Faz o GET do arquivo (na versao especifica)
				get_item.VSSItem.Get(Local=get_full_name)
				full_names.append(get_full_name)
			
			print "+ Diff: %-12s |%-3d - %3d|" %(os.path.basename(full_dir), vssitem_list[0].VersionNumber, vssitem_list[1].VersionNumber)

			user = get_USER(user_diff)

			changed = fcompare(full_names[0], full_names[1], browser=browser)

			for name in full_names:
				if os.path.exists(name):
					os.chmod(name, 0777)
					os.remove(name)

				#print "Linhas Alteradas: %s" %changed
			print_line = "%s\t%d\t%s\t%s\t%s\t%d\t%s" %(full_dir.replace(BASE_LIST[base_num][2],''),
				vssitem_list[0].VersionNumber, user[1], user[2], user[3], changed, "Item OK")
			writeLine(print_line)

#print v.Action, v.VSSItem, v.Label, v.VersionNumber

def openBase(baseNum):

	baseUrl = "%s\\%s" %(BASE_LIST[base_num][1], "srcsafe.ini") 
	
#username = "fabriciols"
#password = "kemmel"

	print "- Abrindo url: %s" %baseUrl

	#Vamos procurar o projeto nesta base
	try:
		print "- Tentando logar com usuario:<%s> senha:<%s>" %(USERNAME, PASSWORD)
		SSafe.Open(baseUrl, USERNAME, PASSWORD)
	except:
		print "- Falha no login"
		os._exit(0)
	else:
		print "- Login ok"
		return 1

def findBase(baseName):
	i = 0
	n = -1
	for base in BASE_LIST:
		if base[0].upper().find(baseName.upper()) is not -1:
			print "|-- %-15s - %-20s (%s)" %(base[0], base[2], os.path.basename(base[1]))
			n = i
			break
		else:
			i += 1
	
	if n is -1:
		print "- Base: %s nao encontrada" %baseName

	return n

def usage():
	print "%s : LABEL USUARIO [BASE] [PROJETO] [-bm]" %os.path.basename(sys.argv[0])
	print "LABEL   - Label onde ocorreu a alteracao"
	print "USUARIO - Usuario que realizou a alteracao ( 0 para todos )"
	print "BASE    - Base que deseja analizar ( nao precisa ser o nome completo )"
	print "PROJETO - Numero do projeto que deseja usar (somente pode ser usado em conjunto com a opcao BASE)"
	print "-L LABEL- Especifica um label de termino, nao terminando no primeiro label encontrado"
	print "-b      - Abre um browser com o DIFF, dando a opcao de entrar manualmente o numer de linhas"
	print "-m MOD  - Modulo a ser revisado (Atualmente os suportados sao APL/USG/SERVER/RET) Default: APL"
	print "caso a opcao -m seja usada com o parametro SERVER/RET, ela deve ser precedida com o nome do SUBMODULO"
	print "Exemplo: -m SERVER grapar	ou -m RET cryto"
	print "-u USER - Usuario para logar no SSAFE"
	print "-p PASS - Senha para logar no SSAFE"

if __name__ == '__main__':

	print "|----------------------------------"
	print "|-- %s - Versao: %-3s (%8s)" %(os.path.basename(sys.argv[0]), VERSAO, DATA)
	print "|----------------------------------"
	print

	if (len(sys.argv)) < 3:
		usage()
		os._exit(0)

	SSafe = win32com.client.Dispatch("SourceSafe")

	###############
	# "Globais"
	###############
	ssafe_base = 0
	base_num = -1
	opened = 0
	browser = 0
	len_args = 0
	module = 0
	SUBMODULE = 0
	###############

	j = 0

	# Parser dos paramestros
	for i in sys.argv:
		if i.upper().find('-B') is not -1:
			browser = 1
		elif i.upper().find('-M') is not -1:
			module = sys.argv[j+1]
			if module.upper() == "SERVER" or module.upper() == "RET":
				SUBMODULE = sys.argv[j+2]
				len_args -= 1
			len_args -= 1
		elif i.upper().find('-U') is not -1:
			USERNAME = sys.argv[j+1]
			len_args -= 1
		elif i.upper().find('-P') is not -1:
			PASSWORD = sys.argv[j+1]
			len_args -= 1
		elif i.upper().find('-L') is not -1:
			LABEL_FINAL = sys.argv[j+1]
			len_args -= 1
		else:
			len_args += 1
		j += 1

	if module is 0:
		module = "APL"

	file_out_name = "%s_%s" %(sys.argv[1], module)

	# Define as constantes por modulo
	BASE_LIST = ALL_BASE_LIST[module.upper()]
	DIR_LIST  = ALL_DIR_LIST[module.upper()]
	ROOT_DIR  = ALL_ROOT_DIR[module.upper()]

	if SUBMODULE is not 0:
		ROOT_DIR = "%s/%s" %(ROOT_DIR, SUBMODULE)
		file_out_name = "%s_%s" %(SUBMODULE)

	file_out_name = "%s.txt" %file_out_name

	if len_args is 3:
		base_num = select_base()
	else:
		base_num = findBase(sys.argv[3])

		if base_num is -1:
			base_num = select_base()

	if len_args is 5:

		projeto = sys.argv[4]

		file_out_name = "%s_%s" %(projeto, file_out_name)

		opened = openBase(base_num)

		ss_dir = SSafe.VSSItem("$/%s" %(projeto))

		# Varremos as linhas de projeto
		i = 1
		print "|-- Procurando linhas de projeto"
		for node in ss_dir.Items:
			if node.Name.upper() != "documento".upper():
				print "|-- %-3d | %s" %(i, node.Name)
				i += 1

		if i is not 2:
			n = int(raw_input("Escolha a linha a ser utilizada: "))
		else:
			n = 1

		linha = ss_dir.Items[n-1].Name

		project_path = "$/%s/%s" %(sys.argv[4], linha)

		print "|-- Linha utilizada: %s" %project_path

		BASE_LIST[base_num][2] = project_path

	# Inicializacao do SourceSafe
	if opened is 0:
		opened = openBase(base_num)

	do_RRT(sys.argv[1], sys.argv[2], browser=browser)

else:
	print "Module %s loaded." %sys.argv[0]
