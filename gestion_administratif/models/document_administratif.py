from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

import datetime
import re


class documents(models.Model):
	_name="document.administratifs"
	_description = "Gestion des documents administratifs"

	titre = fields.Char(string="Titre", default="ATTESTATION DE PRISE EN CHARGE SALARIALE")
	phrase1 = fields.Char(string="Phrase 1", default="Je soussigné, Directeur général de l’Institut national de Formation des Personnels de l’Education, atteste que Monsieur ")
	employe = fields.Many2one('hr.employee',string="Agent")
	matricule = fields.Char(string="Matricule",related="employe.identification_id", readonly=True)
	fonction = fields.Char(string="Fonction",related="employe.job_title", readonly=True)
	phrase2 = fields.Char(string="Phrase 2", default="précédemment en service à la Direction régionale de l’INFPE de la Boucle du Mouhoun (ex-ENEP de Dédougou), a été pris en charge au plan salarial et indemnitaire durant la période allant du")
	date_d = fields.Date(string="Date début", default=datetime.date.today())
	date_f = fields.Date(string="Date fin", default=datetime.date.today())
	phrase3 = fields.Char(string="Phrase 3", default="En foi de quoi, la présente attestation est établie pour servir et valoir ce que de droit.")
	phrase4 = fields.Char(string="Phrase 4", default="Loumbila, le")
	phrase5 = fields.Char(string="Phrase 5", default="Pour Le Directeur général et P/I Le Secrétaire général")
	phrase6 = fields.Char(string="Phrase 6", default="Paul ZONGO")
	phrase7 = fields.Char(string="Phrase 7", default="Administrateur civil Chevalier de l’Ordre de Mérite de l’Administration et du Travail")


	@api.onchange('titre')
	def check_titre(self):
		if self.titre :
			self.titre = self.titre.upper()