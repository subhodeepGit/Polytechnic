# Copyright (c) 2023, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BranchSliding(Document):
	def on_submit(self):
		for t in self.get("students_details"):
			frappe.db.set_value('Program Enrollment', t.program_enrollment , {
				'programs': self.sliding_in_program,
				'program': self.sliding_in_semester
			})
			student = frappe.get_doc('Student', t.student)
			student.set("current_education",[])
			for enroll in frappe.get_all("Program Enrollment",{"docstatus":1,"student":t.student},["program_grade","student_batch_name","school_house","programs","program","academic_year","academic_term"],order_by='creation desc',limit=1):
				student.append("current_education",{
					"programs":enroll.programs,
					"semesters":enroll.program,
					"program_grade":enroll.program_grade,
					"school_house":enroll.school_house,
					"student_batch_name":enroll.student_batch_name,
					"academic_year":enroll.academic_year,
					"academic_term":enroll.academic_term
				})
			student.save()
	
	def on_cancel(self):
		for t in self.get("students_details"):
			frappe.db.set_value('Program Enrollment', t.program_enrollment , {
				'programs': self.programs,
				'program': self.semester
			})
			student = frappe.get_doc('Student', t.student)
			student.set("current_education",[])
			for enroll in frappe.get_all("Program Enrollment",{"docstatus":1,"student":t.student},["program_grade","student_batch_name","school_house","programs","program","academic_year","academic_term"],order_by='creation desc',limit=1):
				student.append("current_education",{
					"programs":enroll.programs,
					"semesters":enroll.program,
					"program_grade":enroll.program_grade,
					"school_house":enroll.school_house,
					"student_batch_name":enroll.student_batch_name,
					"academic_year":enroll.academic_year,
					"academic_term":enroll.academic_term
				})
			student.save()



@frappe.whitelist()
def get_students(academic_term=None, programs=None,class_data=None,
				semester=None):
	enrolled_students = get_program_enrollment(academic_term,programs,class_data)
	if enrolled_students:
		student_list = []
		for s in enrolled_students:
			if frappe.db.get_value("Student", s.student, "enabled"):
				s.update({"active": 1})
			else:
				s.update({"active": 0})
			student_list.append(s)
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