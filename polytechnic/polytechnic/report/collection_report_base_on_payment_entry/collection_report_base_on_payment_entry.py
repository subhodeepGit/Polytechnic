# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

from dataclasses import field
import frappe
from frappe import _

def execute(filters=None):
	payment_entry,head_list=get_data(filters)
	get_columns_info=get_columns(head_list)
	return  get_columns_info,payment_entry

def get_data(filters):
	mode_of_payment=filters.get('mode_of_payment')
	start_date=filters.get('start_date')
	end_date=filters.get('end_date')
	payment_entry=frappe.get_all("Payment Entry",filters=[["mode_of_payment","in",tuple(mode_of_payment)],['posting_date', 'between',[start_date, end_date]],["docstatus","=",1]],
											fields=["name","mode_of_payment","party","party_name","roll_no","academic_year","permanent_registration_number",
														"sams_portal_id","vidyarthi_portal_id","total_allocated_amount","posting_date"])
	if payment_entry:
		payment_entry_list=[]
		for t in payment_entry:
			payment_entry_list.append(t["name"])
		filters=[]
		if len(payment_entry_list)==1:
			payment_entry_reference=frappe.get_all("Payment Entry Reference",filters=[["parent","=",payment_entry_list[0]]],
													fields=["name","parent","fees_category","account_paid_from","allocated_amount"])
		else:
			payment_entry_reference=frappe.get_all("Payment Entry Reference",filters=[["parent","in",tuple(payment_entry_list)]],
												fields=["name","parent","fees_category","account_paid_from","allocated_amount"])
		
		head_list=[]
		for t in payment_entry_reference:
			head_list.append(t["account_paid_from"])
		head_list=list(set(head_list))

		count=0
		for t in payment_entry:
			count=count+1
			t["sl_no"]=count
			for z in head_list:
				t[z]=[]

		for t in payment_entry:
			for j in payment_entry_reference:
				if t["name"]==j["parent"]:
					for z in head_list:
						if j["account_paid_from"]==z:
							t[z].append(j["allocated_amount"])

		for t in payment_entry:
			for z in head_list:
				t[z]=sum(t[z])
		print('\n\n\n\n\n',payment_entry)
		return payment_entry,head_list
	else:
		frappe.throw("No Record Found")	


def get_columns(head_name=None):
	columns = [
		{
			"label": _("Student No"),
			"fieldname": "party",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Roll No"),
			"fieldname": "roll_no",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("SAMS Portal ID"),
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
			"fieldname": "party_name",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width":200
		},
		{
			"label": _("Money Receipt Number"),
			"fieldname": "name",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Programs"),
			"fieldname": "program",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Semester"),
			"fieldname": "semester",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Batch"),
			"fieldname": "batch",
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
			"label": _("Paid Amount"),
			"fieldname": "total_allocated_amount",
			"fieldtype": "Data",
			"width":200
		}
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
	prepared_by={
		"label": _("Prepared By"),
		"fieldname": "prepared_by",
		"fieldtype": "Data",
		"width":200
	}
	columns.append(prepared_by)
	return columns	
