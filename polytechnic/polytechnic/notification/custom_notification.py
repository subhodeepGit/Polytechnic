import frappe
from re import L
from frappe.utils.data import format_date
from frappe.utils import get_url_to_form
from frappe.utils import cint, cstr, parse_addr
from stripe import Recipient
from frappe.utils import random_string, get_url

def student_disabled(doc):
    msg ="""<b>Student Admission has been Cancelled</b><br>"""
    msg+="""<b>Student id.</b>  {0}<br>""".format(doc.get('name'))
    msg+="""<b>Student Name</b>  {0}<br>""".format(doc.get('title'))
    msg+="""<b>Student Email Id</b>  {0}<br>""".format(doc.get('student_email_id'))
    msg+="""<b>Roll no.</b>  {0}<br>""".format(doc.get('roll_no'))
    msg+="""<b>SAMS Portal ID</b>  {0}<br>""".format(doc.get('sams_portal_id'))
    msg+="""<b>Vidyarthi Portal ID</b>  {0}<br>""".format(doc.get('vidyarthi_portal_id'))
    msg+="""<b>Registration Number</b>  {0}<br>""".format(doc.get('permanant_registration_number'))
    recipients= frappe.get_all("User",filters=[["role", "In", ("Accounts Manager","Accounts User","Education Administrator")]],fields=["email"])
    email=[t["email"] for t in recipients]
    send_mail(email,'Student Disabled',msg)

def url_link(doc):
    msg="""<p>Your Program Enrollment is completed. Now you can able to login your profile through this link :- <b>{0}</b></p><br>""".format(frappe.utils.get_url())
    msg+="""<b>If you not completed your registration then go to this link and create your new password :- </b> {0}<br><br>""".format(doc.get('link'))
    msg+="""<b>---------------------Student Details---------------------</b><br>"""
    msg+="""<b>Student Name:</b>  {0}<br>""".format(doc.get('student_name'))
    msg+="""<b>Program:</b>  {0}<br>""".format(doc.get('programs'))
    msg+="""<b>Semester:</b>  {0}<br>""".format(doc.get('program'))
    msg+="""<b>Academic Year:</b>  {0}<br>""".format(doc.get('academic_year') or '-')
    msg+="""<b>Academic Term:</b> {0}<br>""".format(doc.get('academic_term') or '-')
    send_mail(frappe.db.get_value("Student",doc.get('student'),"student_email_id"),'Application status',msg)
    
def send_mail(recipients,subject,message):
    if has_default_email_acc():
        frappe.sendmail(recipients=recipients,subject=subject,message=message,with_container=True)

def has_default_email_acc():
    for d in frappe.get_all("Email Account", {"default_outgoing":1}):
       return "true"
    return ""
