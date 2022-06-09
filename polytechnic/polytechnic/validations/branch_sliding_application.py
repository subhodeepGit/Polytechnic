from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today,getdate
from kp_edtec.ed_tec.utils import get_courses_by_semester

@frappe.whitelist()
def enroll_student(source_name):
    doc=frappe.get_doc("Branch Sliding Application",source_name)
    student=frappe.get_doc("Student",doc.student)
    program_enrollment = frappe.new_doc("Program Enrollment")
    program_enrollment.student = student.name
    program_enrollment.student_category = student.student_category
    program_enrollment.student_name = student.title
    program_enrollment.reference_doctype="Branch Sliding Application"
    program_enrollment.reference_name=source_name
    program_enrollment.programs = doc.sliding_in_program
    program_enrollment.program_grade=frappe.db.get_value("Programs",{"name":doc.sliding_in_program},"program_grade")
    program_enrollment.academic_year=doc.academic_year
    program_enrollment.program = doc.sliding_in_semester
    program_enrollment.sams_portal_id=student.sams_portal_id
    program_enrollment.vidyarthi_portal_id=student.vidyarthi_portal_id
    for cr in get_courses_by_semester(doc.sliding_in_semester):
        program_enrollment.append("courses",{
            "course":cr,
            "course_name":frappe.db.get_value("Course",{"name":cr},"course_name")
        })
    if get_academic_events(doc.sliding_in_program,doc.sliding_in_semester, doc.academic_year):
        for event in get_academic_events(doc.sliding_in_program,doc.sliding_in_semester, doc.academic_year):
            program_enrollment.append("academic_events_table",{
                "academic_events" : event.academic_events,
                "start_date" : event.start_date,
                "end_date" : event.end_date,
                "duration" : event.duration
            })
    if doc.branch_sliding_declaration:
        for seat in [s.available_seats for s in frappe.get_all("Branch Sliding Item",{"parent":doc.branch_sliding_declaration},'available_seats')]:
            program_enrollment.available_seats = seat
    return program_enrollment
    
def get_academic_events(programs,semester,academic_year):
    for d in [c.name for c in frappe.get_all("Academic Calendar Template",{"programs":programs,"program":semester, 'academic_year':academic_year}, 'name')]:
        return frappe.get_all("Academic Events Table",{'parent':d},['academic_events','start_date','end_date','duration'])

def date_validation(doc):
    if doc.branch_sliding_declaration:
        declaration=frappe.get_doc("Branch sliding Declaration",doc.branch_sliding_declaration)
        if (getdate(declaration.application_end_date)<getdate(doc.application_date) and getdate(declaration.application_start_date)<getdate(doc.application_date)) or (getdate(declaration.application_end_date)>getdate(doc.application_date) and getdate(declaration.application_start_date)>getdate(doc.application_date)):
            frappe.throw("Application Date Should be in Between Start and End Date of Declaration")
