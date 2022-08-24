# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	# columns, data = [], []
	get_data_info,head_name=get_data(filters)
	get_columns_info=get_columns(head_name)
	return  get_columns_info,get_data_info

def get_data(filters):
	print("\n\n\n\n\n")
	batch=filters.get('batch')
	gender=filters.get('gender')
	branch=filters.get('programs')
	start_date=filters.get('start_date')
	end_date=filters.get('end_date')
	# semester=filters.get('semester')
	# academic_term=filters.get("academic_term")
	final_list=[]
	head_name=[]
	######################## Student Info 
	# studnet_info=student_info(branch,semester,academic_term)
	studnet_info=student_info(batch,gender,branch)
	if studnet_info:
		########## Gl Entry data
		Gl_entry_Pay_Rec=gl_entry(studnet_info,start_date,end_date)
		print(Gl_entry_Pay_Rec)
		######################## payment and Fee segression 
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
					
		Gl_entry_Pay_Rec=list_for_fee   ############### Fees 
		Gl_entry_payment=list_of_payment #################### payment
		
		########################## dynamic allocation of head in fees
		head_name=head_finding(Gl_entry_Pay_Rec)
		################################### Currency Info
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
		########### Total Fee due		
		total_fee_due=total_fee_due_studnet(head_name,Gl_entry_Pay_Rec,studnet_info)
		####################### head wise outstanding 
		outsatnding_fee_student=head_wise_outsatnding(Gl_entry_Pay_Rec,studnet_info,head_name)
		##################### Total payment data 
		payment_entry_student=payment_entry(Gl_entry_payment,je_enrty_credit,studnet_info)
		########################## Fee waiver doc
		fee_waiver_student=fee_waiver(studnet_info,head_name,Gl_entry_Pay_Rec)
		############################ Fees Refundable / Adjustable collection
		refundable_entry_student=fees_refundable_adjustable(studnet_info,start_date,end_date)
		#########################################
		refunded_amount_student=refunded_amount(studnet_info,start_date,end_date)
		################# out-put for front end 	
		final_list=[]	
		for t in studnet_info:
			stu_info=list(t.values())
			print(stu_info)
			stu_info=['' if v is None else v for v in stu_info]
			stu_info.append(currency_info)
			############## net due
			flag="not found"
			for z in total_fee_due:
				if t['stu_no']==z['student']:
					stu_info.append(z['net_due'])
					flag="done"
					break
			if flag=="not found":
				stu_info.append(0)
			else:
				flag="not found"
			######################### end of net due
			########################################## Head wise due
			net_due=0 	
			for z in outsatnding_fee_student:
				if t['stu_no']==z['student']:
					for v in head_name:
						stu_info.append(z["%s"%(v)])
					stu_info.append(z['net_due'])
					net_due=z['net_due']			
			###################################### end 	of Head wise due 
			#################### paid amount
			for z in payment_entry_student:
				if t['stu_no']==z['student']:
					stu_info.append(z['paid_amount'])		
			######################### end paid amount
			################### fee waiver 
			for z in fee_waiver_student:
				if t['stu_no']==z['student']:
					stu_info.append(z['net_due'])	
			################## end of fee waiver 
			##################### 	Fees Refundable / Adjustable collection		
			for z in refundable_entry_student:
				if t['stu_no']==z['student']:
					stu_info.append(z['refundable_amount_collected'])
			################################end Fees Refundable / Adjustable collection
			# #########################################  	Fees Refundable / Adjustable  paid	
			for z in refunded_amount_student:
				if t['stu_no']==z['student']:
					stu_info.append(z['refunded_amount'])		
			#################### End Fees Refundable / Adjustable  paid	
			########################### ADJUSTMENT AMOUNT = Fees Refundable / Adjustable collection - Fees Refundable / Adjustable  paid
			refundable_collection=stu_info[19]
			refundable_paid=stu_info[20]
			adj_balance=refundable_collection-refundable_paid
			stu_info.append(adj_balance)
			########################### end ADJUSTMENT AMOUNT = Fees Refundable / Adjustable collection - Fees Refundable / Adjustable  paid
			############################ Balance = Total -(REFUND BALANCE-REFUNDED AMOUNT)
			balance=net_due-adj_balance
			stu_info.append(balance)
			#####################
			print(len(stu_info))
			final_list.append(stu_info)
			################### end fee waiver
		####################### 
		return final_list,head_name		
	else:
		frappe.throw("No studnet record found")
	# return final_list,head_name

def student_info(batch,gender,branch):
	filter=[]
	if batch!=None:
		filter.append(["student_batch_name","=",batch])
	if branch!=None:
		filter.append(["programs","=",branch])
	if gender!=None:
		filter.append(["gender","=",gender])

	student_all_data=[]
	student_data=frappe.get_all("Program Enrollment",filters=filter,fields=["student"])
	# 1 Student No.
	# 2 ROLL NO
	# 3 DET No
	# 4 Vidyarthi Portal ID
	# 5 SEX
	# 6 CATEGORY
	student_info=[]
	for t in student_data:
		student_info.append(t['student'])
	student_info = list(set(student_info))
	count=0
	for t in student_info:
		data=frappe.get_all("Student",{"name":t},['name',"roll_no","sams_portal_id","vidyarthi_portal_id","title",
														"gender","student_category","enabled"])
		if data[0]['enabled']==1:
			stu_info={}
			count+=1
			stu_info['sl_no']=count
			stu_info['stu_no']=data[0]['name']
			stu_info['roll_no']=data[0]['roll_no']
			stu_info['sams_portal_id']=data[0]['sams_portal_id']
			stu_info['vidyarthi_portal_id']=data[0]['vidyarthi_portal_id']
			stu_info['student_name']=data[0]['title']
			stu_info['gender']=data[0]['gender']
			stu_info['student_category']=data[0]['student_category']
			student_all_data.append(stu_info)

	return student_all_data

def gl_entry(studnet_list,start_date,end_date):
	party=[]
	for t in studnet_list:
		party.append(t['stu_no'])	
	Gl_entry_Pay_Rec=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],['party','in',tuple(party)],['posting_date', 'between', 
											[start_date, end_date]],["is_cancelled","=",0]],fields=["name","account","debit","credit","voucher_no","voucher_type",
											"account_currency","docstatus","against","party"])							
	return Gl_entry_Pay_Rec

def head_finding(Gl_entry_dew_fees):
	head_name=[]
	for t in Gl_entry_dew_fees:
		head_name.append(t['account'])
	head_name=list(set(head_name))
	return head_name

def total_fee_due_studnet(head_name,Gl_entry_Pay_Rec,studnet_info):
	fee_student=[]
	for t in studnet_info:
		fees_head_dic={}
		fees_head_dic['student']=t['stu_no']
		for z in head_name:
				fees_head_dic['%s'%(z)]=[]
		fee_student.append(fees_head_dic)		

	for t in fee_student:
		for gl_rep in Gl_entry_Pay_Rec:
			if t['student']==gl_rep['party']:
				t['%s'%(gl_rep['account'])].append(gl_rep["debit"])
	
	for student in fee_student:
		net_due=0
		for z in student:
			if z!="student":
				student[z]=sum(student[z])
				net_due=net_due+student[z]
		student['net_due']=net_due			
	return fee_student

def head_wise_outsatnding(Gl_entry_Pay_Rec,studnet_info,head_name):
	outsatnding_fee_student=[]
	for t in studnet_info:
		fees_head_dic={}
		fees_head_dic['student']=t['stu_no']
		for z in head_name:
				fees_head_dic['%s'%(z)]=[]
		fees_head_dic['fee_voucher']=[]	
		outsatnding_fee_student.append(fees_head_dic)

	
	for t in Gl_entry_Pay_Rec:
		for z in outsatnding_fee_student:
			if z['student']==t["party"]:
				z['fee_voucher'].append(t['voucher_no'])


	for t in outsatnding_fee_student:
		t['fee_voucher']=list(set(t['fee_voucher']))

	for student in outsatnding_fee_student:
		for voucher_no in student['fee_voucher']:
			component=frappe.get_all("Fee Component",filters=[["parent","=",voucher_no],["outstanding_fees","!=",0]],
												fields=["fees_category","outstanding_fees","receivable_account"])
			if component:
				for fee_component in component:
					student["%s"%(fee_component["receivable_account"])].append(fee_component['outstanding_fees'])

	for student in outsatnding_fee_student:
		net_due=0
		for z in student:
			if z!="student" and z !="fee_voucher":
				student[z]=sum(student[z])
				net_due=net_due+student[z]
		student['net_due']=net_due										

	return outsatnding_fee_student

def payment_entry(Gl_entry_payment,je_enrty_credit,studnet_info):
	payment_entry_student=[]
	for t in studnet_info:
		payment_head_dic={}
		payment_head_dic['student']=t['stu_no']
		payment_head_dic['paid_amount']=[]
		payment_head_dic['payment_voucher']=[]	
		payment_entry_student.append(payment_head_dic)

	for t in Gl_entry_payment:
		for z in payment_entry_student:
			if z['student']==t["party"]:
				if t["voucher_type"]=="Payment Entry":
					z['paid_amount'].append(t['credit'])
					z['payment_voucher'].append(t['voucher_no'])

	for t in je_enrty_credit:
		for z in payment_entry_student:
			if z['student']==t["party"]:
				if ('Fees Refundable / Adjustable' in t["account"])==False:
					z['paid_amount'].append(t['credit'])
					z['payment_voucher'].append(t['voucher_no'])

	for student in payment_entry_student:
		for z in student:
			if z!="student" and z !="payment_voucher":
				student[z]=sum(student[z])
	return payment_entry_student

def fee_waiver(studnet_info,head_name,Gl_entry_Pay_Rec):
	fee_waiver_student=[]
	for t in studnet_info:
		fees_waiver_head_dic={}
		fees_waiver_head_dic['student']=t['stu_no']
		for z in head_name:
			fees_waiver_head_dic['%s'%(z)]=[]
		fees_waiver_head_dic['fee_voucher']=[]	
		fee_waiver_student.append(fees_waiver_head_dic)


	for t in Gl_entry_Pay_Rec:
		for z in fee_waiver_student:
			if z['student']==t["party"]:
				z['fee_voucher'].append(t['voucher_no'])

	for t in fee_waiver_student:
		t['fee_voucher']=list(set(t['fee_voucher']))

	for student in fee_waiver_student:
		for voucher_no in student['fee_voucher']:
			component=frappe.get_all("Fee Component",filters=[["parent","=",voucher_no],["total_waiver_amount","!=",0]],
												fields=["fees_category","total_waiver_amount","receivable_account"])
			if component:
				for fee_component in component:
					student["%s"%(fee_component["receivable_account"])].append(fee_component['total_waiver_amount'])


	for student in fee_waiver_student:
		net_due=0
		for z in student:
			if z!="student" and z !="fee_voucher":
				student[z]=sum(student[z])
				net_due=net_due+student[z]
		student['net_due']=net_due	
		
	return fee_waiver_student


def fees_refundable_adjustable(studnet_info,start_date,end_date):
	party=[]
	for t in studnet_info:
		party.append(t['stu_no'])	
	########### Extra amount colleted during payment entry
	Gl_entry_payment_ref=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],['party','in',tuple(party)],['voucher_type',"=",'Payment Entry'],['posting_date', 'between', 
								[start_date, end_date]],["account","like","%Fees Refundable / Adjustable%"],["debit","=",0]],
								fields=["name","account","debit","credit","party","voucher_no"])	
	refundable_entry_student=[]
	for t in studnet_info:
		refundable_head_dic={}	
		refundable_head_dic['student']=t['stu_no']
		refundable_head_dic['refundable_amount_collected']=[]
		refundable_head_dic['payment_voucher']=[]
		refundable_entry_student.append(refundable_head_dic)		
			
	for t in Gl_entry_payment_ref:
		for z in refundable_entry_student:
			if z['student']==t["party"]:
				z['refundable_amount_collected'].append(t['credit'])
				z['payment_voucher'].append(t['voucher_no'])

	# ################## Extra amount collected during payment refund
	Gl_entry_payment_ref=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],['against','in',tuple(party)],['voucher_type',"=",'Journal Entry'],['posting_date', 'between', 
								[start_date, end_date]],["account","like","%Fees Refundable / Adjustable%"],["credit","!=",0]],
								fields=["name","account","debit","credit","party","voucher_no"])		
	for t in Gl_entry_payment_ref:
		for z in refundable_entry_student:
			if z['student']==t["party"]:
				z['refundable_amount_collected'].append(t['credit'])
				z['payment_voucher'].append(t['voucher_no'])

	for student in refundable_entry_student:
		for z in student:
			if z!="student" and z !="payment_voucher":
				student[z]=sum(student[z])
	return refundable_entry_student



def refunded_amount(studnet_info,start_date,end_date):
	party=[]
	for t in studnet_info:
		party.append(t['stu_no'])	

	###################### Payment Refund (mode of payment - pay)
	Gl_entry_payment_ref=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],['against','in',tuple(party)],['voucher_type',"=",'Journal Entry'],['posting_date', 'between', 
								[start_date, end_date]],["account","like","%Fees Refundable / Adjustable%"],["debit","!=",0]],
								fields=["name","account","debit","credit","party","voucher_no"])
	refunded_amount_student=[]
	for t in studnet_info:
		refundable_head_dic={}	
		refundable_head_dic['student']=t['stu_no']
		refundable_head_dic['refunded_amount']=[]
		refundable_head_dic['payment_voucher']=[]
		refunded_amount_student.append(refundable_head_dic)	


	for t in Gl_entry_payment_ref:
		for z in refunded_amount_student:
			if z['student']==t["party"]:
				z['refunded_amount'].append(t['debit'])
				z['payment_voucher'].append(t['voucher_no'])	
	
	######################## payment entry (mode of pay - pay)
	Gl_entry_payment_ref=frappe.db.get_list('GL Entry', filters=[["docstatus",'=',1],['against','in',tuple(party)],['voucher_type',"=",'Payment Entry'],['posting_date', 'between', 
								[start_date, end_date]],["account","like","%Fees Refundable / Adjustable%"],["credit","=",0]],
								fields=["name","account","debit","credit","party","voucher_no"]) 

	for t in Gl_entry_payment_ref:
		for z in refunded_amount_student:
			if z['student']==t["party"]:
				z['refunded_amount'].append(t['debit'])
				z['payment_voucher'].append(t['voucher_no'])	

	for student in refunded_amount_student:
		for z in student:
			if z!="student" and z !="payment_voucher":
				student[z]=sum(student[z])

	return refunded_amount_student




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
	if len(head_name)!=0:
		for t in head_name:
			label=t
			fieldname=label.replace(" ", "")
			columns_add={
				"label": _("%s"%(label)),
				"fieldname": "%s"%(fieldname),
				"fieldtype": "Data",
				"width":200
			}
			columns.append(columns_add)
		columns_add={
				"label": _("Total Due"),
				"fieldname":"total_due",
				"fieldtype": "Data",
				"width":200
			}
		columns.append(columns_add)	
		columns_add={
				"label": _("PAID AMOUNT"),
				"fieldname":"paid_amount",
				"fieldtype": "Data",
				"width":200
			}
		columns.append(columns_add)	
		columns_add={
				"label": _("EXEMPTION"),
				"fieldname":"exemption",
				"fieldtype": "Data",
				"width":200
			}
		columns.append(columns_add)	
		columns_add={
				"label": _("REFUNDABLE AMOUNT COLLECTED"),
				"fieldname":"refundable_amount_collected",
				"fieldtype": "Data",
				"width":200
			}
		columns.append(columns_add)	
		columns_add={
				"label": _("REFUNDED AMOUNT"),
				"fieldname":"refunded_amount",
				"fieldtype": "Data",
				"width":200
			}
		columns.append(columns_add)	
		columns_add={
				"label": _("ADJUSTMENT AMOUNT"),
				"fieldname":"adjustment_amount",
				"fieldtype": "Data",
				"width":200
			}
		columns.append(columns_add)	
		columns_add={
				"label": _("BALANCE AMOUNT"),
				"fieldname":"balance_amount",
				"fieldtype": "Data",
				"width":200
			}
		columns.append(columns_add)	
	return columns	
