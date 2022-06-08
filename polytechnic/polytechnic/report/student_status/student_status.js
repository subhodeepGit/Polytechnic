// Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Student Status"] = {
	"filters": [
		{
			"fieldname": "party_type",
			"label": __("Party Type"),
			"fieldtype": "Link",
			"options": "DocType",
			"default": "Student",
			"width": 150,
			"reqd": 1,
			"read_only": 1,
		},
		{
			"fieldname": "party",
			"label": __("Party"),
			"fieldtype": "Link",
			"options": "Student",
			"width": 150,
			"reqd": 1,
		},
		{
			"fieldname": "from",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": 80,
			"reqd": 1,
			"default": dateutil.year_start()
		},
		{
			"fieldname": "to",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": 80,
			"reqd": 1,
			"default": dateutil.year_end()
		},
	]
};
