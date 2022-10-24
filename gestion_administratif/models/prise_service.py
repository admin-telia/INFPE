from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

import datetime
import re


class priseService(models.Model):
	_name="document.priseservice"
	_description = "Gestion des certificats de prise de service"

	titre7 = fields.Char(string="Titre", default="Certificat de PRISE DE SERVICE")
	phrase111 = fields.Char(string="Phrase 1", default="Je soussigné, Directeur général de l’Institut national de Formation des Personnels de l’Education (INFPE), certifie que Madame")
	employe7 = fields.Many2one('hr.employee',string="Agent")
	matricule7 = fields.Char(string="Matricule",related="employe7.identification_id", readonly=True)
	fonction7 = fields.Char(string="Fonction",related="employe7.job_title", readonly=True)
	phrase112 = fields.Char(string="Phrase 2", default=", en service à la Direction régionale de l’INFPE du Plateau central et nommée Chef de Service de la Gestion des Ressources humaines de ladite Direction suivant Décision n°2022-014/INFPE/DG/SG/DRH du 21 janvier 2022, à pris service le")
	date_d7 = fields.Date(string="Date de prise de service", default=datetime.date.today())
	phrase113 = fields.Char(string="Phrase 4", default="En foi de quoi, le présent certificat est établi pour servir et valoir ce que de droit.")
	phrase114 = fields.Char(string="Phrase 5", default="Loumbila, le")
	phrase115 = fields.Char(string="Phrase 6", default="Ampliations :")
	phrase116 = fields.Char(string="Phrase 7", default="-DRINFPE-PLC")
	phrase117 = fields.Char(string="Phrase 8", default="01")
	phrase118 = fields.Char(string="Phrase 9", default="- DRH :")
	phrase119 = fields.Char(string="Phrase 10", default="01")
	phrase120 = fields.Char(string="Phrase 11", default="Dr Etienne OUEDRAOGO")
	phrase121 = fields.Char(string="Phrase 12", default="Chevalier de l’Ordre du Mérite")


	@api.onchange('titre7')
	def check_titre7(self):
		if self.titre7 :
			self.titre7 = self.titre7.upper()