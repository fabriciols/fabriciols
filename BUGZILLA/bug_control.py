import bug        as bug
import xml_parser as xml
import ss         as ss
import sys
import os

RELEASE = "0.1"
DATE    = "16/06/09"

def usage():
	print "Maria"

def print_bug_fields(fields):
	print "|------------------|"
	print "|- Campos do bug: -|"
	print "|------------------|"
	for i in fields.iterkeys():
		print "|- %10s : %s" %(i, fields[i])
	print "|------------------|"

# Preciso no minimo 1 
if len(sys.argv) < 2:
	usage()
	os._exit(0)

BUGZILLA_ID = sys.argv[1]

if len(sys.argv) == 4:
	BUGZILLA_USERNAME = sys.argv[2]
	BUGZILLA_PASSWORD = sys.argv[3]
else:
	BUGZILLA_USERNAME = bug.BUGZILLA_USERNAME
	BUGZILLA_PASSWORD = bug.BUGZILLA_PASSWORD

print "----------------------------------------"
print "-- Bug Control Release %3s (%7s) -- " %(RELEASE,DATE)
print "----------------------------------------"
print
print
print "-------------------------"
print "-> Bug    : %5s" %BUGZILLA_ID
print "-> Usuario: %5s" %BUGZILLA_USERNAME
print "-------------------------"
print "# Coletando informacoes do bug"
print "## Iniciando browser"
br = bug.browser_start()
print "## Realizando login"
bug.do_login(br, BUGZILLA_USERNAME, BUGZILLA_PASSWORD)
print "## Acessando bug"
bug_fields = bug.get_bug_fields(br, BUGZILLA_ID)

print_bug_fields(bug_fields)

# Inicia o XML
dom = xml.start_dom()
tr_list = xml.get_tr_by_os(dom, bug_fields["os"])


if len(tr_list) == 0:
	print "Nenhum caminho a seguir quando os esta em |%s|" %bug_fields["os"]
	os._exit(0)

print
print "----------------------------------------"
print "Voce tem os seguintes caminhos a seguir:"
print "----------------------------------------"
i = 0

for tr in tr_list:
	print "%d - TR%-2s %s" %(i+1, tr, bug.get_desc_by_tr(tr))
	i += 1

print "----------------------------------------"

n = int(raw_input("O que voce deseja fazer? "))
n -= 1

tem_acao = 1

action_list = xml.get_action_by_tr(dom, tr_list[n])

print action_list
