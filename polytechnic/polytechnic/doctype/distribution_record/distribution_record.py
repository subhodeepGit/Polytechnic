# Copyright (c) 2022, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime

class DistributionRecord(Document):
	def validate(self):
		student_check = frappe.get_all("Distribution Record",{"student": self.student,'docstatus':1},['name'])
		stu_dis_list=[]
		acc_year_list=[]
		for t in student_check:
			list_dis=frappe.get_all("Distribution Records List",{"parent":t['name']},
						["name","parent","material__accessory_name","type_of_distribution","quantity","modified"]) 
			for j in list_dis:
				stu_dis_list.append(j)

			acc_year=frappe.get_all("Current Educational Details",{"parent":t['name']},["name","parent","academic_year"])
			for j in acc_year:
				acc_year_list.append(j)

		for t in self.get("list"):
			if t.type_of_distribution == "One Time":
				for i in stu_dis_list:
					if i['material__accessory_name']==t.material__accessory_name:
						frappe.throw("Material is already distributed dated "+str(i["modified"]))
			elif t.type_of_distribution == "Multiple Times":
				acc_year_date=""
				for i in self.get("current_education_fetch"):
					acc_year_date=i.academic_year

				for i in stu_dis_list:
					for j in acc_year_list:
						if i["parent"]==j["parent"]:
							if t.material__accessory_name==i["material__accessory_name"] and acc_year_date==j['academic_year']:
								frappe.throw("Material is already distributed for the Academic Year dated "+str(i["modified"]))
						




		# for t in self.get("list"):
		# 	print(t)
		# 	if t.type_of_distribution == "One Time":
		# 		print("one time")
		# 		if student_check:
		# 			print("student_one_time")
		# 			print(student_check[0]["name"])
		# 			# if frappe.get_all("Distribution Records List",{"parent": frappe.get_all("Distribution Record",{"student": self.student})}):
		# 			# 	print("one_time_item present")
		# 	elif t.type_of_distribution == "Multiple Times":
		# 		print("multiple time")
