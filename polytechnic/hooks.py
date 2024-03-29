from . import __version__ as app_version

app_name = "polytechnic"
app_title = "Polytechnic"
app_publisher = "SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED"
app_description = "SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "soul@soulunileaders.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/polytechnic/css/polytechnic.css"
# app_include_js = "/assets/polytechnic/js/polytechnic.js"
app_include_js = [
                    "/assets/kp_edtec/core_js/program_enrollment.js"
                ]

# include js, css files in header of web template
# web_include_css = "/assets/polytechnic/css/polytechnic.css"
# web_include_js = "/assets/polytechnic/js/polytechnic.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "polytechnic/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Program Enrollment":"public/core_js/program_enrollment.js",
}
doctype_js = {
	"Student" : "public/core_js/student.js",
}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "polytechnic.install.before_install"
# after_install = "polytechnic.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "polytechnic.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Identity Card Tool":"polytechnic.polytechnic.doctype.identity_card_tool.IdentityCardTool",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Payment Entry": {
		"validate": "polytechnic.polytechnic.validations.payment_entry.validate",
		"after_insert": "polytechnic.polytechnic.validations.payment_entry.after_insert"
	},
    "Program Enrollment": {
		"validate": "polytechnic.polytechnic.validations.program_enrollment.validate",
		"on_submit": "polytechnic.polytechnic.validations.program_enrollment.on_submit",
		"before_submit": "polytechnic.polytechnic.validations.program_enrollment.before_submit",
	},
	"Student": {
		"validate": "polytechnic.polytechnic.validations.student.validate",
		"on_change": "polytechnic.polytechnic.validations.student.on_change",
		"before_save": "polytechnic.polytechnic.validations.student.before_save",
		"after_insert": "polytechnic.polytechnic.validations.student.after_insert",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"polytechnic.tasks.all"
# 	],
# 	"daily": [
# 		"polytechnic.tasks.daily"
# 	],
# 	"hourly": [
# 		"polytechnic.tasks.hourly"
# 	],
# 	"weekly": [
# 		"polytechnic.tasks.weekly"
# 	]
# 	"monthly": [
# 		"polytechnic.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "polytechnic.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	# "frappe.desk.doctype.event.event.get_events": "polytechnic.event.get_events"
	# "kp_edtec.kp_edtec.doctype.program_enrollment.get_students":"polytechnic.polytechnic.validations.program_enrollment.get_students",
	"kp_edtec.kp_edtec.doctype.student_applicant.enroll_student": "polytechnic.polytechnic.validations.student_applicant.enroll_student",
	"kp_edtec.kp_edtec.doctype.branch_sliding_application.branch_sliding_application.enroll_student": "polytechnic.polytechnic.validations.branch_sliding_application.enroll_student",
	"kp_edtec.kp_edtec.doctype.identity_card_tool.identity_card_tool.get_students":"polytechnic.polytechnic.doctype.identity_card_tool.get_students",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "polytechnic.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"polytechnic.auth.validate"
# ]


# fixtures = [
# 	{"dt": "Custom DocPerm", "filters": [
# 		[
# 			"parent", "not in", [
# 				"DocType"
# 			]
# 		]
# 	]},
#     {"dt": "Role"},
#     {"dt": "Role Profile"},
#     {"dt": "Module Profile"},
# ]
after_migrate = [
        # 'polytechnic.patches.migrate_patch.add_roles',
        'polytechnic.patches.migrate_patch.set_custom_role_permission',
]
override_doctype_dashboards = {
    "Student": "polytechnic.polytechnic.dashboard.student_dashboard.get_data",	
}
