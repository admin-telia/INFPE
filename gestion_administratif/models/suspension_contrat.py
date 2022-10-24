from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import re


class suspensionContrat(models.Model):
	_name="document.suspensioncontrat"
	_description = "Gestion des notes de suspension de contrat"

	titre11 = fields.Char(string="Titre")
	phrase210 = fields.Char(string="Phrase 1")
	phrase211 = fields.Char(string="Phrase 2")
	employe11 = fields.Many2one('hr.employee',string="Agent")
	matricule11 = fields.Char(string="Matricule",related="employe11.identification_id", readonly=True)
	fonction11 = fields.Char(string="Fonction",related="employe11.job_title", readonly=True)
	phrase212 = fields.Char(string="Phrase 3")
	date_d11 = fields.Date(string="Date de suspension du contrat")
	date_f11 = fields.Date(string="Date d'expiration")
	phrase213 = fields.Char(string="Phrase 4")
	phrase214 = fields.Char(string="Phrase 5")
	phrase215 = fields.Char(string="Phrase 6")
	phrase216 = fields.Char(string="Phrase 7")
	phrase217 = fields.Char(string="Phrase 8")
	phrase218 = fields.Char(string="Phrase 9")
	phrase219 = fields.Char(string="Phrase 10")
	phrase220 = fields.Char(string="Phrase 11")
	phrase221 = fields.Char(string="Phrase 12")
	phrase222 = fields.Char(string="Phrase 13")
	phrase223 = fields.Char(string="Phrase 14")
	phrase224 = fields.Char(string="Phrase 15")
	phrase225 = fields.Char(string="Phrase 16")
	phrase226 = fields.Char(string="Phrase 17")
	phrase227 = fields.Char(string="Phrase 18")
	phrase228 = fields.Char(string="Phrase 19")
	phrase229 = fields.Char(string="Phrase 20")

	@api.onchange('titre11')
	def check_titrep(self):
		if self.titre11 :
			self.titre11 = self.titre11.upper()