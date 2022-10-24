from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import re
import datetime


class paiement(models.Model):
	_name="document.paiement"
	_description = "Gestion cessation de paiement"

	tit1 = fields.Char(string="Titre", default="CERTIFICAT DE CESSATION DE PAIEMENT")
	p160 = fields.Char(string="Phrase 1", default="Le Directeur général de l’Institut national de Formation des Personnels de l’Education (INFPE), soussigné, certifie que Monsieur ")
	e10 = fields.Many2one('hr.employee',string="Agent")
	m10 = fields.Char(string="Matricule",related="e10.identification_id", readonly=True)
	f10 = fields.Char(string="Fonction",related="e10.job_title", readonly=True)
	p161 = fields.Char(string="Phrase 2", default="catégorie")
	p162 = fields.Char(string="Phrase 3", default="A")
	p163 = fields.Char(string="Phrase 4", default="échelle")
	p164 = fields.Char(string="Phrase 5", default="1")
	p165 = fields.Char(string="Phrase 6", default="1ère")
	p166 = fields.Char(string="Phrase 7", default="classe")
	p167 = fields.Char(string="Phrase 8", default="échelon")
	p168 = fields.Char(string="Phrase 9", default="16")
	p169 = fields.Char(string="Phrase 10", default="indice")
	p170 = fields.Char(string="Phrase 11", default="2018")
	p171 = fields.Char(string="Phrase 12", default="précédemment en service à la Direction régionale de l'INFPE des Hauts-Bassins, en départ à la retraite et ayant cessé service")
	d10 = fields.Date(string="Date de cessation de paiement", default=datetime.date.today())
	p172 = fields.Char(string="Phrase 13", default="suivant certificat")
	p173 = fields.Char(string="Phrase 14", default="n°2022-002/INFPE/DG/SG/DRH du 05 janvier 2022,")
	p174 = fields.Char(string="Phrase 15", default="Situation de famille")
	p175 = fields.Char(string="Phrase 16", default=": marié")
	p176 = fields.Char(string="Phrase 17", default="Nombre d’enfant en charge")
	p177 = fields.Char(string="Phrase 18", default=": 01")
	p178 = fields.Char(string="Phrase 19", default="A été régulièrement tenu au courant de ses droits jusqu’au 31 décembre 2021 sur les bases suivantes :")
	p179 = fields.Char(string="Phrase 20", default="Salaire indiciaire")
	p180 = fields.Char(string="Phrase 21", default="391997/pm")
	p181 = fields.Char(string="Phrase 22", default="Allocations familliales")
	p182 = fields.Char(string="Phrase 23", default="0/pm")
	p183 = fields.Char(string="Phrase 24", default="Indemnité de résidence")
	p184 = fields.Char(string="Phrase 25", default="39200/pm")
	p185 = fields.Char(string="Phrase 26", default="Indemnité de logement")
	p186 = fields.Char(string="Phrase 27", default="69300/pm")
	p187 = fields.Char(string="Phrase 28", default="Indemnité de technicité")
	p188 = fields.Char(string="Phrase 29", default="27000/pm")
	p189 = fields.Char(string="Phrase 30", default="Indemnité d'astreintes")
	p190 = fields.Char(string="Phrase 31", default="25000/pm")
	p191 = fields.Char(string="Phrase 32", default="Indemnité spécifique harmonisée")
	p192 = fields.Char(string="Phrase 33", default="15000/pm")
	p193 = fields.Char(string="Phrase 34", default="Il a subi régulièrement les retenues ci-après :")
	p194 = fields.Char(string="Phrase 35", default="Pension civile")
	p195 = fields.Char(string="Phrase 36", default="31359/pm")
	p196 = fields.Char(string="Phrase 37", default="I.U.T.S")
	p197 = fields.Char(string="Phrase 38", default="46579/pm")
	p198 = fields.Char(string="Phrase 39", default="Qu’il n’est redevable d’aucune somme envers l’INFPE.")
	p199 = fields.Char(string="Phrase 40", default="Mode de paiement:")
	p200 = fields.Char(string="Phrase 41", default="banque de domiciliation")
	p201 = fields.Char(string="Phrase 42", default="BIB UBA")
	p202 = fields.Char(string="Phrase 43", default="N° de compte")
	p203 = fields.Char(string="Phrase 44", default=": 04060 1000 2127")
	p204 = fields.Char(string="Phrase 45", default="Loumbila, le")
	p205 = fields.Char(string="Phrase 46", default="P/Le Directeur général et P/I Le Secrétaire général")
	p206 = fields.Char(string="Phrase 47", default="Paul ZONGO")
	p207 = fields.Char(string="Phrase 48", default="Administrateur civil Chevalier de l’Ordre de Mérite de l'Administration et du Travail")
	


	@api.onchange('titre10')
	def check_titrep(self):
		if self.titre10 :
			self.titre10 = self.titre10.upper()