import frappe
from kp_edtec.kp_edtec.doctype.user_permission import add_user_permission


def validate(self, method):
    if self.party_type=="Student":
        student_info=frappe.db.get_list("Student",filters={"name":self.party},fields=["sams_portal_id","vidyarthi_portal_id","permanant_registration_number"])
        self.sams_portal_id=student_info[0]["sams_portal_id"]
        self.vidyarthi_portal_id=student_info[0]["vidyarthi_portal_id"]
        self.permanent_registration_number=student_info[0]["permanant_registration_number"]
        student_data_info=frappe.db.get_list("Current Educational Details",filters={"parent":self.party},fields=["academic_year"])
        self.academic_year=student_data_info[0]["academic_year"]

    self.letter_head=""

def after_insert(self, method):
    set_user_permission(self)	


def set_user_permission(self):
    for stu in frappe.get_all("Student",{"name":self.party},['student_email_id']):
        add_user_permission("Payment Entry",self.name, stu.student_email_id, self)

