import frappe
from frappe.model.document import Document
from polytechnic.polytechnic.notification.custom_notification import student_disabled

def validate(self, method):
    dob = self.date_of_birth
    if dob:
        try:
            from datetime import date,datetime 
            mydate = datetime.strptime(str(dob),'%Y-%m-%d')
            words_date=mydate.strftime("%A,%d %B, %Y")
            self.dob_in_words = words_date
        except:
            mydate = datetime.strptime(str(dob),'%Y-%m-%d %H:%M:%S')
            words_date=mydate.strftime("%A,%d %B, %Y")
            self.dob_in_words = words_date


def on_change(self, method):
    student_disabled_notification(self)
    user_update(self)


def before_save(self, method):
    student = frappe.get_all("Student",{"name":self.name},{"image"})
    if student:
        if self.image!=student[0]["image"]:
            identity_card_photo(self)
            transport_service_photo(self)

    student = frappe.get_all("Student",{"name":self.name},{"roll_no"})
    if student:
        if self.roll_no!=student[0]["roll_no"]:
            roll(self)
            payment(self)
            refund(self) 
            transport_roll_update(self)

def identity_card_photo(self):
    photo = frappe.db.get_all("Identity Card",filters=[["student","=",self.name]],fields=["name"])
    if photo:
        if len(photo)==1:
            frappe.db.sql(""" update `tabIdentity Card` set passport_photo="%s" where name = "%s" """%(self.image,photo[0]["name"]))
        else:
            photo_info=tuple([t["name"] for t in photo])
            frappe.db.sql(""" update `tabIdentity Card` set passport_photo="%s" where name in %s"""%(self.image,photo_info))
        
def transport_service_photo(self):
    photo = frappe.db.get_all("Transport Service",filters=[["student","=",self.name]],fields=["name"])
    if photo:
        if len(photo)==1:
            frappe.db.sql(""" update `tabTransport Service` set image="%s" where name = "%s" """%(self.image,photo[0]["name"]))
        else:
            photo_info=tuple([t["name"] for t in photo])
            frappe.db.sql(""" update `tabTransport Service` set image="%s" where name in %s"""%(self.image,photo_info))

def after_insert(self, method):
    sten=frappe.db.get_all("User", {'email':self.student_email_id},['name','enabled'])
    status=sten[0]['enabled']
    stu_name = sten[0]['name']
    if status == 1:
        update_doc = frappe.get_doc("User",stu_name)
        update_doc.enabled=0
        update_doc.save()

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
        if len(fee)==1:
            frappe.db.sql(""" update `tabFees` set roll_no="%s" where name = "%s" """%(self.roll_no,fee[0]["name"]))
        else:
            fees_info=tuple([t["name"] for t in fee])
            frappe.db.sql(""" update `tabFees` set roll_no="%s" where name in %s"""%(self.roll_no,fees_info))

def payment(self):
    payment = frappe.db.get_all("Payment Entry",filters=[["party","=",self.name]],fields=["name"])
    if payment:
        if len(payment)==1:
            frappe.db.sql(""" update `tabPayment Entry` set roll_no="%s" where name = "%s" """%(self.roll_no,payment[0]["name"]))
        else:
            payment_info=tuple([t["name"] for t in payment])
            frappe.db.sql(""" update `tabPayment Entry` set roll_no="%s" where name in %s"""%(self.roll_no,payment_info))

def refund(self):
    refund = frappe.db.get_all("Payment Refund",filters=[["party","=",self.name]],fields=["name"])
    if refund:
        if len(refund)==1:
            frappe.db.sql(""" update `tabPayment Refund` set roll_no="%s" where name = "%s" """%(self.roll_no,refund[0]["name"]))
        else:
            refund_info = tuple([t["name"] for t in refund])   
            frappe.db.sql(""" update `tabPayment Refund` set roll_no="%s" where name in %s"""%(self.roll_no,refund_info))


def transport_roll_update(self):
    roll_no = frappe.db.get_all("Student",filters=[["student","=",self.name]],fields=["name"])
    if roll_no:
        if len(roll_no)==1:
            frappe.db.sql(""" update `tabTransport Service` set roll_no="%s" where name = "%s" """%(self.roll_no,roll_no[0]["name"]))
        else:
           roll_no_info=tuple([t["name"] for t in roll_no])
           frappe.db.sql(""" update `tabTransport Service` set roll_no="%s" where name in %s"""%(self.roll_no,roll_no_info))            