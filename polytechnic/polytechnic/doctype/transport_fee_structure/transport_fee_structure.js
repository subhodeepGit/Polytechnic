// Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transport Fee Structure', {
	__newname: function(frm) {
			frm.set_value('fee_description', frm.doc.__newname);
	},
});
