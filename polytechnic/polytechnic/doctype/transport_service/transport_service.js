// Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transport Service', {
	refresh: function(frm){
		if(frappe.user.has_role(["Student"]) && !frappe.user.has_role(["Administrator","Education Administrator"]) && frm.doc.docstatus != 1){
			frm.set_df_property('statusf', 'read_only', 1)
		}
	},
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
	setup: function(frm) {
		var today = new Date();
		var dd = String(today.getDate()).padStart(2, '0');
		var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
		var yyyy = today.getFullYear();
		today = yyyy + '-' + mm + '-' + dd;
		frm.set_query("transport_fee_structure", function () {
			return {
				filters: [
					["Transport Fee Structure", "end_date", ">", today],
				]
			}
		});
	},

	location_map: function(frm) {
		let mapdata = JSON.parse(cur_frm.doc.location_map).features[0];
		if (mapdata && mapdata.geometry.type=='Point') {
			let lat = mapdata.geometry.coordinates[1];
			let lon = mapdata.geometry.coordinates[0];
			frappe.call({
				type: "GET",
				url: `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`,
				callback: function(r) {
					frm.set_value('geo_location_name', r.display_name);
				}
			})
		}
	},

	transport_fee_structure: function(frm){
		frappe.call({
            method: "polytechnic.polytechnic.doctype.transport_service.transport_service.get_end_date",
            args: {
                transport_fee_structure: frm.doc.transport_fee_structure,
            },
            callback: function(r) { 
                if (r.message){
                    frm.set_value("due_date",r.message)
                }
            } 
            
        }); 
	}
});
