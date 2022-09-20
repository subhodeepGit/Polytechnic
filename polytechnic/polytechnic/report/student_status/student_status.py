# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from dataclasses import fields
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
	start_date= filters.get('from')
	end_date=filters.get('to') 
	# party_type=filters.get("party_type")
	party=filters.get("party")
	Gl_entry_Pay_Rec=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],["is_cancelled",'=',0],['party','=',party],['posting_date', 'between', 
								[start_date, end_date]]],fields=["name","account","debit","credit","voucher_no","voucher_type","account_currency","docstatus"])														
	list_for_fee=[]
	list_of_payment=[]
	je_entry_debit=[]
	je_enrty_credit=[]
	for gl in Gl_entry_Pay_Rec:
		if gl['voucher_type']=="Fees":
			ck_out=frappe.db.get_list("Fees",filters=[["name","=",gl['voucher_no']]],fields=["name","docstatus"])
			if ck_out[0]["docstatus"]==1:
				list_for_fee.append(gl)
		if gl['voucher_type']=='Payment Entry':
			ck_out=frappe.db.get_list("Payment Entry",filters=[["name","=",gl['voucher_no']]],fields=["name","docstatus"])
			if ck_out[0]["docstatus"]==1:
				list_of_payment.append(gl)
		if gl['voucher_type']=='Journal Entry':
			ck_out=frappe.db.get_list("Payment Refund",filters=[["jv_entry_voucher_no","=",gl['voucher_no']]],fields=["name","docstatus"])
			try:
				if ck_out[0]["docstatus"]==1:
					if gl['debit']!=0:
						je_entry_debit.append(gl)
					if gl['credit']!=0:
						je_enrty_credit.append(gl)	
			except:
				pass
			# if ck_out[0]["docstatus"]==1:
			# 	if gl['debit']!=0:
			# 		je_entry_debit.append(gl)
			# 	if gl['credit']!=0:
			# 		je_enrty_credit.append(gl)						

	Gl_entry_Pay_Rec=list_for_fee   ############### Fees 
	Gl_entry_payment=list_of_payment #################### payment 

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
	for t in je_enrty_credit:
		if ('Fees Refundable / Adjustable' in t["account"])==True:
			ref_dic=fees_head_dic.keys()
			ref_dic1=Payment_head_dic.keys()
			flag=0
			flag1=0
			for t1 in ref_dic:
				if "Fees Refundable / Adjustable" in t1:
					flag=1

			ref_dic=Payment_head_dic.keys()		
			for t2 in ref_dic:
				if "Fees Refundable / Adjustable" in t2:
					flag1=1	
			if flag==0:		
				fees_head_dic['%s'%(t["account"])]=[]
				fees_head_dic["%s"%(t["account"])].append(t["credit"])
			else:
				fees_head_dic["%s"%(t["account"])].append(t["credit"])

			if flag1==0:
				Payment_head_dic['%s'%(t["account"])]=[]
				Payment_head_dic["%s"%(t["account"])].append(t["credit"])
			else:
				Payment_head_dic["%s"%(t["account"])].append(t["credit"])	

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

	voucher_no=[]
	for z in Gl_entry_Pay_Rec:
		if z["voucher_type"]=="Fees":
			voucher_no.append(z['voucher_no'])
	voucher_no = list(set(voucher_no))	

	########################
	Fee_DOC=[]
	for t in voucher_no:
		total_waiver_amount=frappe.db.get_all('Fee Component',{"parent":t},["fees_category","total_waiver_amount","grand_fee_amount","receivable_account"])
		Fee_DOC.append(total_waiver_amount)
		# fees_head_dic["%s"%(t["account"])].append(t["debit"])		 	
	############################

	head_fee=[]
	for Fee_components in Fee_DOC:
		for i in range(len(Fee_components)):
			head_fee.append(Fee_components[i]["receivable_account"])
		head_fee=list(set(head_fee))    

	Fee_cal={}    
	for t in range(len(head_fee)):
		Fee_cal['%s'%(head_fee[t])]=[]
	############################################ Fees Refundable / Adjustable reconcelation 
	########### Extra amount colleted during payment entry
	Gl_entry_payment_ref=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],["is_cancelled",'=',0],['party','=',party],['voucher_type',"=",'Payment Entry'],['posting_date', 'between', 
								[start_date, end_date]],["account","like","%Fees Refundable / Adjustable%"],["debit","=",0]],
								fields=["name","account","debit","credit"])						
	fees_ref_adj_balance={}
	if Gl_entry_payment_ref:
		for t in Gl_entry_payment_ref:
			fees_ref_adj_balance['%s'%(t['account'])]=[]
			break
		for t in Gl_entry_payment_ref:
			fees_ref_adj_balance["%s"%(t['account'])].append(t['credit'])

	fees_ref_adj_balance=dict(zip(fees_ref_adj_balance.keys(),[sum(items) for items in fees_ref_adj_balance.values()]))
	################## Extra amount collected during payment refund
	Gl_entry_payment_ref=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],["is_cancelled",'=',0],['against','=',party],['voucher_type',"=",'Journal Entry'],['posting_date', 'between', 
								[start_date, end_date]],["account","like","%Fees Refundable / Adjustable%"],["credit","!=",0]],
								fields=["name","account","debit","credit"])												
	payment_refund_adj_collection={}
	if Gl_entry_payment_ref:
		for t in Gl_entry_payment_ref:
			payment_refund_adj_collection['%s'%(t['account'])]=[]
			break
		for t in Gl_entry_payment_ref:
			payment_refund_adj_collection["%s"%(t['account'])].append(t['credit'])

	payment_refund_adj_collection=dict(zip(payment_refund_adj_collection.keys(),[sum(items) for items in payment_refund_adj_collection.values()]))
	###################### Payment Refund (mode of payment - pay)
	Gl_entry_payment_ref=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],["is_cancelled",'=',0],['against','=',party],['voucher_type',"=",'Journal Entry'],['posting_date', 'between', 
								[start_date, end_date]],["account","like","%Fees Refundable / Adjustable%"],["debit","!=",0]],
								fields=["name","account","debit","credit"])	
	payment_refund_adj_payment={}
	if Gl_entry_payment_ref:
		for t in Gl_entry_payment_ref:
			payment_refund_adj_payment['%s'%(t['account'])]=[]
			break
		for t in Gl_entry_payment_ref:
			payment_refund_adj_payment["%s"%(t['account'])].append(t['debit'])

	payment_refund_adj_payment=dict(zip(payment_refund_adj_payment.keys(),[sum(items) for items in payment_refund_adj_payment.values()]))
	######################## payment entry (mode of pay - pay)
	Gl_entry_payment_ref=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],["is_cancelled",'=',0],['against','=',party],['voucher_type',"=",'Payment Entry'],['posting_date', 'between', 
								[start_date, end_date]],["account","like","%Fees Refundable / Adjustable%"],["credit","=",0]],
								fields=["name","account","debit","credit"]) 
												
	payment_entry_adj_payment={}
	if Gl_entry_payment_ref:
		for t in Gl_entry_payment_ref:
			payment_entry_adj_payment['%s'%(t['account'])]=[]
			break
		for t in Gl_entry_payment_ref:
			payment_entry_adj_payment["%s"%(t['account'])].append(t['debit'])

	payment_entry_adj_payment=dict(zip(payment_entry_adj_payment.keys(),[sum(items) for items in payment_entry_adj_payment.values()]))
	############################################




	Waver_amount={}
	for t in range(len(head_fee)):
		Waver_amount['%s'%(head_fee[t])]=[]

	for Fee_components in Fee_DOC:
		for i in range(len(Fee_components)):
			Fee_cal['%s'%(Fee_components[i]["receivable_account"])].append(Fee_components[i]['grand_fee_amount'])
			Waver_amount['%s'%(Fee_components[i]["receivable_account"])].append(Fee_components[i]['total_waiver_amount'])

	Fee_cal = dict(zip(Fee_cal.keys(), [sum(item) for item in Fee_cal.values()]))
	Waver_amount = dict(zip(Waver_amount.keys(), [sum(item) for item in Waver_amount.values()]))	
	#######################################################################		
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
	# if len(student_group)==0:
	# 	frappe.throw("Student Group Not Found")
	student_Enrollment=frappe.db.sql(""" select DISTINCT `program_grade` from `tabProgram Enrollment` where `student`='%s'"""%(student))

	g_value=[]
	g_value.append(student_info[0]["title"])
	g_value.append(student_data_info[0]["Semesters"])
	g_value.append(student_data_info[0]["Programs"])
	# g_value.append(student_info[0]["kiit_polytechnic_roll_no"])
	g_value.append(student_info[0]["roll_no"])
	g_value.append(student_info[0]["vidyarthi_portal_id"])
	g_value.append(student_info[0]["sams_portal_id"])
	if len(student_group)==0:
		g_value.append("")
	else:
		g_value.append(student_group[0]["batch"])
	g_value.append("Header")
	g_value.append(student_Enrollment[0][0])
	g_value.append(student_data_info[0]["academic_year"])
	g_value.append("")
	g_value.append("")
	Final_list.append(g_value)	
	# [1, 'Debtors - SOUL', 'INR', 80000.0, 80000.0, '', 'Body', 0.0, 160000.0, 0.0]
		
	# Final_list=["Sl_no","Fees Head","Currency","Dues","paid","Balance","Paid amount","Body","Waver_amount","Grand_total","Refund_fees_head_dic","Refund_Payment_head_dic"]	

	Count=0
	for t in fees_head_dic:
		g_value=[]
		Count=Count+1
		############### Sl No 
		g_value.append(Count)
		############## Fees Head
		g_value.append(t)
		################# Currency
		g_value.append(currency_info)
		################## Dues
		if ('Fees Refundable / Adjustable' in t)==False:
			g_value.append(fees_head_dic[t])
		else:
			g_value.append(0)	
		flag=""
		########################paid
		for j in Payment_head_dic:
			if t==j:
				flag="Done"
				g_value.append(Payment_head_dic[j])		
		if flag!="Done":
			g_value.append(0)
			flag=""	
		else:
			flag=""		

		############################# Balance
		for i in Outsatnding_dict:
			if t==i:
				flag="Done"
				if ('Fees Refundable / Adjustable' in t)==False:
					payment_value=0
					try:
						payment_value=Payment_head_dic[i]
					except:
						pass
					Outsatnding_dict['%s'%(t)]=fees_head_dic[t]-Waver_amount[t]-payment_value
					g_value.append(Outsatnding_dict[i])	
				else:
					####################### nead update for ref/ad. amount.
					#### Collected_amount(payment entry and payment refund)-paid amount (amount consumed in payment entry (Payment_head_dic) and payment refund (JE Entry)) 
					fees_ref_adj_balance_key=fees_ref_adj_balance.keys()
					flag_ck=0
					account=""
					for t1 in fees_ref_adj_balance_key:
						if "Fees Refundable / Adjustable" in t1:
							account=t1
							flag_ck=1
					payment_value=0
					paid_amount=0		
					payment_entry_ref_amount=0
					payment_refund_amount=0
					
					collected_amount_payment_entry=0
					collected_amount_payment_refund=0
					########### collection
					if flag_ck==1:
						collected_amount_payment_entry=fees_ref_adj_balance[account]
					if payment_refund_adj_collection:
						key=payment_refund_adj_collection.keys()
						for z1 in key:
							account1=z1
						collected_amount_payment_refund=payment_refund_adj_collection[account1]	
					col_total_amount=collected_amount_payment_entry+collected_amount_payment_refund	
					################### end collection
					################## payment back
					if payment_refund_adj_payment:
						key=payment_refund_adj_payment.keys()
						for z1 in key:
							account1=z1
						payment_refund_amount=payment_refund_adj_payment[account1]
					if payment_entry_adj_payment:
						key=payment_entry_adj_payment.keys()
						for z1 in key:
							account1=z1
						payment_entry_ref_amount=payment_entry_adj_payment[account1]						
					paid_amount=payment_entry_ref_amount+payment_refund_amount
					############################# end payment back
					payment_value=col_total_amount-paid_amount
					g_value.append(payment_value)	
		if flag!="Done":
			g_value.append(0)
			flag=""	
		else:
			flag=""		


		g_value.append("")			
		g_value.append("Body")
		################################## Waiver amount
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
		###################################


		for j in Fee_cal:
			if j==t:
				flag="Done"
				g_value.append(Fee_cal[t])	
		if flag!="Done":
			g_value.append(0)
			flag=""	
		else:
			flag=""	

		################################# REFUND BALANCE (only Fees Refundable / Adjustable)
		# REFUND BALANCE=Total amount colleted(Payment entry & Payment Refund) - Total amount used for clearing(payment Entry and Payment Refund)
		for i in Outsatnding_dict:
			if t==i:
				flag="Done"
				if ('Fees Refundable / Adjustable' in t)==False:
					g_value.append(0)
				else:
					####################### nead update for ref/ad. amount.
					#### Collected_amount(payment entry and payment refund)-paid amount (amount consumed in payment entry (Payment_head_dic) and payment refund (JE Entry)) 
					fees_ref_adj_balance_key=fees_ref_adj_balance.keys()
					flag_ck=0
					account=""
					for t1 in fees_ref_adj_balance_key:
						if "Fees Refundable / Adjustable" in t1:
							account=t1
							flag_ck=1
					payment_value=0
					paid_amount=0		
					payment_entry_ref_amount=0
					payment_refund_amount=0
					
					collected_amount_payment_entry=0
					collected_amount_payment_refund=0
					########### collection
					if flag_ck==1:
						collected_amount_payment_entry=fees_ref_adj_balance[account]
					if payment_refund_adj_collection:
						key=payment_refund_adj_collection.keys()
						for z1 in key:
							account1=z1
						collected_amount_payment_refund=payment_refund_adj_collection[account1]	
					col_total_amount=collected_amount_payment_entry+collected_amount_payment_refund	
					################### end collection
					################## payment back
					if payment_refund_adj_payment:
						key=payment_refund_adj_payment.keys()
						for z1 in key:
							account1=z1
						payment_refund_amount=payment_refund_adj_payment[account1]
					if payment_entry_adj_payment:
						key=payment_entry_adj_payment.keys()
						for z1 in key:
							account1=z1		##################################################### Refunded amount
						payment_entry_ref_amount=payment_entry_adj_payment[account1]						
					paid_amount=payment_entry_ref_amount+payment_refund_amount
					############################# end payment back
					payment_value=col_total_amount-paid_amount
					g_value.append(payment_value)
		# for j in Refund_fees_head_dic:
		# 	if j==t:
		# 		flag="Done"
		# 		g_value.append(Refund_fees_head_dic[j])	
		if flag!="Done":
			g_value.append(0)
			flag=""
		else:
			flag=""			
		################################################## Payment Refund to the studnet
		# paid amount = amount paid from payment(in the head - mode of payment(Pay))+ amount paid from payment refund(mode of payment)  
		for i in Outsatnding_dict:
			if t==i:
				flag="Done"
				if ('Fees Refundable / Adjustable' in t)==False:
					g_value.append(0)
				else:
					paid_amount=0
					payment_entry_ref_amount=0
					payment_refund_amount=0
					if payment_entry_adj_payment:
						key=payment_entry_adj_payment.keys()
						for z1 in key:
							account1=z1		##################################################### Refunded amount
						payment_entry_ref_amount=payment_entry_adj_payment[account1]
					if payment_refund_adj_payment:
						key=payment_refund_adj_payment.keys()
						for z1 in key:
							account1=z1
						payment_refund_amount=payment_refund_adj_payment[account1]	
					paid_amount=payment_entry_ref_amount+payment_refund_amount
					g_value.append(paid_amount)

		# for j in Refund_Payment_head_dic:
		# 	if j==t:
		# 		flag="Done"
		# 		g_value.append(Refund_Payment_head_dic[j])
		if flag!="Done":
			g_value.append(0)
			flag=""
		else:
			flag=""
		#############################################################				
									
		Final_list.append(g_value)
	dew=0
	paid=0
	Balance=0
	Waiver=0
	Fee_cal=0
	Refund_balance=0
	Payment_ref=0
	for z in Final_list:
		head_of_report=z[7]
		if head_of_report=="Body":
			dew=dew+z[3]
			paid=paid+z[4]
			if ("Fees Refundable / Adjustable" in z[1])==True:
				Balance=Balance-z[5]
			else:
				Balance=Balance+z[5]
			Waiver=Waiver+z[8]
			Fee_cal=Fee_cal+z[8]
			Refund_balance=Refund_balance+z[10]
			Payment_ref=Payment_ref+z[11]
			
	g_value=[]
	g_value.append("")
	g_value.append("Total")
	g_value.append(currency_info)
	g_value.append(dew)
	g_value.append(paid)
	g_value.append(Balance)
	g_value.append("")			
	g_value.append("Body")
	g_value.append(Waiver)
	g_value.append(Fee_cal)
	g_value.append(Refund_balance)
	g_value.append(Payment_ref)
	Final_list.append(g_value)	
	############################################################# payment entry
	Gl_entry_Type_payment=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],["is_cancelled",'=',0],['against','=',party],['voucher_type',"=",'Payment Entry'],['posting_date', 'between', 
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
		g_value.append("Receive")
		g_value.append("")
		g_value.append("")
		Final_list.append(g_value)
	################################### payment refund 
	payment_refund_data=frappe.get_all("Payment Refund",filters=[["docstatus","=",1],['party','=',party],['posting_date', 'between',[start_date, end_date]]],
									fields=['name','posting_date','mode_of_payment','payment_type','paid_from_account_currency','paid_to_account_currency'])
	for data in payment_refund_data:
		payment_refund_data_amount=frappe.get_all("Payment Entry Reference Refund",{"parent":data['name']},["name","total_amount"])	
		amount=payment_refund_data_amount[0]["total_amount"]
		data['amount']=amount
	for t in payment_refund_data:
		Count=Count+1
		g_value=[]
		g_value.append(Count)
		g_value.append(t["posting_date"])
		if t['payment_type']=="Pay":
			g_value.append(t['paid_from_account_currency'])
		if t['payment_type']=="Receive":
			g_value.append(t['paid_to_account_currency'])
		g_value.append(t['mode_of_payment'])
		g_value.append("")
		g_value.append(t['name'])
		g_value.append(t['amount'])
		g_value.append("Lower")
		g_value.append(t['name'])
		g_value.append(t['payment_type'])
		g_value.append("")
		g_value.append("")
		Final_list.append(g_value)	

	print("\n\n\n\n\n")
	print(Final_list)
	for t in Final_list:
		print(len(t))
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