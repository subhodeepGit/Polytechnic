# Copyright (c) 2023, SUSTAINABLE OUTREACH AND UNIVERSAL LEADERSHIP LIMITED and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from collections import defaultdict

def execute(filters=None):
    total_report = get_data(filters)
    get_columns_info = get_columns()
    return get_columns_info, total_report


def get_data(filters):
    # print("\n\n\n")
    start_date = filters.get('from')
    end_date = filters.get('to')

    payment_entry = frappe.db.get_all('Payment Entry',filters=[["docstatus", '=', 1],['posting_date', 'between', [start_date, end_date]],["mode_of_payment", "=", "Fees Refundable / Adjustable"]],fields=["name", "paid_amount"])
    # print(payment_entry)

    account=[]
    debit_amount=[]
    credit_amount=[]

    if payment_entry:
        for p in payment_entry:
            gl_entries = frappe.db.get_all('GL Entry',filters=[["docstatus", '=', 1],["is_cancelled", '=', 0],["voucher_no", "=", p["name"]]],
                                        fields=["name", "account", "debit", "credit", "voucher_type", "account_currency", "docstatus"])

            for t in gl_entries:
                if t['debit']!=0:
                    debit_amount.append(t)
                if t['credit']!=0:
                    credit_amount.append(t) 
                account.append(t["account"])
            account=list(set(account))

        # print(account)
        # print(debit_amount)
        # print(credit_amount)

    total_report=[]
    if account:
        for account in account:
            total_debit = 0
            total_credit = 0
            for debit in debit_amount:
                if debit['account'] == account:
                    total_debit += debit['debit']

            for credit in credit_amount:
                if credit['account'] == account:
                    total_credit += credit['credit']
            total_report.append({'account': account,'total_debit': total_debit,'total_credit': total_credit})

        # print(total_report)
    return total_report


def get_columns():
    columns = [
        {
            "label": _("Particulars"),
            "fieldname": "account",
            "fieldtype": "Data",
            "width": 350
        },
        {
            "label": _("Debit Amount"),
            "fieldname": "total_debit",
            "fieldtype": "Currency",
            "width": 180
        },
        {
            "label": _("Credit Amount"),
            "fieldname": "total_credit",
            "fieldtype": "Currency",
            "width": 180
        }
    ]
    return columns