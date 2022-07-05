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
	start_date=filters.get('from')
	end_date=filters.get('to')
	employee_id=filters.get('employee')
	final_list=[]

	Heading_info=frappe.db.sql(""" SELECT `voucher_no` from `tabGL Entry`
					WHERE `voucher_type`="Payment Entry" and (`posting_date`>="%s" and `posting_date`<="%s")  
					ORDER BY `tabGL Entry`.`voucher_no`  ASC """%(start_date,end_date))

	Payment_Heading_info=frappe.db.sql(""" SELECT `name` from `tabPayment Refund` WHERE `posting_date`>="%s" and `posting_date`<="%s"  ORDER BY 
										`tabPayment Refund`.`name`  ASC """%(start_date,end_date))	
			
	if len(Heading_info)!=0:
		oppening_mr_no=Heading_info[0][0]
		clossing_mr_no=Heading_info[-1][0]
		a=["","Oppening MR No",oppening_mr_no,"Heading_info"]
		final_list.append(a)
		a=["","Clossing MR No",clossing_mr_no,"Heading_info"]
		final_list.append(a)
	if len(Payment_Heading_info):
		oppening_mr_no=Payment_Heading_info[0][0]
		clossing_mr_no=Payment_Heading_info[-1][0]
		a=["","Payment Refund Oppening MR No",oppening_mr_no,"Heading_info"]
		final_list.append(a)
		a=["","Payment Refund Clossing MR No",clossing_mr_no,"Heading_info"]
		final_list.append(a)

	Payment_Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Refund` WHERE `posting_date`>="%s" and `posting_date`<="%s" """%(start_date,end_date))	
	Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Entry` WHERE posting_date>="%s" and posting_date<="%s" """%(start_date,end_date))

	if len(Heading_info)!=0:
		Mr_Prepared=Heading_info[0][0]
		if len(Payment_Heading_info):
			Mr_Prepared=Mr_Prepared+Payment_Heading_info[0][0]
		a=["","No of MR Prepared",Mr_Prepared,"Heading_info"]
		final_list.append(a)						

	Payment_Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Refund` WHERE (`posting_date`>="%s" and `posting_date`<="%s") and `docstatus`=1 """%(start_date,end_date))	
	Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Entry`
									WHERE (posting_date>="%s" and posting_date<="%s") and `docstatus`=1 """%(start_date,end_date))

	if len(Heading_info)!=0:
		Mr_Submited=Heading_info[0][0]
		if len(Payment_Heading_info):
			Mr_Submited=Mr_Submited+Payment_Heading_info[0][0]
		a=["","No of MR Submited",Mr_Submited,"Heading_info"]
		final_list.append(a)		


	Payment_Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Refund` WHERE (`posting_date`>="%s" and `posting_date`<="%s") and `docstatus`=0 """%(start_date,end_date))
	Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Entry`
									WHERE (posting_date>="%s" and posting_date<="%s") and `docstatus`=0"""%(start_date,end_date))

	if len(Heading_info)!=0:
		Mr_Draft=Heading_info[0][0]
		if len(Payment_Heading_info):
			Mr_Draft=Mr_Draft+Payment_Heading_info[0][0]
		a=["","No of MR Skipped",Mr_Draft,"Heading_info"]
		final_list.append(a)


	Payment_Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Refund` WHERE (`posting_date`>="%s" and `posting_date`<="%s") and `docstatus`=2 """%(start_date,end_date))
	Heading_info=frappe.db.sql(""" SELECT count(name) from `tabPayment Entry`
									WHERE (posting_date>="%s" and posting_date<="%s") and `docstatus`=2"""%(start_date,end_date))

	if len(Heading_info)!=0:
		Mr_Canceled=Heading_info[0][0]
		if len(Payment_Heading_info):
			Mr_Canceled=Mr_Canceled+Payment_Heading_info[0][0]
		a=["","No of MR Canceled",Mr_Canceled,"Heading_info"]
		final_list.append(a)	

	
	filter=[]
	filter.append(["name","=",'employee_id'])	
	if employee_id == None:
		frappe.throw("Enter the Employee Id")
		# filter.append(["name","=",'employee_id'])
	employee=frappe.db.get_value('Employee',{"name":employee_id}, ['user_id'], as_dict=True)['user_id']
	Gl_entry=frappe.db.get_list('GL Entry', filters=[['posting_date', 'between', [start_date, end_date]],["owner","=",employee]])
	debit=[]
	credit=[]
	for t in Gl_entry:
		Gl_entry_info=frappe.get_all("GL Entry",{"name":t["name"],"voucher_type":"Payment Entry"},["name","account","debit","credit","voucher_no"])
		if len(Gl_entry_info):
			Gl_entry_info=Gl_entry_info[0]
			Payment_Entry_info=frappe.get_all("Payment Entry",filters=[["name","=",Gl_entry_info['voucher_no']],["payment_type","=","Receive"],["docstatus",'=',1]])  #########
			if len(Payment_Entry_info):
				if Gl_entry_info["debit"]!=0:
					com_data=[Gl_entry_info["debit"],Gl_entry_info["account"]]
					debit.append(com_data)
					del com_data
				elif Gl_entry_info["credit"]!=0:
					com_data=[Gl_entry_info["credit"],Gl_entry_info["account"]]
					credit.append(com_data)
	credit_refund=[]   #### pay entry
	debit_refund=[]    #### pay entry
	#######Payment Refund - Receive / Pay
	for i in Gl_entry:
		com_data=[]
		JV_entry_info=frappe.get_all("GL Entry",{"name":i["name"],"voucher_type":"Journal Entry"},["name","account","debit","credit","voucher_no"])
		if len(JV_entry_info):
			JV_entry_info=JV_entry_info[0]
			# {'name': 'ACC-GLE-2022-00158', 'account': 'Fees Refundable / Adjustable - KP', 'debit': 500.0, 'credit': 0.0, 'voucher_no': 'ACC-JV-2022-00002'}
			# {'name': 'ACC-GLE-2022-00157', 'account': 'Cash - KP', 'debit': 0.0, 'credit': 500.0, 'voucher_no': 'ACC-JV-2022-00002'}
			# {'name': 'ACC-GLE-2022-00156', 'account': 'Fees Refundable / Adjustable - KP', 'debit': 0.0, 'credit': 10000.0, 'voucher_no': 'ACC-JV-2022-00001'}
			# {'name': 'ACC-GLE-2022-00155', 'account': 'Cash - KP', 'debit': 10000.0, 'credit': 0.0, 'voucher_no': 'ACC-JV-2022-00001'}
			if ("Fees Refundable / Adjustable" in JV_entry_info['account'])==True:
				# {'name': 'ACC-GLE-2022-00158', 'account': 'Fees Refundable / Adjustable - KP', 'debit': 500.0, 'credit': 0.0, 'voucher_no': 'ACC-JV-2022-00002'}
				# {'name': 'ACC-GLE-2022-00156', 'account': 'Fees Refundable / Adjustable - KP', 'debit': 0.0, 'credit': 10000.0, 'voucher_no': 'ACC-JV-2022-00001'}
				if JV_entry_info['debit']!=0:
					com_data=[JV_entry_info["debit"],JV_entry_info["account"]]
					credit_refund.append(com_data) #### pay entry

				if 	JV_entry_info['credit']!=0:
					com_data=[JV_entry_info['credit'],JV_entry_info["account"]]
					credit.append(com_data)
			else:
				# {'name': 'ACC-GLE-2022-00157', 'account': 'Cash - KP', 'debit': 0.0, 'credit': 500.0, 'voucher_no': 'ACC-JV-2022-00002'}
				# {'name': 'ACC-GLE-2022-00155', 'account': 'Cash - KP', 'debit': 10000.0, 'credit': 0.0, 'voucher_no': 'ACC-JV-2022-00001'}
				if JV_entry_info["debit"]!=0:
					com_data=[JV_entry_info["debit"],JV_entry_info["account"]]
					debit.append(com_data)
				if JV_entry_info["credit"]!=0: 	
					com_data=[JV_entry_info["credit"],JV_entry_info["account"]]
					debit_refund.append(com_data) #### pay entry

		
	#################################### credit --- Receive
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
	######################################


	#################################### credit --- pay
	credit_head=[]
	for t in credit_refund:
		credit_head.append(t[1])
	
	credit_head = list(set(credit_head))
	credit_head_dic={}

	for t in credit_head:
		credit_head_dic['%s'%(t)]=[]

	for t in credit_refund:
		credit_head_dic["%s"%(t[1])].append(t[0])
	Sl_no=0
	total=0
	for x in credit_head_dic:
		Sl_no=Sl_no+1
		total=total+sum(credit_head_dic[x])
		a=[Sl_no,x,sum(credit_head_dic[x]),"credit-Pay"]
		final_list.append(a)	
	a=["","Grand Total",total,"credit-Pay"]	
	final_list.append(a)
	######################################



	#################################### debit -- Receive
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
	#########################	


	#################################### debit -- Pay
	debit_head=[]
	for t in debit_refund:
		debit_head.append(t[1])
	
	debit_head = list(set(debit_head))
	debit_head_dic={}

	for t in debit_head:
		debit_head_dic['%s'%(t)]=[]

	for t in debit_refund:
		debit_head_dic["%s"%(t[1])].append(t[0])
	Sl_no=0
	total=0
	for x in debit_head_dic:
		Sl_no=Sl_no+1
		total=total+sum(debit_head_dic[x])
		a=[Sl_no,x,sum(debit_head_dic[x]),"debit-pay"]
		final_list.append(a)
	a=["","Grand Total",total,"debit-pay"]	
	final_list.append(a)	
	#########################	


	
		
	return final_list


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
