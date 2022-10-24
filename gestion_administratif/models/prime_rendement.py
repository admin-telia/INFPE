from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

import datetime
import re


class primeRendement(models.Model):
	_name="document.primerendement"
	_description = "Gestion des primes de rendements"

	chef = fields.Char(string="Directeur Général", default="LE DIRECTEUR GENERAL DE L'ECOLE NATIONALE DES ENSEIGNANTS DU PRIMAIRE DE LOUMBILA,")
	phrase68 = fields.Char(string="Phrase 1", default="Vu la Constitution du 02 juin 1991 ; ")
	employe6 = fields.Many2one('hr.employee',string="Agent")
	matricule6 = fields.Char(string="Matricule",related="employe6.identification_id", readonly=True)
	fonction6 = fields.Char(string="Fonction",related="employe6.job_title", readonly=True)
	phrase69 = fields.Char(string="Phrase 2", default="Vu le décret n° 2012-1038/PRES du 31 décembre 2012, portant nomination du Premier Ministre; ")
	date_d5 = fields.Date(string="Date", default=datetime.date.today())
	phrase70 = fields.Char(string="Phrase 3", default="Vu le décret n° 2013-002/PRES/PM du 02 janvier 2013, portant composition du Gouvernement du Burkina Faso; ")
	phrase71 = fields.Char(string="Phrase 4", default="Vu la loi n°010-2013/ AN du 30 avril 2013, portant règles de création des catégories d'établissements publics; ")
	phrase72 = fields.Char(string="Phrase 5", default="Vu la loi n°33-2008/ AN du 22 mai 2008, portant régime juridique applicable aux emplois et aux agents des Etablissements publics de l'Etat; ")
	phrase73 = fields.Char(string="Phrase 6", default="Vu le décret n°085-189/CNR/PRES/EDUC du 28 mars 1985, portant création de l'ENEP de Loumbila;")
	phrase74 = fields.Char(string="Phrase 7", default="Vu le décret n°99-051/P=:Œ:S/PM!~EBA/MEF du 5 mars 1999, portant Statut Général des Etablissement Publics de l'Etat à caractère administratif ; ")
	phrase75 = fields.Char(string="Phrase 8", default="Vu le décret n° 2012-754/PRES/PM/MENA du 24 septembre 2012, portant approbation des Statuts des Ecoles Nationales des Enseignants du Primaire; ")
	phrase76 = fields.Char(string="Phrase 9", default="Vu le décret n02010-391/PRES/PM/MFPRE/MEF du 29 juillet 2010, portant modalités d'octroi d'une prime de rendement au.'{ agents des Etablissements publics de l'Etat décorés pour faits de service public; ")
	phrase77 = fields.Char(string="Phrase 10", default="Vu le décret nO 2012-S20/PRES/PM/MENA du 08 octobre 2012, portant nomination de Directeurs Généraux; ")
	phrase78 = fields.Char(string="Phrase 11", default="Vu le décret n° 2013-S52/PRES!GC du 03 octobre 2013, portant promotion et nomination à titre normal et à titre exceptionnel dans l'Ordre des Palmes Académiques à l'occasion du t 1 décembre 2013; ")
	phrase79 = fields.Char(string="Phrase 12", default="Vu la décision n° 10-095/MENA/SG/ENEP-L/DG du 01 octobre 2010, portant avancement d'échelon; ")
	phrase80 = fields.Char(string="Phrase 13", default="Vu la demande de l'intéressé; ")
	phrase81 = fields.Char(string="Phrase 14", default="DECIDE")
	phrase82 = fields.Char(string="Phrase 15", default="Article 1:")
	phrase83 = fields.Char(string="Phrase 16", default="n application des dispositions du décret n0201 0-391/PRES/PM/MFPRE/MEF du 29 juillet 2010 susvisé, il est accordé une prime de rondement de dix pourcent (10%) pour compter du 11 décembre 2013 à")
	phrase84 = fields.Char(string="Phrase 17", default="de 5è catégorie, échelle B, 7è échelon,")
	phrase85 = fields.Char(string="Phrase 18", default="décoré pour faits de service public.")
	phrase86 = fields.Char(string="Phrase 19", default="Article 2:")
	phrase87 = fields.Char(string="Phrase 20", default="La présente décision qui prend")
	phrase88 = fields.Char(string="Phrase 21", default="effet du point de vue de la soide pour compter du,")
	phrase89 = fields.Char(string="Phrase 22", default="sera enregistrée, pubiiée et communiquée partout où besoin sera.")
	phrase90 = fields.Char(string="Phrase 23", default="Loumbila, le")
	phrase91 = fields.Char(string="Phrase 24", default="Le Directeur Général,")
	phrase92 = fields.Char(string="Phrase 25", default="Regma-Etienne -KABORE")
	phrase93 = fields.Char(string="Phrase 26", default="Chevalier de l'Ordre National")
	phrase94 = fields.Char(string="Phrase 27", default="Ampliations")
	phrase95 = fields.Char(string="Phrase 28", default="DAF:")
	phrase96 = fields.Char(string="Phrase 29", default="01")
	phrase97 = fields.Char(string="Phrase 30", default="AC:")
	phrase98 = fields.Char(string="Phrase 31", default="01")
	phrase99 = fields.Char(string="Phrase 32", default="CF:")
	phrase100 = fields.Char(string="Phrase 33", default="01")
	phrase101= fields.Char(string="Phrase 34", default="SF:")
	phrase102= fields.Char(string="Phrase 35", default="01")
	phrase103= fields.Char(string="Phrase 36", default="Intéressé:")
	phrase104= fields.Char(string="Phrase 37", default="01")
	phrase105= fields.Char(string="Phrase 38", default="Dossier Int:")
	phrase106= fields.Char(string="Phrase 39", default="01")
	phrase107= fields.Char(string="Phrase 40", default="Chrono:")
	phrase108= fields.Char(string="Phrase 41", default="01")
	phrase109= fields.Char(string="Phrase 42", default="")
	phrase110= fields.Char(string="Phrase 43", default="")
	phrase112= fields.Char(string="Phrase 45", default="")
	phrase113= fields.Char(string="Phrase 46", default="")
	phrase114= fields.Char(string="Phrase 47", default="")
	phrase115= fields.Char(string="Phrase 48", default="")

	@api.onchange('change_default')
	def check_chef(self):
		if self.chef :
			self.chef = self.chef.upper()