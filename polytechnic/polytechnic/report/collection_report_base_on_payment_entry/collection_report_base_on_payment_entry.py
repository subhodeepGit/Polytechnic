# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	get_data(filters)
	return columns, data

def get_data(filters):
	mode_of_payment=filters.get('mode_of_payment')
	start_date=filters.get('start_date')
	end_date=filters.get('end_date')
	print("\n\n\n\n\n\n")
	print(mode_of_payment,start_date,end_date)
	payment_entry=frappe.get_all("Payment Entry",filters=[["mode_of_payment","=",mode_of_payment],['posting_date', 'between',[start_date, end_date]],["docstatus","=",1]],
											fields=["name","mode_of_payment","party","party_name","roll_no","academic_year","permanent_registration_number"])
	
	print("\n\n\n\n\n\n")
	print(payment_entry)
	payment_entry_list=[]
	for t in payment_entry:
		payment_entry_list.append(t["name"])
	print(payment_entry_list)
	filters=[]
	payment_entry_reference=frappe.get_all("Payment Entry Reference")

def get_columns(head_name=None):
	columns = [
		{
			"label": _("Sl no"),
			"fieldname": "sl_no",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Student No"),
			"fieldname": "stu_no",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Roll no"),
			"fieldname": "roll_no",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("DET No"),
			"fieldname": "sams_portal_id",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Vidyarthi Portal ID"),
			"fieldname": "vidyarthi_portal_id",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Student Name"),
			"fieldname": "student_name",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Gender"),
			"fieldname": "gender",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Student Category"),
			"fieldname": "student_category",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Currency Info"),
			"fieldname": "currency_info",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("DUES AMOUNT"),
			"fieldname": "due_amount",
			"fieldtype": "Data",
			"width":200
		},

	]
	return columns	
