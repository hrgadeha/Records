# -*- coding: utf-8 -*-
# Copyright (c) 2019, Hardik Gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class LastPurchaseTable(Document):
	pass

@frappe.whitelist(allow_guest=True)
def getLastprice(item_code, supplier):
	balance_qty = "select pinv.name,pitem.item_code,pitem.qty,pitem.rate from `tabPurchase Invoice Item` pitem,`tabPurchase Invoice` pinv where pitem.parent = pinv.name and pitem.item_code = '"+str(item_code)+"' and pinv.supplier = '"+str(supplier)+"' and pinv.docstatus != 2 order by pinv.creation desc limit 5";
	li=[]
	dic=frappe.db.sql(balance_qty, as_dict=True)
	for i in dic:
		name,item_code,qty,rate=i['name'],i['item_code'],i['qty'],i['rate']
		li.append([name,item_code,qty,rate])
	return li

@frappe.whitelist(allow_guest=True)
def getLastSalesprice(item_code, customer):
	balance_qty = "select sinv.name,sitem.item_code,sitem.qty,sitem.rate from `tabSales Invoice Item` sitem,`tabSales Invoice` sinv where sitem.parent = sinv.name and sitem.item_code = '"+str(item_code)+"' and sinv.customer = '"+str(customer)+"' and sinv.docstatus != 2 order by sinv.creation desc limit 5";
	li=[]
	dic=frappe.db.sql(balance_qty, as_dict=True)
	for i in dic:
		name,item_code,qty,rate=i['name'],i['item_code'],i['qty'],i['rate']
		li.append([name,item_code,qty,rate])
	return li
