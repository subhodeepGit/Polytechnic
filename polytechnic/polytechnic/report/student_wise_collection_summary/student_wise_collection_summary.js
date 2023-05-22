// Copyright (c) 2023, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt
/* eslint-disable */


frappe.query_reports["Student Wise Collection Summary"] = {
	"filters": [
		// {
		// 	"fieldname": "mode_of_payment",
		// 	"label": __("Mode of Payment"),
		// 	"fieldtype": "MultiSelectList",
		// 	"options": "Mode of Payment",
		// 	"width": 150,
		// 	"reqd": 1,
		// 	get_data: function(txt) {
		// 		return frappe.db.get_link_options('Mode of Payment')
		// 	}
		// },
		{
			"fieldname": "start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"width": 80,
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"width": 80,
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
	]
};
