// Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["STUDENT WISE EXEMPTION SUMMARY"] = {
	"filters": [
		{
			"fieldname": "student_batch",
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
			"reqd": 1,
		},
		{
			"fieldname": "posting_date1",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"width": 80,
			"reqd": 1,
			// "default": dateutil.year_start()
		},
		{
			"fieldname": "posting_date2",
			"label": __("End Date"),
			"fieldtype": "Date",
			"width": 80,
			// "reqd": 1,
			// "default": dateutil.year_end()
		},
	]
};
