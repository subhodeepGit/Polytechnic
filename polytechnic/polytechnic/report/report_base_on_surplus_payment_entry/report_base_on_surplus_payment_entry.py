# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filters=None):
	# columns, data = [], []
	surplus_payment_entry,head_list=get_data(filters)
	columns=get_columns(head_list)
	return columns, surplus_payment_entry

def get_data(filters):
	payment_type=filters.get('payment_type')
	mode_of_payment=filters.get('mode_of_payment')
	start_date=filters.get('start_date')
	end_date=filters.get('end_date')

	surplus_payment_entry=frappe.get_all("Payment Refund",filters=[["payment_type","=",payment_type],["mode_of_payment","=",mode_of_payment],
														['posting_date', 'between',[start_date, end_date]],["docstatus","=",1]],
														fields=["name","mode_of_payment","payment_type","party","party_name","roll_no","permanent_registration_number",
																"sams_portal_id","vidyarthi_portal_id","jv_entry_voucher_no"])
	if surplus_payment_entry:
		surplus_payment_list=[]
		for t in surplus_payment_entry:
			surplus_payment_list.append(t["name"])
		if len(surplus_payment_list)==1:
			surplus_payment_amount=frappe.get_all("Payment Entry Reference Refund",{"parent":surplus_payment_list[0]},
					 ["parent","name","allocated_amount","account_paid_to","fees_category"])
		else:
			surplus_payment_amount=frappe.get_all("Payment Entry Reference Refund",filters=[["parent","in",surplus_payment_list]],
												fields=["parent","name","allocated_amount","account_paid_to","fees_category"])	

		head_list=[]
		for t in surplus_payment_amount:
			head_list.append(t["fees_category"])
		head_list=list(set(head_list))
		

		for t in surplus_payment_entry:
			for j in head_list:
				t[j]=0
			t["total_amount"]=0	

		for t in surplus_payment_entry:
			for j in surplus_payment_amount:
				if t["name"]==j["parent"]:
					t[j["fees_category"]]=j["allocated_amount"]
					t["total_amount"]=j["allocated_amount"]			
		return surplus_payment_entry,head_list
	else:
		frappe.throw("No recored found")	


def get_columns(head_name=None):
	columns = [
		{
			"label": _("Student No"),
			"fieldname": "party",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Student Name"),
			"fieldname": "party_name",
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
			"label": _("Payment Type"),
			"fieldname": "payment_type",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Payment Entry no"),
			"fieldname": "name",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Journal Entry"),
			"fieldname": "jv_entry_voucher_no",
			"fieldtype": "Data",
			"width":200
		},

	]
	if len(head_name)!=0:
		for t in head_name:
			label=t
			columns_add={
				"label": _("%s"%(label)),
				"fieldname": "%s"%(label),
				"fieldtype": "Data",
				"width":200
			}
			columns.append(columns_add)
	return columns	
