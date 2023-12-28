{
    'name':"Vendor Registration Form",
    'summary':"""this module preparing for vendor registration details purpose""",
    'description':"""this module preparing for vendor registration details purpose""",
    'depends':['base','website'],
    'data': [
        'security/ir.model.access.csv',
        'views/vendor_registration.xml',
        'views/existing_email_view.xml',
        # 'views/assests.xml',
            ],
    'installable':True,
    'auto_install':False,
    'application':False,
}
