// Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transport Service', {

	student: function(frm) {
		frm.trigger("set_program_enrollment");
		frm.set_query("programs", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.fees.get_progarms',
				filters: {
					"student":frm.doc.student
				}
			};
		});
		frm.set_query("program", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.fees.get_sem',
				filters: {
					"student":frm.doc.student
				}
			};
		});
		frm.set_query("academic_term", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.fees.get_term',
				filters: {
					"student":frm.doc.student
				}
			};
		});
		frm.set_query("academic_year", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.fees.get_year',
				filters: {
					"student":frm.doc.student
				}
			};
		});
		frm.set_query("student_category", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.fees.get_student_category',
				filters: {
					"student":frm.doc.student
				}
			};
		});
		frm.set_query("student_batch", function() {
			return {
				query: 'kp_edtec.kp_edtec.doctype.fees.get_batch',
				filters: {
					"student":frm.doc.student
				}
			};
		}); 
	},
	set_program_enrollment(frm) {
        frappe.call({
            method: "kp_edtec.kp_edtec.doctype.program_enrollment.get_program_enrollment",
            args: {
                student: frm.doc.student,
            },
            callback: function(r) { 
                if (r.message){
                    frm.set_value("program_enrollment",r.message['name'])
                }
            } 
            
        }); 
    },

});
