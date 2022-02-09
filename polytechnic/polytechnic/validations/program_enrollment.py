import frappe

@frappe.whitelist()
def get_students(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
                                Select 
                                        distinct(st.name) as student, st.title as student_name,st.kiit_polytechnic_roll_no,st.vidyarthi_portal_id,st.sams_portal_id 
                                from `tabCurrent Educational Details` ced 
                                left join `tabStudent` st on st.name=ced.parent 
                                where enabled=1 and (st.`{0}` LIKE %(txt)s or st.title  LIKE %(txt)s or 
                                st.kiit_polytechnic_roll_no LIKE %(txt)s or st.vidyarthi_portal_id LIKE %(txt)s or
                                st.sams_portal_id LIKE %(txt)s ) and ced.programs='{1}'
                                    """.format(searchfield,filters.get("programs")),dict(txt="%{}%".format(txt)))    