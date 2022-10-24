from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import re


class congeAdministratif(models.Model):
	_name="document.congeadministratif"
	_description = "Gestion des congés administratifs"

	t1 = fields.Char(string="Titre", default="LE DIRECTEUR GENERAL,")
	ph1 = fields.Char(string="Phrase 1", default="Vu	la Constitution ;")
	ph2 = fields.Char(string="Phrase 2", default="Vu	la Charte de la Transition du 1er mars 2022 ;")
	ph3 = fields.Char(string="Phrase 3", default="Vu	le décret n°2022-041PRES du 03 mars 2022 portant nomination du Premier Ministre ;")
	ph4 = fields.Char(string="Phrase 4", default="Vu	le décret n°2022-053/PRES/PM du 05 mars 2022 portant composition du Gouvernement ;")
	ph5 = fields.Char(string="Phrase 5", default="Vu 	la loi n°010-2013/AN du 30 avril 2013, portant règles de création  des catégories d’établissements publics ;")
	ph6 = fields.Char(string="Phrase 6", default="Vu	la loi n°033-2008/AN du 22 mai 2008, portant régime juridique applicable aux emplois et aux agents des établissements publics de l’Etat ;")
	ph7 = fields.Char(string="Phrase 7", default="Vu	le décret n°2020-0832/PRES/PM/MINEFID/MENAPLN du 05 octobre 2020 portant création de l’Institut national de Formation des personnels de l’Education;")
	ph8 = fields.Char(string="Phrase 8", default="Vu    le décret n°2020-0871/PRES/PM/MENAPLN/MINEFID du 12 octobre 2020 portant approbation des Statuts de l’Institut national de Formation des personnels de l’Education ;")
	ph9 = fields.Char(string="Phrase 9", default="Vu	le décret n° 2021-0134/PRES/PM/MENAPLN du 19 mars 2021 portant nomination des Directeurs généraux ;")
	ph10 = fields.Char(string="Phrase 10", default="Vu	l’arrêté n°2021-0113 /MENAPLN/SG /INFPE du 30 avril 2021 portant organisation et fonctionnement de l’Institut national de Formation des personnels de l’Education ;")
	ph11 = fields.Char(string="Phrase 11", default="Vu 	la décision n°2020-002/ MENAPLN/SG /ENEP-FGRM/DG/DRH du 30 décembre 2020 accordant un congé administratif à Monsieur KOANDA Salif et trente-quatre (34) autres en service à l’ENEP de Fada N’Gourma ;")
	ph12 = fields.Char(string="Phrase 12", default="DECIDE")
	ph13 = fields.Char(string="Phrase 13", default="Article 1 : ")
	ph14 = fields.Char(string="Phrase 14", default="Un congé administratif de trente (30) jours à solde entière est accordé au titre d’une période de travail correspondante, aux agents de la direction régionale de l’INFPE de l’Est ci- après :")


	@api.onchange('t1')
	def check_t1(self):
		if self.t1 :
			self.t1 = self.t1.upper()