from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import re


class autorisationConge(models.Model):
	_name="document.conge"
	_description = "Gestion des autorisations de conge"

	titre2 = fields.Char(string="Titre", default="Autorisation de jouissance de conge")
	phrase20 = fields.Char(string="Phrase 1", default="Je sousigné, Directeur Général de l'Institut National de Formation des Personnels de l'Education autorise Madame")
	employe2 = fields.Many2one('hr.employee',string="Agent")
	matricule2 = fields.Char(string="Matricule",related="employe2.identification_id", readonly=True)
	fonction2 = fields.Char(string="Fonction",related="employe2.job_title", readonly=True)
	phrase21 = fields.Char(string="Phrase 2", default=", bénéficiaire d’un congé administratif d’un mois à solde entière au titre de l’année 2021 suivant décision n°2021-035/MENAPLN/SG/ENEP-L/DG/DRH du 19 août 2021, à jouir au Burkina Faso  de la  première tranche dudit congé allant du ")
	phrase22 = fields.Char(string="Phrase 3", default="mardi 11 au mardi 25 janvier 2022")
	phrase23 = fields.Char(string="Phrase 4", default="inclus")
	phrase24 = fields.Char(string="Phrase 5", default="L’intéressée reprendra service le ")
	phrase25 = fields.Char(string="Phrase 6", default="mercredi 26 janvier 2022.")
	phrase26 = fields.Char(string="Phrase 7", default="En foi de quoi, la présente autorisation est établie pour servir et valoir ce que de droit.")
	phrase27 = fields.Char(string="Phrase 8", default="Ampliations")
	phrase28 = fields.Char(string="Phrase 9", default="DRH:01")
	phrase29 = fields.Char(string="Phrase 10", default="Le Directeur des Ressources Humaines")
	phrase30 = fields.Char(string="Phrase 11", default="Le Directeur Général")
	phrase31 = fields.Char(string="Phrase 12", default="Paul ZONGO")
	phrase32 = fields.Char(string="Phrase 13", default="Dr Etienne OUEDRAOGO")
	phrase33 = fields.Char(string="Phrase 14", default="Chevalier de l’Ordre du Mérite")


	@api.onchange('titre2')
	def check_titre2(self):
		if self.titre2 :
			self.titre2 = self.titre2.upper()