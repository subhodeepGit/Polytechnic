import frappe
from frappe.model.document import Document
from polytechnic.polytechnic.notification.custom_notification import student_disabled

def validate(self, method):
    dob = self.date_of_birth
    if dob:
        from datetime import date,datetime 
        mydate = datetime.strptime(str(dob),'%Y-%m-%d')
        words_date=mydate.strftime("%A,%d %B, %Y")
        self.dob_in_words = words_date


def on_change(self, method):
    student_disabled_notification(self)
    user_update(self)


def before_save(self, method):
    student = frappe.get_all("Student",{"name":self.name},{"roll_no"})
    if self.roll_no!=student[0]["roll_no"]:
        roll(self)
        payment(self)
        refund(self)


def student_disabled_notification(self):
    if self.enabled==0:
        student_disabled(self)

def user_update(self):
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

def roll(self):
    fee = frappe.db.get_all("Fees",filters=[["student","=",self.name]],fields=["name"])
    if fee:
            fees_info=tuple([t["name"] for t in fee])
            frappe.db.sql(""" update `tabFees` set roll_no="%s" where name in %s"""%(self.roll_no,fees_info))
    else:
        return

def payment(self):
    payment = frappe.db.get_all("Payment Entry",filters=[["party","=",self.name]],fields=["name"])
    if payment:
        payment_info=tuple([t["name"] for t in payment])
        frappe.db.sql(""" update `tabPayment Entry` set roll_no="%s" where name in %s"""%(self.roll_no,payment_info))
    else:
        return

def refund(self):
    refund = frappe.db.get_all("Payment Refund",filters=[["party","=",self.name]],fields=["name"])
    if refund:
        refund_info = tuple([t["name"] for t in refund])
        frappe.db.sql(""" update `tabPayment Refund` set roll_no="%s" where name in %s"""%(self.roll_no,refund_info))
    else:
        return