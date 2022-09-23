# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

# import frappe

from __future__ import unicode_literals
from dataclasses import fields
from itertools import count
from locale import currency
from frappe import _
import frappe
from frappe import msgprint




def execute(filters=None):
	# columns, data = [], []
	# return columns, data
	if not filters: filters= {}

	data, columns = [], []

	columns = get_columns()
	data = get_cs_data(filters)
	# print(data,"data")

	return columns, data



def get_cs_data(filters):
	print("\n\n\n\n")
	student_batch=filters.get('student_batch')
	programs=filters.get('programs')
	posting_date1=filters.get('posting_date1')
	posting_date2=filters.get('posting_date2')
	# conditions = get_conditions(filters)
	waiver_data_fetch = frappe.get_all(
		doctype='Fee Waiver',
		fields=['posting_date', 'name', 'company', 'programs', 'student_batch', 'student', 'student_name', 'grand_total', 'remarks', 'roll_no'],
		filters=[["student_batch",'=',student_batch],["programs",'=',programs],['posting_date', 'between', 
											[posting_date1, posting_date2]]]
	)
	# waiver_data_fetch = frappe.db.sql(""" SELECT `posting_date`, `name`, `company`, `programs`, `student_batch`, `student`, `student_name`, `grand_total`, `remarks`, `roll_no` from `tabFee Waiver`
	# 				WHERE `student_batch`="%s" or `programs`="%s" or (`posting_date`>="%s" and `posting_date`<="%s")  
	# 				"""%(student_batch,programs,posting_date1,posting_date2))
	# print(waiver_data_fetch)
	# print("\n\n\n\n\n")
	# print("waiver_data_fetch",waiver_data_fetch)
	# print("\n\n\n")

	for t in waiver_data_fetch:
		stu_info=frappe.get_all("Student",{"name":t['student']},["sams_portal_id","vidyarthi_portal_id","roll_no","permanant_registration_number"])
		t["sams_portal_id"]=stu_info[0]["sams_portal_id"]
		t["vidyarthi_portal_id"]=stu_info[0]["vidyarthi_portal_id"]
		t["roll_no"]=stu_info[0]["roll_no"]
		t["permanant_registration_number"]=stu_info[0]["permanant_registration_number"]

	# print("waiver_data_fetch",waiver_data_fetch)

	# if not waiver_data_fetch:
	# 	msgprint(_("No records found"))
	# 	pass


	return waiver_data_fetch

# def get_conditions(filters):
# 	conditions = {}
# 	for key, value in filters.items():
# 		if filters.get(key):
# 			conditions[key] = value
# 			print(conditions[key])
# 	print("conditions",conditions)
# 	return conditions



def get_columns():
	columns=[
		{
			'fieldname': 'posting_date',
			'label': _('VCH DATE'),
			'fieldtype': 'Date',
			'width': '100'
		},
		{
			'fieldname': 'name',
			'label': _('VCH NO'),
			'fieldtype': 'Data',
			'width': '200'
		},
		{
			'fieldname': 'company',
			'label': _('WING'),
			'fieldtype': 'Data',
			'width': '120'
		},
		{
			'fieldname': 'programs',
			'label': _('BRANCH'),
			'fieldtype': 'Data',
			'width': '220'
		},
		{
			'fieldname': 'student_batch',
			'label': _('BATCH'),
			'fieldtype': 'Data',
			'width': '100'
		},
		{
			'fieldname': 'student',
			'label': _('STUDENT'),
			'fieldtype': 'Data',
			'width': '180'
		},
		{
			'fieldname': 'student_name',
			'label': _('STUDENT NAME'),
			'fieldtype': 'Data',
			'width': '180'
		},


		{
			'fieldname': 'roll_no',
			'label': _('ROLL NO'),
			'fieldtype': 'Data',
			'width': '90'
		},

		{
			'fieldname': 'vidyarthi_portal_id',
			'label': _('Vidyarthi Portal Id'),
			'fieldtype': 'Data',
			'width': '90'
		},
		
		{
			'fieldname': 'sams_portal_id',
			'label': _('SAMS Portal Id'),
			'fieldtype': 'Data',
			'width': '90'
		},
				{
			'fieldname': 'permanant_registration_number',
			'label': _('Permanant Registration Number'),
			'fieldtype': 'Data',
			'width': '90'
		},

		{
			'fieldname': 'grand_total',
			'label': _('TOTAL AMOUNT'),
			'fieldtype': 'Data',
			'width': '150'
		},
		{
			'fieldname': 'remarks',
			'label': _('REMARKS'),
			'fieldtype': 'Data',
			'width': '300'
		},

	]	
	return columns