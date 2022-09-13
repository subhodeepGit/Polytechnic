frappe.ui.form.on('Student', {
    onload:function(frm) {
		if(frappe.user.has_role(["Fee Waiver","Transport User"]) && !frappe.user.has_role(["Administrator"])){
  			frm.remove_custom_button('Accounting Ledger');
        }
	}
}


);