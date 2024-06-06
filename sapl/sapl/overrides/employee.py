import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_employee(source_name, target_doc=None):
    doc = frappe.get_doc("Employee Onboarding", source_name)
    doc.validate_employee_creation()

    def set_missing_values(source, target):
        target.personal_email = frappe.db.get_value("Job Applicant", source.job_applicant, "email_id")
        target.status = "Active"

    doc = get_mapped_doc(
        "Employee Onboarding",
        source_name,
        {
            "Employee Onboarding": {
                "doctype": "Employee",
                "field_map": {
                    "first_name": "employee_name",
                    "employee_grade": "grade",
                },
            }
        },
        target_doc,
        set_missing_values,
    )
    onboarding_doc = frappe.get_doc("Employee Onboarding", source_name)
    doc.first_name = onboarding_doc.get("custom_first_name","")
    doc.middle_name = onboarding_doc.get("custom_middle_name","")
    doc.last_name = onboarding_doc.get("custom_last_name","")
    doc.gender = onboarding_doc.get("custom_gender","")
    doc.date_of_birth = onboarding_doc.get("custom_date_of_birth","")
    doc.current_address = onboarding_doc.get("custom_current_address","")
    doc.permanent_address = onboarding_doc.get("custom_permanent_address","")
    doc.current_accommodation_type = onboarding_doc.get("custom_current_address_is","")
    doc.permanent_accommodation_type = onboarding_doc.get("custom_permanent_address_is","")
    doc.salutation = onboarding_doc.get("custom_salutation","")
    doc.pan_number = onboarding_doc.get("custom_pan_number","")
    doc.marital_status = onboarding_doc.get("custom_married_yesno","")
    doc.custom_identification_mark1 = onboarding_doc.get("custom_identification_mark_","")
    doc.blood_group = onboarding_doc.get("custom_blood_group","")
    doc.provident_fund_account = onboarding_doc.get("custom_uan_no","")
    doc.custom_pin_code = onboarding_doc.get("custom_current_address_is","")
    doc.custom_other_bank_name = onboarding_doc.get("custom_bank_name","")
    doc.custom_other_bank_ac_no = onboarding_doc.get("custom_bank_ac_no","")
    doc.custom_other_bank_ifsc_code = onboarding_doc.get("custom_ifsc_code","")
    doc.person_to_be_contacted = onboarding_doc.get("custom_emergency_contact_name","")
    doc.custom_emergency_contact_address = onboarding_doc.get("custom_emergency_contact_address","")
    doc.emergency_phone_number = onboarding_doc.get("custom_emergency_phone","")
    doc.passport_number = onboarding_doc.get("custom_passport_number","")
    doc.valid_upto = onboarding_doc.get("valid_upto","")
    doc.notice_number_of_days = onboarding_doc.get("custom_employee_notice_period_days","")
    doc.custom_father_name = onboarding_doc.get("custom_middle_name","")
    return doc