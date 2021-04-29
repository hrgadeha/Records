from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document
from datetime import date
from datetime import datetime, timedelta
from frappe.utils import money_in_words

@frappe.whitelist(allow_guest=True)
def getStock1(item_code,warehouse):
	stock = frappe.db.sql("""select actual_qty AS 'qty' from `tabBin` where item_code = %s and 
				warehouse = %s""",(item_code,warehouse),as_dict = True)
	return stock[0].qty


def makeSE(doc,method):
	for i in doc.items:
		stock = frappe.db.sql("""select actual_qty as 'qty' from `tabBin` where item_code = %s and 
				warehouse = %s""",(i.item_code,doc.stock_warehouse),as_dict = True)

		items_1 = []
		if stock and (stock[0].qty >= i.qty) and stock[0].qty != 0:
			item_li = {"item_code": i.item_code,"qty": i.qty,"uom":i.stock_uom,"s_warehouse":doc.stock_warehouse,"t_warehouse":doc.set_warehouse,"basic_rate":i.rate}
			items_1.append(item_li)

			mt = frappe.get_doc({
			"doctype": "Stock Entry",
			"company": doc.company,
			"stock_entry_type": "Material Transfer",
			"posting_date": doc.transaction_date,
#			"posting_time": datetime.now(),
			"from_warehouse": doc.stock_warehouse,
			"to_warehouse": doc.set_warehouse,
			"sales_order" : doc.name,
			"items": items_1
			})
			mt.insert(ignore_permissions=True)
			mt.save(ignore_permissions=True)
			mt.submit()


		items_2 = []
		if stock and (stock[0].qty < i.qty) and stock[0].qty != 0:
			item_li = {"item_code": i.item_code,"qty": stock[0].qty,"uom":i.stock_uom,"s_warehouse":doc.stock_warehouse,"t_warehouse":doc.set_warehouse,"basic_rate":i.rate}
			items_2.append(item_li)

			mt = frappe.get_doc({
			"doctype": "Stock Entry",
			"company": doc.company,
			"stock_entry_type": "Material Transfer",
			"posting_date": doc.transaction_date,
#			"posting_time": datetime.now(),
			"from_warehouse": doc.stock_warehouse,
			"to_warehouse": doc.set_warehouse,
			"sales_order" : doc.name,
			"items": items_2
			})
			mt.insert(ignore_permissions=True)
			mt.save(ignore_permissions=True)
			mt.submit()


			n_mr = frappe.get_doc({
			"doctype": "Material Request",
			"material_request_type": "Purchase",
			"schedule_date": doc.transaction_date,
			"against_sales_order": doc.name,
			"items": [{
				"item_code": i.item_code_with_bq,
				"qty": (i.qty - stock[0].qty) / i.po_box_qty,
				"so_qty": i.qty,
				"warehouse": doc.stock_warehouse,
				"sales_order": doc.name,
				"uom": i.stock_uom,
				"schedule_date": doc.transaction_date
			}]
			})
			n_mr.insert(ignore_permissions=True)
			n_mr.save(ignore_permissions=True)
			msgprint("Material Request Generated to Purchase Required Qty")



		if not stock:
			n_mr = frappe.get_doc({
			"doctype": "Material Request",
			"material_request_type": "Purchase",
			"schedule_date": doc.transaction_date,
			"against_sales_order": doc.name,
			"items": [{
				"item_code": i.item_code_with_bq,
				"qty": i.qty / i.po_box_qty,
				"so_qty": i.qty,
				"warehouse": doc.stock_warehouse,
				"sales_order": doc.name,
				"uom": i.stock_uom,
				"schedule_date": doc.transaction_date
			}]
			})
			n_mr.insert(ignore_permissions=True)
			n_mr.save(ignore_permissions=True)
			msgprint("Material Request Generated to Purchase Required Qty")

@frappe.whitelist(allow_guest=True)
def canMR(doc,method):
	mi = frappe.get_list('Material Request', filters={'against_sales_order': doc.name,'per_ordered': 0}, fields=['name'])
	if mi:
		for i in mi:
			mr = frappe.get_doc("Material Request",i)
			if mr.docstatus == 1:
				mr.cancel()
				mr.delete()
			if mr.docstatus == 0:
				mr.delete()

	so = frappe.get_list('Stock Entry', filters={'sales_order': doc.name}, fields=['name'])
	if so:
		for d in so:
			se = frappe.get_doc("Stock Entry",d)
			if se.docstatus == 1:
				se.cancel()
				se.delete()
			if se.docstatus == 0:
				se.delete()
