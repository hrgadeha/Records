# -*- coding: utf-8 -*-
# Copyright (c) 2021, Hardik Gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class OnlineRegistrationForm(Document):
	def on_submit(self):
		if self.party_type == "Supplier" and not frappe.db.exists("Supplier",self.full_name):
			supplier = frappe.get_doc({
			"doctype": "Supplier",
			"supplier_name": self.full_name,
			"supplier_group": self.supplier_group,
			"supplier_type": self.type,
			"gst_category": self.gst_category
			})
			supplier.insert(ignore_permissions=True,ignore_mandatory = True)
			supplier.save(ignore_permissions=True)


			address = frappe.get_doc({
			"doctype": "Address",
			"address_title": self.full_name,
			"address_type": "Billing",
			"address_line1": self.address_line_1,
			"address_line2": self.address_line_2,
			"city": self.city,
			"state": self.state,
			"pincode": self.pincode,
			"email_id": self.email_id,
			"phone": self.mobile_no_1,
			"gstin": self.gstin,
			"pan_no": self.pan_no,
			"is_primary_address": 1,
			"links": [{
				"link_doctype": "Supplier",
				"link_name": self.full_name
			}]
			})
			address.insert(ignore_permissions=True,ignore_mandatory = True)
			address.save(ignore_permissions=True)

			contact = frappe.get_doc({
			"doctype": "Contact",
			"first_name": self.contact_person,
			"email_id": self.email_id,
			"phone": self.mobile_no_2,
			"mobile_no": self.mobile_no_1,
			"is_primary_contact": 1,
			"phone_nos": [{
				"phone": self.mobile_no_1,
				"is_primary_mobile_no": 1
			}],
			"email_ids": [{
				"email_id": self.email_id,
				"is_primary": 1
			}],
			"links": [{
				"link_doctype": "Supplier",
				"link_name": self.full_name
			}]
			})
			contact.insert(ignore_permissions=True,ignore_mandatory = True)
			contact.save(ignore_permissions=True)


		if self.party_type == "Customer" and not frappe.db.exists("Customer",self.full_name):
			supplier = frappe.get_doc({
			"doctype": "Customer",
			"customer_name": self.full_name,
			"customer_group": self.customer_group,
			"customer_type": self.type,
			"gst_category": self.gst_category
			})
			supplier.insert(ignore_permissions=True,ignore_mandatory = True)
			supplier.save(ignore_permissions=True)


			address = frappe.get_doc({
			"doctype": "Address",
			"address_title": self.full_name,
			"address_type": "Billing",
			"address_line1": self.address_line_1,
			"address_line2": self.address_line_2,
			"city": self.city,
			"state": self.state,
			"pincode": self.pincode,
			"email_id": self.email_id,
			"phone": self.mobile_no_1,
			"gstin": self.gstin,
			"pan_no": self.pan_no,
			"is_primary_address": 1,
			"links": [{
				"link_doctype": "Customer",
				"link_name": self.full_name
			}]
			})
			address.insert(ignore_permissions=True,ignore_mandatory = True)
			address.save(ignore_permissions=True)

			contact = frappe.get_doc({
			"doctype": "Contact",
			"first_name": self.contact_person,
			"email_id": self.email_id,
			"phone": self.mobile_no_2,
			"mobile_no": self.mobile_no_1,
			"is_primary_contact": 1,
			"phone_nos": [{
				"phone": self.mobile_no_1,
				"is_primary_mobile_no": 1
			}],
			"email_ids": [{
				"email_id": self.email_id,
				"is_primary": 1
			}],
			"links": [{
				"link_doctype": "Customer",
				"link_name": self.full_name
			}]
			})
			contact.insert(ignore_permissions=True,ignore_mandatory = True)
			contact.save(ignore_permissions=True)
