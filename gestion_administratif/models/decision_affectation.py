from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import re


class decisionAffectation(models.Model):
	_name="document.decisionaffectation"
	_description = "Décision d'affectation"

	t2 = fields.Char(string="Titre", default="LE DIRECTEUR GENERAL,")
	p1 = fields.Char(string="Phrase 1", default="Vu	la Constitution ;")
	p2 = fields.Char(string="Phrase 2", default="Vu	la Charte de la Transition du 1er mars 2022 ;")
	p3 = fields.Char(string="Phrase 3", default="Vu	le décret n°2022-041PRES du 03 mars 2022 portant nomination du Premier Ministre ;")
	p4 = fields.Char(string="Phrase 4", default="Vu	le décret n°2022-053/PRES/PM du 05 mars 2022 portant composition du Gouvernement ;")
	p5 = fields.Char(string="Phrase 5", default="Vu	la loi n°081-2015/CNT du 24 novembre 2015, portant statut général de la fonction publique d’Etat ;")
	p6 = fields.Char(string="Phrase 6", default="Vu	la loi n°033-2008/AN du 22 mai 2008, portant régime juridique applicable aux emplois et aux agents des établissements publics de l’Etat ;")
	p7 = fields.Char(string="Phrase 7", default="Vu	la loi organique n°073-2015/CNT du 6 novembre 2015 relative aux lois de finances ;")
	p8 = fields.Char(string="Phrase 8", default="Vu	la loi n°010-2013/AN du 30 avril 2013 portant règles de création des catégories d’établissements publics ;")
	p9 = fields.Char(string="Phrase 9", default="Vu	le décret n°2016-598/PRES/PM/MINEFID du 8 juillet 2016 portant règlement général sur la comptabilité publique ;")
	p10 = fields.Char(string="Phrase 10", default="Vu	le décret n°2016-599/PRES/PM/MINEFID du 8 juillet 2016 portant régime juridique applicable aux comptables publics ;")
	p11 = fields.Char(string="Phrase 11", default="Vu	le décret n°2019-782/PRES/PM/MINEFID du 18 juillet 2019 portant régime financier et comptable des Etablissements publics au Burkina Faso ;")
	p12 = fields.Char(string="Phrase 12", default="Vu	le décret n°2014-613/PRES/PM/MEF du 24 juillet 2014 portant statut général des Etablissements publics de l’Etat à caractère Administratif (EPA) ; ")
	p13 = fields.Char(string="Phrase 13", default="Vu   le décret n°2020-0832/PRES/PM/MINEFID/MENAPLN du 5 octobre 2020 portant création de l’Institut national de Formation des Personnels de l’Education (INFPE);")
	p14 = fields.Char(string="Phrase 14", default="Vu	le décret n°2020-0871/PRES/PM/MENAPLN/MINEFID du 12 octobre 2020 portant approbation des statuts de l’Institut national de Formation des Personnels de l’Education (INFPE) ;")
	p15 = fields.Char(string="Phrase 15", default="Vu	le décret n°2021-0134/PRES/PM/MENAPLN du 19 mars 2021 portant nomination de Directeurs généraux ;")
	p16 = fields.Char(string="Phrase 16", default="Vu 		l’arrêté n°2021-113/MENAPLN/SG/INFPE du 30 avril 2021 portant organisation et fonctionnement de l’Institut national de Formation des Personnels de l’Education ;")
	p17 = fields.Char(string="Phrase 17", default="DECIDE")
	p18 = fields.Char(string="Phrase 18", default="Article 2 :")
	p19 = fields.Char(string="Phrase 19", default="la présente décision prend effet pour compter de la date de prise de service des intéressés ; ")
	p20 = fields.Char(string="Phrase 20", default="Article 3 :")
	p21 = fields.Char(string="Phrase 21", default="le Secrétaire général est chargé de l’exécution de la présente décision qui sera enregistrée, publiée et communiquée partout où besoin sera.")
	p22 = fields.Char(string="Phrase 22", default="")
	p23 = fields.Char(string="Phrase 23", default="")
	p24 = fields.Char(string="Phrase 24", default="Loumbila, le ")
	p25 = fields.Char(string="Phrase 25", default="Ampliations :")
	p26 = fields.Char(string="Phrase 26", default="DR")
	p27 = fields.Char(string="Phrase 27", default="01")
	p28 = fields.Char(string="Phrase 28", default="DR-PLC")
	p29 = fields.Char(string="Phrase 29", default="01")
	p30 = fields.Char(string="Phrase 30", default="DR-NORD")
	p31 = fields.Char(string="Phrase 31", default="01")
	p32 = fields.Char(string="Phrase 32", default="Le Directeur Général")
	p33 = fields.Char(string="Phrase 33", default="Dr Etienne OUEDRAOGO")
	p34 = fields.Char(string="Phrase 34", default="Chevalier de l’Ordre de Mérite")
	emp = fields.One2many('document.agentaffecte','deci_af_id',string="Employe")

	@api.onchange('t2')
	def check_t2(self):
		if self.t2 :
			self.t2 = self.t2.upper()



class posteAffectation(models.Model):
	_name="document.posteaffectation"
	_description="Gestion des postes d'affectation"
	_rec_name="n_poste"


	n_poste = fields.Char(string="Nouveau poste d'affectation")



class agentAffecte(models.Model):
	_name="document.agentaffecte"
	_description="Agent affecte"

	em = fields.Many2one('hr.employee',string="Agent")
	mat = fields.Char(string="Matricule",related="em.identification_id",readonly=True)
	emploi = fields.Char(string="Emploi",related="em.job_title",readonly=True)
	poste_aff = fields.Many2one('document.posteaffectation',string="Poste d'affectation")
	deci_af_id = fields.Many2one('document.decisionaffectation',string="Decision")




class decisionNomination(models.Model):
	_name="document.decisionnomination"
	_description = "Décision nomination"

	t4 = fields.Char(string="Titre", default="LE DIRECTEUR GENERAL DE L’INSTITUT NATIONAL DE FORMATION DES PERSONNELS DE L’EDUCATION,")
	pr1 = fields.Char(string="Phrase 1", default="Vu	la Constitution ;")
	pr2 = fields.Char(string="Phrase 2", default="Vu	le décret n°2021-1296/PRES du 10 décembre 2021 portant nomination du Premier Ministre ;")
	pr3 = fields.Char(string="Phrase 3", default="Vu	le décret n°2021-1297/PRES/PM du 13 décembre 2021 portant composition du Gouvernement ;")
	pr4 = fields.Char(string="Phrase 4", default="Vu	le décret n°2021-1359/PRES/PM/SGG-CM du 31 décembre 2021 portant attributions des membres du Gouvernement ;")
	pr5 = fields.Char(string="Phrase 5", default="Vu	la loi organique n°073-2015/CNT du 6 novembre 2015 relative aux lois de finances ;")
	pr6 = fields.Char(string="Phrase 6", default="Vu	la loi n°010-2013/AN du 30 avril 2013 portant règles de création des catégories d’établissements publics ;")
	pr7 = fields.Char(string="Phrase 7", default="Vu	le décret n°2016-598/PRES/PM/MINEFID du 8 juillet 2016 portant règlement général sur la comptabilité publique ;")
	pr8 = fields.Char(string="Phrase 8", default="Vu	le décret n°2016-599/PRES/PM/MINEFID du 8 juillet 2016 portant régime juridique applicable aux comptables publics ;")
	pr9 = fields.Char(string="Phrase 9", default="Vu	le décret n°2019-782/PRES/PM/MINEFID du 18 juillet 2019 portant régime financier et comptable des Etablissements publics au Burkina Faso ;")
	pr10 = fields.Char(string="Phrase 10", default="Vu  le décret n°2014-613/PRES/PM/MEF du 24 juillet 2014 portant statut général des Etablissements publics de l’Etat à caractère Administratif (EPA) ; ")
	pr11 = fields.Char(string="Phrase 11", default="Vu  le décret n°2021-1056/PRES/PM/MENAPLN du 21 octobre 2021 portant organisation du Ministère de l’Éducation nationale, de l’Alphabétisation et de la Promotion des Langues nationales;")
	pr12 = fields.Char(string="Phrase 12", default="Vu  le décret n°2020-0832/PRES/PM/MINEFID/MENAPLN du 5 octobre 2020 portant création de l’Institut national de Formation des Personnels de l’Education (INFPE) ;")
	pr13 = fields.Char(string="Phrase 13", default="Vu  le décret n°2020-0871/PRES/PM/MENAPLN/MINEFID du 12 octobre 2020 portant approbation des statuts de l’Institut national de Formation des Personnels de l’Education (INFPE) ;")
	pr14 = fields.Char(string="Phrase 14", default="Vu  le décret n°2021-0134/PRES/PM/MENAPLN du 19 mars 2021 portant nomination de Directeurs généraux ;")
	pr15 = fields.Char(string="Phrase 15", default="Vu  l’arrêté n°2021-113/MENAPLN/SG/INFPE du 30 avril 2021 portant organisation et fonctionnement de l’Institut national de Formation des Personnels de l’Education ;")
	pr16 = fields.Char(string="Phrase 16", default="Vu 	la délibération n°2021-…./INFPE/CA du ……… portant création de caisses de menues dépenses auprès des structures de l’INFPE ;")
	pr17 = fields.Char(string="Phrase 17", default="DECIDE")
	pr18 = fields.Char(string="Phrase 18", default="Article 1 :")
	pr19 = fields.Char(string="Phrase 19", default="Les Responsables ci-après désignés sont nommés Gestionnaires des Caisses de menues dépenses cumulativement à leurs fonctions de chefs de services.")
	pr20 = fields.Char(string="Phrase 20", default="Article 2 :")
	pr21 = fields.Char(string="Phrase 21", default="la présente décision prend effet pour compter de la date de prise de service des intéressés ; ")
	pr22 = fields.Char(string="Phrase 22", default="Article 3 :")
	pr23 = fields.Char(string="Phrase 23", default="le Secrétaire général est chargé de l’exécution de la présente décision qui sera enregistrée, publiée et communiquée partout où besoin sera.")
	pr24 = fields.Char(string="Phrase 24", default="Loumbila, le ")
	pr25 = fields.Char(string="Phrase 25", default="Ampliations:")
	pr26 = fields.Char(string="Phrase 26", default="DRH")
	pr27 = fields.Char(string="Phrase 27", default="01")
	pr28 = fields.Char(string="Phrase 28", default="AC")
	pr29 = fields.Char(string="Phrase 29", default="01")
	pr30 = fields.Char(string="Phrase 30", default="DCMEF")
	pr31 = fields.Char(string="Phrase 31", default="01")
	pr32 = fields.Char(string="Phrase 32", default="DRINFPE")
	pr33 = fields.Char(string="Phrase 33", default="08")
	pr34 = fields.Char(string="Phrase 34", default="Le Directeur Général")
	pr35 = fields.Char(string="Phrase 35", default="Dr Etienne OUEDRAOGO")
	pr36 = fields.Char(string="Phrase 36", default="Chevalier de l'Ordre de Mérite")
	agent_id = fields.One2many('document.agentnomme','nomination',string="Agent")

	@api.onchange('t4')
	def check_t4(self):
		if self.t4 :
			self.t4 = self.t4.upper()


class agentNomme(models.Model):
	_name="document.agentnomme"
	_description="Agent nomme"

	employe_id = fields.Many2one('hr.employee',string="Agent")
	matricule = fields.Char(string="Matricule",related="employe_id.identification_id",readonly=True)
	emplois = fields.Char(string="Emploi",related="employe_id.job_title",readonly=True)
	poste_id = fields.Many2one('document.posteaffectation',string="Nouveau poste")
	nomination = fields.Many2one('document.decisionnomination',string="Nomination")
