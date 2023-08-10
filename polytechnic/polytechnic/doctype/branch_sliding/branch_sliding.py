# Copyright (c) 2023, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BranchSliding(Document):
	def validate(self):
		print(self.sliding_in_program)
		print(self.sliding_in_semester)


@frappe.whitelist()
def get_students(academic_term=None, programs=None,class_data=None,
				semester=None):
	enrolled_students = get_program_enrollment(academic_term,programs,class_data)
	# print("\n\n\n")
	# print(enrolled_students)
	if enrolled_students:
		student_list = []
		for s in enrolled_students:
			if frappe.db.get_value("Student", s.student, "enabled"):
				s.update({"active": 1})
			else:
				s.update({"active": 0})
			student_list.append(s)
		print("\n\n\n",student_list)
		return student_list
		
	else:
		frappe.msgprint("No students found")
		return []

def get_program_enrollment(academic_term,programs=None,class_data=None):
	condition1 = " "
	condition2 = " "

	if programs:
		condition1 += " and pe.programs = %(programs)s"
	if class_data:
		condition1 +=" and pe.school_house = '%s' "%(class_data)
	condition1 +=" and s.enabled =1 "     
	return frappe.db.sql('''
		select
			pe.name, pe.student, pe.student_name,pe.roll_no,pe.permanant_registration_number,s.enabled
		from
			`tabProgram Enrollment` pe {condition2}
		join `tabStudent` s ON s.name=pe.student
		where
			pe.academic_term = %(academic_term)s  {condition1}
		order by
			pe.student_name asc
		'''.format(condition1=condition1, condition2=condition2),
				({"academic_term": academic_term,"programs": programs}), as_dict=1) 