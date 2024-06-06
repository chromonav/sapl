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
    return doc