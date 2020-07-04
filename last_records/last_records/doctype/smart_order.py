from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document
from datetime import date
from frappe.utils import money_in_words

def makeMR(doc,method):
	items = []
	for d in doc.items:
		if d.qty > d.actual_qty and d.qty < d.total_qty:
			mr = frappe.get_doc({
			"doctype": "Material Request",
			"material_request_type": "Material Transfer",
			"schedule_date": date.today(),
			"against_sales_order": doc.name,
			"items": [{
				"item_code": d.item_code,
				"qty": d.qty-d.actual_qty,
				"so_qty": d.qty,
				"warehouse": d.warehouse,
				"sales_order": doc.name,
				"schedule_date": date.today()
				}]
			})
			mr.insert(ignore_permissions=True)
			msgprint("Material Request Generated to Transfer Material From Other Warehouse to Required Warehouse")
			mr.save()

		if d.qty > d.actual_qty and d.qty > d.total_qty:
			n_mr = frappe.get_doc({
			"doctype": "Material Request",
			"material_request_type": "Purchase",
			"schedule_date": date.today(),
			"against_sales_order": doc.name,
			"items": [{
				"item_code": d.item_code,
				"qty": d.qty-d.total_qty,
				"so_qty": d.qty,
				"warehouse": d.warehouse,
				"sales_order": doc.name,
				"schedule_date": date.today()
				}]
			})
			n_mr.insert(ignore_permissions=True)
			msgprint("Material Request Generated to Purchase Required Qty")
			n_mr.save()


@frappe.whitelist(allow_guest=True)
def getStock(item_code):
	mt = frappe.db.sql("""select sum(actual_qty) from `tabBin` where item_code = %s;""",(item_code))
	return mt
