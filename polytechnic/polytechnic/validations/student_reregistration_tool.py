# Copyright (c) 2021, suraj varade and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.education.api import enroll_student
from frappe.utils import cint

class StudentReregistrationTool(Document):
	def onload(self):
		academic_term_reqd = cint(frappe.db.get_single_value('Education Settings', 'academic_term_reqd'))
		self.set_onload("academic_term_reqd", academic_term_reqd)

	@frappe.whitelist()
	def get_students(self):
		students = []
		if not self.program:
			frappe.throw(_("Mandatory field - Program"))
		elif not self.academic_year:
			frappe.throw(_("Mandatory field - Academic Year"))
		else:
			condition = 'and academic_term=%(academic_term)s' if self.academic_term else " "
			self.get_students_from = "Program Enrollment"
			condition2 = 'and student_batch_name=%(student_batch)s' if self.student_batch else " "
			students = frappe.db.sql('''select student, student_name, student_batch_name, kiit_polytechnic_roll_no, student_category from `tabProgram Enrollment`
				where program=%(program)s and academic_year=%(academic_year)s {0} {1} and docstatus != 2'''
				.format(condition, condition2), self.as_dict(), as_dict=1)

			student_list = [d.student for d in students]
			if student_list:
				inactive_students = frappe.db.sql('''
					select name as student, title as student_name from `tabStudent` where name in (%s) and enabled = 0''' %
					', '.join(['%s']*len(student_list)), tuple(student_list), as_dict=1)

				for student in students:
					if student.student in [d.student for d in inactive_students]:
						students.remove(student)

		if students:
			return students
		else:
			frappe.throw(_("No students Found"))

	@frappe.whitelist()
	def enroll_students(self):
		total = len(self.students)
		for i, stud in enumerate(self.students):
			frappe.publish_realtime("student_reregistration_tool", dict(progress=[i+1, total]), user=frappe.session.user)
			if stud.student:
				prog_enrollment = frappe.new_doc("Program Enrollment")
				prog_enrollment.student = stud.student
				prog_enrollment.student_name = stud.student_name
				prog_enrollment.student_category = stud.student_category
				prog_enrollment.programs = self.programs
				prog_enrollment.program = self.new_semester
				prog_enrollment.academic_year = self.new_academic_year
				prog_enrollment.academic_term = self.new_academic_term
				prog_enrollment.is_provisional_admission="No"
				prog_enrollment.admission_status="Admitted"
				prog_enrollment.student_batch_name = stud.student_batch_name if stud.student_batch_name else self.new_student_batch
				for course in frappe.get_all("Program Course",{"parent":self.new_semester},["course","course_name"]):
					prog_enrollment.append("courses",{
						"course":course.course,
						"course_name":frappe.db.get_value("Course",{'name':course.course},"course_name")
					})
				for pe in frappe.get_all("Program Enrollment",filters={"student":stud.student},order_by='`creation` DESC',limit=1):
					prog_enrollment.reference_doctype="Program Enrollment"
					prog_enrollment.reference_name=pe.name
				prog_enrollment.save()
				prog_enrollment.submit()
			
		frappe.msgprint(_("{0} Students have been enrolled").format(total))
