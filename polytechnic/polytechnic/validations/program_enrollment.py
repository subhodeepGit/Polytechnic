import frappe


def validate(doc,method):
        student=frappe.get_doc("Student",doc.student)
        student.vidyarthi_portal_id=doc.vidyarthi_portal_id
        student.sams_portal_id=doc.sams_portal_id
        student.save()

def on_submit(self,method):
        enable_user(self)

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
                        update_doc.send_welcome_email=1
                        update_doc.save()