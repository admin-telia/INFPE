from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

import datetime
import re


class attestationSalariale(models.Model):
	_name="document.attestationsalariale"
	_description = "Gestion des attestations salariales"

	titre5 = fields.Char(string="Titre", default="ATTESTATION DE PRISE EN CHARGE SALARIALE")
	phrase59 = fields.Char(string="Phrase 1", default="Je soussigné, Directeur général de l'Institut national de Formation des Personnels de l'Education, atteste que Monsieur")
	employe5 = fields.Many2one('hr.employee',string="Agent")
	matricule5 = fields.Char(string="Matricule",related="employe5.identification_id", readonly=True)
	fonction5 = fields.Char(string="Fonction",related="employe5.job_title", readonly=True)
	phrase60 = fields.Char(string="Phrase 2", default="auprès dudit Institut suivant Arrêté 11 02021-23-00122/MENAPLN/SG/DRH du 21101/2022 portant détachement sur demande, est pris en charge au plan salarial et indemnitaire à partir du")
	date_d5 = fields.Date(string="Date", default= datetime.date.today())
	phrase61 = fields.Char(string="Phrase 3", default="En foi de quoi, la présente attestation est établie pour servir et valoir ce que de droit.")
	phrase62 = fields.Char(string="Phrase 4", default="Lombila le,")
	phrase63 = fields.Char(string="Phrase 5", default="Ampliations")
	phrase64 = fields.Char(string="Phrase 6", default="DRH:01")
	phrase65 = fields.Char(string="Phrase 7", default="Le Directeur Général")
	phrase66 = fields.Char(string="Phrase 8", default="Dr Etienne OUEDRAOGO")
	phrase67 = fields.Char(string="Phrase 9", default="Chevalier de l'Ordre du Mérite")
	#phrase59 = fields.Char(string="Phrase 13")


	@api.onchange('titre5')
	def check_titre5(self):
		if self.titre5 :
			self.titre5 = self.titre5.upper()