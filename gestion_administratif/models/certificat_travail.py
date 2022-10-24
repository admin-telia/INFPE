from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import re


class certificatTravail(models.Model):
	_name="document.certificattravail"
	_description = "Gestion des certificats de travail"

	titre4 = fields.Char(string="Titre", default="CERTIFICAT DE TRAVAIL")
	phrase47 = fields.Char(string="Phrase 1", default="Je soussigné, Directeur général de l’Institut national de Formation des Personnels de l’Education (INFPE), certifie que Monsieur ")
	employe4 = fields.Many2one('hr.employee',string="Agent")
	matricule4 = fields.Char(string="Matricule",related="employe4.identification_id", readonly=True)
	fonction4 = fields.Char(string="Fonction",related="employe4.job_title", readonly=True)
	phrase48 = fields.Char(string="Phrase 2", default="a travaillé au sein de l’Ecole nationale des Enseignants du Primaire de Ouahigouya en qualité de")
	date_d4 = fields.Date(string="Date de debut du travail")
	date_f4 = fields.Date(string="Date de fin du travail")
	phrase49 = fields.Char(string="Phrase 3", default="Il quitte cet établissement en ce jour libre de tout engagement.")
	phrase50 = fields.Char(string="Phrase 4", default="En foi de quoi, le présent certificat est établi pour servir et valoir ce que de droit.")
	phrase51 = fields.Char(string="Phrase 5", default="Lombila le,")
	phrase52 = fields.Char(string="Phrase 6", default="Ampliations")
	phrase53 = fields.Char(string="Phrase 7", default="CNSS:01")
	phrase54 = fields.Char(string="Phrase 8", default="DRH:01")
	phrase55 = fields.Char(string="Phrase 9", default="P/Le Directeur général et P/D Le Secrétaire Général")
	phrase56 = fields.Char(string="Phrase 10", default="Paul ZONGO")
	phrase57 = fields.Char(string="Phrase 11", default="Administrateur Civil Chevalier de l’Ordre du Mérite, de l’Administration et du Travail")
	phrase58 = fields.Char(string="Phrase 12", invisible=True)
	#phrase59 = fields.Char(string="Phrase 13")


	@api.onchange('titre4')
	def check_titre4(self):
		if self.titre4 :
			self.titre4 = self.titre4.upper()