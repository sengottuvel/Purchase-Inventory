from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import time
import openerp.addons.decimal_precision as dp
from datetime import datetime
import re
import math
dt_time = time.strftime('%m/%d/%Y %H:%M:%S')

class kg_pattern_master(osv.osv):

	_name = "kg.pattern.master"
	_description = "SAM Pattern Master"
	
	_columns = {
			
		'name': fields.char('Part/Pattern No', size=128, required=True),
		'company_id': fields.many2one('res.company', 'Company Name',readonly=True),
		'box_id': fields.many2one('kg.box.master','Box',readonly=True,required=True,domain="[('state','=','approved'), ('active','=','t')]"),		
		'pattern_name': fields.char('Part/Pattern Name', size=128,required=True),
		'code': fields.char('Pattern Code', size=128,required=True),
		'active': fields.boolean('Active'),
		'pcs_weight': fields.float('SS Weight(kgs)'),
		'ci_weight': fields.float('CI Weight(kgs)'),
		'mould_rate': fields.float('Mould Rate(Rs)'),
		'location': fields.selection([('ipd','IPD'),('ppd','PPD')],'Location', required=True),
		'state': fields.selection([('draft','Draft'),('confirmed','WFA'),('approved','Approved'),('reject','Rejected'),('cancel','Cancelled')],'Status', readonly=True),
		'pattern_state': fields.selection([('active','Active'),('hold','Hold'),('rework','Rework'),('reject','Rejected')],'Pattern Status',required=True),
		'notes': fields.text('Notes'),
		'remark': fields.text('Approve/Reject'),
		'cancel_remark': fields.text('Cancel'),
		'line_ids':fields.one2many('ch.mocwise.rate', 'header_id', "MOC Wise Rate"),
		'line_ids_a':fields.one2many('ch.pattern.attachment', 'header_id', "Attachments"),
		'line_ids_b':fields.one2many('ch.pattern.history', 'header_id', "Pattern History"),
		
		### Entry Info ###
		'crt_date': fields.datetime('Creation Date',readonly=True),
		'user_id': fields.many2one('res.users', 'Created By', readonly=True),
		'confirm_date': fields.datetime('Confirmed Date', readonly=True),
		'confirm_user_id': fields.many2one('res.users', 'Confirmed By', readonly=True),
		'ap_rej_date': fields.datetime('Approved/Reject Date', readonly=True),
		'ap_rej_user_id': fields.many2one('res.users', 'Approved/Reject By', readonly=True),	
		'cancel_date': fields.datetime('Cancelled Date', readonly=True),
		'cancel_user_id': fields.many2one('res.users', 'Cancelled By', readonly=True),
		'update_date': fields.datetime('Last Updated Date', readonly=True),
		'update_user_id': fields.many2one('res.users', 'Last Updated By', readonly=True),		
				
	}
	
	_defaults = {
	
		'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'kg.pattern.master', context=c),
		'active': True,
		'state': 'draft',
		'user_id': lambda obj, cr, uid, context: uid,
		'crt_date':fields.datetime.now,	
		
	}
	
	
	"""def _Validation(self, cr, uid, ids, context=None):
		flds = self.browse(cr , uid , ids[0])
		special_char = ''.join( c for c in flds.name if  c in '!@#$%^~*{}?+/=' )
		if special_char:
			return False
		return True
	
	def _CodeValidation(self, cr, uid, ids, context=None):
		flds = self.browse(cr , uid , ids[0])		
		if flds.code:	
			code_special_char = ''.join( c for c in flds.code if  c in '!@#$%^~*{}?+/=' )		
			if code_special_char:
				return False
		return True		"""
		
	def _name_validate(self, cr, uid,ids, context=None):
		rec = self.browse(cr,uid,ids[0])
		res = True
		if rec.name:
			division_name = rec.name
			name=division_name.upper()			
			cr.execute(""" select upper(name) from kg_pattern_master where upper(name)  = '%s' """ %(name))
			data = cr.dictfetchall()
			
			if len(data) > 1:
				res = False
			else:
				res = True				
		return res
			
	
		
	def entry_cancel(self,cr,uid,ids,context=None):
		rec = self.browse(cr,uid,ids[0])
		if rec.cancel_remark:
			self.write(cr, uid, ids, {'state': 'cancel','cancel_user_id': uid, 'cancel_date': time.strftime('%Y-%m-%d %H:%M:%S')})
		else:
			raise osv.except_osv(_('Cancel remark is must !!'),
				_('Enter the remarks in Cancel remarks field !!'))
				
		return True

	def entry_confirm(self,cr,uid,ids,context=None):
		rec = self.browse(cr,uid,ids[0])		
		self.write(cr, uid, ids, {'state': 'confirmed','confirm_user_id': uid, 'confirm_date': time.strftime('%Y-%m-%d %H:%M:%S')})
		return True

	def entry_approve(self,cr,uid,ids,context=None):
		self.write(cr, uid, ids, {'state': 'approved','ap_rej_user_id': uid, 'ap_rej_date': time.strftime('%Y-%m-%d %H:%M:%S')})
		return True

	def entry_reject(self,cr,uid,ids,context=None):
		rec = self.browse(cr,uid,ids[0])
		if rec.remark:
			self.write(cr, uid, ids, {'state': 'reject','ap_rej_user_id': uid, 'ap_rej_date': time.strftime('%Y-%m-%d %H:%M:%S')})
		else:
			raise osv.except_osv(_('Rejection remark is must !!'),
				_('Enter the remarks in rejection remark field !!'))
		return True
		
	def unlink(self,cr,uid,ids,context=None):
		unlink_ids = []		
		for rec in self.browse(cr,uid,ids):	
			if rec.state not in ('draft','cancel'):				
				raise osv.except_osv(_('Warning!'),
						_('You can not delete this entry !!'))
			else:
				unlink_ids.append(rec.id)
		return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
		
	def write(self, cr, uid, ids, vals, context=None):
		vals.update({'update_date': time.strftime('%Y-%m-%d %H:%M:%S'),'update_user_id':uid})
		return super(kg_pattern_master, self).write(cr, uid, ids, vals, context)
		
	
	_constraints = [
		#(_Validation, 'Special Character Not Allowed !!!', ['name']),
		#(_CodeValidation, 'Special Character Not Allowed !!!', ['Check Code']),
		#(_name_validate, 'Pattern No must be unique !!', ['no']),		
		
	]
	
kg_pattern_master()


class ch_mocwise_rate(osv.osv):
	
	_name = "ch.mocwise.rate"
	_description = "MOC Wise Rate"
	
	_columns = {
			
		'header_id':fields.many2one('kg.pattern.master', 'Pattern Entry', required=True, ondelete='cascade'),	
		'moc_id': fields.many2one('kg.moc.master','MOC', required=True,domain="[('state','=','approved'), ('active','=','t')]"),			
		'date':fields.date('Effective Date',required=True),
		'rate':fields.float('Rate(Rs)',required=True),
		'remarks':fields.text('Remarks'),
		
	}
ch_mocwise_rate()



class ch_pattern_history(osv.osv):
	
	_name = "ch.pattern.history"
	_description = "Pattern History"
	
	_columns = {
			
		'header_id':fields.many2one('kg.pattern.master', 'Pattern Entry', required=True, ondelete='cascade'),	
		's_no': fields.integer('S.No.', required=True),			
		'date':fields.date('Date',required=True),
		'reason':fields.text('Reason for Rework',required=True),
		'remarks':fields.text('Remarks'),
		
	}
ch_pattern_history()



class ch_pattern_attachment(osv.osv):
	
	_name = "ch.pattern.attachment"
	_description = "Pattern Attachments"
	
	_columns = {
			
		'header_id':fields.many2one('kg.pattern.master', 'Pattern Entry', required=True, ondelete='cascade'),			
		'date':fields.date('Date',required=True),
		'attach_file':fields.binary('Attachment',required=True),	
		
	}
ch_pattern_attachment()


