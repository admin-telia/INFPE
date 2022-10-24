from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import re


class congeMaternite(models.Model):
	_name="document.congematernite"
	_description = "Conge de maternite"

	titre12 = fields.Char(string="Titre 1")
	titre13 = fields.Char(string="Titre 2")
	phrase230 = fields.Char(string="Phrase 1")
	phrase231 = fields.Char(string="Phrase 2")
	phrase232 = fields.Char(string="Phrase 3")
	phrase234 = fields.Char(string="Phrase 5")
	phrase235 = fields.Char(string="Phrase 6")
	phrase236 = fields.Char(string="Phrase 7")
	phrase237 = fields.Char(string="Phrase 8")
	phrase238 = fields.Char(string="Phrase 9")
	phrase239 = fields.Char(string="Phrase 10")
	phrase240 = fields.Char(string="Phrase 11")
	phrase241 = fields.Char(string="Phrase 12")
	phrase242 = fields.Char(string="Phrase 13")
	employe12 = fields.Many2one('hr.employee',string="Agent")
	matricule12 = fields.Char(string="Matricule",related="employe12.identification_id", readonly=True)
	fonction12 = fields.Char(string="Fonction",related="employe12.job_title", readonly=True)
	phrase233 = fields.Char(string="Phrase 4")
	phrase243 = fields.Char(string="Phrase 14")
	phrase244 = fields.Char(string="Phrase 15")
	phrase245 = fields.Char(string="Phrase 16")
	phrase246 = fields.Char(string="Phrase 17")
	phrase247 = fields.Char(string="Phrase 18")
	phrase248 = fields.Char(string="Phrase 19")
	phrase249 = fields.Char(string="Phrase 20")
	phrase250 = fields.Char(string="Phrase 21")
	phrase251 = fields.Char(string="Phrase 22")
	phrase252 = fields.Char(string="Phrase 23")
	phrase253 = fields.Char(string="Phrase 24")
	phrase254 = fields.Char(string="Phrase 25")
	phrase255 = fields.Char(string="Phrase 26")
	phrase256 = fields.Char(string="Phrase 27")
	phrase257 = fields.Char(string="Phrase 28")
	phrase258 = fields.Char(string="Phrase 29")
	phrase259 = fields.Char(string="Phrase 30")
	phrase260 = fields.Char(string="Phrase 31")



	@api.onchange('titre13')
	def check_titre13(self):
		if self.titre13 :
			self.titre13 = self.titre13.upper()