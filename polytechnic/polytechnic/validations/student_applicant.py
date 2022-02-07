import frappe

@frappe.whitelist()
def enroll_student(source_name):
    from ed_tec.ed_tec.doctype.student_exchange_applicant.student_exchange_applicant import get_academic_calender_table
    from ed_tec.ed_tec.doctype.semesters.semesters import get_courses
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
        program_enrollment.sams_portal_id=st_applicant.sams_portal_id
        program_enrollment.vidyarthi_portal_id=st_applicant.vidyarthi_portal_id
        program_enrollment.kiit_polytechnic_roll_no=st_applicant.kiit_polytechnic_roll_number

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