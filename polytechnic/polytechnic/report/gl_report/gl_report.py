# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe

def execute(filters=None):
	# columns, data = [], []
	get_data_info=get_data(filters)
	get_columns_info=get_columns()
	return get_columns_info,get_data_info

def get_data(filters):
	print("\n\n\n\n\n")

	# _from, to = filters.get('from'), filters.get('to') # date range
	# account=filters.get("fee_head")
	# print(account)
	# data=frappe.get_all("GL Entry")
	# # conditions
	# conditions = " AND 1=1 "
	# if(filters.get('property')):conditions += f" AND name='{filters.get('property')}' "
	# if(filters.get('account')):conditions += f" AND account='{filters.get('account')}' "

	# print(f"\n\n\n\n\n{conditions}\n\n\n\n\n")
	
	# data = frappe.db.sql("""SELECT name, account from `tabGL Entry` WHERE (creation BETWEEN '{_from}' AND '{to}') {conditions};""")
	# data = frappe.db.sql("""SELECT name, account, party_type from `tabGL Entry`""")
	# print(data)
	# Gl_entry=frappe.get_all("GL Entry",{"posting_date":""})
	start_date=filters.get('from')
	end_date=filters.get('to')
	final_list=[]

	Heading_info=frappe.db.sql(""" SELECT `voucher_no` from `tabGL Entry`
					WHERE `voucher_type`="Payment Entry" and (`posting_date`>="%s" and `posting_date`<="%s")  
					ORDER BY `tabGL Entry`.`voucher_no`  ASC """%(start_date,end_date))
			
	if len(Heading_info)!=0:
		oppening_mr_no=Heading_info[0][0]
		clossing_mr_no=Heading_info[-1][0]
		a=["","Oppening MR No",oppening_mr_no,"Heading_info"]
		final_list.append(a)
		a=["","Clossing MR No",clossing_mr_no,"Heading_info"]
		final_list.append(a)


	Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Entry`
									WHERE posting_date>="%s" and posting_date<="%s" """%(start_date,end_date))

	if len(Heading_info)!=0:
		Mr_Prepared=Heading_info[0][0]
		a=["","No of MR Prepared",Mr_Prepared,"Heading_info"]
		final_list.append(a)								

	Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Entry`
									WHERE (posting_date>="%s" and posting_date<="%s") and `docstatus`=1"""%(start_date,end_date))

	if len(Heading_info)!=0:
		Mr_Submited=Heading_info[0][0]
		a=["","No of MR Submited",Mr_Submited,"Heading_info"]
		final_list.append(a)		

	Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Entry`
									WHERE (posting_date>="%s" and posting_date<="%s") and `docstatus`=0"""%(start_date,end_date))

	if len(Heading_info)!=0:
		Mr_Draft=Heading_info[0][0]
		a=["","No of MR Skipped",Mr_Draft,"Heading_info"]
		final_list.append(a)

	Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Entry`
									WHERE (posting_date>="%s" and posting_date<="%s") and `docstatus`=2"""%(start_date,end_date))

	if len(Heading_info)!=0:
		Mr_Canceled=Heading_info[0][0]
		a=["","No of MR Canceled",Mr_Canceled,"Heading_info"]
		final_list.append(a)	
	
	Gl_entry=frappe.db.get_list('GL Entry', filters=[['posting_date', 'between', [start_date, end_date]]])
	debit=[]
	credit=[]
	for t in Gl_entry:
		Gl_entry_info=frappe.get_all("GL Entry",{"name":t["name"],"voucher_type":"Payment Entry"},["name","account","debit","credit","voucher_no"])
		if len(Gl_entry_info):
			Gl_entry_info=Gl_entry_info[0]
			Payment_Entry_info=frappe.get_all("Payment Entry",{"name":Gl_entry_info['voucher_no'],"payment_type":"Receive"})
			if len(Payment_Entry_info):
				if Gl_entry_info["debit"]!=0:
					com_data=[Gl_entry_info["debit"],Gl_entry_info["account"]]
					debit.append(com_data)
					del com_data
				elif Gl_entry_info["credit"]!=0:
					com_data=[Gl_entry_info["credit"],Gl_entry_info["account"]]
					credit.append(com_data)
		
	#################################### credit
	credit_head=[]
	for t in credit:
		credit_head.append(t[1])
	
	credit_head = list(set(credit_head))
	credit_head_dic={}

	for t in credit_head:
		credit_head_dic['%s'%(t)]=[]

	for t in credit:
		credit_head_dic["%s"%(t[1])].append(t[0])
	Sl_no=0
	total=0
	for x in credit_head_dic:
		Sl_no=Sl_no+1
		total=total+sum(credit_head_dic[x])
		a=[Sl_no,x,sum(credit_head_dic[x]),"credit"]
		final_list.append(a)	
	a=["","Grand Total",total,"credit"]	
	final_list.append(a)
	#############################################################

	#################################### debit
	debit_head=[]
	for t in debit:
		debit_head.append(t[1])
	
	debit_head = list(set(debit_head))
	debit_head_dic={}

	for t in debit_head:
		debit_head_dic['%s'%(t)]=[]

	for t in debit:
		debit_head_dic["%s"%(t[1])].append(t[0])
	Sl_no=0
	total=0
	for x in debit_head_dic:
		Sl_no=Sl_no+1
		total=total+sum(debit_head_dic[x])
		a=[Sl_no,x,sum(debit_head_dic[x]),"debit"]
		final_list.append(a)
	a=["","Grand Total",total,"debit"]	
	final_list.append(a)			
	# return [
	# 	['ACC-GLE-2022-00024', 'Cash - SOUL',""],
	# 	['ACC-GLE-2022-00022', 'Cash - SOUL','ABCD'],
	# ]
	#############################################################
	return final_list

# def get_columns():
# 	return[
# 		"Sl. No.:Data:100",
# 		"Particulars:Link/Account:150",
# 		"Amount:Data:100",
# 		"Debit/Credit:Data:100",
# 	]

def get_columns():
	columns = [
		{
			"label": _("Sl. No."),
			"fieldname": "sl_no",
			"fieldtype": "Data",
			"width":100
		},
		{
			"label": _("Particulars"),
			"fieldname": "particulars",
			"fieldtype": "Link",
			"options": "Account",
			"width": 180
		},
		{
			"label": _("Amount"),
			"fieldname": "amount",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Debit / Credit"),
			"fieldname": "debit",
			"fieldtype": "Data",
			"width": 180
		},
	]
	return columns
