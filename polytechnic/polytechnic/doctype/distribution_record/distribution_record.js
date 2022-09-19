// Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt

frappe.ui.form.on('Distribution Record', {
	refresh: function(frm) {
		frm.set_query("material__accessory_name","list", function(_doc, cdt, cdn) {
            var d = locals[cdt][cdn];
            return {
				filters: [
					["Master Distribution Record", "enabled", "=", 1],
				]
            };
        });
	}
});

frappe.ui.form.on("Distribution Record", "student", function (frm) {
	if (frm.doc.student == undefined || frm.doc.student == "" || frm.doc.student == null){

	}else{
	frappe.model.with_doc("Student", frm.doc.student, function () {
		frm.clear_table("current_education_fetch");
		var tabletransfer = frappe.model.get_doc("Student", frm.doc.student);
		cur_frm.doc.current_education = "";
		cur_frm.refresh_field("current_education");
		$.each(tabletransfer.current_education, function (index, row) {
			var d = frappe.model.add_child(cur_frm.doc, "Current Educational Details", "current_education_fetch");
			d.programs = row.programs;
			d.semesters = row.semesters;
			d.academic_year = row.academic_year;
			d.academic_term = row.academic_term;
			cur_frm.refresh_field("current_education_fetch");
		});
	});
}

});

