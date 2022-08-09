# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class IDCardPhotoDownloader(Document):
	pass
@frappe.whitelist()
def get_documents(class_stream,session):
	student_list=frappe.db.get_all("Identity Card",filters=[["session","=","%s"%(session)],["class_stream","=","%s"%(class_stream)]],fields=["student","student_name","roll_no","passport_photo"])
	return student_list
