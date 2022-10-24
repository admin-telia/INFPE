from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import re


class autorisationAbsence(models.Model):
	_name="document.absence"
	_description = "Gestion des autorisations d'absences"

	titre1 = fields.Char(string="Titre", default="Autorisation absence")
	phrase8 = fields.Char(string="Phrase 1", default="Vu la demande de l'intéressé en date du 24 janvier 2022;")
	phrase9 = fields.Char(string="Phrase 2", default="Une autorisation d'absence de quarante-huit (48) heures allant du")
	phrase10 = fields.Char(string="Phrase 3", default="jeudi 27 au vendredi 28 janvier 2022")
	phrase11 = fields.Char(string="Phrase 4", default="est accordé à Monsieur")
	employe1 = fields.Many2one('hr.employee',string="Agent")
	matricule1 = fields.Char(string="Matricule",related="employe1.identification_id", readonly=True)
	fonction1 = fields.Char(string="Fonction",related="employe1.job_title", readonly=True)
	phrase12 = fields.Char(string="Phrase 5", default="afin de lui permettre de se rendre à Orodara province du Kénédougou pour raisons de famille.")
	phrase13 = fields.Char(string="Phrase 6",default="Date de reprise de service:")
	date_d1 = fields.Date(string="Date de reprise")
	phrase14 = fields.Char(string="Phrase 7", default="Lombila le,")
	phrase15 = fields.Char(string="Phrase 8", default="Ampliations")
	phrase16 = fields.Char(string="Phrase 9", default="DRH:01")
	phrase17 = fields.Char(string="Phrase 10", default="Le Directeur Général")
	phrase18 = fields.Char(string="Phrase 11", default="Dr Etienne OUEDRAOGO")
	phrase19 = fields.Char(string="Phrase 12", default="Chevalier de l'Ordre du Mérite")
	#phrase13 = fields.Char(string="Phrase 11")


	@api.onchange('titre1')
	def check_titre1(self):
		if self.titre1 :
			self.titre1 = self.titre1.upper()