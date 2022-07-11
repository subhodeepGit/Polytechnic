// Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["OUTSTANDING DUES STUDENT WISE"] = {
	"filters": [
		{
			"fieldname": "programs",
			"label": __("Programs"),
			"fieldtype": "Link",
			"options": "Programs",
			"width": 150,
			"reqd": 1,
		},
		{
			"fieldname": "semester",
			"label": __("Semester"),
			"fieldtype": "MultiSelectList",
			"options": "Program",
			"width": 150,
			"reqd": 1,
			get_data: function(txt) {
				return frappe.db.get_link_options('Program', txt, {
					programs: frappe.query_report.get_filter_value("programs")
				});
			}
		},
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
