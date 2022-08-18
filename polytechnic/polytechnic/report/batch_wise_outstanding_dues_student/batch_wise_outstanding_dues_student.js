// Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["BATCH WISE OUTSTANDING DUES STUDENT"] = {
	"filters": [
		{
			"fieldname": "batch",
			"label": __("Student Batch Name"),
			"fieldtype": "Link",
			"options": "Student Batch Name",
			"width": 150,
			"reqd": 1,
		},
		{
			"fieldname": "programs",
			"label": __("Programs"),
			"fieldtype": "Link",
			"options": "Programs",
			"width": 150,
			// "reqd": 1,
		},
		{
			"fieldname": "gender",
			"label": __("Gender"),
			"fieldtype": "Link",
			"options": "Gender",
			"width": 150,
			// "reqd": 1,
		},
		// {
		// 	"fieldname": "semester",
		// 	"label": __("Semester"),
		// 	"fieldtype": "MultiSelectList",
		// 	"options": "Program",
		// 	"width": 150,
		// 	"reqd": 1,
		// 	get_data: function(txt) {
		// 		return frappe.db.get_link_options('Program', txt, {
		// 			programs: frappe.query_report.get_filter_value("programs")
		// 		});
		// 	}
		// },
		// {
		// 	"fieldname": "academic_term",
		// 	"label": __("Academic Term"),
		// 	"fieldtype": "Link",
		// 	"options": "Academic Term",
		// 	"width": 150,
		// 	"reqd": 1,
		// },
		{
			"fieldname": "start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"width": 80,
			"reqd": 1,
			"default": dateutil.year_start()
		},
		{
			"fieldname": "end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"width": 80,
			"reqd": 1,
			"default": dateutil.year_end()
		},
	]
};
