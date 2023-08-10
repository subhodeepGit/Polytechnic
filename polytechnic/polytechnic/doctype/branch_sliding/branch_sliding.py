# Copyright (c) 2023, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.desk.form.linked_with import get_linked_doctypes

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
			update_program_enrollment_in_linked_doctype(self, t.program_enrollment)
	
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


def update_program_enrollment_in_linked_doctype(self, pe):
	linked_doctypes = get_linked_doctypes("Program Enrollment")
	for d in linked_doctypes:
		meta = frappe.get_meta(d)
		if not meta.issingle:
			if "programs" in [f.fieldname for f in meta.fields]:
				if d != "Program Enrollment" and d != "Branch Sliding" and d != "Transport Service" and d != "Fee Waiver":
					print(d)
					print(linked_doctypes[d]["fieldname"][0])
					print(self.programs)
					print(self.name)
					print("\n\n\n")
					frappe.db.sql(
						"""UPDATE `tab{0}` set programs = %s where {1} = %s""".format(
							d, linked_doctypes[d]["fieldname"][0]
						),
						(self.sliding_in_program, pe),
					)
			
			if "program" in [f.fieldname for f in meta.fields]:
				if d != "Program Enrollment" and d != "Branch Sliding" and d != "Transport Service" and d != "Fee Waiver":
					frappe.db.sql(
						"""UPDATE `tab{0}` set program = %s where {1} = %s""".format(
							d, linked_doctypes[d]["fieldname"][0]
						),
						(self.sliding_in_semester, pe),
					)

			if "semester" in [f.fieldname for f in meta.fields]:
				if d != "Program Enrollment" and d != "Branch Sliding":
					frappe.db.sql(
						"""UPDATE `tab{0}` set semester = %s where {1} = %s""".format(
							d, linked_doctypes[d]["fieldname"][0]
						),
						(self.sliding_in_semester, pe),
					)


			# if "child_doctype" in linked_doctypes[d].keys() and "student_name" in [
			# 	f.fieldname for f in frappe.get_meta(linked_doctypes[d]["child_doctype"]).fields
			# ]:
			# 	frappe.db.sql(
			# 		"""UPDATE `tab{0}` set student_name = %s where {1} = %s""".format(
			# 			linked_doctypes[d]["child_doctype"], linked_doctypes[d]["fieldname"][0]
			# 		),
			# 		(self.title, self.name),
			# 	)
			