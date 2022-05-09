import frappe


def validate(doc,method):
        student=frappe.get_doc("Student",doc.student)
        student.vidyarthi_portal_id=doc.vidyarthi_portal_id
        student.save()


@frappe.whitelist()
def get_roll(student):
        id_student=frappe.get_all("Student",filters=[['name','=',student]],fields=['name','vidyarthi_portal_id','roll_no','permanant_registration_number'])
        # branch_sliding=frappe.get_all("")
        return id_student[0]


@frappe.whitelist()
def get_students(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
                                Select 
                                        distinct(st.name) as student, st.title as student_name,st.roll_no,st.vidyarthi_portal_id,st.sams_portal_id 
                                from `tabCurrent Educational Details` ced 
                                left join `tabStudent` st on st.name=ced.parent 
                                where enabled=1 and (st.`{0}` LIKE %(txt)s or st.title  LIKE %(txt)s or 
                                st.roll_no LIKE %(txt)s or st.vidyarthi_portal_id LIKE %(txt)s or
                                st.sams_portal_id LIKE %(txt)s ) and ced.programs='{1}'""".format(searchfield,filters.get("programs")),dict(txt="%{}%".format(txt)))  
