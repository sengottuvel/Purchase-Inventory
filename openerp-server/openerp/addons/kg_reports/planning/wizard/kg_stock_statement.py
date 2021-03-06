# -*- coding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from osv import fields, osv
import netsvc
import pooler
import time
from datetime import date
from osv.orm import browse_record, browse_null
from tools.translate import _
from datetime import datetime
import datetime as lastdate

a = datetime.now()
dt_time = a.strftime('%m/%d/%Y %H:%M:%S')

class kg_stock_statement(osv.osv_memory):
	_name = "kg.stock.statement"
	_description = "Stock Statement"
	
	_columns = {
	
		'as_on_date': fields.date("As On Date",required=True),
		'division_id': fields.many2one('kg.division.master','Division'),
		'company_id': fields.many2one('res.company', 'Company'),
		'print_date': fields.datetime('Creation Date', readonly=True),
		'printed_by': fields.many2one('res.users','Printed By',readonly=True),   
	   
	}
	
	
		
	_defaults = {
		'as_on_date': fields.date.context_today,
		'print_date': fields.datetime.now,
		'printed_by': lambda obj, cr, uid, context: uid,		
		'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'kg.stock.statement', context=c),
	 }
	
	def _Validation(self, cr, uid, ids, context=None):
		flds = self.browse(cr , uid , ids[0])			
		if flds.as_on_date > str(date.today()):
			return False
		return True
	
	def create_report(self, cr, uid, ids, context={}):	
	
		rec = self.browse(cr,uid,ids[0])	
		data = self.read(cr,uid,ids,)[-1]		
		print data,' create_report('
		return {
			'type'		 : 'ir.actions.report.xml',
			'report_name'   : 'jasper_stock_statement_report',
			'datas': {
					'model':'kg.stock.statement',
					'id': context.get('active_ids') and context.get('active_ids')[0] or False,
					'ids': context.get('active_ids') and context.get('active_ids') or [],
					'report_type': 'pdf',
					'form':data
				},
			'nodestroy': False
			}
			
	_constraints = [
		(_Validation, 'System not allow to Generate Report with future date. !!', ['Start Date']),		
	]
	
kg_stock_statement()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
