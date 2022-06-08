# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from itertools import count
from locale import currency
from frappe import _
import frappe

def execute(filters=None):
	# columns, data = [], []
	get_data_info=get_data(filters)
	get_columns_info=get_columns()
	return get_columns_info,get_data_info

def get_data(filters):
	print("\n\n\n\n\n")
	start_date= filters.get('from')
	end_date=filters.get('to') 
	party_type=filters.get("party_type")
	party=filters.get("party")
	Gl_entry_Pay_Rec=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],['party','=',party],['posting_date', 'between', 
								[start_date, end_date]]],fields=["name","account","debit","credit","voucher_no","voucher_type","account_currency","docstatus"])	

	list_for_fee=[]
	list_of_payment=[]
	for gl in Gl_entry_Pay_Rec:
		if gl['voucher_type']=="Fees":
			ck_out=frappe.db.get_list("Fees",filters=[["name","=",gl['voucher_no']]],fields=["name","docstatus"])
			if ck_out[0]["docstatus"]==1:
				list_for_fee.append(gl)
		if gl['voucher_type']=='Payment Entry':
			ck_out=frappe.db.get_list("Payment Entry",filters=[["name","=",gl['voucher_no']]],fields=["name","docstatus"])
			if ck_out[0]["docstatus"]==1:
				list_of_payment.append(gl)	
	
	Gl_entry_Pay_Rec=list_for_fee   ############### Fees 
	Gl_entry_payment=list_of_payment #################### payment 
	# "docstatus":("!=",2)

	fees_head=[]
	Payment_head=[]
	currency_info=""
	for t in Gl_entry_Pay_Rec:
		if t["voucher_type"]=="Fees":
			fees_head.append(t["account"])
			currency_info=t["account_currency"]



	for t in Gl_entry_payment:
		if t["voucher_type"]=="Payment Entry":
			Payment_head.append(t["account"])
			currency_info=t["account_currency"]	

	fees_head = list(set(fees_head))
	Payment_head = list(set(Payment_head))
	########################### Fees
	fees_head_dic={}
	for t in fees_head:
		fees_head_dic['%s'%(t)]=[]

	
	for t in Gl_entry_Pay_Rec:
		if t["voucher_type"]=="Fees":
			fees_head_dic["%s"%(t["account"])].append(t["debit"])	
	############################# End Fees
	############################ payment 
	Payment_head_dic={}
	for t in Payment_head:
		Payment_head_dic['%s'%(t)]=[]

	for t in Gl_entry_payment:
		if t["voucher_type"]=="Payment Entry":
			if ('Fees Refundable / Adjustable' in t["account"])==False:
				Payment_head_dic["%s"%(t["account"])].append(t["credit"])
			else:
				Payment_head_dic["%s"%(t["account"])].append(t["credit"])
				ref_dic=fees_head_dic.keys()
				flag=0
				for t1 in ref_dic:
					if "Fees Refundable / Adjustable" in t1:
						flag=1
				if flag==0:		
					fees_head_dic['%s'%(t["account"])]=[]
					fees_head_dic["%s"%(t["account"])].append(t["credit"])
				else:
					fees_head_dic["%s"%(t["account"])].append(t["credit"])			
	# if len(Payment_head_dic)==0:
	# 	for t in fees_head:
	# 		Payment_head_dic['%s'%(t)]=[0]


	fees_head_dic = dict(zip(fees_head_dic.keys(), [sum(item) for item in fees_head_dic.values()]))
	
	Payment_head_dic = dict(zip(Payment_head_dic.keys(), [sum(item) for item in Payment_head_dic.values()]))
	

	Outsatnding_dict={}
	for t in fees_head_dic:
		for j in Payment_head_dic:
			if t==j:
				Outsatnding_dict['%s'%(t)]=fees_head_dic[t]-Payment_head_dic[j]
				break
			else:
				Outsatnding_dict['%s'%(t)]=fees_head_dic[t]	

	if len(Outsatnding_dict)==0:
		Outsatnding_dict=fees_head_dic.copy()


	Fee_DOC=[]
	for t in Gl_entry_Pay_Rec:
		if t["voucher_type"]=="Fees":
			total_waiver_amount=frappe.db.get_all('Fee Component',{"parent":t['voucher_no']},["fees_category","total_waiver_amount","grand_fee_amount","receivable_account"])
			Fee_DOC.append(total_waiver_amount)
			# fees_head_dic["%s"%(t["account"])].append(t["debit"])		
	
	head_fee=[]
	for Fee_components in Fee_DOC:
		for i in range(len(Fee_components)):
			head_fee.append(Fee_components[i]["receivable_account"])
		head_fee=list(set(head_fee))    

	Fee_cal={}    
	for t in range(len(head_fee)):
		Fee_cal['%s'%(head_fee[t])]=[]

	Waver_amount={}
	for t in range(len(head_fee)):
		Waver_amount['%s'%(head_fee[t])]=[]

	for Fee_components in Fee_DOC:
		for i in range(len(Fee_components)):
			Fee_cal['%s'%(Fee_components[i]["receivable_account"])].append(Fee_components[i]['grand_fee_amount'])
			Waver_amount['%s'%(Fee_components[i]["receivable_account"])].append(Fee_components[i]['total_waiver_amount'])

	Fee_cal = dict(zip(Fee_cal.keys(), [sum(item) for item in Fee_cal.values()]))
	Waver_amount = dict(zip(Waver_amount.keys(), [sum(item) for item in Waver_amount.values()]))		
			
	Refund_fees_head_dic={}
	for t in fees_head:
		Refund_fees_head_dic['%s'%(t)]=[]

	
	for t in Gl_entry_Pay_Rec:
		if t["voucher_type"]=="Fees":
			Refund_fees_head_dic["%s"%(t["account"])].append(t["credit"])	

	Refund_Payment_head_dic={}
	for t in Payment_head:
		Refund_Payment_head_dic['%s'%(t)]=[]
	

	for t in Gl_entry_Pay_Rec:
		if t["voucher_type"]=="Payment Entry":
			Refund_Payment_head_dic["%s"%(t["account"])].append(t["debit"])
	
	if len(Refund_Payment_head_dic)==0:
		for t in fees_head:
			Refund_Payment_head_dic['%s'%(t)]=[0]


	Refund_fees_head_dic= dict(zip(Refund_fees_head_dic.keys(), [sum(item) for item in Refund_fees_head_dic.values()]))
	Refund_Payment_head_dic = dict(zip(Refund_Payment_head_dic.keys(), [sum(item) for item in Refund_Payment_head_dic.values()]))


	Final_list=["Sl_no","Fees Head","Currency","Dues","paid","Balance","Paid amount","Body","Waver_amount","Grand_total","Refund_fees_head_dic","Refund_Payment_head_dic"]	
	Final_list=[]

	student=party
	student_data_info=frappe.db.get_list("Current Educational Details",filters={"parent":student},fields=["name","Semesters","Programs","academic_year"])
	# student_info=frappe.db.get_list("Student",filters={"name":student},fields=["sams_portal_id","kiit_polytechnic_roll_no","vidyarthi_portal_id","title"])	
	student_info=frappe.db.get_list("Student",filters={"name":student},fields=["sams_portal_id","roll_no","vidyarthi_portal_id","title"])
	student_group=frappe.db.get_list("Student Group",filters={"programs":student_data_info[0]["Programs"]},fields=["name","batch","programs"])
	if len(student_group)==0:
		frappe.throw("Student Group Not Found")
	student_Enrollment=frappe.db.sql(""" select DISTINCT `program_grade` from `tabProgram Enrollment` where `student`='%s'"""%(student))

	g_value=[]
	g_value.append(student_info[0]["title"])
	g_value.append(student_data_info[0]["Semesters"])
	g_value.append(student_data_info[0]["Programs"])
	# g_value.append(student_info[0]["kiit_polytechnic_roll_no"])
	g_value.append(student_info[0]["roll_no"])
	g_value.append(student_info[0]["vidyarthi_portal_id"])
	g_value.append(student_info[0]["sams_portal_id"])
	g_value.append(student_group[0]["batch"])
	g_value.append("Header")
	g_value.append(student_Enrollment[0][0])
	g_value.append(student_data_info[0]["academic_year"])
	g_value.append("")
	g_value.append("")
	Final_list.append(g_value)	
	# [1, 'Debtors - SOUL', 'INR', 80000.0, 80000.0, '', 'Body', 0.0, 160000.0, 0.0]
		


	Count=0
	for t in fees_head_dic:
		g_value=[]
		Count=Count+1
		g_value.append(Count)
		g_value.append(t)
		g_value.append(currency_info)
		if ('Fees Refundable / Adjustable' in t)==False:
			g_value.append(fees_head_dic[t])
		else:
			g_value.append(0)	
		flag=""
		for j in Payment_head_dic:
			if t==j:
				flag="Done"
				g_value.append(Payment_head_dic[j])		
		if flag!="Done":
			g_value.append(0)
			flag=""	
		else:
			flag=""		


		for i in Outsatnding_dict:
			if t==i:
				flag="Done"
				if ('Fees Refundable / Adjustable' in t)==False:
					payment_value=0
					try:
						print(Payment_head_dic[i])
						payment_value=Payment_head_dic[i]
					except:
						pass
					Outsatnding_dict['%s'%(t)]=fees_head_dic[t]-Waver_amount[t]-payment_value
					g_value.append(Outsatnding_dict[i])	
				else:
					g_value.append(0)	
		if flag!="Done":
			g_value.append(0)
			flag=""	
		else:
			flag=""		


		g_value.append("")			
		g_value.append("Body")



		for j in Waver_amount:
			if j==t:
				flag="Done"
				if ('Fees Refundable / Adjustable' in t)==False:
					g_value.append(Waver_amount[t])
		if flag!="Done":
			g_value.append(0)
			flag=""	
		else:
			flag=""		



		for j in Fee_cal:
			if j==t:
				flag="Done"
				g_value.append(Fee_cal[t])	
		if flag!="Done":
			g_value.append(0)
			flag=""	
		else:
			flag=""	



		for j in Refund_fees_head_dic:
			if j==t:
				flag="Done"
				g_value.append(Refund_fees_head_dic[j])	
		if flag!="Done":
			g_value.append(0)
			flag=""
		else:
			flag=""			


		for j in Refund_Payment_head_dic:
			if j==t:
				flag="Done"
				g_value.append(Refund_Payment_head_dic[j])
		if flag!="Done":
			g_value.append(0)
			flag=""
		else:
			flag=""			
									
		Final_list.append(g_value)

	Gl_entry_Type_payment=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],['against','=',party],['voucher_type',"=",'Payment Entry'],['posting_date', 'between', 
								[start_date, end_date]]],fields=["name","account","debit","credit","voucher_no","voucher_type","account_currency","posting_date"])	
	list_for_payment=[]					
	for payment in Gl_entry_Type_payment:
		if payment['voucher_type']=="Payment Entry":
			ck_out=frappe.db.get_list("Payment Entry",filters=[["name","=",payment['voucher_no']]],fields=["name","docstatus"])
			if ck_out[0]["docstatus"]==1:
				list_for_payment.append(payment)
	Gl_entry_Type_payment=list_for_payment					
	Count=0
	for t in Gl_entry_Type_payment:
		Count =Count+1
		g_value=[]
		payment_entry= frappe.db.get_value('Payment Entry', t["voucher_no"], ['name', 'mode_of_payment',"reference_date","reference_no","paid_amount"], as_dict=1)
		g_value.append(Count)
		g_value.append(t["posting_date"])
		g_value.append(currency_info)
		g_value.append(payment_entry.mode_of_payment)
		g_value.append(payment_entry.reference_date)
		g_value.append(payment_entry.reference_no)
		g_value.append(payment_entry.paid_amount)
		g_value.append("Lower")
		g_value.append(payment_entry.name)
		g_value.append("")
		g_value.append("")
		g_value.append("")
		Final_list.append(g_value)
	



	return Final_list

def get_columns():
	columns = [
		{
			"label": _("Sl_no"),
			"fieldname": "sl_no",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Fees Head"),
			"fieldname": "fees_head",
			"fieldtype": "Data",
			"width":200
		},
		{
			"label": _("Currency"),
			"fieldname": "currency",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Dues"),
			"fieldname": "dues",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Paid"),
			"fieldname": "paid",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Balance"),
			"fieldname": "balance",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Lower Table Amount"),
			"fieldname": "ltamt",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Table Posi"),
			"fieldname": "table_posi",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Waiver Amount"),
			"fieldname": "waiver_amt",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Grand Total"),
			"fieldname": "grand_total",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Refund Fees"),
			"fieldname": "Refund_fees_head_dic",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Refund Payment"),
			"fieldname": "Refund_Payment_head_dic",
			"fieldtype": "Data",
			"width": 180
		},
		
	]
	return columns


	