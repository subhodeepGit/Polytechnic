import frappe

@frappe.whitelist()
def enroll_student(source_name):
    from kp_edtec.ed_tec.doctype.student_exchange_applicant.student_exchange_applicant import get_academic_calender_table
    from kp_edtec.ed_tec.doctype.semesters.semesters import get_courses
    st_applicant=frappe.get_doc("Student Applicant", source_name)
    for student in frappe.get_all("Student",{"student_applicant":source_name},['name','student_category','title']):
        program_enrollment = frappe.new_doc("Program Enrollment")
        program_enrollment.student = student.name
        program_enrollment.student_category = student.student_category
        program_enrollment.student_name = student.title
        program_enrollment.programs = st_applicant.programs_
        program_enrollment.program = st_applicant.program
        program_enrollment.academic_year=st_applicant.academic_year
        program_enrollment.academic_term=st_applicant.academic_term
        program_enrollment.reference_doctype="Student Applicant"
        program_enrollment.reference_name=source_name
        program_enrollment.program_grade = st_applicant.program_grade
        program_enrollment.gender=st_applicant.gender
        program_enrollment.physically_disabled=st_applicant.physically_disabled
        program_enrollment.award_winner=st_applicant.award_winner
        program_enrollment.boarding_student=st_applicant.hostel_required
        program_enrollment.sams_portal_id=st_applicant.sams_portal_id
        program_enrollment.vidyarthi_portal_id=student.vidyarthi_portal_id
        # program_enrollment.kiit_polytechnic_roll_no=st_applicant.kiit_polytechnic_roll_number
        
        for d in st_applicant.get("disable_type"):
            program_enrollment.append("disable_type",{
                "disability_type":d.disability_type,
                "percentage_of_disability":d.percentage_of_disability
            })
        
        for d in st_applicant.get("awards_list"):
            program_enrollment.append("awards_list",{
                "awards":d.awards,
                "won_in_year":d.won_in_year
            })

        if st_applicant.program:
            for crs in get_courses(st_applicant.program):
                program_enrollment.append("courses",crs)
        if st_applicant.student_admission:
            st_admission=frappe.get_doc("Student Admission",st_applicant.student_admission)
            if st_admission.admission_fees=="YES":
                for fs in st_admission.get("admission_fee_structure"):
                    if fs.student_category==student.student_category:
                        program_enrollment.append("fee_structure_item",{
                            "student_category":student.student_category,
                            "fee_structure":fs.fee_structure,
                            "amount":fs.amount,
                            "due_date":fs.due_date
                        })
                    
            if st_admission.academic_calendar:
                for d in get_academic_calender_table(st_admission.academic_calendar):
                    program_enrollment.append("academic_events_table",d)
        return program_enrollment



# @frappe.whitelist()
# def get_students(doctype, txt, searchfield, start, page_len, filters):
#     print("\n\n\n\n\n\n")
#     print("my hooks")
#     return frappe.db.sql("""
#                                 Select 
#                                         distinct(st.name) as student, st.title as student_name,st.kiit_polytechnic_roll_no,st.vidyarthi_portal_id,st.sams_portal_id 
#                                 from `tabCurrent Educational Details` ced 
#                                 left join `tabStudent` st on st.name=ced.parent 
#                                 where enabled=1 and (st.`{0}` LIKE %(txt)s or st.title  LIKE %(txt)s or 
#                                 st.kiit_polytechnic_roll_no LIKE %(txt)s or st.vidyarthi_portal_id LIKE %(txt)s or
#                                 st.sams_portal_id LIKE %(txt)s ) and ced.programs='{1}'
#                                     """.format(searchfield,filters.get("programs")),dict(txt="%{}%".format(txt)))   

@frappe.whitelist()
def get_students(doctype, txt, searchfield, start, page_len, filters):
    print("\n\n\n\n\n\n")
    print("my hooks")
    return frappe.db.sql("""
                                Select 
                                        distinct(st.name) as student, st.title as student_name,st.vidyarthi_portal_id,st.sams_portal_id 
                                from `tabCurrent Educational Details` ced 
                                left join `tabStudent` st on st.name=ced.parent 
                                where enabled=1 and (st.`{0}` LIKE %(txt)s or st.title  LIKE %(txt)s or 
                                st.vidyarthi_portal_id LIKE %(txt)s or
                                st.sams_portal_id LIKE %(txt)s ) and ced.programs='{1}'
                                    """.format(searchfield,filters.get("programs")),dict(txt="%{}%".format(txt)))  










