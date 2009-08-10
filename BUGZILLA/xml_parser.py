#!/usr/bin/python
# -*- coding: latin-1 -*-

from xml.dom import minidom

FLUXO_XML = "fluxo.xml"

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def start_dom():
	dom = minidom.parse(FLUXO_XML)
	return dom

def get_tr_by_os(dom, os):

	tr_list = []

	tag =	dom.getElementsByTagName('lista_de_os')

	for OS in tag[0].childNodes:
		if OS.nodeType == dom.ELEMENT_NODE:
			#print OS.getAttributeNode('name').nodeValue
			#print os
			if OS.getAttributeNode('name').nodeValue.upper() == os.upper():
				for TR in OS.childNodes:
					if TR.nodeType == dom.ELEMENT_NODE:
						tr_list.append(TR.getAttributeNode('id').nodeValue)
	return tr_list

def get_action_by_tr(dom, tr):

	action_dict = {}
	
	tag =	dom.getElementsByTagName('transicoes')

	for TR in tag[0].childNodes:
		if TR.nodeType == dom.ELEMENT_NODE:
			if TR.getAttributeNode('id').nodeValue.upper() == tr.upper():
						for node in TR.childNodes:
							if node.nodeType == dom.ELEMENT_NODE:
								action_dict[node.nodeName] = getText(node.childNodes)

	return action_dict
