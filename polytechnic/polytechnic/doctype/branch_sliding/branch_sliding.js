// Copyright (c) 2023, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt

frappe.ui.form.on('Branch Sliding', {
	onload: function(frm) {
		frm.set_df_property('students_details', 'cannot_add_rows', true);
		frm.set_query("academic_term", function() {
			return {
				filters: {
					"academic_year":frm.doc.academic_year
				}
			};
		});
		frm.set_query("semester", function() {
			return {
				filters: {
					"programs":frm.doc.programs
				}
			};
		});
		frm.set_query("programs", function() {
			return {
				filters: {
					"program_grade":frm.doc.program_grade
				}
			};
		});
		frm.set_query("sliding_in_program", function () {
			return {
				filters: [
					["name", "not in", frm.doc.programs],
				]
			}
		});
		frm.set_query("sliding_in_semester", function () {
			return {
				filters: [
					["name", "not in", frm.doc.semester],
					["programs", "=", frm.doc.sliding_in_program],
				]
			}
		});
	},

	academic_year: function(frm){
		frm.set_value("academic_term","")
	},

	program_grade: function(frm){
		frm.set_value("programs","")
	},

	programs: function(frm){
		frm.set_value("semester","")
	},

	sliding_in_program: function(frm){
		frm.set_value("sliding_in_semester","")
	},

	academic_term: function(frm){
		frm.set_value("programs","")
	},

	get_students: function(frm){
		frm.clear_table("students_details");
		frappe.call({
			method: 'polytechnic.polytechnic.doctype.branch_sliding.branch_sliding.get_students',
			args:{
				programs: frm.doc.programs,
				academic_term: frm.doc.academic_term,
                class_data: frm.doc.class,
				semester:frm.doc.semester
			},
			callback: function(r) {
				(r.message).forEach(element => {
					var row = frm.add_child("students_details")
					row.program_enrollment=element.name
					row.student=element.student
					row.student_name=element.student_name
                    row.roll_number = element.roll_no
                    row.permanent_registration_number = element.permanant_registration_number
				});
				frm.refresh_field("students_details")
				
			}
		})
	},
});
