from __future__ import unicode_literals, print_function

import frappe
from frappe.utils.password import update_password as _update_password, check_password, get_password_reset_limit
from frappe.utils import random_string, get_url
from polytechnic.polytechnic.notification.custom_notification import url_link

def validate(doc,method):
        student=frappe.get_doc("Student",doc.student)
        student.vidyarthi_portal_id=doc.vidyarthi_portal_id
        student.sams_portal_id=doc.sams_portal_id
        student.save()

# def before_submit(self,method):
#         password = frappe.get_all("Program Enrollment",{"student":self.student,"docstatus":1},{"student"})
#         if password:
#                 if len(password)==1:
#                         reset_password(self)
        
def on_submit(self,method):
        enable_user(self)
        email = frappe.get_all("Program Enrollment",{"student":self.student,"docstatus":1},{"student"})
        if email:
                if len(email)==1:
                        reset_password(self)
                        url_link(self)

@frappe.whitelist()
def get_roll(student):
        id_student=frappe.get_all("Student",filters=[['name','=',student]],fields=['name','vidyarthi_portal_id','permanant_registration_number','sams_portal_id'])
        # branch_sliding=frappe.get_all("")
        return id_student[0]


@frappe.whitelist()
def get_students(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
                                Select 
                                        distinct(st.name) as student, st.title as student_name,st.vidyarthi_portal_id,st.sams_portal_id 
                                from `tabCurrent Educational Details` ced 
                                left join `tabStudent` st on st.name=ced.parent 
                                where enabled=1 and (st.`{0}` LIKE %(txt)s or st.title  LIKE %(txt)s or 
                                st.vidyarthi_portal_id LIKE %(txt)s or
                                st.sams_portal_id LIKE %(txt)s ) and ced.programs='{1}'""".format(searchfield,filters.get("programs")),dict(txt="%{}%".format(txt)))  

def enable_user(self):
        stu_info =  frappe.get_all("Student",{"name":self.student},["student_email_id"])
        if stu_info:
                student_email_id=stu_info[0]['student_email_id']
                sten=frappe.db.get_all("User", {'email':student_email_id},['name','enabled'])
                status=sten[0]['enabled']
                stu_name = sten[0]['name']
                if status == 0:
                        update_doc = frappe.get_doc("User",stu_name)
                        update_doc.enabled=1
                        update_doc.save()


def reset_password(self):
                key = random_string(32)
                self.set("reset_password_key", key)
                student =  frappe.get_all("Student",{"name":self.student},["student_email_id"])
                if student:
                        student_email_id=student[0]['student_email_id']
                        user = frappe.db.get_all("User", {'email':student_email_id},['name'])
                        if user:
                                if len(user)==1:
                                        frappe.db.sql(""" update `tabUser` set reset_password_key="%s" where name = "%s" """%(self.reset_password_key,user[0]["name"]))

                url = "/update-password?key=" + key

                link = get_url(url)
                self.set("link", link)

                return link