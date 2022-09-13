# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from polytechnic.polytechnic.validations.payment_entry import validate

class TransportFeeStructure(Document):
	def validate(self):
		if(self.start_date > self.end_date):
			frappe.throw("Start Date cannot be greater than End Date!!")
