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
    start_date=filters.get('start_date')
    end_date=filters.get('end_date')

    payment_entry=frappe.get_all("Payment Entry",filters=[['posting_date', 'between',[start_date, end_date]],["docstatus","=",1]],
                                            fields=["name","mode_of_payment","party","party_name","roll_no","academic_year","permanent_registration_number",
                                                        "sams_portal_id","vidyarthi_portal_id","total_allocated_amount","posting_date","owner","payment_type"])
    surplus_payment_entry=frappe.get_all("Payment Refund",filters=[['posting_date', 'between',[start_date, end_date]],["docstatus","=",1]],
                                                        fields=["name","mode_of_payment","payment_type","party","party_name","roll_no","permanent_registration_number",
                                                                "sams_portal_id","vidyarthi_portal_id","jv_entry_voucher_no","posting_date","owner","payment_type"])
    ############Payment Entry##################
    head_list=[]
    payment_entry_list=[]
    if payment_entry: 
        for t in payment_entry:
            payment_entry_list.append(t["name"])
        filters=[]
        if len(payment_entry_list)==1:
            payment_entry_reference=frappe.get_all("Payment Entry Reference",filters=[["parent","=",payment_entry_list[0]]],
                                                    fields=["name","parent","fees_category","account_paid_from","allocated_amount"])
        else:
            payment_entry_reference=frappe.get_all("Payment Entry Reference",filters=[["parent","in",tuple(payment_entry_list)]],
                                                fields=["name","parent","fees_category","account_paid_from","allocated_amount"])
        
        
        for t in payment_entry_reference:
            head_list.append(t["fees_category"])
        head_list=list(set(head_list))

        if surplus_payment_entry:
            a="Fees Refundable / Adjustable" in head_list
            if a==False:
                head_list.append("Fees Refundable / Adjustable") 


        for t in payment_entry:
            if frappe.get_all('Employee',{'personal_email':t["owner"]},['employee_name']):
                prepared_by=frappe.get_all("Employee",{'personal_email':t["owner"]},["employee_name"])[0]['employee_name']
                t["prepared_by"]=prepared_by
            
            stu_info=frappe.get_all("Student",{"name":t["party"]},["gender","student_category"])
            stu_program = frappe.get_all("Current Educational Details",{"parenttype":"Student","parent":t["party"]},["programs","semesters","student_batch_name"])
            t["program"]=stu_program[0]["programs"]
            t["semester"]=stu_program[0]["semesters"]
            t["batch"]=stu_program[0]["student_batch_name"]
            t["gender"]=stu_info[0]["gender"]
            t["student_category"]=stu_info[0]["student_category"]
            t['dt']="Payment Entry"
            
            for z in head_list:
                t[z]=[]

        for t in payment_entry:
            for j in payment_entry_reference:
                if t["name"]==j["parent"]:
                    flag="No"
                    for z in head_list:
                        if j["fees_category"]==z:
                            t[z].append(j["allocated_amount"])

        for t in payment_entry:
            for z in head_list:
                t[z]=sum(t[z])
    ###############Surplus Payment Entry#####################
    # surplus_payment_entry=frappe.get_all("Payment Refund",filters=[['posting_date', 'between',[start_date, end_date]],["docstatus","=",1]],
    #                                                     fields=["name","mode_of_payment","payment_type","party","party_name","roll_no","permanent_registration_number",
    #                                                             "sams_portal_id","vidyarthi_portal_id","jv_entry_voucher_no","posting_date","owner","payment_type"])
    surplus_payment_list=[]
    if surplus_payment_entry:
        for t in surplus_payment_entry:
            surplus_payment_list.append(t["name"])
        if len(surplus_payment_list)==1:
            surplus_payment_amount=frappe.get_all("Payment Entry Reference Refund",{"parent":surplus_payment_list[0]},
                     ["parent","name","allocated_amount","account_paid_to","fees_category"])
        else:
            surplus_payment_amount=frappe.get_all("Payment Entry Reference Refund",filters=[["parent","in",surplus_payment_list]],
                                                fields=["parent","name","allocated_amount","account_paid_to","fees_category"])
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
                    t["total_allocated_amount"]=j["allocated_amount"]
    for a in surplus_payment_entry:
        if frappe.get_all('Employee',{'personal_email':a["owner"]},['employee_name']):
            prepared_by_owner=frappe.get_all("Employee",{'personal_email':a["owner"]},["employee_name"])[0]['employee_name']
            a["prepared_by"]=prepared_by_owner
        stu_info=frappe.get_all("Student",{"name":a["party"]},["gender","student_category"])
        stu_program = frappe.get_all("Current Educational Details",{"parenttype":"Student","parent":a["party"]},["programs","semesters","student_batch_name"])
            
        a["program"]=stu_program[0]["programs"]
        a["semester"]=stu_program[0]["semesters"]
        a["batch"]=stu_program[0]["student_batch_name"]
        a["gender"]=stu_info[0]["gender"]
        a["student_category"]=stu_info[0]["student_category"]
        a["dt"]="Surplus Payment"
        payment_entry.append(a)

    return payment_entry,head_list
    	
def get_columns(head_name=None):
    columns = [
        {
            "label": _("Student No"),
            "fieldname": "party",
            "fieldtype": "Link",
            "options": "Student",
            "width":180
        },
        {
            "label": _("Roll No"),
            "fieldname": "roll_no",
            "fieldtype": "Data",
            "width":100
        },
        {
            "label": _("SAMS Portal ID"),
            "fieldname": "sams_portal_id",
            "fieldtype": "Data",
            "width":100
        },
        {
            "label": _("Student Name"),
            "fieldname": "party_name",
            "fieldtype": "Data",
            "width":180
        },
        {
            "label": _("Money Receipt No"),
            "fieldname": "name",
            "fieldtype": "Data",
            "width":180
        },
        {
            "label": _("Mode Of Payment"),
            "fieldname": "mode_of_payment",
            "fieldtype": "Data",
            "width":200
        },
        {
            "label": _("Collection Type"),
            "fieldname": "dt",
            "fieldtype": "Data",
            "width":180
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width":100
        },
        {
            "label": _("Payment Type"),
            "fieldname": "payment_type",
            "fieldtype": "Data",
            "width":180
        },
        {
            "label": _("Programs"),
            "fieldname": "program",
            "fieldtype": "Link",
            "options": "Programs",
            "width":180
        },
        {
            "label": _("Semester"),
            "fieldname": "semester",
            "fieldtype": "Link",
            "options": "Program",
            "width":180
        },
        {
            "label": _("Student Batch Name"),
            "fieldname": "batch",
            "fieldtype": "Data",
            "width":180
        },
        {
            "label": _("Gender"),
            "fieldname": "gender",
            "fieldtype": "Data",
            "width":180
        },
        {
            "label": _("Student Category"),
            "fieldname": "student_category",
            "fieldtype": "Data",
            "width":180
        },
        {
            "label": _("Paid Amount"),
            "fieldname": "total_allocated_amount",
            "fieldtype": "Data",
            "width":180
        }
    ]
    if len(head_name)!=0:
        for t in head_name:
            label=t
            columns_add={
                "label": _("%s"%(label)),
                "fieldname": "%s"%(label),
                "fieldtype": "Data",
                "width":180
            }
            columns.append(columns_add)
    prepared_by={
        "label": _("Prepared By"),
        "fieldname": "prepared_by",
        "fieldtype": "Data",
        "width":180
    }
    columns.append(prepared_by)
    return columns	
