from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

import datetime
import re


class certificatAdministratif(models.Model):
	_name="document.certificatadministratif"
	_description = "Gestion des certificats administratifs"

	titre8 = fields.Char(string="Titre", default="CERTIFICAT ADMINISTRATIF")
	phrase122 = fields.Char(string="Phrase 1", default="Je soussigné, Directeur général de l’Institut national de Formation des Personnels de l’Education (INFPE), certifie que Madame")
	employe8 = fields.Many2one('hr.employee',string="Agent")
	matricule8 = fields.Char(string="Matricule",related="employe8.identification_id", readonly=True)
	fonction8 = fields.Char(string="Fonction",related="employe8.job_title", readonly=True)
	phrase123 = fields.Char(string="Phrase 2", default="et qui a pris service le")
	date_d8 = fields.Date(string="Date de prise de service", default=datetime.date.today())
	phrase124 = fields.Char(string="Phrase 3", default="suivant certificat no 2022-030/INFPE/DG/SG/DRH du 21 février 2022, n’est  pas logée dans un bâtiment administratif depuis cette date.")
	phrase125 = fields.Char(string="Phrase 4", default="Par conséquent, l’intéressée peut prétendre aux indemnités suivantes:")
	phrase126 = fields.Char(string="Phrase 5", default="-	Logement :")
	phrase127 = fields.Char(string="Phrase 6", default="déjà servie")
	phrase128 = fields.Char(string="Phrase 7", default="-	Responsabilité :")
	phrase129 = fields.Char(string="Phrase 8", default="P/C du 24/01/2022")
	phrase130 = fields.Char(string="Phrase 9", default="-	Astreinte :")
	phrase131 = fields.Char(string="Phrase 10", default="déjà servie")
	phrase132 = fields.Char(string="Phrase 11", default="-	Technicité :")
	phrase133 = fields.Char(string="Phrase 12", default="déjà servie")
	phrase134 = fields.Char(string="Phrase 13", default="-	Spécifique harmonisée :")
	phrase135 = fields.Char(string="Phrase 14", default="déjà servie")
	phrase136 = fields.Char(string="Phrase 15", default="En foi de quoi, le présent certificat est établi pour servir et valoir ce que de droit.")
	phrase137 = fields.Char(string="Phrase 16", default="Loumbila, le")
	phrase138 = fields.Char(string="Phrase 17", default="Ampliations :")
	phrase139 = fields.Char(string="Phrase 18", default="SG")
	phrase140 = fields.Char(string="Phrase 19", default="01")
	phrase141 = fields.Char(string="Phrase 20", default="DRH")
	phrase142 = fields.Char(string="Phrase 21", default="01")
	phrase143 = fields.Char(string="Phrase 22", default="DAF")
	phrase144 = fields.Char(string="Phrase 23", default="01")
	phrase145 = fields.Char(string="Phrase 24", default="DCMEF")
	phrase146 = fields.Char(string="Phrase 25", default="01")
	phrase147 = fields.Char(string="Phrase 26", default="AC")
	phrase148 = fields.Char(string="Phrase 27", default="01")
	pi1 = fields.Char(string="Phrase 28", default="Le Directeur Général")
	phrase149 = fields.Char(string="Phrase 29", default="Dr Etienne OUEDRAOGO")
	phrase150 = fields.Char(string="Phrase 30", default="Chevalier de l'Ordre du Mérite")


	@api.onchange('titre8')
	def check_titre8(self):
		if self.titre8 :
			self.titre8 = self.titre8.upper()