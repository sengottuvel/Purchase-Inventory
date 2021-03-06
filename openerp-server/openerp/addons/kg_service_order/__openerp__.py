##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).

##############################################################################
{
    'name': 'KG_Service_Order',
    'version': '0.1',
    'author': 'sengottuvel',
    'category': 'Service_Management',
    'images': ['images/purchase_requisitions.jpeg'],
    'website': 'http://www.openerp.com',
    'description': """
This module allows you to manage your Purchase Requisition.
===========================================================

When a purchase order is created, you now have the opportunity to save the
related requisition. This new object will regroup and will allow you to easily
keep track and order all your purchase orders.
""",
    'depends' : ['base', 'product','kg_depmaster','kg_gate_pass'],
    'data': [
			
			'wizard/so2_service_bill_view.xml',
			'wizard/kg_service_order_wizard.xml',
			'kg_service_order_view.xml',
			'service_order_report_view.xml',
			
			
			
			],
    'auto_install': False,
    'installable': True,
}

