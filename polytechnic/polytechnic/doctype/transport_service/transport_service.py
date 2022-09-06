# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TransportService(Document):
	def validate(self):
		self.mobile_number_validation()
		self.validate_duplicate_data()

	def on_submit(self):
		self.create_fees()

	def on_cancel(self):
		self.cancel_fees()

	def create_fees(self):
		if self.fees_applicable == "" and self.statusf == "":
			frappe.throw("Status and Fees Applicable are mandatory")
		if self.fees_applicable == "Yes" and self.amount != 0:
			fees = frappe.new_doc("Fees")
			fees.student = self.student
			fees.valid_from = self.valid_from
			fees.valid_to = self.valid_to
			fees.due_date = self.due_date
			fees.program_enrollment = self.program_enrollment
			fees.programs = self.programs
			fees.program = self.semester
			fees.student_batch = self.student_batch
			fees.student_category = self.student_category
			fees.academic_year = self.academic_year
			fees.academic_term = self.academic_term
			fees.cost_center = "Main - KP"
			# ref_details = frappe.get_all("Fee Component",{"parent":self.hostel_fee_structure},['fees_category','amount','receivable_account','income_account','company','grand_fee_amount','outstanding_fees'],order_by="idx asc")
			# for i in ref_details:
			fees.append("components",{
				'fees_category' : "Transportation Fees",
				'amount' : self.amount,
				'receivable_account' : "Transportation Fees - KP",
				'income_account' : "Transportation Fees Income - KP",
				'company' : "KiiT Polytechnic",
				'grand_fee_amount' : self.amount,
				'outstanding_fees' : self.amount,
			})
			fees.save()
			fees.submit()	
			self.fees_id = fees.name
			frappe.db.set_value("Transport Service",self.name,"fees_id",fees.name)
			
	def cancel_fees(self):
		if self.fees_id:
			cancel_doc = frappe.get_doc("Fees",self.fees_id)
			cancel_doc.cancel()

	def mobile_number_validation(self):
		if self.emergency_contact_number:
			if not (self.emergency_contact_number).isdigit():
				frappe.throw("Field <b>Emergency Number</b> Accept Digits Only")
			if len(self.emergency_contact_number)>10:
				frappe.throw("Field <b>Emergency Number</b> must be 10 Digits")
			if len(self.emergency_contact_number)<10:
				frappe.throw("Field <b>Emergency Number</b> must be 10 Digits")

	def validate_duplicate_data(self):
		duplicateData=frappe.get_all("Transport Service", filters={
			"program_enrollment":self.program_enrollment,
			"programs":self.programs,
			"semester": self.semester,
			"statusf": "Approved",
			"academic_year":self.academic_year,
			"academic_term": self.academic_term,
			"docstatus":1
		})
		print(duplicateData)
		if duplicateData:
			frappe.throw(("Student has already applied for Transportaion Service")) 