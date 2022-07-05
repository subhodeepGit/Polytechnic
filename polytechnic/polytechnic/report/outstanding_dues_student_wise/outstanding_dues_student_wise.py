# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	# columns, data = [], []
	get_data_info=get_data(filters)
	get_columns_info=get_columns()
	return  get_columns_info,get_data_info

def get_data(filters):
	branch=filters.get('programs')
	semester=filters.get('semester')
	start_date=filters.get('start_date')
	end_date=filters.get('end_date')
	######################## Student Info 
	studnet_info=student_info(branch,semester)
	if not studnet_info:
		frappe.throw("No studnet Record Found")

	########## Gl Entry data
	Gl_entry_Pay_Rec=gl_entry(studnet_info,start_date,end_date)
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
	################# out-put for front end  	
	final_list=[]	
	for t in studnet_info:
		a=list(t.values())
		b=['' if v is None else v for v in a]
		final_list.append(b)
	####################### 		
	return final_list

def student_info(branch=None,semester=None):
	student_all_data=[]
	if branch!=None and semester!=None:
		student_data=frappe.get_all("Current Educational Details",filters=[["programs","=",branch],["semesters","in",tuple(semester)],["parenttype","=","student"]],fields=["parent"])
		# 1 Student No.
		# 2 ROLL NO
		# 3 DET No
		# 4 Vidyarthi Portal ID
		# 5 SEX
		# 6 CATEGORY
		count=0
		for t in student_data:
			data=frappe.get_all("Student",{"name":t['parent']},['name',"roll_no","sams_portal_id","vidyarthi_portal_id","title",
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
								[start_date, end_date]]],fields=["name","account","debit","credit","voucher_no","voucher_type","account_currency","docstatus"])
	return Gl_entry_Pay_Rec






def get_columns():
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

	]
	return columns	