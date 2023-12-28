{
    'name': 'RDP HR Ticket',
    'version': '12.0.0.1',
    'category': 'Project',
    'author': 'RDP',
    'summary': 'This module help us to create HR Tickets',
    'website': 'www.rdp.in',
    'sequence': '10',
    'description': """
     This module help us to create HR Tickets'
    """,
    'depends': ['base', 'mail', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/ticket_view.xml',
        'data/data.xml',
        'data/hr_ticket_template.xml'
    ],

    # 'license': 'OPL-1',
    'application': True,
    'installable': True,


}