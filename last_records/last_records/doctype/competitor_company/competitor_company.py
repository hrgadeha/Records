# -*- coding: utf-8 -*-
# Copyright (c) 2021, Hardik Gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.naming import set_name_by_naming_series
from frappe import _, msgprint
import frappe.defaults
from frappe.utils import flt, cint, cstr, today, get_formatted_email
from frappe.desk.reportview import build_match_conditions, get_filters_cond
from erpnext.utilities.transaction_base import TransactionBase
from erpnext.accounts.party import validate_party_accounts, get_dashboard_info, get_timeline_data # keep this
from frappe.contacts.address_and_contact import load_address_and_contact, delete_contact_and_address
from frappe.model.rename_doc import update_linked_doctypes
from frappe.model.mapper import get_mapped_doc
from frappe.utils.user import get_users_with_role

class CompetitorCompany(TransactionBase):
	pass
