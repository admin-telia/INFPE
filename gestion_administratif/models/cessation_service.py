from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

import datetime
import re


class cessationService(models.Model):
	_name="document.cessationservice"
	_description = "Gestion des certificats de cessation du service"

	titre3 = fields.Char(string="Titre", default="Certificat de cessation  DE SERVICE")
	phrase34 = fields.Char(string="Phrase 1", default="Je soussigné, Directeur général de l’Institut national de Formation des Personnels de l’Education (INFPE), certifie que  Monsieur")
	employe3 = fields.Many2one('hr.employee',string="Agent")
	matricule3 = fields.Char(string="Matricule",related="employe3.identification_id", readonly=True)
	fonction3 = fields.Char(string="Fonction",related="employe3.job_title", readonly=True)
	phrase35 = fields.Char(string="Phrase 2", default=", précédemment  en service à la Direction régionale de l’INFPE des Hauts-Bassins et nommé  Directeur de l’Administration et des Finances de l’Agence de l’eau des Cascades suivant Décret n° 2021-1173/PRES/PM/MEA du 23 novembre 2021, a effectivement cessé service le")
	date_d3 = fields.Date(string="Date de cessation du service", default= datetime.date.today())
	phrase36 = fields.Char(string="Phrase 4", default="En foi de quoi, le présent certificat est établi pour servir et valoir ce que de droit.")
	phrase37 = fields.Char(string="Phrase 5", default="Lombila le,")
	phrase38 = fields.Char(string="Phrase 6", default="Ampliations")
	phrase39 = fields.Char(string="Phrase 7", default="DG:01")
	phrase40 = fields.Char(string="Phrase 8", default="DRH:01")
	phrase41 = fields.Char(string="Phrase 9", default="INFPE DR HB:01")
	phrase42 = fields.Char(string="Phrase 10", default="P/Le Directeur général et P/D Le Secrétaire Général")
	phrase43 = fields.Char(string="Phrase 11", default="Paul ZONGO")
	phrase44 = fields.Char(string="Phrase 12", default="Administrateur Civil Chevalier de l’Ordre du Mérite, de l’Administration et du Travail")
	phrase45 = fields.Char(string="Phrase 13", invisible=True)
	phrase46 = fields.Char(string="Phrase 14", invisible=True)


	@api.onchange('titre3')
	def check_titre3(self):
		if self.titre3 :
			self.titre3 = self.titre3.upper()