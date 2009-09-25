import win32com.client
import time
import os
import sys

USER_LIST = [
	[ "usuario"    , "Nome Completo"              , "Tempo de experiencia",         	   "Cargo"                      ],
	[ "fabriciols" , "Fabricio Lopes de Souza"    , "Menos de 3 anos de experiencia",   "Analista/Engenheiro Junior" ],
	[ "kemmel"     , "Kemmel Scarpellini"         , "Menos de 3 anos de experiencia",   "Analista/Engenheiro Junior" ],
	[ "dpsilva"    , "Danilo Penin"               , "Menos de 3 anos de experiencia",   "Analista/Engenheiro Junior" ],
	[ "mizutani"   , "Thiago Mizutani"            , "Menos de 3 anos de experiencia",	"Analista/Engenheiro Junior" ],
	[ "mftoledo"   , "Marcelo Ferrari Toledo"     , "Entre 5 e 10 anos de experiencia", "Analista/Engenheiro Especialista" ],
	[ "fabiobs"    , "Fabio Brochado da Silva"    , "Entre 5 e 10 anos de experiencia", "Analista/Engenheiro Especialista" ],
	[ "rosanab"    , "Rosana Bergamasco Kamimura" , "Mais de 10 anos de experiencia",   "Analista/Engenheiro Especialista" ],
	[ "claudiol"   , "Claudio Yua Shen Ling"      , "Entre 5 e 10 anos de experiencia", "Analista/Engenheiro Especialista" ],
	[ "rmoroz"     , "Raphael Moroz Mazzaro"      , "Entre 5 e 10 anos de experiencia", "Analista/Engenheiro Senior" ],
	[ "nnesouza"   , "Nildson Nei Elias de Souza" , "Entre 5 e 10 anos de experiencia", "Analista/Engenheiro Especialista" ],
]

def get_USER(username):

	username = username.lower()

	for user in USER_LIST:
		if user[0] == username:
			return user
	print username
	return USER_LIST[0]


def ChangeBugNum(bug, book):
	# Informacao do Bug que fica na aba 'Projeto'
	sheet = book.Worksheets[1]
	
	SetCell(sheet.Cells(7, 3), bug)

def ChangeDate(book):

	sheet = book.Worksheets[1]

	now = time.localtime(time.time())

	# Data em DD/MM/AA
	# Nao sei pq diabos a data da primeira aba eh invertida MM/DD/AA
	# o_o
	now_str = time.strftime("%m/%d/%Y", now)
	SetCell(sheet.Cells(11, 3), now_str)

	now_str_2 = time.strftime("%d/%m/%Y", now)
	sheet = book.Worksheets[2]
	SetCell(sheet.Cells(5, 4), now_str_2)
	
def ChangeResp(resp, book):

	sheet = book.Worksheets[1]

	user = get_USER(resp)

	SetCell(sheet.Cells(11, 4), user[1])

	sheet2 = book.Worksheets[2]

	SetCell(sheet2.Cells(11, 4), user[1])

def ChangeAISOwner(owner, book):

	# Aba resumo
	sheet = book.Worksheets[2]

	user = get_USER(owner)

	# Define o nome
	SetCell(sheet.Cells(7, 4), user[1])

	# Define a experiencia
	SetCell(sheet.Cells(8, 4), user[2])

	# Define o Cargo
	SetCell(sheet.Cells(9, 4), user[3])

	# Define o moderador que sempre eh o Zanni
	SetCell(sheet.Cells(10, 4), 'Ricardo Zanni')

	# Define o numero da revisao, sempre 1
	SetCell(sheet.Cells(4, 4), '1')

	# Define o tempo, sempre 01:00
	SetCell(sheet.Cells(6, 4), '01:00')

def SetAccept(book):

	sheet = book.Worksheets[2]

	SetCell(sheet.Cells(14, 4), 'Aprovado')
	SetCell(sheet.Cells(12, 4), 'Individual/Peer Review')

def SetCell(cell, value):

	cell.Font.Color  = 0x000000
	cell.Font.Bold   = False
	cell.Font.Italic = False
	cell.Value = value

def SetChecklist(book):

	#Aba Checklist RT 1
	sheet = book.Worksheets[3]

	# Define o checklist
	SetCell(sheet.Cells(6, 5), 'Item OK')
	SetCell(sheet.Cells(7, 5), 'Nao se Aplica')
	SetCell(sheet.Cells(8, 5), 'Item OK')
	SetCell(sheet.Cells(9, 5), 'Item OK')
	SetCell(sheet.Cells(10, 5), 'Nao se Aplica')
	SetCell(sheet.Cells(11, 5), 'Nao se Aplica')
	SetCell(sheet.Cells(12, 5), 'Item OK')
	SetCell(sheet.Cells(13, 5), 'Item OK')
	SetCell(sheet.Cells(14, 5), 'Nao se Aplica')
	SetCell(sheet.Cells(15, 5), 'Item OK')
	SetCell(sheet.Cells(16, 5), 'Item OK')
	SetCell(sheet.Cells(17, 5), 'Item OK')
	SetCell(sheet.Cells(18, 5), 'Item OK')
	SetCell(sheet.Cells(19, 5), 'Item OK')
	SetCell(sheet.Cells(20, 5), 'Item OK')
	SetCell(sheet.Cells(21, 5), 'Item OK')
	SetCell(sheet.Cells(22, 5), 'Item OK')


def SaveFile(bug, book):
	# Padrao de nome RRT_AIS_999999.xls
	book.SaveAs("%s/RRT_AIS_%06d.xls" %(os.getcwd(), int(bug)));


def ChangeProject(book, project=False):

	sheet = book.Worksheets[1]

	if project is False:
		SetCell(sheet.Cells(5, 3), '63450')
		SetCell(sheet.Cells(6, 3), 'Manutencao 2009 {Siac_Brasil}')

def do_RRT_AIS(bug, resp, owner):

	file_name = "%s/RRT_AIS_999999.xls" %os.getcwd()
	excel = win32com.client.Dispatch("Excel.Application")
	excel.Visible = 1
	book = excel.Workbooks.Open(file_name)

	ChangeBugNum(bug, book)
	ChangeDate(book)
	ChangeResp(resp, book)
	ChangeAISOwner(owner, book)
	ChangeProject(book);
	SetAccept(book)
	SetChecklist(book)
	SaveFile(bug, book)
#excel.Quit()

def usage():
	print "%s : BUG AUTOR -r RESPONSAVEL" %os.path.basename(sys.argv[0])
	print "BUG     - Numero do bug que sera realizado a AIS"
	print "AUTOR   - Quem fez a AIS que devera ser revisada"
	print "-r RESP - Quem e o responsavel pela a RRT"


if __name__ == '__main__':

	if len(sys.argv) < 3:
		usage()
		os._exit(1)

	# Trata linha de comando
	bug   = sys.argv[1]
	owner = sys.argv[2]

	try:
		resp = sys.argv[4]
	except:
		resp = os.environ['UserName']

	do_RRT_AIS(bug, resp, owner)

