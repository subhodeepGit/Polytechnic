// Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["GL Report"] = {
	"filters": [
		{
			"fieldname": "account",
			"label": __("Account"),
			"fieldtype": "Data",
			"width": 100,
			"reqd": 0,
		},
		{
			"fieldname": "fee_head",
			"label": __("FEES HEAD"),
			"fieldtype": "Link",
			"options": "Account",
			"width": 100,
			"reqd": 0,
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
		// {
		// 	"fieldname": "status",
		// 	"label": __("Status"),
		// 	"fieldtype": "Select",
		// 	"options": ['Sale', 'Rent', 'Lease'],
		// 	"width": 100,
		// 	"reqd": 0,
		// 	"default": "",
		// },
	]
};
