import frappe

def validate(self, method):
    if self.party_type=="Student":
        student_info=frappe.db.get_list("Student",filters={"name":self.party},fields=["sams_portal_id","kiit_polytechnic_roll_no","vidyarthi_portal_id"])
        self.kiit_polytechnic_roll_no=student_info[0]['kiit_polytechnic_roll_no']
        self.sams_portal_id=student_info[0]["sams_portal_id"]
        self.vidyarthi_portal_id=student_info[0]["vidyarthi_portal_id"]
        student_data_info=frappe.db.get_list("Current Educational Details",filters={"parent":self.party},fields=["academic_year"])
        self.academic_year=student_data_info[0]["academic_year"]

    self.letter_head=""

