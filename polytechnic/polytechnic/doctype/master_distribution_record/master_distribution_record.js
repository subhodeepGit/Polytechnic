// Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt

frappe.ui.form.on('Master Distribution Record', {
	// refresh: function(frm) {

	// }
	__newname: function(frm) {
		frm.set_value("material__accessory_name", frm.doc.__newname)
	}
});
