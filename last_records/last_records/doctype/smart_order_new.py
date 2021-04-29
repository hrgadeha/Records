from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document
from datetime import date
from datetime import datetime, timedelta
from frappe.utils import money_in_words

@frappe.whitelist(allow_guest=True)
def getStock1(item_code,warehouse):
	stock = frappe.db.sql("""select actual_qty from `tabBin` where item_code = %s and 
				warehouse = %s""",(item_code,warehouse))
	return stock[0][0]


def makeSE(doc,method):
	for i in doc.items:
		stock = frappe.db.sql("""select actual_qty from `tabBin` where item_code = %s and 
				warehouse = %s""",(i.item_code,doc.stock_warehouse))

		if stock and stock[0][0] != 0:
			if stock[0][0] >= i.qty:
				mt = frappe.get_doc({
				"doctype": "Stock Entry",
				"company": doc.company,
				"stock_entry_type": "Reservation of Stock",
				"posting_date": doc.transaction_date,
#				"posting_time": datetime.now(),
				"from_warehouse": doc.stock_warehouse,
				"to_warehouse": doc.set_warehouse,
				"sales_order" : doc.name,
				"items": [{
					"item_code": i.item_code,
					"qty": i.qty,
					"uom":i.uom,
					"s_warehouse":doc.stock_warehouse,
					"t_warehouse":doc.set_warehouse,
					"basic_rate":i.rate
				}]
				})
				mt.insert(ignore_permissions=True)
				mt.save(ignore_permissions=True)
				frappe.msgprint(frappe._("Qty {0} Of Item {1} Transfered to {2} From {3}.").format(i.qty,i.item_code,doc.set_warehouse,doc.stock_warehouse))


			if stock[0][0] < i.qty:
				mt = frappe.get_doc({
				"doctype": "Stock Entry",
				"company": doc.company,
				"stock_entry_type": "Reservation of Stock",
				"posting_date": doc.transaction_date,
#				"posting_time": datetime.now(),
				"from_warehouse": doc.stock_warehouse,
				"to_warehouse": doc.set_warehouse,
				"sales_order" : doc.name,
				"items": [{
					"item_code": i.item_code,
					"qty": stock[0][0],
					"uom":i.uom,
					"s_warehouse":doc.stock_warehouse,
					"t_warehouse":doc.set_warehouse,
					"basic_rate":i.rate
				}]
				})
				mt.insert(ignore_permissions=True)
				mt.save(ignore_permissions=True)
				frappe.msgprint(frappe._("Qty {0} Of Item {1} Transfered to {2} From {3}.").format(stock[0][0],i.item_code,doc.set_warehouse,doc.stock_warehouse))

				n_mr = frappe.get_doc({
				"doctype": "Material Request",
				"material_request_type": "Purchase",
				"schedule_date": doc.transaction_date,
				"transaction_date": doc.transaction_date,
				"against_sales_order": doc.name,
				"items": [{
					"item_code": i.item_code_with_bq,
					"qty":(i.qty - stock[0][0]) / i.po_box_qty,
					"uom":i.uom,
					"so_qty": i.qty,
					"warehouse":doc.set_warehouse,
					"sales_order":doc.name,
					"schedule_date": doc.transaction_date
				}]
				})
				n_mr.insert(ignore_permissions=True)
				n_mr.save(ignore_permissions=True)
				frappe.msgprint(frappe._("Material Request Generated For Item {0} with Qty {1}.").format(i.item_code_with_bq,((i.qty - stock[0][0]) / i.po_box_qty)))


		if not stock or stock[0][0] == 0:
			n_mr = frappe.get_doc({
			"doctype": "Material Request",
			"material_request_type": "Purchase",
			"schedule_date": doc.transaction_date,
			"transaction_date": doc.transaction_date,
			"against_sales_order": doc.name,
			"items": [{
				"item_code": i.item_code_with_bq,
				"qty":(i.qty / i.po_box_qty),
				"uom":i.uom,
				"so_qty": i.qty,
				"warehouse":doc.set_warehouse,
				"sales_order":doc.name,
				"schedule_date": doc.transaction_date
			}]
			})
			n_mr.insert(ignore_permissions=True)
			n_mr.save(ignore_permissions=True)
			frappe.msgprint(frappe._("Material Request Generated For Item {0} with Qty {1}.").format(i.item_code_with_bq,(i.qty / i.po_box_qty)))

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
			se.cancel()
			se.delete()
