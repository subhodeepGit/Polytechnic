import frappe
from frappe.model.document import Document

def validate(self, method):
    dob = self.date_of_birth
    if dob:
        from datetime import date,datetime 
        mydate = datetime.strptime(str(dob),'%Y-%m-%d')
        words_date=mydate.strftime("%A,%d %B, %Y")
        self.dob_in_words = words_date





def on_change(self, method):
    user_info=frappe.get_list("User",{"location":self.name},["name","location","username"])
    if user_info:
        if user_info[0]["name"]!=self.student_email_id:
            old_user=user_info[0]["name"]
            old_user_name=user_info[0]["username"]
            # frappe.rename_doc(“Your Doctype”, “old_name”, “new_name”)
            frappe.rename_doc("User", old_user, self.student_email_id)
            frappe.db.commit()
            user=frappe.get_doc("User",self.student_email_id)
            user.email=self.student_email_id
            user.username=old_user_name
            user.save()

    else:
        frappe.db.sql(""" update `tabUser` set location="%s" where name="%s" """%(self.name,self.student_email_id))