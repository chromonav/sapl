import frappe
from frappe.rate_limiter import rate_limit
from frappe import _, scrub
from frappe.core.doctype.file.utils import remove_file_by_url
import json

@frappe.whitelist(allow_guest=True)
@rate_limit(key="web_form", limit=10, seconds=60)
def accept(web_form, data):
    """Save the web form"""
    data = frappe._dict(json.loads(data))

    files = []
    files_to_delete = []

    web_form = frappe.get_doc("Web Form", web_form)
    doctype = web_form.doc_type
    user = frappe.session.user

    if web_form.anonymous and frappe.session.user != "Guest":
        frappe.session.user = "Guest"

    if data.name and not web_form.allow_edit:
        frappe.throw(_("You are not allowed to update this Web Form Document"))

    frappe.flags.in_web_form = True
    meta = frappe.get_meta(doctype)

    if data.name:
        # update
        doc = frappe.get_doc(doctype, data.name)
    elif web_form.name =="employee-onboarding-final":
        doc = frappe.get_doc(doctype, {"job_applicant":data.job_applicant,"job_offer":data.job_offer})
    else:
        # insert
        doc = frappe.new_doc(doctype)

    # set values
    for field in web_form.web_form_fields:
        fieldname = field.fieldname
        df = meta.get_field(fieldname)
        value = data.get(fieldname, "")

        if df and df.fieldtype in ("Attach", "Attach Image"):
            if value and "data:" and "base64" in value:
                files.append((fieldname, value))
                if not doc.name:
                    doc.set(fieldname, "")
                continue

            elif not value and doc.get(fieldname):
                files_to_delete.append(doc.get(fieldname))

        doc.set(fieldname, value)

    if doc.name:
        if web_form.has_web_form_permission(doctype, doc.name, "write"):
            doc.save(ignore_permissions=True)
        else:
            # only if permissions are present
            doc.save()
    elif web_form.name =="employee-onboarding-final":
        doc.save()
    else:
        # insert
        if web_form.login_required and frappe.session.user == "Guest":
            frappe.throw(_("You must login to submit this form"))

        ignore_mandatory = True if files else False

        doc.insert(ignore_permissions=True, ignore_mandatory=ignore_mandatory)

    # add files
    if files:
        for f in files:
            fieldname, filedata = f

            # remove earlier attached file (if exists)
            if doc.get(fieldname):
                remove_file_by_url(doc.get(fieldname), doctype=doctype, name=doc.name)

            # save new file
            filename, dataurl = filedata.split(",", 1)
            _file = frappe.get_doc(
                {
                    "doctype": "File",
                    "file_name": filename,
                    "attached_to_doctype": doctype,
                    "attached_to_name": doc.name,
                    "content": dataurl,
                    "decode": True,
                }
            )
            _file.save()

            # update values
            doc.set(fieldname, _file.file_url)

        doc.save(ignore_permissions=True)

    if files_to_delete:
        for f in files_to_delete:
            if f:
                remove_file_by_url(f, doctype=doctype, name=doc.name)

    if web_form.anonymous and frappe.session.user == "Guest" and user:
        frappe.session.user = user

    frappe.flags.web_form_doc = doc
    return doc
