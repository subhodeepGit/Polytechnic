# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	get_data_info=get_data(filters)
	return columns, data

def get_data(filters):
	branch=filters.get('programs')
	semester=filters.get('semester')
	start_date=filters.get('start_date')
	end_date=filters.get('end_date')
	print("\n\n\n\n")
	print(branch)
	print(semester)
	######################## Student Info 
	student_info(branch,semester)


def student_info(branch=None,semester=None):
	if branch!=None and semester!=None:
		student_data=frappe.get_all("Current Educational Details",filters=[["programs","=",branch],["semesters","in",tuple(semester)]],fields=["parent"])
		print("\n\n\n\n\n")
		print(student_data)