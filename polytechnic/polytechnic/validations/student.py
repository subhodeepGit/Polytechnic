import frappe
from frappe.model.document import Document

def validate(self, method):
    dob = self.date_of_birth
    if dob:
        from datetime import date,datetime 
        mydate = datetime.strptime(str(dob),'%Y-%m-%d')
        words_date=mydate.strftime("%A,%d %B, %Y")
        self.dob_in_words = words_date