import frappe
from re import L
from frappe.utils.data import format_date
from frappe.utils import get_url_to_form
from frappe.utils import cint, cstr, parse_addr
from stripe import Recipient

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

def send_mail(recipients,subject,message):
    if has_default_email_acc():
        frappe.sendmail(recipients=recipients,subject=subject,message=message,with_container=True)

def has_default_email_acc():
    for d in frappe.get_all("Email Account", {"default_outgoing":1}):
       return "true"
    return ""
