from odoo import fields, api, models, tools, _
import string
from datetime import datetime, date
import pdb
import calendar
from calendar import monthrange
from odoo.exceptions import UserError, ValidationError
from math import *


# Creation de la classe fonction avec ses attributs
class HrFonction(models.Model):
    _name = "hr_fonctionss"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    # code = fields.Char(string = 'Code',size = 2,required = True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# Creation de la classe emploi avec ses attributs
class HrEmploi(models.Model):
    _name = "hr_emploi"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    # code = fields.Char(string = 'Code',size = 2,required = True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# from Util import global_variables


# Creation de la classe HR_INDEMNITE POUR l'attribution des indemnités d'un employé
class HrEmployeeIndemnites(models.Model):
    _name = "hr_employee_indemnite"
    emp_id = fields.Many2one('hr.employee', string='Employee')
    x_mntnt_idemn = fields.Char(string='Montant')
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True)


# Classe pour gerer le compteur pour les matricules
class Compteur_employee(models.Model):
    _name = "hr_compteur_matricules"
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_matricule = fields.Integer()


# Creation de la classe hr_employee_ fichier_oint_line permettant d'ajouter un  fichier prouvant le ch    changement de grade
class HrEmployeePiece(models.Model):
    _name = "hr_employee_piece"
    x_employee_id = fields.Many2one('hr.employee', string='Employee')
    objet_grade = fields.Text(string='Objet', required=True)
    fichier_joint = fields.Binary(string='Pièce jointe', attachment=True, required=True)


# Creation de la classe hr_employee_ fichier_oint_line permettant d'ajouter un  acte de detachement
class HrEmployeePieceDetachement(models.Model):
    _name = "hr_piece_detachement"
    x_employees_id = fields.Many2one('hr.employee', string='Employee')
    date_acte = fields.Date(string="Date acte")
    date_effet = fields.Date(string="Date effet")
    date_fin = fields.Date(string="Date fin")
    ref_acte = fields.Char(string="Ref acte")
    fichier_joint = fields.Binary(string='Joindre acte', attachment=True)

    # fonction de calcul de la date de in du detachement qui est de cinq ans-
    @api.onchange("date_effet")
    def compute_annee_detachement(self):
        if self.date_effet:
            date1 = self.date_effet.strftime("%Y-%m-%d")
            date2 = self.date_effet.year + 3
            if self.date_effet.day == 1:
                if self.date_effet.month == 1:
                    jour = 31
                    annee = self.date_effet.year + 3 - 1
                    self.date_fin = datetime(annee, 12, jour, 0, 0, 0, 0).date()
                else:
                    mois = self.date_effet.month - 1
                    year = int(self.date_effet.year)
                    month = int(self.date_effet.month)
                    jour = calendar.monthrange(year, month)[1]
                    self.date_fin = datetime(date2, mois, jour, 0, 0, 0, 0).date()
            else:
                self.date_fin = datetime(date2, self.date_effet.month, (self.date_effet.day - 1), 0, 0, 0, 0).date()


# Creation de la classe hr_employee_ decret_nomination permettant d'ajouter un  acte de nomination
class HrEmployeeDecretNomination(models.Model):
    _name = "hr_decret_nomination"
    x_employees_id = fields.Many2one('hr.employee', string='Employee')
    date_nomination = fields.Date(string="Date nomination")
    date_effet = fields.Date(string="Date effet")
    date_fin = fields.Date(string="Date fin")
    ref_acte = fields.Char(string="Ref acte nomination")
    fichier_joint = fields.Binary(string='Joindre acte', attachment=True)
    etat_nomination = fields.Selection([
        (1, "En cours"),
        (2, "Terminé"),
    ], required=True, string="Etat Nomination", default=1)


# Creation de la classe hr_employee_ fichier_oint_line permettant d'ajouter un  acte de decision
class HrEmployeePieceDecision(models.Model):
    _name = "hr_piece_disposition"
    x_employees_id = fields.Many2one('hr.employee', string='Employee')
    date_acte_dec = fields.Date(string="Date acte disposition")
    date_effet_dec = fields.Date(string="Date effet disposition")
    date_fin_dec = fields.Date(string="Date fin disposition")
    ref_acte_dec = fields.Char(string="Ref acte disposition")
    fichier_joint_dec = fields.Binary(string='Joindre acte disposition', attachment=True)


# Creation de la classe hr_employee_line permettant d'ajouter une ligne avec ses attributs comme historisation du grade de l'employé
class HrEmployeeLineHistorique(models.Model):
    _name = "hr_employee_historique"
    employee_id = fields.Many2one('hr.employee', string='Employee')
    x_categorie_c_id = fields.Many2one('hr_categorie', string='Catégorie')
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle')
    x_echellon_c_id = fields.Many2one('hr_echellon', string='Echelon')
    date_modif = fields.Char(string="Date effet")
    date_op = fields.Char(string="Date modification")
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='Année',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))


# Creation de la classe hr_employee_ fichier_joint_line permettant de suivre le dossier individuel du personnel
class HrEmployeeDossierIndividuel(models.Model):
    _name = "hr_dossier_individuel"
    x_employees_id = fields.Many2one('hr.employee', string='Employee')
    date_op = fields.Date(string="Date", default=date.today())
    objet_ligne = fields.Char(string="Intitulé")
    fichier_joint = fields.Binary(string='Joindre Fichier', attachment=True)


# heritage type de contrat
class HrTypeContrats(models.Model):
    _inherit = 'hr.contract.type'
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_structure_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)


# Creation de la classe grille des contractuels du burkina faso avec ses attributs
class HrGrilleSalarialeContractuel(models.Model):
    _name = "hr_grillesalariale_contractuel"
    _rec_name = "x_salbase_ctrt"
    x_class_c_id = fields.Many2one('hr_classe', string='Classe')
    x_indice_c = fields.Float(string="Indice")
    x_categorie_c_id = fields.Many2one('hr_categorie', string='Catégorie', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_echellon_c_id = fields.Many2one('hr_echellon', string='Echelon', required=True)
    x_salbase_ctrt = fields.Float(string="Salaire Base", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    active = fields.Boolean(string="Etat", default=True)


# heritage de la classe contrat
class Contract(models.Model):
    _inherit = "hr.contract"
    date_signature = fields.Date(string="Date signature acte/decision d'engagement")
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_structure_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)
    # x_solde_indiciaire = fields.Float(string = "Salaire de base")
    x_solde_indiciaire_ctrct = fields.Float(related="employee_id.x_solde_indiciaire_ctrct", string="Salaire de base")
    x_emolument_ctrct_net = fields.Float(string="Emolument Net", related="employee_id.x_emolument_ctrct_net")

    # Declaration variables Indemnités
    x_indem_resp = fields.Float(string="Indemn.Resp", related="employee_id.x_indem_resp")
    x_indem_astr = fields.Float(string="Indemn.Astreinte", related="employee_id.x_indem_astr")
    x_indem_techn = fields.Float(string="Indemn.Technicité", related="employee_id.x_indem_techn")
    x_indem_specif = fields.Float(string="Indemn.Spécifique GRH", related="employee_id.x_indem_specif")
    x_indem_spec_inspect_trav = fields.Float(string="Indemn.Spécifique IT",
                                             related="employee_id.x_indem_spec_inspect_trav")
    x_indem_spec_inspect_irp = fields.Float(string="Indemn.Spécifique IRP",
                                            related="employee_id.x_indem_spec_inspect_irp")
    x_indem_spec_inspect_ish = fields.Float(string="Indemn.Spécifique ISH",
                                            related="employee_id.x_indem_spec_inspect_ish")
    x_indem_spec_inspect_ifc = fields.Float(string="Indemn.Spécifique IFC",
                                            related="employee_id.x_indem_spec_inspect_ifc")
    x_indem_prime_rendement = fields.Float(string="Prime Rendement", related="employee_id.x_indem_prime_rendement")
    x_indem_loge = fields.Float(string="Indemn.Logement", related="employee_id.x_indem_loge")
    x_indem_transp = fields.Float(string="Indemn.Transport", related="employee_id.x_indem_transp")
    x_indem_inform = fields.Float(string="Indemn.Informatique", related="employee_id.x_indem_inform")
    x_indem_exploit = fields.Float(string="Indemn.Exploitation-Réseau", related="employee_id.x_indem_exploit")
    x_indem_finance = fields.Float(string="Indemn.Resp.Financière", related="employee_id.x_indem_finance")
    x_indem_garde = fields.Float(string="Indemn.Garde", related="employee_id.x_indem_garde")
    x_indem_risque = fields.Float(string="Indemn.Risque.Contagion", related="employee_id.x_indem_risque")
    x_indem_suj = fields.Float(string="Indemn.Sujétion Géographique", related="employee_id.x_indem_suj")
    x_indem_form = fields.Float(string="Indemn.Formation", related="employee_id.x_indem_form")
    x_indem_caisse = fields.Float(string="Indemn.Caisse", related="employee_id.x_indem_caisse")
    x_indem_veste = fields.Float(string="Indemn.Vestimentaire", related="employee_id.x_indem_veste")
    x_mnt_taux_retenu_emolmt = fields.Float(string="Montant Taux", related="employee_id.x_mnt_taux_retenu_emolmt")

    x_allocation_familial = fields.Float(string="Allocation familiale", related="employee_id.x_allocation_familial")

    # Calcul UITS

    # Total indemnités = Total de toutes les indemnités auxquelles l'employé à droit
    x_total_indemnites = fields.Float(string="Total Indemn", related="employee_id.x_total_indemnites", store=True)
    # total_indemnite = fields.Float(compute='',string = "Total Indemnité", readonly = True, store=True)
    # Remuneration total = Salaire de base + Total indemnités

    # Montant CNSS = 5.5% de la remuneration total
    x_mnt_cnss = fields.Float(string="Montant CNSS", related="employee_id.x_mnt_cnss")

    # Montant CARFO = 8% de la remuneration total
    x_mnt_carfo = fields.Float(string="Montant CARFO", related="employee_id.x_mnt_carfo")
    # x_mnt_carfo_p = fields.Float(string="Montant CARFO", related="employee_id.x_mnt_carfo_p")

    # Rappel total = somm rappel(indemnitéss et salaire)
    mnt_total_rappel = fields.Float(string="Montant total Rappel", related="employee_id.mnt_total_rappel")

    # Rappel total = somm rappel(indemnitéss et salaire)
    mnt_total_trop_percu = fields.Float(string="Montant total trop perçu", related="employee_id.mnt_total_trop_percu")

    x_base_imposable_ctrct = fields.Float(string="Base imposable", related="employee_id.x_base_imposable_ctrct")

    # Retenue IUTS
    x_retenue_iuts = fields.Float(string="Retenue IUTS", related="employee_id.x_retenue_iuts")

    # Montant charge
    x_montant_charge = fields.Float(string="Montant charge", related="employee_id.x_montant_charge")

    # IUTS Net
    x_iuts_net = fields.Float(string="IUTS Net", related="employee_id.x_iuts_net")

    # Net à payer contractuel
    x_net_payer_ctrct = fields.Float(string="Net à payer", related="employee_id.x_net_payer_ctrct")

    # total retenues cnss
    x_total_retenue_cnss = fields.Float(string="Total retenues CNSS", related="employee_id.x_total_retenue_cnss")

    # total retenues carfo
    x_total_retenue_carfo = fields.Float(string="Total retenues CARFO", related="employee_id.x_total_retenue_carfo")


# Creation de la classe motif avec ses attributs
class HrMotif(models.Model):
    _name = "hr_motif"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of motif.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# Creation de la classe nature avec ses attributs
class HrNature(models.Model):
    _name = "hr_nature"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of nature.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# Creation de la classe assurance avec ses attributs
class HrAssuranceEmployee(models.Model):
    _name = "hr_assurance"
    name = fields.Char(string="Libéllé long", size=65, required=True)
    libcourt = fields.Char(string="Libéllé court", size=35, required=True)
    active = fields.Boolean(string="Etat", default=True)


# Creation de la classe type retenue avec ses attributs
class HrTypeRetenue(models.Model):
    _name = "hr_typeretenue"
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libéllé long")
    active = fields.Boolean(string="Etat", default=True)


# Creation de la classe type rappel avec ses attributs
class HrTypeRappel(models.Model):
    _name = "hr_typerappel"
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libéllé long")
    active = fields.Boolean(string="Etat", default=True)


# Classe pour gerer les indemnités de responsabilité
class HrParametrageIndemniteResponsabilite(models.Model):
    _name = "hr_paramindemniteresp"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de responsabilité")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    # x_emploi_id = fields.Many2one('hr_emploi', string = 'Emploi', required = False)
    # x_categorie_c_id = fields.Many2one('hr_categorie', string = "Catégorie", required = True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    # x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required = True)
    # x_volum_fond_manipule_id = fields.Many2one('hr_fond', string='Fond manipulé')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_fonction_id', '=', self.x_fonction_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_resp = vals['x_taux']
        return super(HrParametrageIndemniteResponsabilite, self).write(vals)

# Classe pour gerer les indemnités de d'astreintes liées à l'emploi
class HrParametrageIndemniteAstreinte(models.Model):
    _name = "hr_paramindemniteastr"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité astreinte")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
                [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
                 ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
                 ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_astr = vals['x_taux']
        return super(HrParametrageIndemniteAstreinte, self).write(vals)

# Classe pour gerer les indemnités de d'astreintes liées à la fonction
class HrParametrageIndemniteAstreintes(models.Model):
    _name = "hr_paramindemniteastrs"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité astreinte")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')


# Classe pour gerer les indemnités de de logement
class HrParametrageIndemniteLogement(models.Model):
    _name = "hr_paramindemnitelogement"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de logement")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_loge = vals['x_taux']
        return super(HrParametrageIndemniteLogement, self).write(vals)

# Classe pour gerer les indemnités de de logement liées à la fonction
class HrParametrageIndemniteLogements(models.Model):
    _name = "hr_paramindemnitelogements"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de logement")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités de technicité
class HrParametrageIndemniteTecnicite(models.Model):
    _name = "hr_paramindemnitetechnicite"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de technicité")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_techn = vals['x_taux']
        return super(HrParametrageIndemniteTecnicite, self).write(vals)

# Classe pour gerer les indemnités de technicité liées à la fonction
class HrParametrageIndemniteTecnicites(models.Model):
    _name = "hr_paramindemnitetechnicites"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de technicité")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités spécifiques GRH
class HrParametrageIndemniteSpecifiqueGRH(models.Model):
    _name = "hr_paramindemnitespecifique"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité spécifique GRH")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_specif = vals['x_taux']
        return super(HrParametrageIndemniteSpecifiqueGRH, self).write(vals)

# Classe pour gerer les indemnités spécifiques  IT
class HrParametrageIndemniteSpecifiqueIT(models.Model):
    _name = "hr_paramindemnitespecifique_it"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité spécifique IT")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_spec_inspect_trav = vals['x_taux']
        return super(HrParametrageIndemniteSpecifiqueIT, self).write(vals)

# Classe pour gerer les indemnités spécifiques  IFC (Indemnité Forfaitaire Compensatrice)
class HrParametrageIndemniteSpecifiqueIFC(models.Model):
    _name = "hr_paramindemnitespecifique_ifc"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité spécifique ICF")]), readonly=True)
    # x_emploi_id = fields.Many2one('hr_emploi', string = 'Emploi', required = True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    # x_zone_id = fields.Many2one('hr_zone', string = 'Zone', required = True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    # x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required = True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_spec_inspect_ifc = vals['x_taux']
        return super(HrParametrageIndemniteSpecifiqueIFC, self).write(vals)

# Classe pour gerer les indemnités spécifiques  IRP (Indemnité Responsabilite Pecunière)
class HrParametrageIndemniteSpecifiqueIRP(models.Model):
    _name = "hr_paramindemnitespecifique_irp"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité spécifique IRP")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_spec_inspect_irp = vals['x_taux']
        return super(HrParametrageIndemniteSpecifiqueIRP, self).write(vals)

# Classe pour gerer les indemnités spécifiques  ISH (Indemnité Spécifique Harmonisée pour le  Personnel du MENA et du MESRSI)
class HrParametrageIndemniteSpecifiqueISH(models.Model):
    _name = "hr_paramindemnitespecifique_ish"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité spécifique ISH")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_spec_inspect_ish = vals['x_taux']
        return super(HrParametrageIndemniteSpecifiqueISH, self).write(vals)

# Classe pour gerer les indemnités spécifiques liées à la fonction
class HrParametrageIndemniteSpecifiques(models.Model):
    _name = "hr_paramindemnitespecifiques"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité spécifique")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités de transport
class HrParametrageIndemniteTransport(models.Model):
    _name = "hr_paramindemnitetransport"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de transport")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')


# Classe pour gerer les indemnités de transport liées à la fonction
class HrParametrageIndemniteTransports(models.Model):
    _name = "hr_paramindemnitetransports"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de transport")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités de Informatique
class HrParametrageIndemniteInformatique(models.Model):
    _name = "hr_paramindemniteinformatique"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité informatique")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_inform = vals['x_taux']
        return super(HrParametrageIndemniteInformatique, self).write(vals)

# Classe pour gerer les indemnités de Informatique liées à la fonction
class HrParametrageIndemniteInformatiques(models.Model):
    _name = "hr_paramindemniteinformatiques"
    _rec_name = "x_type_indem_id"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité informatique")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités de Exploitation reseaux
class HrParametrageIndemniteExploiReseau(models.Model):
    _name = "hr_paramindemniteexploireseau"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité exploitation réseaux")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_exploit = vals['x_taux']
        return super(HrParametrageIndemniteAstreinte, self).write(vals)

# Classe pour gerer les indemnités de Exploitation reseauxliées à la fonction
class HrParametrageIndemniteExploiReseaus(models.Model):
    _name = "hr_paramindemniteexploireseaus"
    _rec_name = "x_type_indem_id"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité exploitation réseaux")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités de resp.financière
class HrParametrageIndemniteRespFinanciere(models.Model):
    _name = "hr_paramindemniterespfinanciere"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de responsabilité financière")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_finance = vals['x_taux']
        return super(HrParametrageIndemniteRespFinanciere, self).write(vals)

# Classe pour gerer les indemnités de resp.financière liées à la fonction
class HrParametrageIndemniteRespFinancieres(models.Model):
    _name = "hr_paramindemniterespfinancieres"
    _rec_name = "x_type_indem_id"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de responsabilité financière")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités de garde
class HrParametrageIndemniteGarde(models.Model):
    _name = "hr_paramindemnitegarde"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de garde")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_garde = vals['x_taux']
        return super(HrParametrageIndemniteGarde, self).write(vals)

# Classe pour gerer les indemnités de gardeliée à la fonction
class HrParametrageIndemniteGardes(models.Model):
    _name = "hr_paramindemnitegardes"
    _rec_name = "x_type_indem_id"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de garde")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités de risque de contagion
class HrParametrageIndemniteRisque(models.Model):
    _name = "hr_paramindemniterisquecontagion"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de contagion et de contamination")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_risque = vals['x_taux']
        return super(HrParametrageIndemniteRisque, self).write(vals)

# Classe pour gerer les indemnités de risque de contagion liée à la fonction
class HrParametrageIndemniteRisques(models.Model):
    _name = "hr_paramindemniterisquecontagions"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de contagion et de contamination")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités de sujetion de contagion
class HrParametrageIndemniteSujetion(models.Model):
    _name = "hr_paramindemnitesujetion"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de sujétion géographique")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_suj = vals['x_taux']
        return super(HrParametrageIndemniteSujetion, self).write(vals)

# Classe pour gerer les indemnités de sujetion de contagion liée à la fonction
class HrParametrageIndemniteSujetions(models.Model):
    _name = "hr_paramindemnitesujetions"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de sujétion géographique")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités de formation spécialisée
class HrParametrageIndemniteFormationSp(models.Model):
    _name = "hr_paramindemniteformation"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de formation spécialisée")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id), ('x_zone_id', '=', self.x_zone_id.id),
             ('x_echelle_c_id', '=', self.x_echelle_c_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_form = vals['x_taux']
        return super(HrParametrageIndemniteFormationSp, self).write(vals)

# Classe pour gerer les indemnités de formation spécialisée liée à la fonction
class HrParametrageIndemniteFormationSps(models.Model):
    _name = "hr_paramindemniteformations"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de formation spécialisée")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités de caisse
class HrParametrageIndemniteCaisse(models.Model):
    _name = "hr_paramindemnitecaisse"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de caisse")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')

    @api.multi
    def write(self, vals):
        employees = self.env['hr.employee'].search(
            [('x_emploi_id', '=', self.x_emploi_id.id),
             ('x_categorie_c_id', '=', self.x_categorie_c_id.id), ('company_id', '=', self.company_id.id)])
        for emp in employees:
            emp.x_indem_caisse = vals['x_taux']
        return super(HrParametrageIndemniteCaisse, self).write(vals)

# Classe pour gerer les indemnités de caisse  liée à la fonction
class HrParametrageIndemniteCaisses(models.Model):
    _name = "hr_paramindemnitecaisses"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité de caisse")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


# Classe pour gerer les indemnités vestimentaire
class HrParametrageIndemniteVestimentaire(models.Model):
    _name = "hr_paramindemnitevest"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité vestimentaire")]), readonly=True)
    x_emploi_id = fields.Many2one('hr_emploi', string='Emploi', required=True)
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=True)
    x_categorie_c_id = fields.Many2one('hr_categorie', string="Catégorie", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')


# Classe pour gerer les indemnités de vestimentaire liée à la fonction
class HrParametrageIndemnitevestimentaires(models.Model):
    _name = "hr_paramindemnitevests"
    _rec_name = "x_type_indem_id"
    x_type_indem_id = fields.Many2one('hr_typeindemnite', string='Type Indemnité', required=True,
                                      default=lambda self: self.env['hr_typeindemnite'].search(
                                          [('name', '=', "Indemnité vestimentaire")]), readonly=True)
    x_fonction_id = fields.Many2one('hr_fonctionss', string='Fonction', required=True)
    x_taux = fields.Float(string='Taux à servir', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string='N°Exercice')
    x_zone_id = fields.Many2one('hr_zone', string='Zone', required=True)


class HrDepartment(models.Model):
    _inherit = 'hr.department'
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_structure_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)
    code = fields.Char(string="Code", required=True)


# Creation de la classe service avec ses attributs
class RefService(models.Model):
    _name = "hr_service"
    x_direction_id = fields.Many2one('hr.department', 'Département/Direction', required=True)
    code = fields.Char(string="code", required=True, size=65)
    name = fields.Char(string="Libéllé long", required=True, size=65)
    libcourt = fields.Char(string="Libéllé court", required=True, size=35)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)
    est_stock = fields.Selection([
        ('1', 'Oui'),
        ('2', 'Non'),
    ], string="Est Service du Stock ?", default='2', required=True)
    responsable = fields.Many2one('res.users', string='Responsable')


# Creation de la classe unité avec ses attributs
class RefUnite(models.Model):
    _name = "hr_unite"
    x_service_id = fields.Many2one('hr_service', 'Service', required=True)
    code = fields.Char(string="code", required=True, size=65)
    name = fields.Char(string="Libéllé long", required=True, size=65)
    libcourt = fields.Char(string="Libéllé court", required=True, size=35)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)
    responsable = fields.Many2one('res.users', string='Responsable')


# Creation de la classe section avec ses attributs
class RefSection(models.Model):
    _name = "hr_section"
    x_unite_id = fields.Many2one('hr_unite', 'Unité', required=True)
    code = fields.Char(string="code", required=True, size=65)
    name = fields.Char(string="Libéllé long", required=True, size=65)
    libcourt = fields.Char(string="Libéllé court", required=True, size=35)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)
    responsable = fields.Many2one('res.users', string='Responsable')


# creation table pour contenir le nombre d'année de depart a la retraite des employés
class HrNbreAnnee(models.Model):
    _name = 'hr_nbreannee'
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_structure_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)
    name = fields.Integer(string="Nombre année", required=True)


# Creation de la classe registre des employés avec ses attributs
class HrRegistreEmploye(models.Model):
    _name = "hr_regemployes"
    name = fields.Many2one('hr.payroll.structure', string='Type employé', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_ids = fields.One2many('hr_regemployes_line', 'x_regemp_id', string="Liste des élements")
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)
    date_imp = fields.Datetime('Date/heure impression', default=datetime.today())
    x_direction_id = fields.Many2one('hr.department', string='Direction')
    x_service_id = fields.Many2one('hr_service', string='Service')

    def action_rech(self):
        if self.name:
            x_struct_id = int(self.company_id.id)
            print('x_struct_id', x_struct_id)
            x_type_id = int(self.name)
            print('x_type_id', x_type_id)
            x_ty = str(self.name.name)
            print('x_ty', x_ty)
            x_direction = int(self.x_direction_id)
            print('id direction', x_direction)
            x_service = int(self.x_service_id)
            print('id service', x_service)
            for vals in self:
                if x_ty == 'Fonctionnaire Detaché' or x_ty == 'Fonctionnaire Mis à Disposition':
                    if x_direction != False and x_service != False:
                        print('bonjour1')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule, (E.matricule_genere) as matricule_ctrct,(E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi, (D.name) as departement, (S.name) as service, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D, hr_service S, hr_zone Z, hr_payroll_structure ST WHERE E.x_categorie_id = C.id AND E.x_echelle_id = EC.id AND E.x_echellon_id = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.hr_service = S.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and ST.name = '%s' and E.x_direction_id = %d and E.hr_service = %d and E.company_id = %d""" % (
                                x_ty, x_direction, x_service, x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': line['service'], 'zone': line['zone'],
                                                  'type': line['structure']}))
                        self.x_line_ids = result
                    elif x_direction != False and x_service == False:
                        print('bonjour2')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule, (E.matricule_genere) as matricule_ctrct,(E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi, (D.name) as departement, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D, hr_zone Z, hr_payroll_structure ST WHERE E.x_categorie_id = C.id AND E.x_echelle_id = EC.id AND E.x_echellon_id = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and ST.name = '%s' and E.x_direction_id = %d and E.company_id = %d""" % (
                                x_ty, x_direction, x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': '', 'zone': line['zone'], 'type': line['structure']}))
                        self.x_line_ids = result


                    elif x_direction == False and x_service == False:
                        print('bonjour4')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule, (E.matricule_genere) as matricule_ctrct,(E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi, (D.name) as departement, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D, hr_zone Z, hr_payroll_structure ST WHERE E.x_categorie_id = C.id AND E.x_echelle_id = EC.id AND E.x_echellon_id = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and ST.name = '%s' and E.company_id = %d""" % (
                                x_ty, x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': '', 'zone': line['zone'], 'type': line['structure']}))
                        self.x_line_ids = result

                elif x_ty == 'Contractuel' or x_ty == 'CONTRACTUEL':
                    if x_direction != False and x_service != False:
                        print('bonjour1')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule, (E.matricule_genere) as matricule_ctrct,(E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi,(D.name) as departement, (S.name) as service, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D, hr_service S, hr_zone Z, hr_payroll_structure ST WHERE E.x_categorie_c_id = C.id AND E.x_echelle_c_id = EC.id AND E.x_echellon_c_id = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.hr_service = S.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and ST.name = '%s' and E.x_direction_id = %d and E.hr_service = %d and E.company_id = %d""" % (
                                x_ty, x_direction, x_service, x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': line['service'], 'zone': line['zone'],
                                                  'type': line['structure']}))
                        self.x_line_ids = result

                    elif x_direction != False and x_service == False:
                        print('bonjour2')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule, (E.matricule_genere) as matricule_ctrct,(E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi,(D.name) as departement, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D, hr_zone Z, hr_payroll_structure ST WHERE E.x_categorie_c_id = C.id AND E.x_echelle_c_id = EC.id AND E.x_echellon_c_id = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and ST.name = '%s' and E.x_direction_id = %d and E.company_id = %d""" % (
                                x_ty, x_direction, x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': '', 'zone': line['zone'], 'type': line['structure']}))
                        self.x_line_ids = result

                    elif x_direction == False and x_service == False:
                        print('bonjour3')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule, (E.matricule_genere) as matricule_ctrct,(E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi,(D.name) as departement, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D, hr_zone Z, hr_payroll_structure ST WHERE E.x_categorie_c_id = C.id AND E.x_echelle_c_id = EC.id AND E.x_echellon_c_id = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and ST.name = '%s' and E.company_id = %d""" % (
                                x_ty, x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': '', 'zone': line['zone'], 'type': line['structure']}))
                        self.x_line_ids = result

                elif x_ty == 'Tout Type':
                    if x_direction != False and x_service != False:
                        print('bonjour1')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule,(E.matricule_genere) as matricule_ctrct, (E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi,(D.name) as departement, (S.name) as service, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D, hr_service S, hr_zone Z, hr_payroll_structure ST  WHERE E.x_categorie_c_id = C.id AND E.x_echelle_c_id = EC.id AND E.x_echellon_c_id = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.hr_service = S.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and E.x_direction_id = %d and E.hr_service = %d and E.company_id = %d""" % (
                                x_direction, x_service, x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': line['service'], 'zone': line['zone'],
                                                  'type': line['structure']}))
                        self.x_line_ids = result

                    elif x_direction != False and x_service == False:
                        print('bonjour2')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule,(E.matricule_genere) as matricule_ctrct, (E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi,(D.name) as departement, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D, hr_zone Z, hr_payroll_structure ST  WHERE E.x_categorie_c_id = C.id AND E.x_echelle_c_id = EC.id AND E.x_echellon_c_id = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and E.x_direction_id = %d and E.company_id = %d""" % (
                                x_direction, x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': '', 'zone': line['zone'], 'type': line['structure']}))
                        self.x_line_ids = result

                    elif x_direction == False and x_service == False:
                        print('bonjour3')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule,(E.matricule_genere) as matricule_ctrct, (E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi,(D.name) as departement, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D, hr_zone Z, hr_payroll_structure ST  WHERE E.x_categorie_c_id = C.id AND E.x_echelle_c_id = EC.id AND E. = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and E.company_id = %d""" % (
                                x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': '', 'zone': line['zone'], 'type': line['structure']}))
                        self.x_line_ids = result

                # pour les hospitalo-universitaires
                else:
                    if x_direction != False and x_service != False:
                        print('bonjour1')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule,(E.matricule_genere) as matricule_ctrct, (E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi,(D.name) as departement, (S.name) as service, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D, hr_service S, hr_zone Z, hr_payroll_structure ST  WHERE E.x_categorie_c_id = C.id AND E.x_echelle_c_id = EC.id AND E.x_echellon_c_id = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.hr_service = S.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and ST.name = '%s' and E.x_direction_id = %d and E.hr_service = %d and E.company_id = %d""" % (
                                x_ty, x_direction, x_service, x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': line['service'], 'zone': line['zone'],
                                                  'type': line['structure']}))
                        self.x_line_ids = result

                    elif x_direction != False and x_service == False:
                        print('bonjour2')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule,(E.matricule_genere) as matricule_ctrct, (E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi,(D.name) as departement, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D,hr_zone Z, hr_payroll_structure ST  WHERE E.x_categorie_c_id = C.id AND E.x_echelle_c_id = EC.id AND E.x_echellon_c_id = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and ST.name = '%s' and E.x_direction_id = %d and E.company_id = %d""" % (
                                x_ty, x_direction, x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': '', 'zone': line['zone'], 'type': line['structure']}))
                        self.x_line_ids = result

                    elif x_direction == False and x_service == False:
                        print('bonjour3')
                        vals.env.cr.execute(
                            """SELECT (C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule,(E.matricule_genere) as matricule_ctrct, (E.genre) as genre, (E.situation_marital) as etat, (E.x_date_retraite) as date, (F.name) as fonction, (EM.name) as emploi,(D.name) as departement, (Z.name) as zone, (ST.name) as structure FROM hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_fonctionss F,hr_emploi EM, hr_department D,hr_zone Z, hr_payroll_structure ST  WHERE E.x_categorie_c_id = C.id AND E.x_echelle_c_id = EC.id AND E.x_echellon_c_id = ECH.id AND E.x_fonction_id = F.id AND E.x_emploi_id = EM.id AND E.x_direction_id = D.id AND E.x_zone_id = Z.id AND E.x_type_employe_id = ST.id and ST.name = '%s'and E.company_id = %d""" % (
                                x_ty, x_struct_id))
                        rows = vals.env.cr.dictfetchall()
                        result = []

                        # delete old payslip lines
                        vals.x_line_ids.unlink()
                        for line in rows:
                            result.append((0, 0, {'mat': line['matricule'], 'mat_ctrct': line['matricule_ctrct'],
                                                  'nom': line['employe'], 'categorie': line['categorie'],
                                                  'echelle': line['echelle'], 'echelon': line['echelon'],
                                                  'genre': line['genre'], 'eta_civil': line['etat'],
                                                  'retraite': line['date'], 'emploi': line['emploi'],
                                                  'fonction': line['fonction'], 'dep': line['departement'],
                                                  'service': '', 'zone': line['zone'], 'type': line['structure']}))
                        self.x_line_ids = result


class HrRegistreEmployeLine(models.Model):
    _name = "hr_regemployes_line"
    x_regemp_id = fields.Many2one('hr_regemployes')
    mat = fields.Char(string='Mlle Fonctionnaire', readonly=True)
    mat_ctrct = fields.Char(string='Mlle Contractuel', readonly=True)
    nom = fields.Char(string='Nom/Prénom(s)', readonly=True)
    categorie = fields.Char(string="Catégorie", readonly=True)
    echelle = fields.Char(string='Echelle', readonly=True)
    echelon = fields.Char(string='Echelon', readonly=True)
    genre = fields.Char(string='Genre', readonly=True)
    eta_civil = fields.Char('Etat', readonly=True)
    retraite = fields.Char('Retraite', readonly=True)
    emploi = fields.Char('Emploi', readonly=True)
    fonction = fields.Char('Fonction', readonly=True)
    dep = fields.Char('Département', readonly=True)
    service = fields.Char('Service', readonly=True)
    zone = fields.Char('Zone', readonly=True)
    type = fields.Char('Type employé', readonly=True)


class HRCreation(models.Model):
    _name = 'fction_procd'
    _auto = False

    @api.model
    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'fction_procd')
        self.env.cr.execute("""CREATE OR REPLACE FUNCTION public.get_salaire_de_base(
                x_classe character varying,
                x_cat character varying,
                x_echel character varying,
                x_echelon character varying)
                RETURNS void AS
                $BODY$
                DECLARE
                  Salaire VARCHAR;
                BEGIN
                      SELECT x_salbase INTO Salaire FROM hr_grillesalariale WHERE x_classees_id = x_classe and x_categorie_id = x_cat and x_echelle_id = x_echel and x_echellon_id = x_echelon;
                END; 
                $BODY$
                LANGUAGE plpgsql VOLATILE""")


# PARTIE EVALUATION DES EMPLOYÉS


# Definition des Classes pour gerer l'evaluation de la fiche A des employés de la fonction publique
class HrEvaluation(models.Model):
    _name = "hr_evaluation"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of Evalauation.", default=10)
    x_line_ids = fields.One2many('hr_sous_critere_evaluation_line', 'x_evaluation_id')
    x_categorie_employe_id = fields.Many2one("hr_catemp", string="Catégorie employé", required=True)
    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    x_type_employe_recev_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_f_ids = fields.One2many('hr_ficheattente_recup_line', 'x_evaluation_id')

    # INFOS CONCERNANT L'EMPLOYE A NOTER
    _rec_name = "employee_id"
    employee_id = fields.Many2one('hr.employee', string='Nom/Prénom(s)', required=True)
    name = fields.Integer(string="Classe", readonly=True)
    x_categorie = fields.Char(string="Catégorie", readonly=True)
    x_echelle = fields.Char(string="Echelle", readonly=True)
    x_echellon = fields.Char(string="Echelon", readonly=True)
    x_service = fields.Char(string="Service", readonly=True)
    x_emploi = fields.Char(string="Emploi", readonly=True)
    x_fonction = fields.Char(string="Fonction", readonly=True)

    x_matricule_c = fields.Char(string="Mle Contractuel ", readonly=True)
    x_matricule_f = fields.Char(string="Mle Fonctionnaire ", readonly=True)
    x_titre_id = fields.Many2one('hr_titreevaluation', string='Titre', required=True)

    # INFOS CONCERNANT LE SUPERIEUR HIERARCHIQUE DIRECT
    employee_id_imm = fields.Many2one('hr.employee', string='Nom/Prénom(s)', required=True)
    x_categorie_imm = fields.Char(string="Catégorie", readonly=True)
    x_echelle_imm = fields.Char(string="Echelle", readonly=True)
    x_echellon_imm = fields.Char(string="Echelon", readonly=True)
    x_service_imm = fields.Char(string="Service", readonly=True)
    x_fonction_imm = fields.Char(string="Fonction", readonly=True)
    x_matricule_imm_c = fields.Char(string="Mle Contractuel", readonly=True)
    x_matricule_imm_f = fields.Char(string="Mle Fonctionnaire", readonly=True)

    annee_evaluation = fields.Many2one('ref_exercice',
                                       default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                       string='Année', readonly=False, required=False)
    date_evaluation = fields.Date(string='Date', default=date.today())
    x_localite_id = fields.Char(string='Localité')
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)

    observation_sup_imm = fields.Text()
    contrainte_realisation = fields.Text()
    point_divergence = fields.Text()
    observation_amelioration = fields.Text()

    # fonction de recuperation de l'année en cours
    @api.onchange('employee_id')
    def _annee_en_cours(self):
        vals = datetime.now()
        vals1 = vals.year
        self.annee_evaluation = vals1

    # fonction pour emplir les champs de l'employé a noter

    @api.onchange('employee_id')
    def remplir_champ1(self):
        if self.x_type_employe_id.name == 'Fonctionnaire Detaché' or self.x_type_employe_id.name == 'fonctionnaire detaché' or self.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or self.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or self.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION' or self.x_type_employe_id.name == 'Hospitalo-Universitaire' or self.x_type_employe_id.name == 'HOSPITALO-UNIVERSITAIRE':
            self.x_categorie = self.employee_id.x_categorie_id.name
        else:
            self.x_categorie = self.employee_id.x_categorie_c_id.name

    @api.onchange('employee_id')
    def remplir_champ2(self):
        if self.x_type_employe_id.name == 'Fonctionnaire Detaché' or self.x_type_employe_id.name == 'fonctionnaire detaché' or self.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or self.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or self.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION' or self.x_type_employe_id.name == 'Hospitalo-Universitaire' or self.x_type_employe_id.name == 'HOSPITALO-UNIVERSITAIRE':
            self.x_echelle = self.employee_id.x_echelle_id.name
        else:
            self.x_echelle = self.employee_id.x_echelle_c_id.name

    @api.onchange('employee_id')
    def remplir_champ3(self):
        if self.x_type_employe_id.name == 'Fonctionnaire Detaché' or self.x_type_employe_id.name == 'fonctionnaire detaché' or self.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or self.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or self.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION' or self.x_type_employe_id.name == 'Hospitalo-Universitaire' or self.x_type_employe_id.name == 'HOSPITALO-UNIVERSITAIRE':
            self.x_echellon = self.employee_id.x_echellon_id.name
        else:
            self.x_echellon = self.employee_id.x_echellon_c_id.name

    @api.onchange('employee_id')
    def remplir_champ4(self):
        self.x_service = self.employee_id.hr_service.name

    @api.onchange('employee_id')
    def remplir_champ5(self):
        self.x_emploi = self.employee_id.x_emploi_id.name
        self.x_fonction = self.employee_id.x_fonction_id.name

    @api.onchange('employee_id')
    def remplir_champ6(self):
        self.x_matricule_c = self.employee_id.matricule_genere
        self.x_matricule_f = self.employee_id.matricule
        self.x_localite_id = self.company_id.ref_localite_id.name

    # fonction pour emplir les champs du superieur immédiat

    @api.onchange('employee_id_imm')
    def remplir_champ_imm_1(self):
        if self.x_type_employe_id.name == 'Fonctionnaire Detaché' or self.x_type_employe_id.name == 'fonctionnaire detaché' or self.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or self.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or self.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION' or self.x_type_employe_id.name == 'Hospitalo-Universitaire' or self.x_type_employe_id.name == 'HOSPITALO-UNIVERSITAIRE':
            self.x_categorie_imm = self.employee_id.x_categorie_id.name
        else:
            self.x_categorie_imm = self.employee_id_imm.x_categorie_c_id.name

    @api.onchange('employee_id_imm')
    def remplir_champ_imm_2(self):
        if self.x_type_employe_id.name == 'Fonctionnaire Detaché' or self.x_type_employe_id.name == 'fonctionnaire detaché' or self.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or self.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or self.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION' or self.x_type_employe_id.name == 'Hospitalo-Universitaire' or self.x_type_employe_id.name == 'HOSPITALO-UNIVERSITAIRE':
            self.x_echelle_imm = self.employee_id.x_echelle_id.name
        else:
            self.x_echelle_imm = self.employee_id_imm.x_echelle_c_id.name

    @api.onchange('employee_id_imm')
    def remplir_champ_imm_3(self):
        if self.x_type_employe_id.name == 'Fonctionnaire Detaché' or self.x_type_employe_id.name == 'fonctionnaire detaché' or self.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or self.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or self.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION' or self.x_type_employe_id.name == 'Hospitalo-Universitaire' or self.x_type_employe_id.name == 'HOSPITALO-UNIVERSITAIRE':
            self.x_echellon_imm = self.employee_id.x_echellon_id.name
        else:
            self.x_echellon_imm = self.employee_id_imm.x_echellon_c_id.name

    @api.onchange('employee_id_imm')
    def remplir_champ_imm_4(self):
        self.x_service_imm = self.employee_id_imm.hr_service.name

    @api.onchange('employee_id_imm')
    def remplir_champ_imm_5(self):
        self.x_fonction_imm = self.employee_id_imm.x_fonction_id.name

    @api.onchange('employee_id_imm')
    def remplir_champ_imm_6(self):
        self.x_matricule_imm_c = self.employee_id_imm.matricule_genere
        self.x_matricule_imm_f = self.employee_id_imm.matricule

    # NOTE  DE L'EMPLOYE EN FONCTION DES CRITERES
    x_note_globales = fields.Float(string='Note globale/10')
    x_note_globaless = fields.Float(string='Note globale/10', default=0, readonly=True)

    x_note_globale_agents = fields.Float(string='Note globale agent/10')
    x_note_globales_agentss = fields.Float(string='Note globale agent/10', default=0)

    # Competence professionnelle
    x_note_comps = fields.Float(string='Note competence/12')
    x_note_compss = fields.Float(string='Note competence/12', default=0)

    x_note_realisations_attentes = fields.Float(string='Note realisation attente/10')
    x_note_realisations_attentess = fields.Float(default=0, string='Note realisation attente/10')

    x_note_sens_org = fields.Float(string='Note sens organisation/1')
    x_note_sens_orgs = fields.Float(string='Note sens organisation/1')

    x_note_esprit_initiative = fields.Float(string='Note esprit initiative/1')
    x_note_esprit_initiatives = fields.Float(string='Note esprit initiative/1')

    x_note_total_comp_pro_agent = fields.Float(string='Note totale Comp.Pro.Agent/12')
    x_note_total_comp_pro_agents = fields.Float(string='Note totale Comp.Pro.Agent/12')

    # Conscience professionnelle
    x_note_assiduite = fields.Float(string='Note assiduité/1')
    x_note_assiduites = fields.Float(string='Note assiduité/1')

    x_note_ethique_prof = fields.Float(string='Note Ethique pro/2')
    x_note_ethique_profs = fields.Float(string='Note Ethique pro/2')

    x_note_sens_responsabilite = fields.Float(string='Note sens resp/1')
    x_note_sens_responsabilites = fields.Float(string='Note sens resp/1')

    x_note_ponctualite = fields.Float(string='Note Ponctualité/1')
    x_note_ponctualites = fields.Float(string='Note Ponctualité/1')

    x_note_total_consc_pro = fields.Float(string='Note totale Consc.Pro')
    x_note_total_consc_pros = fields.Float(string='Note totale Consc.Pro')

    x_note_total_consc_pro_agent = fields.Float(string='Note totale Consc.Pro.Agent')
    x_note_total_consc_pro_agents = fields.Float(string='Note totale Consc.Pro.Agent')

    # Leadership
    x_note_sens_animation = fields.Float(string='Note sens anim./1')
    x_note_sens_animations = fields.Float(string='Note sens anim./1')

    x_note_aptitude_enc = fields.Float(string='Note Aptitude/2')
    x_note_aptitude_encs = fields.Float(string='Note Aptitude/2')

    x_note_capacite_evaluer = fields.Float(string='Note capacité/1')
    x_note_capacite_evaluers = fields.Float(string='Note capacité/1')

    x_note_total_lead = fields.Float(string='Note totale Leadership/4')
    x_note_total_leads = fields.Float(string='Note totale Leadership/4')

    # Sens du service public
    x_note_esprit_sacrifice = fields.Float(string='Note esprit sacrifice./1')
    x_note_esprit_sacrifices = fields.Float(string='Note esprit sacrifice./1')

    x_note_respect_bien_public = fields.Float(string='Note respect bien public/2')
    x_note_respect_bien_publics = fields.Float(string='Note respect bien public/2')

    x_note_respect_hierarchie = fields.Float(string='Note respect hiérarchie/1')
    x_note_respect_hierarchies = fields.Float(string='Note respect hiérarchie/1')

    x_note_total_sens_public = fields.Float(string='Note totale sens public/4')
    x_note_total_sens_publics = fields.Float(string='Note totale sens public/4')

    # @api.depends('x_line_ids')
    @api.multi
    def action_confrimer(self):

        val_exo = int(self.x_exercice_id)
        val_emp = int(self.employee_id)
        x_categorie_employe_id = int(self.x_categorie_employe_id)
        for vals in self:

            # LES NOTES DE L'AGENT NON INVESTI DE POUVOIR DE NOTATION

            """Comptence Professionnelle"""
            # retourne la note de l'agent liée à la competence professionnelle(taux) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere NOT IN ('Sens organisation','Esprit initiative') AND C.name = 'Compétence Professionnelle' " % (
                    val_emp, self.id))
            res_a = vals.env.cr.fetchone()
            vals.x_note_realisations_attentess = res_a and res_a[0] or 0.0

            # retourne la note de l'agent non investi liée à la competence professionnelle(sens organisation) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Sens organisation' AND C.name = 'Compétence Professionnelle' " % (
                    val_emp, self.id))
            res_o = vals.env.cr.fetchone()
            vals.x_note_sens_orgs = res_o and res_o[0] or 0.0

            # retourne la note de l'agent non investi liée à la competence professionnelle(esprit initiative) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Esprit initiative' AND C.name = 'Compétence Professionnelle' " % (
                    val_emp, self.id))
            res = vals.env.cr.fetchone()
            vals.x_note_esprit_initiatives = res and res[0] or 0.0

            """Conscience Professionnelle"""

            # retourne la note de l'agent non investi liée à la conscience professionnelle(Ponctualité) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Ponctualité' AND C.name = 'Conscience Professionnelle' " % (
                    val_emp, self.id))
            res_pc = vals.env.cr.fetchone()
            vals.x_note_ponctualites = res_pc and res_pc[0] or 0.0

            # retourne la note de l'agent non investi liée à la conscience professionnelle(Assiduité) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Assiduité' AND C.name = 'Conscience Professionnelle' " % (
                    val_emp, self.id))
            res_ass = vals.env.cr.fetchone()
            vals.x_note_assiduites = res_ass and res_ass[0] or 0.0

            # retourne la note de l'agent non investi liée à la conscience professionnelle(Ethique Professionnelle) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Ethique Professionnelle' AND C.name = 'Conscience Professionnelle' " % (
                    val_emp, self.id))
            res_eth = vals.env.cr.fetchone()
            vals.x_note_ethique_profs = res_eth and res_eth[0] or 0.0

            """Sens du service public"""

            # retourne la note de l'agent non investi liée au sens du service public(Esprit de sacrifice) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Esprit de sacrifice' AND C.name = 'Sens du service public' " % (
                    val_emp, self.id))
            res_es = vals.env.cr.fetchone()
            vals.x_note_esprit_sacrifices = res_es and res_es[0] or 0.0

            # retourne la note de l'agent non investi liée au sens du service public(Respect du bien public) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Respect du bien public' AND C.name = 'Sens du service public' " % (
                    val_emp, self.id))
            res_rb = vals.env.cr.fetchone()
            vals.x_note_respect_bien_publics = res_rb and res_rb[0] or 0.0

            # retourne la note de l'agent non investi liée au sens du service public(Respect de la hierarchie) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Respect de la hiérarchie' AND C.name = 'Sens du service public' " % (
                    val_emp, self.id))
            res_rh = vals.env.cr.fetchone()
            vals.x_note_respect_hierarchies = res_rh and res_rh[0] or 0.0

            # La note globale /10 de l'agent
            vals.env.cr.execute(
                "SELECT SUM(L.x_note_sous) FROM hr_sous_critere_evaluation_line L, hr_evaluation E WHERE L.x_evaluation_id = E.id and L.x_cocher = TRUE and L.x_evaluation_id = %d" % (
                    self.id))
            res_ng = vals.env.cr.fetchone()
            vals.x_note_globales_agentss = (res_ng and res_ng[0] or 0.0) / 2.0

            # LES NOTES DE L'AGENT INVESTI DE POUVOIR DE NOTATION

            """Comptence Professionnelle"""

            # retourne la note de l'agent qui reçoit une lettre liée à la competence professionnelle(taux) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere NOT IN ('Assiduité','Ethique Professionnelle','Sens de la responsabilité','Sens animation équipe','Aptitude encadrement','Capacité à évoluer') AND C.name = 'Compétence Professionnelle' " % (
                    val_emp, self.id))
            res_l = vals.env.cr.fetchone()
            vals.x_note_compss = res_l and res_l[0] or 0.0

            """Conscience Professionnelle"""

            # retourne la note de l'agent qui reçoit une lettre liée à la competence professionnelle(Assiduité) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND SC.x_categorie_employe_id = E.x_categorie_employe_id AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Assiduité' AND C.name = 'Conscience Professionnelle' AND E.x_categorie_employe_id = %d " % (
                    val_emp, self.id, x_categorie_employe_id))
            res_a_i = vals.env.cr.fetchone()
            vals.x_note_assiduites = res_a_i and res_a_i[0] or 0.0

            # retourne la note de l'agent qui reçoit une lettre liée à la competence professionnelle(Ethique Professionnelle) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND SC.x_categorie_employe_id = E.x_categorie_employe_id AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Ethique Professionnelle' AND C.name = 'Conscience Professionnelle' AND E.x_categorie_employe_id = %d " % (
                    val_emp, self.id, x_categorie_employe_id))
            res_eh_i = vals.env.cr.fetchone()
            vals.x_note_ethique_profs = res_eh_i and res_eh_i[0] or 0.0

            # retourne la note de l'agent qui reçoit une lettre liée à la competence professionnelle(Sens de la responsabilité) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND SC.x_categorie_employe_id = E.x_categorie_employe_id AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Sens de la responsabilité' AND C.name = 'Conscience Professionnelle' AND E.x_categorie_employe_id = %d " % (
                    val_emp, self.id, x_categorie_employe_id))
            res_sr_i = vals.env.cr.fetchone()
            vals.x_note_sens_responsabilites = res_sr_i and res_sr_i[0] or 0.0

            """Leadership"""

            # retourne la note de l'agent qui reçoit une lettre liée à leadership(Sens animation équipe) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND SC.x_categorie_employe_id = E.x_categorie_employe_id AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Sens animation équipe' AND C.name = 'Leadership' AND E.x_categorie_employe_id = %d " % (
                    val_emp, self.id, x_categorie_employe_id))
            res_san_i = vals.env.cr.fetchone()
            vals.x_note_sens_animations = res_san_i and res_san_i[0] or 0.0

            # retourne la note de l'agent qui reçoit une lettre liée à leadership(Aptitude à l'encadrement) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND SC.x_categorie_employe_id = E.x_categorie_employe_id AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Aptitude encadrement' AND C.name = 'Leadership' AND E.x_categorie_employe_id = %d " % (
                    val_emp, self.id, x_categorie_employe_id))
            res_ap_i = vals.env.cr.fetchone()
            vals.x_note_aptitude_encs = res_ap_i and res_ap_i[0] or 0.0

            # retourne la note de l'agent qui reçoit une lettre liée à leadership(Capacité à evaluer) en fonction de ce qui est coché
            vals.env.cr.execute(
                "SELECT L.x_note_sous FROM hr_sous_critere_evaluation_line L, hr_evaluation E, hr_critere_evaluation C,hr_sous_critere_evaluation SC WHERE L.x_evaluation_id = E.id AND C.id = L.x_critere_id AND L.x_cocher = TRUE AND L.x_sous_critere = SC.lib_long AND SC.x_categorie_employe_id = E.x_categorie_employe_id AND E.employee_id = %d AND L.x_evaluation_id = %d AND L.x_sous_critere = 'Capacité à évoluer' AND C.name = 'Leadership' AND E.x_categorie_employe_id = %d " % (
                    val_emp, self.id, x_categorie_employe_id))
            res_cap_i = vals.env.cr.fetchone()
            vals.x_note_capacite_evaluers = res_cap_i and res_cap_i[0] or 0.0

            # La note globale /10 de l'agent
            vals.env.cr.execute(
                "SELECT SUM(L.x_note_sous) FROM hr_sous_critere_evaluation_line L, hr_evaluation E WHERE L.x_evaluation_id = E.id and L.x_cocher = TRUE and L.x_evaluation_id = %d" % (
                    self.id))
            res_gl = vals.env.cr.fetchone()
            vals.x_note_globaless = (res_gl and res_gl[0] or 0.0) / 2.0
            # print('note globale chef',vals.x_note_globaless)

            """Les conditions pour avoir le total par critère par categorie d'agent"""

            if vals.x_note_realisations_attentess or vals.x_note_esprit_initiatives or vals.x_note_sens_orgs:
                vals.x_note_total_comp_pro_agents = vals.x_note_sens_orgs + vals.x_note_esprit_initiatives + vals.x_note_realisations_attentess
                # print('note totale comp_agent',vals.x_note_total_comp_pro_agents)

            if vals.x_note_sens_responsabilites or vals.x_note_ethique_profs or vals.x_note_assiduites:
                vals.x_note_total_consc_pros = vals.x_note_sens_responsabilites + vals.x_note_ethique_profs + vals.x_note_assiduites
                # print('note totale consc_prof',vals.x_note_total_consc_pros)

            if vals.x_note_ponctualites or vals.x_note_ethique_profs or vals.x_note_assiduites:
                vals.x_note_total_consc_pro_agents = vals.x_note_ponctualites + vals.x_note_ethique_profs + vals.x_note_assiduites
                # print('note totale consc_prof_agent',vals.x_note_total_consc_pro_agents)

            if vals.x_note_capacite_evaluers or vals.x_note_aptitude_encs or vals.x_note_sens_animations:
                vals.x_note_total_leads = vals.x_note_capacite_evaluers + vals.x_note_aptitude_encs + vals.x_note_sens_animations
                # print('note totale leads',vals.x_note_total_leads)

            if vals.x_note_esprit_sacrifices or vals.x_note_respect_hierarchies or vals.x_note_respect_bien_publics:
                vals.x_note_total_sens_publics = vals.x_note_respect_bien_publics + vals.x_note_esprit_sacrifices + vals.x_note_respect_hierarchies
                # print('note totale sens resp',vals.x_note_total_sens_publics)

    # fonction de remplissage du tableau
    @api.multi
    def action_rechercher(self):
        if self.employee_id:
            emp_id = int(self.employee_id)
            x_struct_id = int(self.company_id)
            x_exo_id = int(self.x_exercice_id)
            x_cat_id = int(self.x_categorie_employe_id)
            print('categorie id', x_cat_id)
            for vals in self:
                vals.env.cr.execute(
                    """select (L.objectif) as objectif from hr_ficheattente_line L, hr_ficheattente F where F.id = L.name and F.name = %d and F.company_id = %d and F.x_exercice_id = %d""" % (
                        emp_id, x_struct_id, x_exo_id))
                rows = vals.env.cr.dictfetchall()
                result = []

                # delete old payslip lines
                vals.x_line_f_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'objectif': line['objectif']}))
                self.x_line_f_ids = result

                # requête pour afficher les sous critères en fonction de la categorie de l'employé
                vals.env.cr.execute(
                    """SELECT * FROM hr_sous_critere_evaluation WHERE x_categorie_employe_id = %d""" % (x_cat_id))
                rows_s = vals.env.cr.dictfetchall()
                result = []

                # delete old payslip lines
                vals.x_line_ids.unlink()
                for lines in rows_s:
                    result.append((0, 0, {'x_critere_id': lines['x_critere_evaluation_id'],
                                          'x_sous_critere': lines['lib_long'],
                                          'x_note_sous': lines['note_sous_critere']}))
                self.x_line_ids = result


class HrSousCritereEvaluation(models.Model):
    _name = 'hr_sous_critere_evaluation'
    _order = 'sequence, id'
    _rec_name = "lib_long"

    sequence = fields.Integer(help="Gives the sequence when displaying a list of Sous Critères Evalauation.",
                              default=10)
    name = fields.Char(string="Borne inférieure")
    born_sup = fields.Char(string="Borne supérieure")
    lib_court = fields.Char(string="Libelle court")
    lib_long = fields.Char(string="Libelle long")
    lib_p = fields.Char(string="Concat.")
    note_sous_critere = fields.Float(string="Note", required=True)
    x_critere_evaluation_id = fields.Many2one('hr_critere_evaluation', string='Choisir Critère', required=True)
    x_categorie_employe_id = fields.Many2one("hr_catemp", string="Catégorie employé", required=True)

    # fonction de concatenation
    @api.onchange('name', 'born_sup')
    def _concat(self):
        for tests in self:
            tests.lib_p = "Taux compris entre " + str(tests.name) + " et " + str(tests.born_sup) + "%"


# classe de la fiche d'attente line
class HrFicheAttenteLine(models.Model):
    _name = 'hr_ficheattente_recup_line'
    x_evaluation_id = fields.Many2one("hr_evaluation")
    objectif = fields.Text(string='Objectifs', readonly=True)


class HrSousCritereEvaluationLine(models.Model):
    _name = "hr_sous_critere_evaluation_line"
    x_evaluation_id = fields.Many2one("hr_evaluation")
    # x_sous_critere_id = fields.Many2one("hr_sous_critere_evaluation", string = "Sous Critère")
    x_critere_id = fields.Many2one("hr_critere_evaluation", string="Critère", readonly=True)
    x_sous_critere = fields.Char(string="Sous Critère", readonly=True)
    x_note_sous = fields.Float(string="Note")
    x_cocher = fields.Boolean('Cocher ?', default=False)

    @api.onchange('x_sous_critere_id')
    def remplir_note(self):
        self.x_note_sous = self.x_sous_critere_id.note_sous_critere


class HrCritereEvalaution(models.Model):
    _name = "hr_critere_evaluation"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of Critères Evalauation.", default=10)
    name = fields.Char(string="Libelle long", required=True)
    lib_court = fields.Char(string="Libelle court")
    active = fields.Boolean(string="Etat", default=True)
    description = fields.Text(string="Description", size="1000")


# Creation de la classe titre avec ses attributs
class HrTitreEvaluation(models.Model):
    _name = "hr_titreevaluation"
    _order = 'sequence, id'
    _rec_name = 'lib_long'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of nature.", default=10)
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# classe de la fiche d'attente
class HrFicheAttente(models.Model):
    _name = 'hr_ficheattente'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of ministere.", default=10)

    name = fields.Many2one('hr.employee', string='Employé', required=True)
    x_drh_id = fields.Many2one('hr.employee', string='DRH', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_op = fields.Date(string="Date", default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_ficheattente_line', 'name', string='Liste Des Objectifs',
                                 states={'A': [('readonly', True)]})
    active = fields.Boolean(string="Etat", default=True)
    fichier_joint = fields.Binary(string="Joindre Contrat d'objectif", attachment=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('V', 'Soumettre'),
        ('NV', 'Annuler'),
        ('C', 'Valider'),
        ('NC', 'Rejetter'),
        ('A', 'Approuver'),
        ('NA', 'Rejetter'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    # Les fonctions permettant de changer d'etat
    @api.multi
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def action_valider(self):
        self.write({'state': 'V'})

    @api.multi
    def action_non_valider(self):
        self.write({'state': 'NV'})

    @api.multi
    def action_confirmer(self):
        self.write({'state': 'C'})

    @api.multi
    def action_non_confirmer(self):
        self.write({'state': 'NC'})

    @api.multi
    def action_appr(self):
        self.write({'state': 'A'})

    @api.multi
    def action_non_appr(self):
        self.write({'state': 'NA'})


# classe de la fiche d'attente line
class HrFicheAttenteLine(models.Model):
    _name = 'hr_ficheattente_line'
    name = fields.Many2one('hr_ficheattente')
    objectif = fields.Text(string='Objectifs')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)


# classe de la convention de precompte
class HrConventionPrecompte(models.Model):
    _name = 'hr_conventionprecptes'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of convention precompte.", default=10)

    _rec_name = 'x_employe_id'
    name = fields.Char(string='Objet', readonly=False)
    x_employe_id = fields.Many2one('hr.employee', string='Employé', required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_op = fields.Date(string="Date", default=date.today(), readonly=True)
    active = fields.Boolean(string="Etat", default=True)
    x_line_ids = fields.One2many('hr_conventionprecptes_lines', 'name', string='Liste Des Conventions precomptes')
    x_line_ret_ids = fields.One2many('hr_echeanceretenue_line', 'name', string='Echéance des retenues')
    x_line_reg_ids = fields.One2many('hr_regleecheance_line', 'name', string='Règle Echéance')
    mnt_totals = fields.Float(string='Montant total', readonly=True, default=0.0)

    date = fields.Date(string='Date')
    mnt_echeance = fields.Float(string='Montant')
    reste_echeance = fields.Float(string="Reste à l'instant t", readonly=True)
    reste_a_payer = fields.Float(string='Reste', readonly=True)
    x_mode_id = fields.Many2one('ref_modereglement', string='Mode règlement')
    x_mode = fields.Char(string='Mode règlement')

    ref_piece = fields.Char(string='Réf.pièce')
    observation = fields.Text(string='Observations')

    # fonction de recueration du libellé de mode de paiement
    @api.onchange('x_mode_id')
    def remplir(self):
        if self.x_mode_id:
            self.x_mode = self.x_mode_id.lb_long

    # fonction de calcul du reste
    # @api.onchange('date')
    def action_ok(self):
        x_struct_id = int(self.company_id)
        x_empl_id = int(self.x_employe_id)

        for vals in self:
            if vals.date:
                val_id = vals.id
                vals.env.cr.execute(
                    """select sum(L.mnt_cvtion_reste) as mnt from hr_conventionprecptes_lines L, hr_conventionprecptes C where C.id = L.name and C.id = %s and C.x_employe_id = %s and C.company_id = %s""",
                    (val_id, x_empl_id, x_struct_id))
                lo = self.env.cr.fetchone()
                vals.reste_echeance = lo and lo[0] or 0

    # fonction de calcul du reste
    @api.onchange('x_mode_id')
    def remplir_mnt(self):
        if self.mnt_echeance:
            self.reste_a_payer = self.reste_echeance - self.mnt_echeance

            # fonction de validation du règlement

    def valider_action(self):
        for record in self:

            record.reste_a_payer = record.reste_echeance - record.mnt_echeance

            val_id = int(self.id)
            val_date = record.date
            val_mnt_echeance = record.mnt_echeance
            val_reste_echeance = record.reste_echeance
            val_reste = record.reste_a_payer
            val_id_mod = int(record.x_mode_id.id)
            val_mod = str(record.x_mode)
            val_ref_piece = record.ref_piece
            x_struct_id = int(self.company_id)
            x_exo_id = int(self.x_exercice_id)

            if val_mnt_echeance > val_reste_echeance:
                raise ValidationError(_(
                    'Vous avez saisi un montant supérieur au montant restant, veuillez ré-saisir un montant inférieur ou égal au montant restant à payer svp!'))
            elif val_mnt_echeance == 0:
                raise ValidationError(_('Saisissez un montant valide svp!'))
            elif val_reste_echeance == 0:
                raise ValidationError(_('Echéance terminée'))
            else:
                record.env.cr.execute(
                    """INSERT INTO hr_regleecheance_line(name,date,mnt_echeance,reste_echeance,reste_a_payer,x_mode_id,x_mode,ref_piece) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (val_id, val_date, val_mnt_echeance, val_reste_echeance, val_reste, val_id_mod, val_mod,
                     val_ref_piece))

        for rec in self.x_line_ids:
            val_ids = rec.id
            record.env.cr.execute(
                """UPDATE hr_conventionprecptes_lines SET mnt_cvtion_reste = mnt_cvtion_reste - %d WHERE id = %d""" % (
                    val_mnt_echeance, val_ids))

    # fonction de calcul du total des conventions
    def action_valider_prcpte(self):
        x_struct_id = int(self.company_id)
        x_empl_id = int(self.x_employe_id)

        # self.mnt_totals.unlink()
        self.mnt_totals = 0.0
        for vals in self.x_line_ids:
            # vals.env.cr.execute("""select sum(L.mnt_cvtions) as mnt from hr_conventionprecptes_lines L, hr_conventionprecptes C where C.id = L.name and C.x_employe_id = %d and C.company_id = %d""" %(x_empl_id,x_struct_id))
            # lo = self.env.cr.fetchone()
            # self.mnt_totals = lo and lo[0] or 0"""
            self.mnt_totals += vals['mnt_cvtions']

            vals.env.cr.execute(
                "select SUM(mnt_totals) as somme from hr_conventionprecptes where x_employe_id = %d" % (x_empl_id))
            rows = vals.env.cr.dictfetchall()
            print('Liste', rows)
            mnt_total = rows[0]['somme']
            print('Montant', mnt_total)
            vals.env.cr.execute("""UPDATE hr_employee SET x_precompte = %d WHERE id = %d """ % (mnt_total, x_empl_id))


# classe de la convention de precompte line
class HrConventionPrecompteLines(models.Model):
    _name = 'hr_conventionprecptes_lines'
    name = fields.Many2one('hr_conventionprecptes')

    date_mise_en_place = fields.Date(string='Date mise en place', required=True, etat={'Oui': [('readonly', True)]})
    type_acte = fields.Many2one('ref_piece_justificatives', string='Type acte', etat={'Oui': [('readonly', True)]})
    ref_acte = fields.Char(string='Réf.acte', etat={'Oui': [('readonly', True)]})
    mnt_cvtions = fields.Float(string='Montant Total', etat={'Oui': [('readonly', True)]})
    mnt_cvtion_reste = fields.Float(string='Montant Restant', readonly=True, etat={'Oui': [('readonly', True)]})
    mnt_elt = fields.Float(string='Montant', etat={'Oui': [('readonly', True)]})
    date_effet = fields.Date(string='Date effet', required=True, etat={'Oui': [('readonly', True)]})
    date_fin = fields.Date(string='Date fin', required=True, etat={'Oui': [('readonly', True)]})
    elt_sal_id = fields.Many2one('hr_nature', string='Nature', etat={'Oui': [('readonly', True)]})
    x_nbre_jourss = fields.Integer(string='Durée', readonly=True)
    x_nbre_j = fields.Integer(string='Durée', readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    etat = fields.Selection([
        ('Oui', 'Oui'),
        ('Non', 'Non'),
    ], 'Soldé ?', default='Non')

    # fonction de recuperation du nombre de jours entre deux dates
    @api.onchange('date_effet', 'date_fin')
    def nbre_j(self):
        for vals in self:
            if vals.date_fin and vals.date_effet:
                vals.x_nbre_j = (vals.date_fin - vals.date_effet).days

    # fonction de calcul du reste comme mnt initial
    @api.onchange('mnt_cvtions')
    def mnt_cvtion(self):
        for vals in self:
            if vals.mnt_cvtions:
                vals.mnt_cvtion_reste = vals.mnt_cvtions


# classe de l'echeance de retenue de precompte line
class HrEcheaanceRetenueLine(models.Model):
    _name = 'hr_echeanceretenue_line'
    name = fields.Many2one('hr_conventionprecptes')

    date = fields.Date(string='Date', required=True)
    mnt_echeance = fields.Float(string='Montant', required=True)
    x_mode = fields.Many2one('ref_modereglement', string='Mode règlement', required=True)
    ref_piece = fields.Char(string='Réf.pièce')
    observation = fields.Text(string='Observations')

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)


# classe règle de l'echeance  de precompte line
class HrRegleEcheaanceLine(models.Model):
    _name = 'hr_regleecheance_line'
    name = fields.Many2one('hr.employee', readonly=True)
    date = fields.Char(string='Date', readonly=True)
    mnt_echeance = fields.Float(string='Montant/Mois', readonly=True)
    reste_echeance = fields.Float(string="Reste à l'instant t", readonly=True)
    reste_a_payer = fields.Float(string='Reste à payer', readonly=True)
    date_debut = fields.Date(string='Date début', readonly=True)
    date_fin = fields.Date(string='Date fin', readonly=True)
    duree_prcpte = fields.Integer(string='Durée(jours)', readonly=True)
    nature_prcpte_id = fields.Many2one('hr_nature', string='Nature Précompte')


# classe règle de l'echeance  de precompte line
class HrRegleEcheaanceDetailsLine(models.TransientModel):
    _name = 'hr_regleecheancedetails_line'
    name = fields.Many2one('hr.employee', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    mnt_echeance = fields.Float(string='Montant/Mois', readonly=True)
    reste_echeance = fields.Float(string="Reste à l'instant t", readonly=True)
    reste_a_payer = fields.Float(string='Reste à payer', readonly=True)
    date_debut = fields.Date(string='Date début', readonly=True)
    date_fin = fields.Date(string='Date fin', readonly=True)
    duree_prcpte = fields.Integer(string='Durée(jours)', readonly=True)
    nature_prcpte_id = fields.Many2one('hr_nature', string='Nature Précompte')


# ecran de similation des salaires
class HrSimulationSalaire(models.Model):
    _name = "hr_simulsalaire"
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of simulation salaire.", default=10)

    name = fields.Many2one('hr.employee', string='Nom', required=True)
    active = fields.Boolean(string="Etat", default=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice', string="Année",
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    readonly=True)
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    date_op = fields.Date(string="Date", default=date.today(), readonly=True)
    x_date_debut = fields.Date(string='Date début', required=True)
    x_date_fin = fields.Date(string='Date fin', required=True)
    x_nbre_jours = fields.Integer(string='Durée', readonly=True)
    observation = fields.Text('Observations')
    x_line_ids = fields.One2many('hr_simulsalaire_line', 'x_simul_id', string='Liste Des Elements')

    # fonction de recuperation du nombre de jours entre deux dates
    @api.onchange('x_date_debut', 'x_date_fin')
    def _nombre_jours(self):
        for vals in self:
            if vals.x_date_debut and vals.x_date_fin:
                vals.x_nbre_jours = (vals.x_date_fin - vals.x_date_debut).days

    def action_valider(self):
        if self.x_date_debut and self.x_date_fin:
            x_struct_id = int(self.company_id)
            x_emp = str(self.name)
            ddbut = str(self.x_date_debut.strftime("%Y-%m-%d"))
            ddfin = str(self.x_date_fin.strftime("%Y-%m-%d"))
            for vals in self:
                vals.env.cr.execute(
                    """SELECT (P.id) AS id,(C.name) AS categorie, (EC.name) as echelle, (ECH.name) as echelon, (E.name) as employe, (E.matricule) as matricule,(EM.name) as emploi, (E.x_solde_indiciaire_net) as salaire_base, (E.x_indem_resp) as resp, (E.x_indem_astr) as astr, (E.x_indem_techn) as techn, (E.x_indem_specif) as spec, (E.x_indem_loge) as loge, (E.x_indem_transp) as transp, (E.x_indem_inform) as inf, (E.x_indem_exploit) as reseau, (E.x_indem_finance) as finance, (E.x_allocation_familial) as allocation, (E.x_remuneration_total) as remu_total, (E.x_mnt_carfo) as carfo, (E.x_mnt_cnss) as cnss, (E.x_base_imposable_ctrct) as base_impo, (E.x_iuts_net) as iuts,(E.x_mnt_patronal_cnss) as p_cnss,(E.x_mnt_patronal_carfo) as p_carfo, (E.mnt_foner) as foner, (E.x_indem_garde) as garde, (E.x_indem_risque) as risque,(E.x_indem_suj) as suje,(E.x_indem_form) as formation,(E.x_indem_caisse) as caisse,(E.x_indem_veste) as veste,(E.x_net_payer_ctrct) as net FROM  hr_payslip P, hr_employee E, hr_categorie C, hr_echelle EC, hr_echellon ECH, hr_emploi EM WHERE E.id = P.employee_id AND E.x_categorie_c_id = C.id AND E.x_echelle_c_id = EC.id AND E.x_echellon_c_id = ECH.id AND E.x_emploi_id = EM.id  AND P.date_from >= %s AND P.date_to <= %s AND E.x_type_employe_id = %s AND E.company_id = %s AND P.state = 'done'""",
                    (ddbut, ddfin, x_type_id, x_struct_id))
                rows = vals.env.cr.dictfetchall()
                result = []

                # delete old payslip lines
                vals.x_line_ids.unlink()
                for line in rows:
                    result.append((0, 0,
                                   {'mat': line['matricule'], 'nom': line['employe'], 'categorie': line['categorie'],
                                    'echelle': line['echelle'], 'echelon': line['echelon'], 'emploi': line['emploi'],
                                    'salaire_base': line['salaire_base'], 'resp': line['resp'], 'astr': line['astr'],
                                    'loge': line['loge'], 'tech': line['techn'], 'spec': line['spec'],
                                    'transp': line['transp'], 'inf': line['inf'], 'reseau': line['reseau'],
                                    'financ': line['finance'], 'x_indem_garde': line['garde'],
                                    'x_indem_risque': line['risque'], 'x_indem_suj': line['suje'],
                                    'x_indem_form': line['formation'], 'x_indem_caisse': line['caisse'],
                                    'x_indem_veste': line['veste'], 'alloc_f': line['allocation'],
                                    'renum_t': line['remu_total'], 'mnt_agent_carfo': line['carfo'],
                                    'mnt_patronal_carfo': line['p_carfo'], 'mnt_agent_cnss': line['cnss'],
                                    'mnt_patronal_cnss': line['p_cnss'], 'base_imp': line['base_impo'],
                                    'iuts': line['iuts'], 'net': line['net']}))
                self.x_line_ids = result

            # class pour gerer les lignes de simulation de salaire


class HrSimulationSalaireLine(models.Model):
    _name = 'hr_simulsalaire_line'
    x_simul_id = fields.Many2one('hr_simulsalaire')

    x_elt_sal = fields.Char(string='Element de salaire', readonly=True)
    x_mnt = fields.Float(string='Montant', readonly=True)
    x_mnt_simul = fields.Float(string='Montant simulé', readonly=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)


# classe de la convention de precompte line
class HrConventionPrecompteLine(models.Model):
    _name = 'hr_conventionprecpte_line'
    name = fields.Many2one('hr_conventionprecpte')

    date_mise_en_place = fields.Date(string='Date mise en place', required=True)
    obje = fields.Char(string='Objet')
    type_acte = fields.Many2one('hr_emploi', string='Type acte')
    ref_acte = fields.Char(string='Réf.acte')
    mnt_cvtion = fields.Float(string='Montant Convention')
    mnt_elt = fields.Float(string='Montant')
    date_effet = fields.Date(string='Date effet', required=True)
    date_fin = fields.Date(string='Date fin', required=True)
    elt_sal_id = fields.Many2one('hr_nature', string='Nature')
    x_nbre_jours = fields.Integer(string='Durée')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)


# Class de cessation de service
class HrCessationService(models.Model):
    _name = 'hr_cessation_service'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of cessation service.", default=10)

    name = fields.Many2one('hr.employee', string='Agent', required=True)
    x_date_cess = fields.Date(string='Date Cessation', default=date.today(), required=True)
    date_debut_affect = fields.Date(string='Date Prise', readonly=True)
    x_motif_cess = fields.Many2one('hr_motif', string='Motif Cessation', required=True)
    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    x_titre_id = fields.Many2one('hr_titreposte', string='Titre', required=True)
    x_titre = fields.Char(string='Titre', default='CERTIFICAT DE CESSATION DE SERVICE')
    p1 = fields.Char(string='Phrase 1', default='Je soussigné, ')
    p2 = fields.Char(string='Phrase 2', default='certifie que M./Mme/Mlle')
    matricule = fields.Char('Matricule', readonly=True)
    categorie = fields.Char('Catégorie', readonly=True)
    echelle = fields.Char('Echelle', readonly=True)
    classe = fields.Char('Classe', readonly=True)
    echelon = fields.Char('Echelon', readonly=True)
    indice = fields.Char('Indice', readonly=True)
    # p3 = fields.Char(string = 'Phrase 3', default = 'au  ')
    # p4 = fields.Char(string = 'Phrase 4', default = 'qui a pris fonction du ')
    # p5 = fields.Char(string = 'Phrase 5',default = ',précédemment en service au')
    p3 = fields.Char(string='Phrase 3', default='précédemment en service au ')
    p4 = fields.Char(string='Phrase 4', default='a mis fin à son détachement et a cessé service le  ')
    p5 = fields.Char(string='Phrase 5', default='pour cause de ')
    p6 = fields.Char(string='Phrase 6',
                     default='En foi de quoi, la présente attestation lui est délivrée pour servir et valoir ce que de droit')
    responsale = fields.Many2one('hr.employee', string='Responsable')
    x_emploi = fields.Char(string='Emploi', readonly=True)
    x_fonction = fields.Char(string='Fonction', readonly=True)
    x_direction = fields.Char(string='Direction', readonly=True)
    x_service = fields.Char(string='Service', readonly=True)
    date_attest = fields.Date(string="Date", default=date.today())
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)
    observation = fields.Text(string='Observations')
    company_id = fields.Many2one('res.company', string="Structure", readonly=True,
                                 default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)
    x_line_cess_ids = fields.One2many('hr_cessation_service_line', 'x_cess_id', string="Liste des ampliations",
                                      readonly=False)

    @api.onchange('responsale')
    def remplir_fonction_resp(self):
        self.x_fonction = self.name.x_fonction_id.lib_long

    @api.onchange('name')
    def remplir_employe(self):
        if self.x_type_employe_id.name == 'Fonctionnaire Detaché' or self.x_type_employe_id.name == 'fonctionnaire detaché' or self.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or self.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or self.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION':
            self.x_emploi = self.name.x_emploi_id.name
            self.x_service = self.name.hr_service.name
            self.date_debut_affect = self.name.date_debut
            self.matricule = self.name.matricule
            self.categorie = self.name.x_categorie_id.name
            self.echelle = self.name.x_echelle_id.name
            self.classe = self.name.x_classees_id.name
            self.echelon = self.name.x_echellon_id.name
            self.indice = self.name.x_indice
        else:
            self.x_emploi = self.name.x_emploi_id.name
            self.x_service = self.name.hr_service.name
            self.date_debut_affect = self.name.date_embauche
            self.matricule = self.name.matricule_genere
            self.categorie = self.name.x_categorie_c_id.name
            self.echelle = self.name.x_echelle_c_id.name
            self.classe = ''
            self.echelon = self.name.x_echellon_c_id.name


class hr_cessation_serviceLine(models.Model):
    _name = "hr_cessation_service_line"
    x_cess_id = fields.Many2one('hr_cessation_service')

    name = fields.Char(string='Ampliations', required=True)
    observations = fields.Char(string='Observations')


# classe titre poste
class HrTitrePoste(models.Model):
    _name = 'hr_titreposte'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)
    _rec_name = 'lib_long'
    name = fields.Char(string="Libéllé court", required=True)
    lib_long = fields.Char(string="Libellé long", size=35, required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# Class de reprise de service
class HrRepriseService(models.Model):
    _name = 'hr_reprise_service'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of reprise service.", default=10)

    name = fields.Many2one('hr.employee', string='Nom', required=True)
    x_date_cess = fields.Date(string='Date Reprise', default=date.today(), required=True)
    date_debut_affect = fields.Date(string='Date Prise', readonly=True)
    x_motif_cess = fields.Many2one('hr_motif', string='Motif Cessation', required=True)

    x_titre = fields.Char(string='Titre', default='CESSATION DE SERVICE')
    p1 = fields.Char(string='Phrase 1', default='Je soussigné, ')
    p2 = fields.Char(string='Phrase 2', default='atteste que M./Mme/Mlle')
    p3 = fields.Char(string='Phrase 3', default='au  ')
    p4 = fields.Char(string='Phrase 4', default='qui a pris fonction du ')
    p5 = fields.Char(string='Phrase 5', default='Au')
    p6 = fields.Char(string='Phrase 6', default='au sein de ')
    p7 = fields.Char(string='Phrase 7', default='a cessé sa fonction pour cause de  ')
    p8 = fields.Char(string='Phrase 8',
                     default='En foi de quoi, la présente attestation lui est délivrée pour servir et valoir ce que de droit')
    responsale = fields.Many2one('hr.employee', string='Responsable')
    x_emploi = fields.Char(string='Emploi', readonly=True)
    x_fonction = fields.Many2one('hr_fonctionss', string='Fonction')
    x_direction = fields.Char(string='Direction', readonly=True)
    x_service = fields.Char(string='Service', readonly=True)
    date_attest = fields.Date(string="Date", default=date.today())
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)
    observation = fields.Text(string='Observations')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)

    @api.onchange('name')
    def remplir_employe(self):
        if self.name:
            self.x_emploi = self.name.x_emploi_id.name
            self.x_direction = self.name.department_id.name
            self.x_service = self.name.hr_service.name
            self.date_debut_affect = self.name.date_debut
            # self.responsale = self.name.department_id.manager_id.name


# Class de certificat de travail
class HrCertificatTravail(models.Model):
    _name = 'hr_certificat_travail'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of certificat", default=10)

    name = fields.Many2one('hr.employee', string='Agent', required=True)
    x_date_cess = fields.Date(string='Date Fin', default=date.today(), required=True)
    date_debut_affect = fields.Date(string='Date Prise', readonly=True)

    x_titre = fields.Char(string='Titre', default='ATTESTATION/CERTIFICAT DE TRAVAIL')
    p1 = fields.Char(string='Phrase 1', default='Je soussigné, ')
    p2 = fields.Char(string='Phrase 2', default='atteste que M./Mme/Mlle')
    p3 = fields.Char(string='Phrase 3', default='au  ')
    p4 = fields.Char(string='Phrase 4', default='qui a pris fonction du ')
    p5 = fields.Char(string='Phrase 5', default='Au')
    p6 = fields.Char(string='Phrase 6', default='au sein de ')
    p7 = fields.Char(string='Phrase 7', default='a effectué avec succès les tâches qui lui ont été attribuées ')
    p8 = fields.Char(string='Phrase 8',
                     default='En foi de quoi, la présente attestation lui est délivrée pour servir et valoir ce que de droit')
    responsale = fields.Many2one('hr.employee', string='Responsable')
    x_emploi = fields.Char(string='Emploi', readonly=True)
    x_fonction = fields.Char(string='Fonction', readonly=True)
    x_direction = fields.Char(string='Direction', readonly=True)
    x_service = fields.Char(string='Service', readonly=True)
    date_attest = fields.Date(string="Date", default=date.today())
    current_user = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    active = fields.Boolean(string="Etat", default=True)
    observation = fields.Text(string='Observations')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]),
                                    string='Année', readonly=True)

    @api.onchange('responsale')
    def remplir_fonction_resp(self):
        self.x_fonction = self.name.x_fonction_id.lib_long

    @api.onchange('name')
    def remplir_employe(self):
        if self.name:
            self.x_emploi = self.name.x_emploi_id.name
            self.x_direction = self.name.department_id.name
            self.x_service = self.name.hr_service.name
            self.date_debut_affect = self.name.date_debut
            # self.responsale = self.name.department_id.manager_id.name


# classe personnel avançable
class HrPersonnelAvancable(models.Model):
    _name = 'hr_personnel_avancable'
    _order = 'sequence, id'
    sequence = fields.Integer(help="Gives the sequence when displaying a list of session.", default=10)

    name = fields.Many2one("hr_catemp", string="Catégorie employé", required=True)
    x_line_ids = fields.One2many('hr_personnel_categorie_line', 'x_pers_id', string='Liste Personnel')
    x_line_a_ids = fields.One2many('hr_personnel_avancable_line', 'x_pers_a_id', string='Liste Personnel Avançable')
    date_op = fields.Datetime(string='Date/Heure', default=datetime.today(), readonly=True)
    currents_users = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)
    x_line_avc_ids = fields.One2many('hr_personnel_avance_line', 'x_pers_avc_id', string='Liste Personnel Avancée')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('R', 'Recherché'),
        ('C', 'Confirmé'),
        ('Ap', 'Approuvé'),
        ('Av', 'Avancé'),
    ], 'Etat', default='draft', index=True, required=True, readonly=True, copy=False, track_visibility='always')

    # Les fonctions permettant de changer d'etat
    @api.multi
    def action_eng_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def action_recherche(self):
        for record in self:
            x_struct_id = int(self.company_id)
            x_type_empl = int(record.name)
            # record.env.cr.execute("SELECT count(*) FROM hr_cmpteur_avancer WHERE id_user = %d" %())
            record.env.cr.execute(
                """select (CA.name) as cat_emp, (T.id) as typeemp, (E.x_matricule_c) as mat_c, (E.x_matricule_f) as mat_f,(EM.id) as employe,(E.x_categorie) as cat,(E.x_echelle) as echel, (E.x_echellon) as echelon, (E.x_service) as service, (E.x_emploi) as emploi from hr_evaluation E,hr_payroll_structure T, hr_employee EM, hr_catemp CA Where CA.id = E.x_categorie_employe_id and E.x_type_employe_id = T.id and E.employee_id = EM.id and CA.id = %d and E.company_id = %d""" % (
                    x_type_empl, x_struct_id))
            rows = record.env.cr.dictfetchall()
            print('tableau recherche', rows)
            result = []

            # delete old payslip lines
            record.x_line_ids.unlink()
            for line in rows:
                result.append((0, 0,
                               {'x_type_employe_id': line['typeemp'], 'mat_f': line['mat_f'], 'mat_c': line['mat_c'],
                                'name': line['employe'], 'x_cat_id': line['cat'], 'x_echel_id': line['echel'],
                                'x_echelon_id': line['echelon'], 'x_service': line['service'],
                                'x_emploi': line['emploi']}))
            self.x_line_ids = result
            self.write({'state': 'R'})

    @api.multi
    def action_afficher_avancable(self):
        x_struct_id = int(self.company_id)
        print('struct', x_struct_id)
        for record in self.x_line_ids:
            x_empl_id = int(record.name.id)
            print('id emp', x_empl_id)
            date_fin = date.today()
            print('date fin', date_fin)

            record.env.cr.execute(
                "SELECT date_dernier_avancement FROM hr_cmpteur_avancer WHERE id_user = %d" % (x_empl_id))
            nbre = record.env.cr.fetchone()
            date_dernier = nbre and nbre[0] or 0
            print('date', date_dernier)
            """nb = nbre[0]['nbr']
            print('nb', nb)
            date_dernier = nbre[0]['date_dernier_avancement']
            print('date', date_dernier)"""

            if date_dernier == 0:
                record.env.cr.execute(
                    """select (CA.name) as cat_emp, (T.id) as typeemp, (E.x_matricule_c) as mat_c, (E.x_matricule_f) as mat_f,(EM.id) as employe,(E.x_categorie) as cat,(E.x_echelle) as echel, (E.x_echellon) as echelon, (E.x_service) as service, (E.x_emploi) as emploi,(E.x_note_globaless) as note from hr_evaluation E,hr_payroll_structure T, hr_employee EM, hr_catemp CA Where CA.id = E.x_categorie_employe_id and E.x_type_employe_id = T.id and E.employee_id = EM.id and E.x_note_globaless >= 6 and ('%s' - (EM.date_embauche)) >= 17 and EM.id = %d and EM.company_id = %d""" % (
                        date_fin, x_empl_id, x_struct_id))
                rows = record.env.cr.dictfetchall()
                print('tableau AVANCABLE', rows)
                result = []

                # delete old payslip lines
                self.x_line_a_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'x_type_employe_id': line['typeemp'], 'mat_f': line['mat_f'],
                                          'mat_c': line['mat_c'], 'name': line['employe'], 'x_cat_id': line['cat'],
                                          'x_echel_id': line['echel'], 'x_echelon_id': line['echelon'],
                                          'x_service': line['service'], 'x_emploi': line['emploi'],
                                          'x_note': line['note']}))
                self.x_line_a_ids = result
            else:
                record.env.cr.execute(
                    """select (CA.name) as cat_emp, (T.id) as typeemp, (E.x_matricule_c) as mat_c, (E.x_matricule_f) as mat_f,(EM.id) as employe,(E.x_categorie) as cat,(E.x_echelle) as echel, (E.x_echellon) as echelon, (E.x_service) as service, (E.x_emploi) as emploi,(E.x_note_globaless) as note from hr_evaluation E,hr_payroll_structure T, hr_employee EM, hr_catemp CA Where CA.id = E.x_categorie_employe_id and E.x_type_employe_id = T.id and E.employee_id = EM.id and E.x_note_globaless >= 7 and (date('%s') - date('%s')) >= 17 and EM.id = %d and EM.company_id = %d""" % (
                        date_fin, date_dernier, x_empl_id, x_struct_id))
                rows = record.env.cr.dictfetchall()
                print('tableau AVANCABLE COMPTEUR', rows)
                result = []

                # delete old payslip lines
                self.x_line_a_ids.unlink()
                for line in rows:
                    result.append((0, 0, {'x_type_employe_id': line['typeemp'], 'mat_f': line['mat_f'],
                                          'mat_c': line['mat_c'], 'name': line['employe'], 'x_cat_id': line['cat'],
                                          'x_echel_id': line['echel'], 'x_echelon_id': line['echelon'],
                                          'x_service': line['service'], 'x_emploi': line['emploi'],
                                          'x_note': line['note']}))
                self.x_line_a_ids = result

    @api.multi
    def action_confirme(self):
        self.write({'state': 'C'})

    @api.multi
    def action_approuve(self):
        self.write({'state': 'Ap'})

    @api.multi
    def action_avance(self):
        for record in self.x_line_a_ids:

            record.env.cr.execute("""SELECT * FROM hr_categorie""")
            rows_cat = record.env.cr.dictfetchall()
            print('tableau catégorie', rows_cat)

            record.env.cr.execute("""SELECT * FROM hr_echelle""")
            rows_echel = record.env.cr.dictfetchall()
            print('tableau echelle', rows_echel)

            record.env.cr.execute("""SELECT * FROM hr_echellon""")
            rows_echelon = record.env.cr.dictfetchall()
            print('tableau echelon', rows_echelon)

            for cat in rows_cat:
                if record.x_cat_id == 1:
                    self.x_line_avc_ids.x_cat_id = 2
                elif record.x_cat_id == 2:
                    self.x_line_avc_ids.x_cat_id = 3
                elif record.x_cat_id == 3:
                    self.x_line_avc_ids.x_cat_id = 4
                elif record.x_cat_id == 4:
                    self.x_line_avc_ids.x_cat_id = 5
                elif record.x_cat_id == 5:
                    self.x_line_avc_ids.x_cat_id = 6
                else:
                    print('rien à faire pour la catégorie')

        self.write({'state': 'Av'})

    # classe personnel avançable line


class HrPersonnelAvancableLine(models.Model):
    _name = 'hr_personnel_categorie_line'
    x_pers_id = fields.Many2one('hr_personnel_avancable')

    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", readonly=True)
    mat_f = fields.Char(string="Mle Fct", readonly=True)
    mat_c = fields.Char(string="Mle Ctrct", readonly=True)
    name = fields.Many2one('hr.employee', string='Employé', readonly=True)
    x_cat_id = fields.Char(string='Catégorie', readonly=True)
    x_echel_id = fields.Char(string='Echelle', readonly=True)
    x_echelon_id = fields.Char(string='Echelon', readonly=True)
    x_service = fields.Char(string='Service', readonly=True)
    x_emploi = fields.Char(string='Emploi', readonly=True)
    currents_users = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# classe personnel avançable line
class HrPersonnelAvancableLine(models.Model):
    _name = 'hr_personnel_avancable_line'
    x_pers_a_id = fields.Many2one('hr_personnel_avancable')

    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", readonly=True)
    mat_f = fields.Char(string="Mle Fct", readonly=True)
    mat_c = fields.Char(string="Mle Ctrct", readonly=True)
    name = fields.Many2one('hr.employee', string='Employé', readonly=True)
    x_cat_id = fields.Char(string='Catégorie', readonly=True)
    x_echel_id = fields.Char(string='Echelle', readonly=True)
    x_echelon_id = fields.Char(string='Echelon', readonly=True)
    x_service = fields.Char(string='Service', readonly=True)
    x_emploi = fields.Char(string='Emploi', readonly=True)
    x_note = fields.Float(string='Note globale', readonly=True)
    currents_users = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


# Classe pour gerer le compteur pour le personnel avancé
class Compteur_Code_Personnel_Avancer(models.Model):
    _name = "hr_cmpteur_avancer"
    id_user = fields.Integer('Id User')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    no_code = fields.Integer()
    date_dernier_avancement = fields.Date('Date dernier avancement')


# classe personnel avancé line
class HrPersonnelAvanceLine(models.Model):
    _name = 'hr_personnel_avance_line'
    x_pers_avc_id = fields.Many2one('hr_personnel_avancable')

    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", readonly=True)
    mat_f = fields.Char(string="Mle Fct", readonly=True)
    mat_c = fields.Char(string="Mle Ctrct", readonly=True)
    name = fields.Many2one('hr.employee', string='Employé', readonly=True)
    x_cat_id = fields.Many2one('hr_categorie', string='Catégorie', readonly=True)
    x_echel_id = fields.Many2one('hr_echelle', string='Echelle', readonly=True)
    x_echelon_id = fields.Many2one('hr_echellon', string='Echelon', readonly=True)
    currents_users = fields.Many2one('res.users', 'Utilisateur', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string="Etat", default=True)


class HrEmployeePrecompte(models.Model):
    _name = "hr_precompte"
    x_employees_id = fields.Many2one('hr.employee', string='Employee')
    nature_prcpte_id = fields.Many2one('hr_nature', string='Nature Précompte')
    x_precompte = fields.Float(string='Précompte :', readonly=False)
    x_retrait_prcpt_mois = fields.Float(string='Montant/Mois :')
    x_datedebut_prcpt = fields.Date(string='Date début', default=date.today())
    x_datefin_prcpt = fields.Date(string='Date fin', default=date.today())
    # date_jour = fields.Date(string='Date du jour', default=date.today() )
    duree = fields.Integer(string='Durée(en Jr)', readonly=True, store=True)

    # fonction pour contrôler les dates (date de debut ne doit pas etre superieur à la date de fin)
    @api.constrains('x_datedebut_prcpt', 'x_datefin_prcpt')
    def CtrlDate(self):

        for val in self:
            if val.x_datedebut_prcpt > val.x_datefin_prcpt:
                raise ValidationError(_(
                    "Enregistrement impossible. La date de début du precompte doit être toujours inférieure à la date de fin du precompte"))

    # fonction de recuperation du nombre de jours entre deux dates
    @api.onchange('x_datefin_prcpt', 'x_datedebut_prcpt')
    def nbre_jr_prct(self):
        for vals in self:
            if vals.x_datefin_prcpt and vals.x_datedebut_prcpt:
                vals.duree = (vals.x_datefin_prcpt - vals.x_datedebut_prcpt).days

    # fonction pour contrôler les montants precompte et le montant à prelever par mois
    @api.constrains('x_precompte', 'x_retrait_prcpt_mois')
    def CtrlMontant(self):

        for val in self:
            if val.x_retrait_prcpt_mois > val.x_precompte:
                raise ValidationError(_(
                    "Enregistrement impossible. Le montant du précompte ne doit pas être inférieur au montant à prélever mensuellement."))

    etat_prcpte = fields.Selection([
        ('active', "Activé"),
        ('desactive', "Désactivé"),
    ], required=False, string="Etat")


# Creation classe pour la gestion au prorata
class HrProrata(models.Model):
    _name = "hr_prorata"
    sequence = fields.Integer(help="Gives the sequence when displaying a list of prorata", default=10)
    """
    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = rec.employee_id
            result.append((rec.id, name))
        return result

    x_classe2 = fields.Integer(string="Classe2", readonly=True)
    """

    x_classe = fields.Integer(string="Classe", readonly=True)
    x_categorie = fields.Char(string="Catégorie", readonly=True)
    x_categorie_c = fields.Char(string="Catégorie Contractuelle", readonly=True)
    x_echelle = fields.Char(string="Echelle", readonly=True)
    x_echellon = fields.Char(string="Echelon", readonly=True)
    x_service = fields.Char(string="Service", readonly=True)
    x_emploi = fields.Char(string="Emploi", readonly=True)
    x_fonction = fields.Char(string="Fonction", readonly=True)
    x_banque = fields.Char(string="Banque", readonly=True)
    intitule = fields.Char(string="Intitule", readonly=True)
    num_banque = fields.Char(string="N° compte", readonly=True)
    x_type_employe = fields.Char(string="Type employe", readonly=True)
    x_matricule_c = fields.Char(string="Mle Contractuel ", readonly=True)
    x_matricule_f = fields.Char(string="Mle Fonctionnaire ", readonly=True)

    date_debut = fields.Date('Date debut', default=date.today())
    date_fin = fields.Date('Date fin', default=date.today())
    v_mois = fields.Char(string='mois')
    v_annee = fields.Char(string='mois')
    concat = fields.Char(string="Période", store=True)
    conc = fields.Char(store=True)

    # fonction pour retourner le mois en fonction de la date saisie
    @api.onchange('date_debut')
    def CtrlMois(self):
        for vals in self:
            if vals.date_debut:
                mois = vals.date_debut
                valeur_mois = str(mois.month)
                vals.v_mois = valeur_mois
                valeur_annee = str(mois.year)
                vals.v_annee = valeur_annee
                if vals.v_mois == '1':
                    vals.x_moi = 'janvier'
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)
                elif vals.v_mois == '2':
                    vals.x_moi = 'fevrier'
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)
                elif vals.v_mois == '3':
                    vals.x_moi = 'mars'
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)
                elif vals.v_mois == '4':
                    vals.x_moi = 'avril'
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)
                elif vals.v_mois == '5':
                    vals.x_moi = 'mai'
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)
                elif vals.v_mois == '6':
                    vals.x_moi = 'juin'
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)
                elif vals.v_mois == '7':
                    vals.x_moi = 'juillet'
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)
                elif vals.v_mois == '8':
                    vals.x_moi = 'aout'
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)
                elif vals.v_mois == '9':
                    vals.x_moi = 'septembre'
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)
                elif vals.v_mois == '10':
                    vals.x_moi = 'octobre'
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)
                elif vals.v_mois == '11':
                    vals.x_moi = 'novembre'
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)
                else:
                    vals.x_moi = 'decembre'

    x_mnt_carfo_p = fields.Float(string="Montant CARFO", readonly=False, compute="mnt_carfo_p_fields")
    x_mnt_patronal_carfo_p = fields.Float(string="Montant Patronal CARFO", readonly=False)
    x_mnt_cnss_p = fields.Float(string="Montant CNSS ", readonly=False, compute="mnt_cnss_p_field")
    x_mnt_patronal_cnss_p = fields.Float(string="Montant Patronal CNSS", readonly=False)

    nbre_jour_reel = fields.Integer(string="Nombre jour réel", required=True)
    nbre_jour_effectif = fields.Integer(string="Nombre jour effectif", required=True)
    _rec_name = "employee_id"
    # employee_id = fields.Many2one('hr.employee', string='Nom/Prénom(s)', required=True)
    employee_id = fields.Many2one('hr.employee', string='Nom/Prénom(s)', required=True)
    charge_p = fields.Integer(string='Charge', related="employee_id.charge")
    # x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    tout_coch_prorata = fields.Boolean(string='Tout Cocher')

    allocation_prorata = fields.Float(string='Allocation familiale', related="employee_id.x_allocation_familial")
    x_solde_indiciaire_ctrct = fields.Float(string='Salaire de Base', related="employee_id.x_solde_indiciaire_ctrct")
    x_indem_resp = fields.Float(string='Indem.Respon', related="employee_id.x_indem_resp")
    x_indem_astr = fields.Float(string='Indem.Astreinte', related="employee_id.x_indem_astr")
    x_indem_loge = fields.Float(string='Indem.Logement', related="employee_id.x_indem_loge")
    x_indem_techn = fields.Float(string='Indem.Techni', related="employee_id.x_indem_techn")
    x_indem_specif = fields.Float(string='Indem.Spécif', related="employee_id.x_indem_specif")
    x_indem_transp = fields.Float(string='Indem.Transport', related="employee_id.x_indem_transp")
    x_indem_inform = fields.Float(string='Indem.Informatique', related="employee_id.x_indem_inform")
    x_indem_exploit = fields.Float(string='Indem.Techni', related="employee_id.x_indem_exploit")
    x_indem_finance = fields.Float(string='Indem.Financ', related="employee_id.x_indem_finance")
    x_indem_garde = fields.Float(string='Indem.Garde', related="employee_id.x_indem_garde")
    x_indem_risque = fields.Float(string='Indem.Risque', related="employee_id.x_indem_risque")
    x_indem_caisse = fields.Float(string='Indem.Caisse', related="employee_id.x_indem_caisse")
    x_indem_veste = fields.Float(string='Indem.Veste', related="employee_id.x_indem_veste")
    x_indem_suj = fields.Float(string='Indem.Suj', related="employee_id.x_indem_suj")
    x_indem_form = fields.Float(string='Indem.Formation', related="employee_id.x_indem_form")
    x_indem_spec_inspect_ifc = fields.Float(string='Indem.Spec.ifc', related="employee_id.x_indem_spec_inspect_ifc")
    x_indem_spec_inspect_irp = fields.Float(string='Indem.Spec.ifc', related="employee_id.x_indem_spec_inspect_irp")
    x_indem_spec_inspect_ish = fields.Float(string='Indem.Spec.ish', related="employee_id.x_indem_spec_inspect_ish")
    x_indem_spec_inspect_trav = fields.Float(string='Indem.Spec.Trav', related="employee_id.x_indem_spec_inspect_trav")

    x_total_indemnites_prorata = fields.Float(string='Total indemnités', required=False, compute="depend_field_prorata",
                                              store=True)
    x_remuneration_total_prorata = fields.Float(string='Remuneration totale', readonly=True,
                                                compute="renum_total_field_p", store=True)
    x_salaire_brut_p = fields.Float(string='Salaire brut', required=False, compute="calcul_salaire_brut_p", store=True)
    x_abattement_forfaitaire_p = fields.Float(string='Abattement Forfaitaire', required=False,
                                              compute="calcul_abattement_p", store=True)

    mnt_prorata_salaire = fields.Float(string='Salaire de base', required=False)
    sal_coch_p = fields.Boolean(string='Salaire de base')

    mnt_prorata_resp = fields.Float(string='Indemn.Resp.', required=False)
    mnt_prorata_resp_exo = fields.Float(string='Exo.Resp.', required=False,
                                        compute='calcul_exoneration_responsabilite_p')
    resp_coch_p = fields.Boolean(string='Indemn.Resp.')

    mnt_prorata_astr = fields.Float(string='Indemn.Astreinte', required=False)
    astr_coch_p = fields.Boolean(string='Indemn.Astreinte')
    mnt_prorata_astr_exo = fields.Float(string='Exo.Astreinte.', required=False,
                                        compute='calcul_exoneration_astreintes_p')

    mnt_prorata_loge = fields.Float(string='Indemn.Logement', required=False)
    loge_coch_p = fields.Boolean(string='Indemn.Logement')

    mnt_prorata_techn = fields.Float(string='Indemn.Technicité', required=False)
    techn_coch_p = fields.Boolean(string='Indemn.Technicité')
    mnt_prorata_techn_exo = fields.Float(string='Exo.Technicite.', required=False,
                                         compute='calcul_exoneration_technicites_p')

    mnt_prorata_spec = fields.Float(string='Indemn.Spécifique GRH', required=False)
    spec_coch_p = fields.Boolean(string='Indemn.Spécifique GRH')
    mnt_prorata_spec_exo = fields.Float(string='Exo.GRH.', required=False, compute='calcul_exoneration_specifiques_p')

    mnt_prorata_trans = fields.Float(string='Indemn.Transport', required=False)
    transp_coch_p = fields.Boolean(string='Indemn.Transport')
    mnt_prorata_trans_exo = fields.Float(string='Exo.Trans.', required=False, compute='calcul_exoneration_transport_p')

    mnt_prorata_inf = fields.Float(string='Indemn.Informatique', required=False)
    resp_inf_p = fields.Boolean(string='Indemn.Informatique')
    mnt_prorata_inf_exo = fields.Float(string='Exo.Informatique.', required=False,
                                       compute='calcul_exoneration_informatique_p')

    mnt_prorata_explot = fields.Float(string='Indemn.Exploit-Reseaux', required=False)
    reseau_coch_p = fields.Boolean(string='Indemn.Exploit-Reseaux')
    mnt_prorata_explot_exo = fields.Float(string='Exo.Exploit-Reseaux.', required=False,
                                          compute='calcul_exoneration_informatique_p')

    mnt_prorata_resp_financ = fields.Float(string='Indemn.Resp.Financière', required=False)
    finac_coch_p = fields.Boolean(string='Indemn.Resp.Financière')
    mnt_prorata_resp_financ_exo = fields.Float(string='Exo.Resp.Financière.', required=False,
                                               compute='calcul_exoneration_resp_finance_p')

    mnt_prorata_garde = fields.Float(string='Indemn.Garde', required=False)
    garde_coch_p = fields.Boolean(string='Indemn.Garde')
    mnt_prorata_garde_exo = fields.Float(string='Exo.Garde.', required=False, compute='calcul_exoneration_garde_p')

    mnt_prorata_risque = fields.Float(string='Indemn.Risque', required=False)
    risq_coch_p = fields.Boolean(string='Indemn.Risque')
    mnt_prorata_risque_exo = fields.Float(string='Exo.Risque.', required=False, compute='calcul_exoneration_risque_p')

    mnt_prorata_sujetion = fields.Float(string='Indemn.Sujétion', required=False)
    sujetion_coch_p = fields.Boolean(string='Indemn.Sujétion')
    mnt_prorata_sujetion_exo = fields.Float(string='Exo.Sujétion.', required=False,
                                            compute='calcul_exoneration_sujetion_p')

    mnt_prorata_formation = fields.Float(string='Indemn.Formation', required=False)
    formation_coch_p = fields.Boolean(string='Indemn.Formation')
    mnt_prorata_formation_exo = fields.Float(string='Exo.Formation.', required=False,
                                             compute='calcul_exoneration_formation_p')

    mnt_prorata_caisse = fields.Float(string='Indemn.Caisse', required=False)
    caisse_coch_p = fields.Boolean(string='Indemn.Caisse')
    mnt_prorata_caisse_exo = fields.Float(string='Exo.Caisse.', required=False, compute='calcul_exoneration_caisse_p')

    mnt_prorata_veste = fields.Float(string='Indemn.Veste', required=False)
    veste_coch_p = fields.Boolean(string='Indemn.Veste')
    mnt_prorata_veste_exo = fields.Float(string='Exo.Veste.', required=False, compute='calcul_exoneration_veste_p')

    mnt_prorata_it = fields.Float(string='Indemn.IT', required=False)
    it_coch_p = fields.Boolean(string='Indemn.IT')
    mnt_prorata_it_exo = fields.Float(string='Exo.IT.', required=False, compute='calcul_exoneration_specifiques_p')

    mnt_prorata_ifc = fields.Float(string='Indemn.IFC', required=False)
    ifc_coch_p = fields.Boolean(string='Indemn.IFC')
    mnt_prorata_ifc_exo = fields.Float(string='Exo.IFC.', required=False,
                                       compute='calcul_exoneration_specifiques_ifc_p')

    mnt_prorata_irp = fields.Float(string='Indemn.IRP', required=False)
    irp_coch_p = fields.Boolean(string='Indemn.IRP')
    mnt_prorata_irp_exo = fields.Float(string='Exo.IRP', required=False, compute='calcul_exoneration_specifiques_irp')

    mnt_prorata_ish = fields.Float(string='Indemn.ISH', required=False)
    ish_coch_p = fields.Boolean(string='Indemn.ISH')
    mnt_prorata_ish_exo = fields.Float(string='Exo.IRP', required=False, compute='calcul_exoneration_specifiques_ish_p')

    autres_mnt_prorata = fields.Float(string='Autres', required=False)

    mnt_total_prorata = fields.Float(string='Total Prorata')

    # x_renum_total_exo = fields.Float(store=True, string="Rénum.Total", readonly=True)
    x_total_p_exo = fields.Float(store=True, string="Exo.Total", readonly=True, compute='calcul_exoneration_p_total')
    x_salaire_net_imposable_p = fields.Float(store=True, string="SNI", readonly=True, compute='calcul_sni_p')
    x_retenue_iuts_p = fields.Float(store=True, string="Retenue IUTS", readonly=True, compute='retenue_iuts_field_p')
    x_montant_charge_p = fields.Float(store=True, string="Montant Charge", readonly=True, compute='mnt_charge_field_p')
    x_iuts_net_p = fields.Float(store=True, string="IUTS NET", readonly=True, compute='net_iuts_fields_p')
    x_net_payer_ctrct_p = fields.Float(store=True, string="Salaire NET", readonly=True,
                                       compute='net_payer_ctrct_field_p')

    @api.onchange('employee_id')
    def remplir_champ5(self):
        self.x_emploi = self.employee_id.x_emploi_id.name
        self.x_fonction = self.employee_id.x_fonction_id.name
        self.x_type_employe = self.employee_id.x_type_employe_id.name
        self.x_service = self.employee_id.hr_service.name
        self.x_matricule_c = self.employee_id.matricule_genere
        self.x_matricule_f = self.employee_id.matricule
        self.x_echelle = self.employee_id.x_echelle_c_id.name
        self.x_echellon = self.employee_id.x_echellon_id.name
        self.x_categorie = self.employee_id.x_categorie_id.name
        self.x_categorie_c = self.employee_id.x_categorie_c_id.name
        self.x_classe = self.employee_id.x_classees_id.name
        self.x_banque = self.employee_id.x_banque_id.name
        self.intitule = self.employee_id.intitule
        self.num_banque = self.employee_id.num_banque

    @api.onchange('tout_coch_prorata')
    def tout_cocher(self):
        tout_coche = self.tout_coch_prorata
        for vals in self:
            if tout_coche == True:
                vals.sal_coch_p = True
                vals.resp_coch_p = True
                vals.astr_coch_p = True
                vals.loge_coch_p = True

                vals.techn_coch_p = True
                vals.spec_coch_p = True
                vals.transp_coch_p = True
                vals.resp_inf_p = True
                vals.reseau_coch_p = True
                vals.alloc_coch_p = True
                vals.finac_coch_p = True
                vals.garde_coch_p = True
                vals.risq_coch_p = True
                vals.sujetion_coch_p = True
                vals.formation_coch_p = True
                vals.caisse_coch_p = True
                vals.veste_coch_p = True
                vals.it_coch_p = True
                vals.ifc_coch_p = True
                vals.irp_coch_p = True
                vals.ish_coch_p = True

            else:
                vals.sal_coch_p = False
                vals.resp_coch_p = False
                vals.astr_coch_p = False
                vals.loge_coch_p = False

                vals.techn_coch_p = False
                vals.spec_coch_p = False
                vals.transp_coch_p = False
                vals.resp_inf_p = False
                vals.reseau_coch_p = False
                vals.alloc_coch_p = False
                vals.finac_coch_p = False
                vals.garde_coch_p = False
                vals.risq_coch_p = False
                vals.sujetion_coch_p = False
                vals.formation_coch_p = False
                vals.caisse_coch_p = False
                vals.veste_coch_p = False
                vals.it_coch_p = False
                vals.ifc_coch_p = False
                vals.irp_coch_p = False
                vals.ish_coch_p = False

    # fonction de calcul automatique des montants prorata des elements de salaire
    def action_prorata_ok(self):
        for vals in self:
            if vals.tout_coch_prorata == True:
                vals.mnt_prorata_salaire = round(
                    (vals.nbre_jour_effectif * vals.x_solde_indiciaire_ctrct) / vals.nbre_jour_reel)
                vals.mnt_prorata_resp = round((vals.nbre_jour_effectif * vals.x_indem_resp) / vals.nbre_jour_reel)
                vals.mnt_prorata_astr = round((vals.nbre_jour_effectif * vals.x_indem_astr) / vals.nbre_jour_reel)
                vals.mnt_prorata_loge = round((vals.nbre_jour_effectif * vals.x_indem_loge) / vals.nbre_jour_reel)
                vals.mnt_prorata_it = round(
                    (vals.nbre_jour_effectif * vals.x_indem_spec_inspect_trav) / vals.nbre_jour_reel)

                vals.mnt_prorata_techn = round((vals.nbre_jour_effectif * vals.x_indem_techn) / vals.nbre_jour_reel)
                vals.mnt_prorata_spec = round((vals.nbre_jour_effectif * vals.x_indem_specif) / vals.nbre_jour_reel)
                vals.mnt_prorata_trans = round((vals.nbre_jour_effectif * vals.x_indem_transp) / vals.nbre_jour_reel)
                vals.mnt_prorata_inf = round((vals.nbre_jour_effectif * vals.x_indem_inform) / vals.nbre_jour_reel)
                vals.mnt_prorata_explot = round((vals.nbre_jour_effectif * vals.x_indem_exploit) / vals.nbre_jour_reel)
                # vals.mnt_prorata_allocation = round((vals.nombre_jours * vals.x_allocation_familial) / 30)
                vals.mnt_prorata_resp_financ = round(
                    (vals.nbre_jour_effectif * vals.x_indem_finance) / vals.nbre_jour_reel)
                vals.mnt_prorata_garde = round((vals.nbre_jour_effectif * vals.x_indem_garde) / vals.nbre_jour_reel)
                vals.mnt_prorata_risque = round((vals.nbre_jour_effectif * vals.x_indem_risque) / vals.nbre_jour_reel)
                vals.mnt_prorata_sujetion = round((vals.nbre_jour_effectif * vals.x_indem_suj) / vals.nbre_jour_reel)
                vals.mnt_prorata_formation = round((vals.nbre_jour_effectif * vals.x_indem_form) / vals.nbre_jour_reel)
                vals.mnt_prorata_caisse = round((vals.nbre_jour_effectif * vals.x_indem_caisse) / vals.nbre_jour_reel)
                vals.mnt_prorata_veste = round((vals.nbre_jour_effectif * vals.x_indem_veste) / vals.nbre_jour_reel)
                vals.mnt_prorata_ifc = round(
                    (vals.nbre_jour_effectif * vals.x_indem_spec_inspect_ifc) / vals.nbre_jour_reel)
                vals.mnt_prorata_irp = round(
                    (vals.nbre_jour_effectif * vals.x_indem_spec_inspect_irp) / vals.nbre_jour_reel)
                vals.mnt_prorata_ish = round(
                    (vals.nbre_jour_effectif * vals.x_indem_spec_inspect_ish) / vals.nbre_jour_reel)

            if vals.sal_coch_p == True:
                vals.mnt_prorata_salaire = round(
                    (vals.nbre_jour_effectif * vals.x_solde_indiciaire_ctrct) / vals.nbre_jour_reel)
            if vals.resp_coch_p == True:
                vals.mnt_prorata_resp = round((vals.nbre_jour_effectif * vals.x_indem_resp) / vals.nbre_jour_reel)
            if vals.astr_coch_p == True:
                vals.mnt_prorata_astr = round((vals.nbre_jour_effectif * vals.x_indem_astr) / vals.nbre_jour_reel)
            if vals.loge_coch_p == True:
                vals.mnt_prorata_loge = round((vals.nbre_jour_effectif * vals.x_indem_loge) / vals.nbre_jour_reel)
            if vals.techn_coch_p == True:
                vals.mnt_prorata_techn = round((vals.nbre_jour_effectif * vals.x_indem_techn) / vals.nbre_jour_reel)
            if vals.spec_coch_p == True:
                vals.mnt_prorata_spec = round((vals.nbre_jour_effectif * vals.x_indem_specif) / vals.nbre_jour_reel)
            if vals.transp_coch_p == True:
                vals.mnt_prorata_trans = round((vals.nbre_jour_effectif * vals.x_indem_transp) / vals.nbre_jour_reel)
            if vals.resp_inf_p == True:
                vals.mnt_prorata_inf = round((vals.nbre_jour_effectif * vals.x_indem_inform) / vals.nbre_jour_reel)
            if vals.reseau_coch_p == True:
                vals.mnt_prorata_explot = round((vals.nbre_jour_effectif * vals.x_indem_exploit) / vals.nbre_jour_reel)
            if vals.finac_coch_p == True:
                vals.mnt_prorata_resp_financ = round(
                    (vals.nbre_jour_effectif * vals.x_indem_finance) / vals.nbre_jour_reel)
            if vals.garde_coch_p == True:
                vals.mnt_prorata_garde = round((vals.nbre_jour_effectif * vals.x_indem_garde) / vals.nbre_jour_reel)
            if vals.risq_coch_p == True:
                vals.mnt_prorata_risque = round((vals.nbre_jour_effectif * vals.x_indem_risque) / vals.nbre_jour_reel)
            if vals.sujetion_coch_p == True:
                vals.mnt_prorata_sujetion = round((vals.nbre_jour_effectif * vals.x_indem_suj) / vals.nbre_jour_reel)
            if vals.formation_coch_p == True:
                vals.mnt_prorata_formation = round((vals.nbre_jour_effectif * vals.x_indem_form) / vals.nbre_jour_reel)
            if vals.veste_coch_p == True:
                vals.mnt_prorata_veste = round((vals.nbre_jour_effectif * vals.x_indem_veste) / vals.nbre_jour_reel)
            if vals.caisse_coch_p == True:
                vals.mnt_prorata_caisse = round((vals.nbre_jour_effectif * vals.x_indem_caisse) / vals.nbre_jour_reel)
            if vals.it_coch_p == True:
                vals.mnt_prorata_it = round(
                    (vals.nbre_jour_effectif * vals.x_indem_spec_inspect_trav) / vals.nbre_jour_reel)
            if vals.ifc_coch_p == True:
                vals.mnt_prorata_ifc = round(
                    (vals.nbre_jour_effectif * vals.x_indem_spec_inspect_ifc) / vals.nbre_jour_reel)
            if vals.irp_coch_p == True:
                vals.mnt_prorata_irp = round(
                    (vals.nbre_jour_effectif * vals.x_indem_spec_inspect_irp) / vals.nbre_jour_reel)
            if vals.ish_coch_p == True:
                vals.mnt_prorata_irp = round(
                    (vals.nbre_jour_effectif * vals.x_indem_spec_inspect_ish) / vals.nbre_jour_reel)

    # Fonction pour reinitialiser les champs
    """
    @api.onchange('employee_id')
    def reinitialiser(self):
        val_id = int(self.employee_id)
        print("employe", val_id)
        self.env.cr.execute("UPDATE hr_prorata set nbre_jour_reel = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set nbre_jour_effectif = 0.0 where employee_id = %d" %(val_id))
        #self.env.cr.execute("UPDATE hr_prorata set allocation_prorata = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_salaire = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_resp = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_astr = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_loge = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_techn = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_spec = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_trans = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_inf = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_explot = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_resp_financ = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_garde = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_risque = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_sujetion = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_formation = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_caisse = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_veste = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_ifc = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_irp = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_ish = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set mnt_prorata_it = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set x_total_indemnites_prorata = 0.0 where employee_id = %d" %(val_id))
        self.env.cr.execute("UPDATE hr_prorata set x_remuneration_total_prorata = 0.0 where employee_id = %d" %(val_id))
        """

    # fonction qui permet d'additionner les indemnités
    @api.depends('mnt_prorata_resp', 'mnt_prorata_astr', 'mnt_prorata_loge', 'mnt_prorata_techn',
                 'mnt_prorata_spec', 'mnt_prorata_it',
                 'mnt_prorata_trans', 'mnt_prorata_inf', 'mnt_prorata_explot', 'mnt_prorata_resp_financ',
                 'mnt_prorata_garde', 'mnt_prorata_risque', 'mnt_prorata_sujetion', 'mnt_prorata_formation',
                 'mnt_prorata_caisse', 'mnt_prorata_veste', 'mnt_prorata_ifc', 'mnt_prorata_irp', 'mnt_prorata_ish'
                 )
    # @api.onchange('x_indem_loge')
    def depend_field_prorata(self):
        for val in self:
            val.x_total_indemnites_prorata = round(
                val.mnt_prorata_resp + val.mnt_prorata_astr + val.mnt_prorata_loge + val.mnt_prorata_techn + val.mnt_prorata_spec + val.mnt_prorata_trans + val.mnt_prorata_inf + val.mnt_prorata_explot + val.mnt_prorata_resp_financ + val.mnt_prorata_garde + val.mnt_prorata_risque + val.mnt_prorata_sujetion + val.mnt_prorata_formation + val.mnt_prorata_caisse + val.mnt_prorata_garde + val.mnt_prorata_ifc + val.mnt_prorata_irp + val.mnt_prorata_ish)
            # val.total_indemnites = val.x_total_indemnites
            # print("total  des indemnite", val.x_total_indemnites_prorata)

    # fonction permettant de calculer la remuneration au prorata
    @api.depends('mnt_prorata_salaire', 'x_total_indemnites_prorata', 'allocation_prorata')
    def renum_total_field_p(self):
        for val in self:
            print("SB prorata", val.mnt_prorata_salaire)
            print("total indemnités _prorata", val.x_total_indemnites_prorata)
            print("allocation au _prorata", val.allocation_prorata)
            # val.x_remuneration_total = round(val.x_solde_indiciaire_ctrct + val.x_total_indemnites + val.x_emolument_ctrct_net + val.x_allocation_familial)
            val.x_remuneration_total_prorata = round(
                val.mnt_prorata_salaire + val.x_total_indemnites_prorata + val.allocation_prorata)
            print("remuneration total", val.x_remuneration_total_prorata)

    # fonction qui permet d'avoir le montant carfo à partir du salaire de base au prorata
    @api.depends('mnt_prorata_salaire')
    def mnt_carfo_p_fields(self):
        for val in self:
            if val.employee_id.x_type_employe_id.name == 'Fonctionnaire Detaché' or val.employee_id.x_type_employe_id.name == 'fonctionnaire detaché' or val.employee_id.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or val.employee_id.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or val.employee_id.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION':
                # print('Type employe',val.x_type_employe_id.name)
                val.x_mnt_carfo_p = round((val.mnt_prorata_salaire * 8) / 100)
                val.x_mnt_patronal_carfo_p = round((val.mnt_prorata_salaire * 15.5) / 100)

                val.x_mnt_cnss_p = 0.0
                val.x_mnt_patronal_cnss_p = 0.0

    # fonction qui permet d'avoir le montant cnss à partir du salaire de base
    @api.onchange('employee_id')
    @api.depends('x_remuneration_total_prorata')
    def mnt_cnss_p_field(self):
        for val in self:
            if val.employee_id.x_type_employe_id.name == 'Contractuel' or val.employee_id.x_type_employe_id.name == 'contractuel' or val.employee_id.x_type_employe_id.name == 'CONTRACTUEL':
                resul = round((val.x_remuneration_total_prorata * 5.5) / 100)
                if resul > 33000:
                    val.x_mnt_cnss_p = 33000
                    val.x_mnt_carfo_p = 0.0
                    val.x_mnt_patronal_carfo_p = 0.0
                else:
                    val.x_mnt_cnss_p = round((val.x_remuneration_total_prorata * 5.5) / 100)
                    val.x_mnt_patronal_cnss_p = round((val.x_remuneration_total_prorata * 16) / 100)
                    val.x_mnt_carfo_p = 0.0
                    val.x_mnt_patronal_carfo_p = 0.0

    # calcul du salaire brut pour le fonctionnaire puisque Rénumeration Totale déjà connue
    @api.onchange('employee_id')
    @api.depends('x_remuneration_total_prorata', 'x_mnt_carfo_p', 'x_mnt_cnss_p')
    def calcul_salaire_brut_p(self):
        for vals in self:
            type_emp = vals.employee_id.x_type_employe_id.name
            if type_emp == "Contractuel" or type_emp == "CONTRACTUEL":
                vals.x_salaire_brut_p = vals.x_remuneration_total_prorata - vals.x_mnt_cnss_p
            else:
                vals.x_salaire_brut_p = vals.x_remuneration_total_prorata - vals.x_mnt_carfo_p

    # calcul DU SALAIRE NET IMPOSABLE (SNI)
    @api.depends('x_salaire_brut_p', 'x_total_p_exo', 'x_abattement_forfaitaire_p')
    def calcul_sni_p(self):
        for vals in self:
            val1 = vals.x_salaire_brut_p - vals.x_total_p_exo - vals.x_abattement_forfaitaire_p
            print('Val1', val1)
            val2 = val1 - (val1 % 100)
            print('Val2', val2)
            vals.x_salaire_net_imposable_p = val2

    # calcul abattement forfaitaire
    @api.depends('mnt_prorata_salaire')
    def calcul_abattement_p(self):
        for vals in self:
            type_emp = vals.employee_id.x_type_employe_id.name
            x_cat = vals.employee_id.x_categorie_c_id.name
            x_cat_f = vals.employee_id.x_categorie_id.name
            if type_emp == "Contractuel" or type_emp == "CONTRACTUEL":
                if x_cat == '1' or x_cat == '2' or x_cat == '6':
                    vals.x_abattement_forfaitaire_p = round((vals.mnt_prorata_salaire * 20) / 100)
                else:
                    vals.x_abattement_forfaitaire_p = round((vals.mnt_prorata_salaire * 25) / 100)
            else:
                if x_cat_f == 'A' or x_cat_f == 'B' or x_cat_f == 'P':
                    vals.x_abattement_forfaitaire_p = round((vals.mnt_prorata_salaire * 20) / 100)
                else:
                    vals.x_abattement_forfaitaire_p = round((vals.mnt_prorata_salaire * 25) / 100)

    # fonction qui permet d'avoir la de l'iuts pour les deux
    @api.depends('x_salaire_net_imposable_p')
    def retenue_iuts_field_p(self):
        for val in self:
            if 0 <= val.x_salaire_net_imposable_p <= 30000.0:
                val.x_retenue_iuts_p = round(val.x_salaire_net_imposable_p * 0)
            elif 30001.0 <= val.x_salaire_net_imposable_p <= 50000.0:
                val.x_retenue_iuts_p = round((val.x_salaire_net_imposable_p - 30001.0) * 12.1 / 100)
            elif 50001.0 <= val.x_salaire_net_imposable_p <= 80000.0:
                val.x_retenue_iuts_p = round(((val.x_salaire_net_imposable_p - 50001.0) * 13.9 / 100) + 2420)
            elif 80001.0 <= val.x_salaire_net_imposable_p <= 120000.0:
                val.x_retenue_iuts_p = round(((val.x_salaire_net_imposable_p - 80001.0) * 15.7 / 100) + 6590)
            elif 120001.0 <= val.x_salaire_net_imposable_p <= 170000.0:
                val.x_retenue_iuts_p = round(((val.x_salaire_net_imposable_p - 120001.0) * 18.4 / 100) + 12870)
            elif 170001.0 <= val.x_salaire_net_imposable_p <= 250000.0:
                val.x_retenue_iuts_p = round(((val.x_salaire_net_imposable_p - 170001.0) * 21.7 / 100) + 22070)
            else:
                val.x_retenue_iuts_p = round(((val.x_salaire_net_imposable_p - 250001.0) * 25 / 100) + 39430)

    # indemnités de responsabilité
    @api.onchange('employee_id')
    @api.depends('mnt_prorata_resp', 'x_salaire_brut_p')
    def calcul_exoneration_responsabilite_p(self):
        premiere_limite = 0
        for vals in self:
            print("Indemn.resp", vals.mnt_prorata_resp)
            print("Salaire Brut", vals.x_salaire_brut_p)
            premiere_limite_res = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_resp_exo = min([premiere_limite_res, vals.mnt_prorata_resp, 50000])

    """Indemnités de transport"""

    @api.depends('mnt_prorata_trans', 'x_salaire_brut_p')
    def calcul_exoneration_transport_p(self):
        for vals in self:
            premiere_limite_trans = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_trans_exo = min([premiere_limite_trans, vals.mnt_prorata_trans, 30000])

    # indemnités de astreintes

    @api.depends('mnt_prorata_astr', 'x_salaire_brut_p')
    def calcul_exoneration_astreintes_p(self):
        for vals in self:
            premiere_limite_astr = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_astr_exo = min([premiere_limite_astr, vals.mnt_prorata_astr, 50000])
            print("EXO astr", vals.mnt_prorata_astr_exo)

    # indemnités de technicités

    @api.depends('mnt_prorata_techn', 'x_salaire_brut_p')
    def calcul_exoneration_technicites_p(self):
        for vals in self:
            premiere_limite_tech = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_techn_exo = min([premiere_limite_tech, vals.mnt_prorata_techn, 50000])

    # indemnités de spécifiques GRH

    @api.depends('mnt_prorata_spec', 'x_salaire_brut_p')
    def calcul_exoneration_specifiques_p(self):
        premiere_limite_spec = 0
        for vals in self:
            premiere_limite_spec = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_spec_exo = min([premiere_limite_spec, vals.mnt_prorata_spec, 50000])

    # indemnités de spécifiques IT

    @api.depends('mnt_prorata_it', 'x_salaire_brut_p')
    def calcul_exoneration_specifiques_it_p(self):
        for vals in self:
            premiere_limite_spec_it = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_it_exo = min([premiere_limite_spec_it, vals.mnt_prorata_it, 50000])

    # indemnités d'informatiques
    @api.depends('mnt_prorata_inf', 'x_salaire_brut_p')
    def calcul_exoneration_informatique_p(self):
        for vals in self:
            premiere_limite_info = round(vals.x_salaire_brut_p * 0.05)
            vals.mnt_prorata_inf_exo = min([premiere_limite_info, vals.mnt_prorata_inf, 50000])

    # indemnités de exploitations reseaux
    @api.depends('mnt_prorata_explot', 'x_salaire_brut_p')
    def calcul_exoneration_exploitation_p(self):
        for vals in self:
            premiere_limite_exploi = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_explot_exo = min([premiere_limite_exploi, vals.mnt_prorata_explot, 50000])

    # indemnités de spécifiques IRP
    @api.depends('mnt_prorata_irp', 'x_salaire_brut_p')
    def calcul_exoneration_specifiques_irp(self):
        for vals in self:
            premiere_limite_spec_irp = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_irp_exo = min([premiere_limite_spec_irp, vals.mnt_prorata_irp, 50000])

    # indemnités de spécifiques IFC
    @api.depends('mnt_prorata_ifc', 'x_salaire_brut_p')
    def calcul_exoneration_specifiques_ifc_p(self):
        for vals in self:
            premiere_limite_ifc = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_ifc_exo = min([premiere_limite_ifc, vals.mnt_prorata_ifc, 50000])

    # indemnités de spécifiques ISH
    @api.depends('mnt_prorata_ish', 'x_salaire_brut_p')
    def calcul_exoneration_specifiques_ish_p(self):
        for vals in self:
            premiere_limite_spec_ish = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_ish_exo = min([premiere_limite_spec_ish, vals.mnt_prorata_ish, 15000])

    # indemnités de responsabilités financières
    @api.depends('mnt_prorata_resp_financ', 'x_salaire_brut_p')
    def calcul_exoneration_resp_finance_p(self):
        for vals in self:
            premiere_limite_finance = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_resp_financ_exo = min([premiere_limite_finance, vals.mnt_prorata_resp_financ, 50000])

    # indemnités de garde
    @api.depends('mnt_prorata_garde', 'x_salaire_brut_p')
    def calcul_exoneration_garde_p(self):
        for vals in self:
            premiere_limite_garde = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_garde_exo = min([premiere_limite_garde, vals.mnt_prorata_garde, 50000])

    # indemnités de risque
    @api.depends('mnt_prorata_risque', 'x_salaire_brut_p')
    def calcul_exoneration_risque_p(self):
        for vals in self:
            premiere_limite_risque = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_risque_exo = min([premiere_limite_risque, vals.mnt_prorata_risque, 50000])

    # indemnités de sujetion
    @api.depends('mnt_prorata_sujetion', 'x_salaire_brut_p')
    def calcul_exoneration_sujetion_p(self):
        for vals in self:
            premiere_limite_suj = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_sujetion_exo = min([premiere_limite_suj, vals.mnt_prorata_sujetion, 50000])

    # indemnités de formation
    @api.depends('mnt_prorata_formation', 'x_salaire_brut_p')
    def calcul_exoneration_formation_p(self):
        for vals in self:
            premiere_limite_form = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_formation_exo = min([premiere_limite_form, vals.mnt_prorata_formation, 50000])

    # indemnités de caisse
    @api.depends('mnt_prorata_caisse', 'x_salaire_brut_p')
    def calcul_exoneration_caisse_p(self):
        for vals in self:
            premiere_limite_caisse = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_caisse_exo = min([premiere_limite_caisse, vals.mnt_prorata_caisse, 50000])

    # indemnités de veste
    @api.depends('mnt_prorata_veste', 'x_salaire_brut_p')
    def calcul_exoneration_veste_p(self):
        for vals in self:
            premiere_limite_veste = round((vals.x_salaire_brut_p * 5) / 100)
            vals.mnt_prorata_veste_exo = min([premiere_limite_veste, vals.mnt_prorata_veste, 50000])

    # Calcul total exonérations
    @api.depends('mnt_prorata_veste_exo', 'mnt_prorata_caisse_exo', 'mnt_prorata_formation_exo',
                 'mnt_prorata_risque_exo',
                 'mnt_prorata_garde_exo', 'mnt_prorata_resp_financ_exo', 'mnt_prorata_ish_exo',
                 'mnt_prorata_ifc_exo', 'mnt_prorata_irp_exo', 'mnt_prorata_explot_exo', 'mnt_prorata_it_exo',
                 'mnt_prorata_inf_exo', 'mnt_prorata_spec_exo', 'mnt_prorata_techn_exo', 'mnt_prorata_astr_exo',
                 'mnt_prorata_resp_exo', 'mnt_prorata_trans_exo', 'mnt_prorata_sujetion_exo')
    def calcul_exoneration_p_total(self):
        for vals in self:
            vals.x_total_p_exo = vals.mnt_prorata_trans_exo + vals.mnt_prorata_resp_exo + vals.mnt_prorata_astr_exo + vals.mnt_prorata_techn_exo + vals.mnt_prorata_spec_exo + vals.mnt_prorata_inf_exo + vals.mnt_prorata_ifc_exo + vals.mnt_prorata_irp_exo + vals.mnt_prorata_explot_exo + vals.mnt_prorata_it_exo + vals.mnt_prorata_ish_exo + vals.mnt_prorata_resp_financ_exo + vals.mnt_prorata_garde_exo + vals.mnt_prorata_risque_exo + vals.mnt_prorata_formation_exo + vals.mnt_prorata_caisse_exo + vals.mnt_prorata_veste_exo + vals.mnt_prorata_sujetion_exo

    # fonction qui permet d'avoir le montant en fonction du nombre de charge pour les deux
    @api.depends('charge_p')
    def mnt_charge_field_p(self):
        for val in self:
            if val.charge_p == 0:
                val.x_montant_charge_p = round(val.x_retenue_iuts_p * 0)
            elif val.charge_p == 1:
                val.x_montant_charge_p = round((val.x_retenue_iuts_p * 8) / 100)
            elif val.charge_p == 2:
                val.x_montant_charge_p = round((val.x_retenue_iuts_p * 10) / 100)
            elif val.charge_p == 3:
                val.x_montant_charge_p = round((val.x_retenue_iuts_p * 12) / 100)
            elif val.charge_p == 4:
                val.x_montant_charge_p = round((val.x_retenue_iuts_p * 14) / 100)
            else:
                print("Nombre d'enfant maximum pris en charge atteint donc du coup on prend pour les 4 enfants")
                val.x_montant_charge_p = round((val.x_retenue_iuts_p * 14) / 100)

    # fonction qui permet d'avoir le montant net de l'iuts pour le contractuel
    @api.depends('x_retenue_iuts_p', 'x_montant_charge_p')
    def net_iuts_fields_p(self):
        for val in self:
            val.x_iuts_net_p = round(val.x_retenue_iuts_p - val.x_montant_charge_p)

    # fonction qui permet d'avoir le montant net à payer pour les contractuels
    @api.depends('employee_id.x_type_employe_id', 'x_remuneration_total_prorata', 'x_mnt_cnss_p', 'x_mnt_carfo_p',
                 'x_iuts_net_p')
    def net_payer_ctrct_field_p(self):
        for val in self:
            if val.x_remuneration_total_prorata:
                if val.employee_id.x_type_employe_id.name == 'Fonctionnaire Detaché' or val.employee_id.x_type_employe_id.name == 'fonctionnaire detaché' or val.employee_id.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or val.employee_id.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or val.employee_id.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION':
                    val.x_net_payer_ctrct_p = round(
                        val.x_remuneration_total_prorata - val.x_iuts_net_p - val.x_mnt_carfo_p)
                elif val.employee_id.x_type_employe_id.name == 'Contractuel' or val.employee_id.x_type_employe_id.name == 'CONTRACTUEL' or val.employee_id.x_type_employe_id.name == 'contractuel':
                    val.x_net_payer_ctrct_p = round(
                        val.x_remuneration_total_prorata - val.x_iuts_net_p - val.x_mnt_cnss_p)

    """
    # indemnités de residence
    @api.depends('x_solde_indiciaire', 'x_salaire_brut')
    def calcul_exoneration_residence(self):
        for vals in self:
            premiere_limite = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_residence_exo = min([premiere_limite, vals.x_solde_indiciaire, 50000])

    # exoneration prime de rendement
    @api.depends('x_indem_prime_rendement', 'x_salaire_brut')
    def calcul_exoneration_prime(self):
        for vals in self:
            premiere_limite = round((vals.x_salaire_brut * 5) / 100)
            vals.x_prime_exo = min([premiere_limite, vals.x_indem_prime_rendement, 50000])

    # Calcul total exonérations
    @api.depends('x_indem_resp_exo', 'x_indem_astr_exo', 'x_indem_techn_exo', 'x_indem_specif_exo',
                 'x_indem_specif_it_exo', 'x_indem_specif_ifc_exo', 'x_indem_specif_irp_exo',
                 'x_indem_specif_ish_exo', 'x_indem_loge_exo', 'x_indem_transp_exo', 'x_indem_inform_exo',
                 'x_indem_exploit_exo', 'x_indem_finance_exo', 'x_indem_garde_exo', 'x_indem_risque_exo',
                 'x_indem_suj_exo', 'x_indem_form_exo', 'x_indem_caisse_exo', 'x_indem_veste_exo', 'x_prime_exo')
    def calcul_exoneration_total(self):
        for vals in self:
            vals.x_total_exo = vals.x_indem_resp_exo + vals.x_indem_astr_exo + vals.x_indem_techn_exo + vals.x_indem_specif_exo + vals.x_indem_loge_exo + vals.x_indem_transp_exo + vals.x_indem_inform_exo + vals.x_indem_exploit_exo + vals.x_indem_finance_exo + vals.x_indem_garde_exo + vals.x_indem_risque_exo + vals.x_indem_suj_exo + vals.x_indem_form_exo + vals.x_indem_caisse_exo + vals.x_indem_veste_exo + vals.x_indem_specif_it_exo + vals.x_indem_specif_ifc_exo + vals.x_indem_specif_irp_exo + vals.x_indem_specif_ish_exo + vals.x_prime_exo

    # calcul DU SALAIRE NET IMPOSABLE (SNI)
    @api.depends('x_salaire_brut', 'x_total_exo', 'x_abattement_forfaitaire')
    def calcul_sni(self):
        for vals in self:
            val1 = vals.x_salaire_brut - vals.x_total_exo - vals.x_abattement_forfaitaire
            print('Val1', val1)
            val2 = val1 - (val1 % 100)
            print('Val2', val2)
            vals.x_salaire_net_imposable = val2



    """


# heritage de la classe employee
class HrEmployees(models.Model):
    _inherit = "hr.employee"

    #information sur le salaire
    x_salaire_base = fields.Float(string='Salaire de base')
    x_total_indemnites = fields.Float(string="Totale Indemnité", readonly=True, compute='depend_field', store=True)
    x_remuneration_total = fields.Float("Rémunération totale", readonly=True, compute='renum_total_field', store=True)
    x_salaire_brut = fields.Float(store=True, string="Salaire Brut", readonly=True, compute='calcul_salaire_brut')
    x_abattement_forfaitaire = fields.Float(store=True, string="Abattement", readonly=True, compute='calcul_abattement')
    x_salaire_net_imposable = fields.Float(store=True, string="SNI", readonly=True, compute='calcul_sni')
    x_total_exo = fields.Float(store=True, string="Exo.Total", readonly=True, compute='calcul_exoneration_total')

    # Fonction permettant de concatener pour obtenir la classification globale de l'employé dans la fonction publique
    @api.onchange('x_solde_indiciaire_net', 'x_solde_indiciaire_ctrct', 'x_type_employe_id')
    def set_x_salaire_base(self):
        for rec in self:
            if rec.x_type_employe_id.code == 'FCT_MD':
                rec.x_salaire_base = rec.x_solde_indiciaire_net
            if rec.x_type_employe_id.code in ('CTRCT', 'FCT_DETACH'):
                rec.x_salaire_base = rec.x_solde_indiciaire_ctrct

    # Fonction permettant de concatener pour obtenir la classification globale de l'employé dans la fonction publique
    @api.onchange('x_categorie_id', 'x_echelle_id', 'x_echellon_id')
    def _result_conc(self):
        for concat in self:
            concat.x_classification = str(concat.x_categorie_id.name) + '.' + str(concat.x_echelle_id.name) + '.' + str(
                concat.x_echellon_id.name)

    # Fonction permettant de concatener pour obtenir la classification globale de l'employé dans l'epe
    @api.onchange('x_categorie_c_id', 'x_echelle_c_id', 'x_echellon_c_id')
    def _result_conc_ctrct(self):
        for concat in self:
            concat.x_classification_ctrct = str(concat.x_categorie_c_id.name) + '.' + str(
                concat.x_echelle_c_id.name) + '.' + str(concat.x_echellon_c_id.name)

    x_compte_conge = fields.Integer(string="Congés Annuels Restants", default=0, readonly=True)
    x_compte_conge_maternite = fields.Integer(string="Congés de Maternité Restants", default=0, readonly=True)
    x_compte_conge_paternite = fields.Integer(string="Congés de Paternite Restants", default=0, readonly=True)
    x_compte_auto_abs = fields.Integer(string="Autorisations Absences Restants", default=0, readonly=True)
    x_compte_examens = fields.Integer(string="Congés Examens/Concours Restants", default=0, readonly=True)

    matricule_genere = fields.Char(string="Matricule")
    matricule = fields.Char(string="Mle Fonctionnaire ")
    x_email = fields.Char(string="Email")
    x_nb_annee_retraite = fields.Many2one("hr_nbreannee", string="Age de retraite", required=True)
    # hr_service = fields.Many2one("hr_service",string = "Service")
    x_categorie_employe_id = fields.Many2one("hr_catemp", string="Catégorie employé", required=True)
    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    x_lib_type_emp = fields.Char('Libelle', readonly=True)
    x_fonction_id = fields.Many2one("hr_fonctionss", string="Fonction", required=True,
                                    default=lambda self: self.env['hr_fonctionss'].search(
                                        [('name', '=', 'Choisir Fonction')]))
    x_emploi_id = fields.Many2one("hr_emploi", string="Emploi", required=True,
                                  default=lambda self: self.env['hr_emploi'].search([('name', '=', 'Choisir Emploi')]))
    x_zone_id = fields.Many2one("hr_zone", string="Zone", required=True)
    x_type_piece_id = fields.Many2one("hr_typepiece", string="Type pièce", required=True)
    x_diplome_id = fields.Many2one("hr_diplome", string="Dernier diplôme")
    x_diplome_recrut_id = fields.Many2one("hr_diplome", string="Diplôme de recrutement")
    x_date_naissance = fields.Date(string='Date de naissance', required=True)
    x_date_retraite = fields.Date(string='Date retraite')
    tel = fields.Char(string='Telephone', required=True)

    resultat_visite_medic = fields.Text(string='Resultats medical')
    x_vehicule_fction_id = fields.Many2one('fleet.vehicle', string='Véhicule de fonction')
    x_vehicule_service_id = fields.Many2one('fleet.vehicle', string='Véhicule de service')
    x_vehicule_affect_id = fields.Many2one('fleet.vehicle', string='Véhicule affecté')
    fichier_joint = fields.Binary(string='Joindre Laisser passer', attachment=True)

    x_nationalite_id = fields.Many2one('ref_nationalite', default=lambda self: self.env['ref_nationalite'].search(
        [('code_nationalite', '=', 'BF')]), string='Nationalité')
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_structure_id = fields.Many2one('res.company', string="Structure",
                                     default=lambda self: self.env.user.company_id.id)
    genre = fields.Selection([
        ('masculin', 'Masculin'),
        ('feminin', 'Feminin'),
        ('autre', 'Autre')
    ], string='Genre', default="masculin")
    situation_marital = fields.Selection([
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
        ('concubinage', 'Concubinage'),
        ('veuf(ve)', 'Veuf(ve)'),
        ('divorce', 'Divorcé(e)')
    ], string='Etat Civil', groups="hr.group_hr_user", default='celibataire')
    nom_conjoint = fields.Char(string='Nom du conjoint(e)')
    date_naiss_conjoint = fields.Date(string='Date de naissance')
    branche = fields.Char(string="Branche d'étude")
    ecole = fields.Char(string="Ecole/Université")
    personne_id = fields.Char('Personne à prevenir en cas de besoin', required=True)
    charge_femme = fields.Integer(string="Charge femme", required=True)
    charge_enfant = fields.Integer(string="Charge enfant", required=True, compute="calcul_charge_enfant")
    charge = fields.Integer(store=True, string="Charge total", readonly=True)
    lieu_naiss = fields.Many2one('ref_localite', string='Lieu de naissance')
    ref_identification = fields.Char(string='Ref.Identification', required=True)
    observations = fields.Text(string='Observations')
    num_declaration = fields.Char(string='N°CNSS')
    x_lines_ids = fields.One2many('hr_employee_piece', 'x_employee_id', string='Ajouter Pièce jointe')
    x_acte_ids = fields.One2many('hr_piece_detachement', 'x_employees_id', string='Joindre acte Detachement')
    x_acte_dec_ids = fields.One2many('hr_piece_disposition', 'x_employees_id', string='Joindre acte Decision')
    x_actes_ids = fields.One2many('hr_decret_nomination', 'x_employees_id', string='Joindre acte de nomination')
    x_dossier_ind_ids = fields.One2many('hr_dossier_individuel', 'x_employees_id', string='Joindre Fichiers')
    x_precompte_ids = fields.One2many('hr_precompte', 'x_employees_id', string='Ajouter precompte')
    x_retrait_prcpt_mois = fields.Float(string='Montant/Mois :')

    x_line_reg_ids = fields.One2many('hr_regleecheance_line', 'name', string='Règle Echéance', readonly=True)
    x_line_reg_details_ids = fields.One2many('hr_regleecheancedetails_line', 'name', string='Règle Echéance Détails',
                                             readonly=True)
    x_indemn_ids = fields.One2many('hr_employee_indemnite', 'emp_id', string='Indemnites')
    x_allocation_familial = fields.Float(store=True, string='Allocation Familiale')
    x_indemnite_residence = fields.Float(string='Indemnité de residence')
    x_indice = fields.Float(string='Indice')

    est_responsable = fields.Selection([
        (1, "Oui"),
        (2, "Non"),
    ], required=False, string="Est responsable")

    @api.onchange('x_type_employe_id')
    def remplir_lib(self):
        for vals in self:
            vals.x_lib_type_emp = vals.x_type_employe_id.name

    # fonction de recuperation du nombre de jours entre deux dates
    @api.onchange('x_datefin_prcpt', 'x_datedebut_prcpt')
    def nbre_jr_prct(self):
        for vals in self:
            if vals.x_datefin_prcpt and vals.x_datedebut_prcpt:
                vals.duree = (vals.x_datefin_prcpt - vals.x_datedebut_prcpt).days

    def action_rafraichir(self):
        for vals in self:
            val_id = self.id

    # fonction de calcul du montant de precompte d'un employé
    def action_rechercher(self):
        for vals in self:
            val_id = self.id
            val_id_prcpt = self.nature_prcpte_id
            vals.env.cr.execute("select * from hr_regleecheance_line where name = %d and nature_prcpte_id = %d" % (
                val_id, val_id_prcpt))
            rows = vals.env.cr.dictfetchall()
            print('lignes', rows)
            result = []

            # delete old details transactions lines
            vals.x_line_reg_details_ids.unlink()
            for line in rows:
                result.append((0, 0, {'name': line['name'], 'date': line['date'], 'mnt_echeance': line['mnt_echeance'],
                                      'reste_echeance': line['reste_echeance'], 'reste_a_payer': line['reste_a_payer'],
                                      'date_debut': line['date_debut'], 'date_fin': line['date_fin'],
                                      'duree_prcpte': line['duree_prcpte'],
                                      'nature_prcpte_id': line['nature_prcpte_id']}))
            self.x_line_reg_details_ids = result

    # fonction de calcul du montant de l'allocation a ajouter pour EMO
    @api.onchange('charge_enfant', 'x_lib_type_emp')
    def mnt_alloc(self):
        for vals in self:
            typ_emp = vals.x_lib_type_emp
            if vals.x_type_employe_id.code == 'CTRCT':
                vals.x_allocation_familial = 0
            else:
                vals.x_allocation_familial = vals.charge_enfant * 2000

    # FONCTION DE calcul de la date de depart a la retraite d'un employe
    @api.onchange("x_date_naissance", "x_nb_annee_retraite")
    def _compute_date_retraite(self):
        if self.x_nb_annee_retraite or self.x_date_naissance:
            anne = int(self.x_nb_annee_retraite.name)
            date1 = self.x_date_naissance.strftime("%Y-%m-%d")
            date2 = self.x_date_naissance.year + anne
            self.x_date_retraite = datetime(date2, self.x_date_naissance.month, (self.x_date_naissance.day), 0, 0, 0,
                                            0).date()

    # Rappel sur salaire et indemnités
    date_debut_rappel = fields.Date(string='Date début')
    date_fin_rappel = fields.Date(string='Date fin')
    nombre_jours_total = fields.Integer(string='Nombre de jours')

    mnt_rappel_salaire_net = fields.Float(string='Rappel Sur Salaire net', required=False, default=0)
    salaire_net_coch = fields.Boolean(string='Rappel Sur Salaire net')

    tout_coch = fields.Boolean(string='Tout Cocher')

    mnt_rappel_salaire = fields.Float(string='Salaire de base', required=False)
    sal_coch = fields.Boolean(string='Salaire de base')

    mnt_rappel_resp = fields.Float(string='Indemn.Resp.', required=False)
    resp_coch = fields.Boolean(string='Indemn.Resp.')

    mnt_rappel_astr = fields.Float(string='Indemn.Astreinte', required=False)
    astr_coch = fields.Boolean(string='Indemn.Astreinte')

    mnt_rappel_loge = fields.Float(string='Indemn.Logement', required=False)
    loge_coch = fields.Boolean(string='Indemn.Logement')

    mnt_rappel_techn = fields.Float(string='Indemn.Technicité', required=False)
    techn_coch = fields.Boolean(string='Indemn.Technicité')

    mnt_rappel_spec = fields.Float(string='Indemn.Spécifique GRH', required=False)
    spec_coch = fields.Boolean(string='Indemn.Spécifique GRH')

    mnt_rappel_trans = fields.Float(string='Indemn.Transport', required=False)
    transp_coch = fields.Boolean(string='Indemn.Transport')

    mnt_rappel_inf = fields.Float(string='Indemn.Informatique', required=False)
    resp_inf = fields.Boolean(string='Indemn.Informatique')

    mnt_rappel_explot = fields.Float(string='Indemn.Exploit-Resaeux', required=False)
    reseau_coch = fields.Boolean(string='Indemn.Exploit-Resaeux')

    mnt_rappel_allocation = fields.Float(string='Allocation familiale', required=False)
    alloc_coch = fields.Boolean(string='Allocation familiale')

    mnt_rappel_resp_financ = fields.Float(string='Indemn.Resp.Financière', required=False)
    finac_coch = fields.Boolean(string='Indemn.Resp.Financière')

    mnt_rappel_garde = fields.Float(string='Indemn.Garde', required=False)
    garde_coch = fields.Boolean(string='Indemn.Garde')

    mnt_rappel_risque = fields.Float(string='Indemn.Risque', required=False)
    risq_coch = fields.Boolean(string='Indemn.Risque')

    mnt_rappel_sujetion = fields.Float(string='Indemn.Sujétion', required=False)
    sujetion_coch = fields.Boolean(string='Indemn.Sujétion')

    mnt_rappel_formation = fields.Float(string='Indemn.Formation', required=False)
    formation_coch = fields.Boolean(string='Indemn.Formation')

    mnt_rappel_caisse = fields.Float(string='Indemn.Caisse', required=False)
    caisse_coch = fields.Boolean(string='Indemn.Caisse')

    mnt_rappel_veste = fields.Float(string='Indemn.Veste', required=False)
    veste_coch = fields.Boolean(string='Indemn.Veste')

    mnt_rappel_it = fields.Float(string='Indemn.IT', required=False)
    it_coch = fields.Boolean(string='Indemn.IT')

    mnt_rappel_ifc = fields.Float(string='Indemn.IFC', required=False)
    ifc_coch = fields.Boolean(string='Indemn.IFC')

    mnt_rappel_irp = fields.Float(string='Indemn.IRP', required=False)
    irp_coch = fields.Boolean(string='Indemn.IRP')

    mnt_rappel_ish = fields.Float(string='Indemn.ISH', required=False)
    ish_coch = fields.Boolean(string='Indemn.ISH')

    autres_mnt_rappel = fields.Float(string='Autres', required=False)

    mnt_total_rappel = fields.Float(string='Total Rappel')

    mnt_total_avoir = fields.Float(string='Total avoir', readonly=False, store=True)

    total_prcpt = fields.Float(string='Total precompte', required=False, store=True)

    @api.onchange('salaire_net_coch')
    def coh_sal(self):
        net_coche = self.salaire_net_coch
        for val in self:
            if net_coche == True:
                val.net_coche = True

    @api.onchange('tout_coch')
    def tout_cocher(self):
        tout_coche = self.tout_coch
        for vals in self:
            if tout_coche == True:
                vals.sal_coch = True
                vals.resp_coch = True
                vals.astr_coch = True
                vals.loge_coch = True

                vals.techn_coch = True
                vals.spec_coch = True
                vals.transp_coch = True
                vals.resp_inf = True
                vals.reseau_coch = True
                vals.alloc_coch = True
                vals.finac_coch = True
                vals.garde_coch = True
                vals.risq_coch = True
                vals.sujetion_coch = True
                vals.formation_coch = True
                vals.caisse_coch = True
                vals.veste_coch = True
                vals.it_coch = True
                vals.ifc_coch = True
                vals.irp_coch = True
                vals.ish_coch = True

            else:
                vals.sal_coch = False
                vals.resp_coch = False
                vals.astr_coch = False
                vals.loge_coch = False

                vals.techn_coch = False
                vals.spec_coch = False
                vals.transp_coch = False
                vals.resp_inf = False
                vals.reseau_coch = False
                vals.alloc_coch = False
                vals.finac_coch = False
                vals.garde_coch = False
                vals.risq_coch = False
                vals.sujetion_coch = False
                vals.formation_coch = False
                vals.caisse_coch = False
                vals.veste_coch = False
                vals.it_coch = False
                vals.ifc_coch = False
                vals.irp_coch = False
                vals.ish_coch = False

    # fonction de calcul automatique des rappels de salaire
    def action_ok(self):
        for vals in self:
            if vals.tout_coch == True:
                vals.mnt_rappel_salaire = round((vals.nombre_jours_total * vals.x_solde_indiciaire_ctrct) / 30)
                vals.mnt_rappel_resp = round((vals.nombre_jours_total * vals.x_indem_resp) / 30)
                vals.mnt_rappel_astr = round((vals.nombre_jours_total * vals.x_indem_astr) / 30)
                vals.mnt_rappel_loge = round((vals.nombre_jours_total * vals.x_indem_loge) / 30)

                vals.mnt_rappel_techn = round((vals.nombre_jours_total * vals.x_indem_techn) / 30)
                vals.mnt_rappel_spec = round((vals.nombre_jours_total * vals.x_indem_specif) / 30)
                vals.mnt_rappel_trans = round((vals.nombre_jours_total * vals.x_indem_transp) / 30)
                vals.mnt_rappel_inf = round((vals.nombre_jours_total * vals.x_indem_inform) / 30)
                vals.mnt_rappel_explot = round((vals.nombre_jours_total * vals.x_indem_exploit) / 30)
                vals.mnt_rappel_allocation = round((vals.nombre_jours_total * vals.x_allocation_familial) / 30)
                vals.mnt_rappel_resp_financ = round((vals.nombre_jours_total * vals.x_indem_finance) / 30)
                vals.mnt_rappel_garde = round((vals.nombre_jours_total * vals.x_indem_garde) / 30)
                vals.mnt_rappel_risque = round((vals.nombre_jours_total * vals.x_indem_risque) / 30)
                vals.mnt_rappel_sujetion = round((vals.nombre_jours_total * vals.x_indem_suj) / 30)
                vals.mnt_rappel_formation = round((vals.nombre_jours_total * vals.x_indem_form) / 30)
                vals.mnt_rappel_caisse = round((vals.nombre_jours_total * vals.x_indem_caisse) / 30)
                vals.mnt_rappel_veste = round((vals.nombre_jours_total * vals.x_indem_veste) / 30)
                vals.mnt_rappel_it = round((vals.nombre_jours_total * vals.x_indem_spec_inspect_trav) / 30)
                vals.mnt_rappel_ifc = round((vals.nombre_jours_total * vals.x_indem_spec_inspect_ifc) / 30)
                vals.mnt_rappel_irp = round((vals.nombre_jours_total * vals.x_indem_spec_inspect_irp) / 30)
                vals.mnt_rappel_ish = round((vals.nombre_jours_total * vals.x_indem_spec_inspect_ish) / 30)

            if vals.sal_coch == True:
                vals.mnt_rappel_salaire = round((vals.nombre_jours_total * vals.x_solde_indiciaire_ctrct) / 30)
            if vals.alloc_coch == True:
                vals.mnt_rappel_allocation = round((vals.nombre_jours_total * vals.x_allocation_familial) / 30)
            if vals.resp_coch == True:
                vals.mnt_rappel_resp = round((vals.nombre_jours_total * vals.x_indem_resp) / 30)
            if vals.astr_coch == True:
                vals.mnt_rappel_astr = round((vals.nombre_jours_total * vals.x_indem_astr) / 30)
            if vals.loge_coch == True:
                vals.mnt_rappel_loge = round((vals.nombre_jours_total * vals.x_indem_loge) / 30)
            if vals.techn_coch == True:
                vals.mnt_rappel_techn = round((vals.nombre_jours_total * vals.x_indem_techn) / 30)
            if vals.spec_coch == True:
                vals.mnt_rappel_spec = round((vals.nombre_jours_total * vals.x_indem_specif) / 30)
            if vals.transp_coch == True:
                vals.mnt_rappel_trans = round((vals.nombre_jours_total * vals.x_indem_transp) / 30)
            if vals.resp_inf == True:
                vals.mnt_rappel_inf = round((vals.nombre_jours_total * vals.x_indem_inform) / 30)
            if vals.reseau_coch == True:
                vals.mnt_rappel_explot = round((vals.nombre_jours_total * vals.x_indem_exploit) / 30)
            if vals.finac_coch == True:
                vals.mnt_rappel_resp_financ = round((vals.nombre_jours_total * vals.x_indem_finance) / 30)
            if vals.garde_coch == True:
                vals.mnt_rappel_garde = round((vals.nombre_jours_total * vals.x_indem_garde) / 30)
            if vals.risq_coch == True:
                vals.mnt_rappel_risque = round((vals.nombre_jours_total * vals.x_indem_risque) / 30)
            if vals.sujetion_coch == True:
                vals.mnt_rappel_sujetion = round((vals.nombre_jours_total * vals.x_indem_suj) / 30)
            if vals.formation_coch == True:
                vals.mnt_rappel_formation = round((vals.nombre_jours_total * vals.x_indem_form) / 30)
            if vals.veste_coch == True:
                vals.mnt_rappel_veste = round((vals.nombre_jours_total * vals.x_indem_veste) / 30)
            if vals.caisse_coch == True:
                vals.mnt_rappel_caisse = round((vals.nombre_jours_total * vals.x_indem_caisse) / 30)
            if vals.it_coch == True:
                vals.mnt_rappel_it = round((vals.nombre_jours_total * vals.x_indem_spec_inspect_trav) / 30)
            if vals.ifc_coch == True:
                vals.mnt_rappel_ifc = round((vals.nombre_jours_total * vals.x_indem_spec_inspect_ifc) / 30)
            if vals.irp_coch == True:
                vals.mnt_rappel_irp = round((vals.nombre_jours_total * vals.x_indem_spec_inspect_irp) / 30)
            if vals.irp_coch == True:
                vals.mnt_rappel_ish = round((vals.nombre_jours_total * vals.x_indem_spec_inspect_ish) / 30)

    # fonction qui permet d'avoir le montant Total des avoirs des employés
    @api.onchange('x_type_employe_id', 'x_remuneration_total', 'mnt_total_rappel')
    def total_avoir_field(self):
        for val in self:
            if val.x_remuneration_total or val.mnt_total_rappel:
                val.mnt_total_avoir = round(val.x_remuneration_total + val.mnt_total_rappel)

    # fonction de recuperation du nombre de jours entre deux dates
    @api.onchange('date_debut_rappel', 'date_fin_rappel')
    def _nombre_jours_rappel(self):
        for vals in self:
            if vals.date_debut_rappel and vals.date_fin_rappel:
                vals.nombre_jours_total = (vals.date_fin_rappel - vals.date_debut_rappel).days

    # fonction qui permet d'avoir le montant total des rappels
    @api.onchange('mnt_rappel_salaire', 'mnt_rappel_resp', 'mnt_rappel_astr', 'mnt_rappel_loge', 'mnt_rappel_techn',
                  'mnt_rappel_spec', 'mnt_rappel_it', 'mnt_rappel_ifc', 'mnt_rappel_irp', 'mnt_rappel_trans',
                  'mnt_rappel_inf', 'mnt_rappel_explot', 'mnt_rappel_resp_financ', 'mnt_rappel_allocation',
                  'mnt_rappel_garde', 'mnt_rappel_risque', 'mnt_rappel_sujetion', 'mnt_rappel_formation',
                  'mnt_rappel_caisse', 'mnt_rappel_veste')
    def rappel_net_field(self):
        for val in self:
            val.mnt_total_rappel = round(
                val.mnt_rappel_salaire + val.mnt_rappel_resp + val.mnt_rappel_astr + val.mnt_rappel_loge + val.mnt_rappel_techn + val.mnt_rappel_spec + val.mnt_rappel_trans + val.mnt_rappel_inf + val.mnt_rappel_explot + val.mnt_rappel_resp_financ + val.mnt_rappel_allocation + val.mnt_rappel_garde + val.mnt_rappel_risque + val.mnt_rappel_sujetion + val.mnt_rappel_formation + val.mnt_rappel_caisse + val.mnt_rappel_veste + val.mnt_rappel_it + val.mnt_rappel_ifc + val.mnt_rappel_irp)

    # Rappel sur trop perçu sur salaire et indemnités
    # Cette partie n'es plus utilisée pour le moment car jugé que precompte la remplace

    date_debut_percu = fields.Date(string='Date début')
    date_fin_percu = fields.Date(string='Date fin')
    nombre_jours_total_percu = fields.Integer(string='Nombre de jours')

    mnt_percu_salaire = fields.Float(string='Salaire de base', required=False)

    mnt_avance_salaire = fields.Float(string='Avance/Salaire', required=False)
    mnt_foner = fields.Float(string='Foner', required=False)

    mnt_percu_resp = fields.Float(string='Indemn.Resp.', required=False)
    mnt_percu_astr = fields.Float(string='Indemn.Astreinte', required=False)
    mnt_percu_loge = fields.Float(string='Indemn.Logement', required=False)
    mnt_percu_techn = fields.Float(string='Indemn.Technicité', required=False)
    mnt_percu_spec = fields.Float(string='Indemn.Spécifique', required=False)
    mnt_percu_trans = fields.Float(string='Indemn.Transport', required=False)
    mnt_percu_inf = fields.Float(string='Indemn.Informatique', required=False)
    mnt_percu_explot = fields.Float(string='Indemn.Exploit-Reseaux', required=False)
    mnt_percu_allocation = fields.Float(string='Allocation familiale', required=False)
    mnt_percu_resp_financ = fields.Float(string='Indemn.Resp.Financière', required=False)
    mnt_percu_spec_ifc = fields.Float(string='Indemn.Spec.ICF', required=False)
    mnt_percu_spec_irp = fields.Float(string='Indemn.Spec.IRP', required=False)
    mnt_percu_spec_ish = fields.Float(string='Indemn.Spec.ISH', required=False)
    mnt_percu_spec_grh = fields.Float(string='Indemn.Spec.GRH', required=False)
    autres_mnt_percu = fields.Float(string='Autres', required=False)

    mnt_percu_garde = fields.Float(string='Indemn.Garde', required=False)
    mnt_percu_risque = fields.Float(string='Indemn.Risque', required=False)
    mnt_percu_caisse = fields.Float(string='Indemn.Caisse', required=False)
    mnt_percu_veste = fields.Float(string='Indemn.Vestimentaire', required=False)
    mnt_percu_sujetion = fields.Float(string='Indemn.Sujétion', required=False)
    mnt_percu_formation = fields.Float(string='Indemn.Formation', required=False)

    mnt_total_trop_percu = fields.Float(string='Total Trop Perçu')

    mnt_total_retenues = fields.Float(string='Total retenues')
    mnt_total_retenue = fields.Float(string='Total retenues', store=True, compute='total_retenue_field')

    # fonction qui permet d'avoir le montant Total des retenues des employés
    @api.depends('x_mnt_carfo', 'x_iuts_net', 'x_mnt_cnss')
    def total_retenue_field(self):
        print("totalret")
        for val in self:
            val.mnt_total_retenue = 0
            val.mnt_total_retenue = val.x_mnt_carfo + val.x_iuts_net + val.x_mnt_cnss

    # # fonction qui permet d'avoir le montant Total des retenues des employés
    # @api.onchange('x_type_employe_id', 'x_mnt_carfo', 'x_iuts_net', 'x_mnt_cnss', 'mnt_total_trop_percu',
    #               'x_mnt_taux_retenu_emolmt', 'x_retrait_prcpt_mois')
    # def total_retenue_field(self):
    #     for val in self:
    #         if val.x_type_employe_id.name == 'Fonctionnaire Detaché' or val.x_type_employe_id.name == 'fonctionnaire detaché' or val.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or val.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or val.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION':
    #             if self.x_precompte != 0:
    #                 val.mnt_total_retenues = round(
    #                     val.x_mnt_carfo + val.x_iuts_net + val.mnt_total_trop_percu + val.x_retrait_prcpt_mois)
    #             else:
    #                 val.mnt_total_retenues = round(val.x_mnt_carfo + val.x_iuts_net + val.mnt_total_trop_percu)
    #         elif val.x_type_employe_id.name == 'Contractuel' or val.x_type_employe_id.name == 'CONTRACTUEL' or val.x_type_employe_id.name == 'contractuel':
    #             if self.x_precompte != 0:
    #                 val.mnt_total_retenues = round(
    #                     val.x_mnt_cnss + val.x_iuts_net + val.mnt_total_trop_percu + val.x_retrait_prcpt_mois)
    #             else:
    #                 val.mnt_total_retenues = round(val.x_mnt_cnss + val.x_iuts_net + val.mnt_total_trop_percu)
    #         else:
    #             if self.x_precompte != 0:
    #                 val.mnt_total_retenues = round(
    #                     val.x_mnt_taux_retenu_emolmt + val.mnt_total_trop_percu + val.x_retrait_prcpt_mois + val.x_iuts_net)
    #             else:
    #                 val.mnt_total_retenues = round(
    #                     val.x_mnt_taux_retenu_emolmt + val.mnt_total_trop_percu + val.x_iuts_net)

    # fonction de recuperation du nombre de jours entre deux dates
    @api.onchange('date_debut_percu', 'date_fin_percu')
    def _nombre_jours_trop(self):
        if self.date_debut_percu and self.date_fin_percu:
            for vals in self:
                vals.nombre_jours_total_percu = (vals.date_fin_percu - vals.date_debut_percu).days

    # fonction qui permet d'avoir le montant total des rappels sur trop perçu
    @api.onchange('mnt_percu_salaire', 'mnt_avance_salaire', 'mnt_foner', 'mnt_percu_resp', 'mnt_percu_astr',
                  'mnt_percu_loge', 'mnt_percu_techn', 'mnt_percu_spec', 'mnt_percu_trans', 'mnt_percu_inf',
                  'mnt_percu_explot', 'mnt_percu_resp_financ', 'mnt_percu_allocation', 'mnt_percu_garde',
                  'mnt_percu_risque', 'mnt_percu_sujetion', 'mnt_percu_formation', 'mnt_percu_caisse',
                  'mnt_percu_veste', 'mnt_percu_spec_irp', 'mnt_percu_spec_ifc', 'mnt_percu_spec_ish')
    def trop_percu_net_field(self):
        for val in self:
            val.mnt_total_trop_percu = round(
                val.mnt_foner + val.mnt_percu_salaire + val.mnt_avance_salaire + val.mnt_percu_resp + val.mnt_percu_astr + val.mnt_percu_loge + val.mnt_percu_techn + val.mnt_percu_spec + val.mnt_percu_trans + val.mnt_percu_inf + val.mnt_percu_explot + val.mnt_percu_resp_financ + val.mnt_percu_allocation + val.mnt_percu_garde + val.mnt_percu_risque + val.mnt_percu_sujetion + val.mnt_percu_formation + val.mnt_percu_caisse + val.mnt_percu_veste + val.mnt_percu_spec_irp + val.mnt_percu_spec_ifc + val.mnt_percu_spec_ish
            )

    # Fonction pour faire la sommation du montant recompte par mois
    @api.constrains('company_id')
    def total_prcpt_fields(self):
        for val in self:
            val_id = int(val.id)
            if val.company_id != False:
                val.env.cr.execute(
                    "select sum(p.x_retrait_prcpt_mois) from hr_precompte p, hr_employee h where h.id = p.x_employees_id and p.x_employees_id = %d" % (
                        val_id))
                res = val.env.cr.fetchone()
                val.total_prcpt = res and res[0] or 0
            else:
                val.total_prcpt = 0

    x_mode_paiement = fields.Selection([
        ('billetage', 'Billetage'),
        ('virement', 'Virement'),
    ], string="Mode de Paiement", default='billetage', required=True)

    num_banque = fields.Char('N° compte bancaire', required=True)
    x_banque_id = fields.Many2one('res.bank', 'Banque', required=True)
    # num_banque = fields.Many2one('res.partner.bank', 'N° compte bancaire')
    intitule = fields.Char(string="Intitulé du compte")
    nomprenoms = fields.Char(string="Nom&Prénom(s)")

    # salaire de base des fonctionnaires
    x_solde_indiciaire = fields.Float(string="Solde Indiciaire", readonly=True)

    # salaire de base des fonctionnaires + montant residence
    x_solde_indiciaire_net = fields.Float(string="Salaire de base", readonly=True)

    # salaire de base des contractuels
    x_solde_indiciaire_ctrct = fields.Float(string="Salaire de base", required=True)

    # cALCUL DE L'EMOLUMENT
    x_emolument_ctrct = fields.Float(string="Emolument Brut")
    x_taux_retenu_emolmt = fields.Float(string="Taux retenue (%)")
    x_mnt_taux_retenu_emolmt = fields.Float(string="Montant Taux")
    x_emolument_ctrct_net = fields.Float(string="Emolument Net", readonly=True)

    # classificvation fonctionnaire
    x_classification = fields.Char(store=True, string="Classification")

    # classificvation contractuel
    x_classification_ctrct = fields.Char(store=True, string="Classification")

    # Declaration variables Indemnités
    x_indem_resp = fields.Float(store=True, string="Indemn.Resp", readonly=False)
    x_indem_astr = fields.Float(store=True, string="Indemn.Astreinte", readonly=False)
    x_indem_techn = fields.Float(store=True, string="Indemn.Technicité", readonly=False)
    x_indem_specif = fields.Float(store=True, string="Indemn.Spécifique GRH", readonly=False)
    x_indem_loge = fields.Float(store=True, string="Indemn.Logement", readonly=False)
    x_indem_transp = fields.Float(store=True, string="Indemn.Transport", readonly=False)
    x_indem_inform = fields.Float(store=True, string="Indemn.Informatique", readonly=False)
    x_indem_exploit = fields.Float(store=True, string="Indemn.Exploitation-Réseau", readonly=False)
    x_indem_finance = fields.Float(store=True, string="Indemn.Resp.Financière", readonly=False)
    x_indem_garde = fields.Float(store=True, string="Indemn.Garde", readonly=False)
    x_indem_risque = fields.Float(store=True, string="Indemn.Risque.Contagion", readonly=False)
    x_indem_suj = fields.Float(store=True, string="Indemn.Sujétion Géographique", readonly=False)
    x_indem_form = fields.Float(store=True, string="Indemn.Formation", readonly=False)
    x_indem_caisse = fields.Float(store=True, string="Indemn.Caisse", readonly=True)
    x_indem_veste = fields.Float(store=True, string="Indemn.Vestimentaire", readonly=True)
    x_indem_spec_inspect_trav = fields.Float(store=True, string="Indemn.Spécifique Inspecteur de Travail",
                                             readonly=True)
    x_indem_spec_inspect_ifc = fields.Float(store=True, string="Indemn.Spécifique Forfaitaire Compensatrice",
                                            readonly=True)
    x_indem_spec_inspect_irp = fields.Float(store=True, string="Indemn.Spécifique de Responsabilité Pécunière",
                                            readonly=True)
    x_indem_spec_inspect_ish = fields.Float(store=True, string="Indemn.Spécifique Harmonisée Personnel MENA et MESRSI",
                                            readonly=True)

    x_indem_prime_rendement = fields.Float(store=True, string="Prime rendement", readonly=True)

    # Calcul UITS


    # x_total_indemnites_prorata = fields.Float(string="Total Indemn", readonly=True, compute='depend_field_prorata', store=True)
    x = fields.Float(compute='', string="Total Indemnité", readonly=True, store=True)

    # Remuneration total = Salaire de base + Total indemnités
    # x_remuneration_total = fields.Float(string="Rémuneration totale", readonly=True, store=True)
    # x_remuneration_total_prorata = fields.Float(string="Rémuneration totale", readonly=True, store=True)
    # Montant CNSS = 5.5% de la remuneration total
    x_mnt_cnss = fields.Float(string="Montant CNSS", readonly=False, store=True, compute='mnt_cnss_field')

    # Montant CNSS Patronal = 16% de la remuneration total
    x_mnt_patronal_cnss = fields.Float(string="Part Patronale CNSS", readonly=False, store=True)

    # Montant CARFO = 8% du salaire de base
    x_mnt_carfo = fields.Float(string="Montant CARFO", readonly=False)

    # Montant CARFO Patronal = 15.5% du salaire de base
    x_mnt_patronal_carfo = fields.Float(string="Part Patronale CARFO", readonly=False)

    # Rappel total = somm rappel(indemnitéss et salaire)
    mnt_total_rappel = fields.Float(string="Montant total Rappel", readonly=False, store=True)
    date_jour = fields.Date(string='Date du jour', default= date.today())
    date_jours = fields.Date(string='Date du jour', default=date.today())

    # Rappel total = somm rappel(indemnitéss et salaire)
    mnt_total_trop_percu = fields.Float(string="Montant total trop perçu", readonly=False, store=True)

    # Base imposable des contractuels = remun à imposer - cnss deductible- indemn deductible total - abattement forfetaire
    x_base_imposable_ctrct = fields.Float(string="Base imposable", readonly=False)

    # Retenue IUTS
    x_retenue_iuts = fields.Float(store=True, string="Retenue IUTS", readonly=False, compute='retenue_iuts_field')

    # Montant charge
    x_montant_charge = fields.Float(store=True, string="Montant charge", readonly=True, compute='mnt_charge_field')

    # IUTS Net
    x_iuts_net = fields.Float(store=True, string="IUTS Net", readonly=True, compute='net_iuts_fields')

    # Net à payer fonctionnaire
    x_net_payer = fields.Float(string="Net à payer", readonly=False, store=True, compute='net_payer_field')

    # Net à payer contractuel
    x_net_payer_ctrct = fields.Float(store=True, string="Net à payer", readonly=True, compute='net_payer_ctrct_field')

    x_salaire_net = fields.Float(string="Net à payer", readonly=True)
    x_salaire_net_ctrct = fields.Float(string="Net à payer Contractuel", readonly=True)

    # total retenues cnss
    x_total_retenue_cnss = fields.Float(string="Total retenues CNSS", readonly=False)

    # total retenues carfo
    x_total_retenue_carfo = fields.Float(string="Total retenues CARFO", readonly=False)

    # Nouvelle manière de calculer le salaire et l'iuts pour les fonctionnaires

    x_indem_resp_exo = fields.Float(store=True, string="Exo.Resp", readonly=True,
                                    compute='calcul_exoneration_responsabilite')
    x_indem_astr_exo = fields.Float(store=True, string="Exo.Astreinte", readonly=True,
                                    compute='calcul_exoneration_astreintes')
    x_indem_techn_exo = fields.Float(store=True, string="Exo.Technicité", readonly=True,
                                     compute='calcul_exoneration_technicites')
    x_indem_specif_exo = fields.Float(store=True, string="Exo.Spécifique GRH", readonly=True,
                                      compute='calcul_exoneration_specifiques')
    x_indem_specif_it_exo = fields.Float(store=True, string="Exo.Spécifique IT", readonly=True,
                                         compute='calcul_exoneration_specifiques_it')
    x_indem_specif_irp_exo = fields.Float(store=True, string="Exo.Spécifique IRP", readonly=True,
                                          compute='calcul_exoneration_specifiques_irp')
    x_indem_specif_ifc_exo = fields.Float(store=True, string="Exo.Spécifique IFC", readonly=True,
                                          compute='calcul_exoneration_specifiques_ifc')
    x_indem_specif_ish_exo = fields.Float(store=True, string="Exo.Spécifique ISH", readonly=True,
                                          compute='calcul_exoneration_specifiques_ish')

    x_indem_loge_exo = fields.Float(store=True, string="Exo.Logement", readonly=True,
                                    compute='calcul_exoneration_logement')
    x_indem_transp_exo = fields.Float(store=True, string="Exo.Transport", readonly=True,
                                      compute='calcul_exoneration_transport')
    x_indem_inform_exo = fields.Float(store=True, string="Exo.Informatique", readonly=True,
                                      compute='calcul_exoneration_informatique')
    x_indem_exploit_exo = fields.Float(store=True, string="Exo.Exploitation-Réseau", readonly=True,
                                       compute='calcul_exoneration_exploitation')
    x_indem_finance_exo = fields.Float(store=True, string="Exo.Resp.Financière", readonly=True,
                                       compute='calcul_exoneration_resp_finance')
    x_indem_garde_exo = fields.Float(store=True, string="Exo.Garde", readonly=True, compute='calcul_exoneration_garde')
    x_indem_risque_exo = fields.Float(store=True, string="Exo.Risque.Contagion", readonly=True,
                                      compute='calcul_exoneration_risque')
    x_indem_suj_exo = fields.Float(store=True, string="Exo.Sujétion Géographique", readonly=True,
                                   compute='calcul_exoneration_sujetion')
    x_indem_form_exo = fields.Float(store=True, string="Exo.Formation", readonly=True,
                                    compute='calcul_exoneration_formation')
    x_indem_caisse_exo = fields.Float(store=True, string="Exo.Caisse", readonly=True,
                                      compute='calcul_exoneration_caisse')
    x_indem_veste_exo = fields.Float(store=True, string="Exo.Vestimentaire", readonly=True,
                                     compute='calcul_exoneration_veste')
    x_indem_residence_exo = fields.Float(store=True, string="Exo.Résidence", readonly=True,
                                         compute='calcul_exoneration_residence')
    x_prime_exo = fields.Float(store=True, string="Exo.Prime Rendement", readonly=True,
                               compute='calcul_exoneration_prime')

    x_renum_total_exo = fields.Float(store=True, string="Rénum.Total", readonly=True)


    # fonction de recherche permettant de retourner le salaire de base dans la grille des contractuels en fonction des paramètres
    @api.onchange('x_echellon_c_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def sal_basec(self):
        val_echel_c = int(self.x_echelle_c_id)
        print('val_echel_c', val_echel_c)
        val_echellon_c = int(self.x_echellon_c_id)
        print('val_echellon_c', val_echellon_c)
        val_struct = int(self.company_id.id)
        print('val_struct', val_struct)
        val_cat_c = int(self.x_categorie_c_id)
        print('val_cat_c', val_cat_c)
        if val_echel_c != False and val_echellon_c != False and val_cat_c != False and val_struct != False:
            res = self.env['hr_grillesalariale_contractuel'].search(
                [('x_echellon_c_id', '=', val_echellon_c), ('x_categorie_c_id', '=', val_cat_c),
                 ('x_echelle_c_id', '=', val_echel_c), ('company_id', '=', val_struct)])
            self.x_solde_indiciaire_ctrct = round(res.x_salbase_ctrt)

            print('x_solde_indiciaire_ctrct', self.x_solde_indiciaire_ctrct)

    # calcul abattement forfaitaire
    @api.depends('x_salaire_base', 'mnt_rappel_salaire')
    def calcul_abattement(self):
        for vals in self:
            type_emp = vals.x_lib_type_emp
            x_cat = vals.x_categorie_c_id.name
            x_cat_f = vals.x_categorie_id.name
            #salaire_base = vals.x_salaire_base + vals.mnt_rappel_salaire - vals.mnt_percu_salaire
            salaire_base = vals.x_salaire_base
            print("Meda")
            print(salaire_base)
            if vals.x_type_employe_id.code == 'CTRCT':
                if x_cat == '1' or x_cat == '2' or x_cat == '6':
                    vals.x_abattement_forfaitaire = round((salaire_base * 20) / 100)
                else:
                    vals.x_abattement_forfaitaire = round((salaire_base * 25) / 100)
            else:
                if x_cat_f == 'A' or x_cat_f == 'B' or x_cat_f == 'P':
                    vals.x_abattement_forfaitaire = round((salaire_base * 20) / 100)
                else:
                    vals.x_abattement_forfaitaire = round((salaire_base * 25) / 100)

    # calcul du salaire brut pour le fonctionnaire puisque Rénumeration Totale déjà connue
    @api.depends('x_remuneration_total', 'x_mnt_carfo', 'x_mnt_cnss', 'x_allocation_familial')
    def calcul_salaire_brut(self):
        for vals in self:
            vals.x_salaire_brut = vals.x_remuneration_total - vals.x_mnt_cnss - vals.x_mnt_carfo - vals.x_allocation_familial

    # fonctions de calcul des exonérations selon le type d'indemnités

    """Indemnités de logement"""
    @api.depends('x_indem_loge', 'x_salaire_brut')
    def calcul_exoneration_logement(self):
        premiere_limite = 0
        for vals in self:
            premiere_limite_log = round((vals.x_salaire_brut * 20) / 100)
            vals.x_indem_loge_exo = min([premiere_limite_log, vals.x_indem_loge, 75000])
            print("Exo.logement", vals.x_indem_loge_exo)

    """Indemnités de transport"""

    @api.depends('x_indem_transp', 'x_salaire_brut')
    def calcul_exoneration_transport(self):
        for vals in self:
            premiere_limite_trans = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_transp_exo = min([premiere_limite_trans, vals.x_indem_transp, 30000])

    """Calcul sur les Autres indemnités"""

    # indemnités de responsabilité
    @api.depends('x_indem_resp', 'x_salaire_brut', 'mnt_rappel_resp', 'mnt_percu_resp')
    def calcul_exoneration_responsabilite(self):
        for vals in self:
            premiere_limite_res = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_resp_exo = min([premiere_limite_res,
                                         vals.x_indem_resp + vals.mnt_rappel_resp - vals.mnt_percu_resp,
                                         50000])

    # indemnités de astreintes
    @api.depends('x_indem_astr', 'x_salaire_brut')
    def calcul_exoneration_astreintes(self):
        for vals in self:
            premiere_limite_astr = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_astr_exo = min([premiere_limite_astr, vals.x_indem_astr, 50000])
            print("EXO astr", vals.x_indem_astr_exo)

    # indemnités de technicités
    @api.depends('x_indem_techn', 'x_salaire_brut')
    def calcul_exoneration_technicites(self):
        for vals in self:
            premiere_limite_tech = round((vals.x_salaire_brut * 5) / 100)
            x_indem_techn = round(vals.x_indem_techn)
            vals.x_indem_techn_exo = min([premiere_limite_tech, x_indem_techn, 50000])

    # indemnités de spécifiques GRH
    @api.depends('x_indem_specif', 'x_salaire_brut')
    def calcul_exoneration_specifiques(self):
        premiere_limite_spec = 0
        for vals in self:
            vals.x_indem_specif_exo = 0
            premiere_limite_spec = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_specif_exo = min([premiere_limite_spec, vals.x_indem_specif, 50000])

    # indemnités de spécifiques IT
    @api.depends('x_indem_spec_inspect_trav', 'x_salaire_brut')
    def calcul_exoneration_specifiques_it(self):
        for vals in self:
            premiere_limite_spec_it = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_specif_it_exo = min([premiere_limite_spec_it, vals.x_indem_spec_inspect_trav, 50000])

    # indemnités de spécifiques IRP
    @api.depends('x_indem_spec_inspect_irp', 'x_salaire_brut')
    def calcul_exoneration_specifiques_irp(self):
        for vals in self:
            premiere_limite_spec_irp = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_specif_irp_exo = min([premiere_limite_spec_irp, vals.x_indem_spec_inspect_irp, 50000])

    # indemnités de spécifiques ISH
    @api.depends('x_indem_spec_inspect_ish', 'x_salaire_brut')
    def calcul_exoneration_specifiques_ish(self):
        for vals in self:
            premiere_limite_spec_ish = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_specif_ish_exo = min([premiere_limite_spec_ish, vals.x_indem_spec_inspect_ish, 15000])

    # indemnités de spécifiques IFC
    @api.depends('x_indem_spec_inspect_ifc', 'x_salaire_brut')
    def calcul_exoneration_specifiques_ifc(self):
        for vals in self:
            premiere_limite_ifc = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_specif_ifc_exo = min([premiere_limite_ifc, vals.x_indem_spec_inspect_ifc, 50000])

    # indemnités d'informatiques
    @api.depends('x_indem_inform', 'x_salaire_brut')
    def calcul_exoneration_informatique(self):
        for vals in self:
            premiere_limite_info = round(vals.x_salaire_brut * 0.05)
            vals.x_indem_inform_exo = min([premiere_limite_info, vals.x_indem_inform, 50000])

    # indemnités de exploitations reseaux
    @api.depends('x_indem_exploit', 'x_salaire_brut')
    def calcul_exoneration_exploitation(self):
        for vals in self:
            premiere_limite_exploi = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_exploit_exo = min([premiere_limite_exploi, vals.x_indem_exploit, 50000])

    # indemnités de responsabilités financières
    @api.depends('x_indem_finance', 'x_salaire_brut')
    def calcul_exoneration_resp_finance(self):
        for vals in self:
            premiere_limite_finance = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_finance_exo = min([premiere_limite_finance, vals.x_indem_finance, 50000])

    # indemnités de garde
    @api.depends('x_indem_garde', 'x_salaire_brut')
    def calcul_exoneration_garde(self):
        for vals in self:
            premiere_limite_garde = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_garde_exo = min([premiere_limite_garde, vals.x_indem_garde, 50000])

    # indemnités de risque
    @api.depends('x_indem_risque', 'x_salaire_brut')
    def calcul_exoneration_risque(self):
        for vals in self:
            premiere_limite_risque = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_risque_exo = min([premiere_limite_risque, vals.x_indem_risque, 50000])

    # indemnités de sujetion
    @api.depends('x_indem_suj', 'x_salaire_brut')
    def calcul_exoneration_sujetion(self):
        for vals in self:
            premiere_limite_suj = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_suj_exo = min([premiere_limite_suj, vals.x_indem_suj, 50000])

    # indemnités de formation
    @api.depends('x_indem_form', 'x_salaire_brut')
    def calcul_exoneration_formation(self):
        for vals in self:
            premiere_limite_form = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_form_exo = min([premiere_limite_form, vals.x_indem_form, 50000])

    # indemnités de caisse
    @api.depends('x_indem_caisse', 'x_salaire_brut')
    def calcul_exoneration_caisse(self):
        for vals in self:
            premiere_limite_caisse = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_caisse_exo = min([premiere_limite_caisse, vals.x_indem_caisse, 50000])

    # indemnités de veste
    @api.depends('x_indem_veste', 'x_salaire_brut')
    def calcul_exoneration_veste(self):
        for vals in self:
            premiere_limite_veste = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_veste_exo = min([premiere_limite_veste, vals.x_indem_veste, 50000])

    # indemnités de residence
    @api.depends('x_solde_indiciaire', 'x_salaire_brut')
    def calcul_exoneration_residence(self):
        for vals in self:
            premiere_limite = round((vals.x_salaire_brut * 5) / 100)
            vals.x_indem_residence_exo = min([premiere_limite, vals.x_solde_indiciaire, 50000])

    # exoneration prime de rendement
    @api.depends('x_indem_prime_rendement', 'x_salaire_brut')
    def calcul_exoneration_prime(self):
        for vals in self:
            premiere_limite = round((vals.x_salaire_brut * 5) / 100)
            vals.x_prime_exo = min([premiere_limite, vals.x_indem_prime_rendement, 50000])

    # Calcul total exonérations
    @api.depends('x_indem_resp_exo', 'x_indem_astr_exo', 'x_indem_techn_exo', 'x_indem_specif_exo',
                 'x_indem_specif_it_exo', 'x_indem_specif_ifc_exo', 'x_indem_specif_irp_exo',
                 'x_indem_specif_ish_exo', 'x_indem_loge_exo', 'x_indem_transp_exo', 'x_indem_inform_exo',
                 'x_indem_exploit_exo', 'x_indem_finance_exo', 'x_indem_garde_exo', 'x_indem_risque_exo',
                 'x_indem_suj_exo', 'x_indem_form_exo', 'x_indem_caisse_exo', 'x_indem_veste_exo', 'x_prime_exo')
    def calcul_exoneration_total(self):
        for vals in self:
            vals.x_total_exo = vals.x_indem_resp_exo + vals.x_indem_astr_exo + vals.x_indem_techn_exo + vals.x_indem_specif_exo + vals.x_indem_loge_exo + vals.x_indem_transp_exo + vals.x_indem_inform_exo + vals.x_indem_exploit_exo + vals.x_indem_finance_exo + vals.x_indem_garde_exo + vals.x_indem_risque_exo + vals.x_indem_suj_exo + vals.x_indem_form_exo + vals.x_indem_caisse_exo + vals.x_indem_veste_exo + vals.x_indem_specif_it_exo + vals.x_indem_specif_ifc_exo + vals.x_indem_specif_irp_exo + vals.x_indem_specif_ish_exo + vals.x_prime_exo

    # calcul DU SALAIRE NET IMPOSABLE (SNI)
    @api.depends('x_salaire_brut', 'x_total_exo', 'x_abattement_forfaitaire')
    def calcul_sni(self):
        for vals in self:
            val1 = vals.x_salaire_brut - vals.x_total_exo - vals.x_abattement_forfaitaire
            val2 = val1 - (val1 % 100)
            vals.x_salaire_net_imposable = val2

    # calcul de la rénumeration totale x_renum_total_exo
    @api.onchange('x_type_employe_id', 'x_solde_indiciaire', 'x_total_indemnites', 'x_solde_indiciaire_ctrct')
    def calcul_renum_total_exo(self):
        for vals in self:
            type_emp = vals.x_lib_type_emp
            if type_emp == "Contractuel" or type_emp == "CONTRACTUEL":
                vals.x_renum_total_exo = vals.x_solde_indiciaire_ctrct + vals.x_total_indemnites
            else:
                vals.x_renum_total_exo = vals.x_solde_indiciaire + vals.x_total_indemnites

    # fonction qui permet d'avoir le montant Total des retenues des declarations a la CARFO et CNSS à partir du montant carfo, iuts net
    @api.onchange('x_mnt_carfo', 'x_iuts_net', 'x_mnt_cnss', 'x_retrait_prcpt_mois')
    def total_retenue_carfo_cnss_field(self):
        for val in self:
            if val.x_type_employe_id.name == 'Fonctionnaire Detaché' or val.x_type_employe_id.name == 'fonctionnaire detaché' or val.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or val.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or val.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION':
                if self.x_precompte != 0:
                    val.x_total_retenue_carfo = round(val.x_mnt_carfo + val.x_iuts_net + val.x_retrait_prcpt_mois)
                    val.x_total_retenue_cnss = 0.0
                else:
                    val.x_total_retenue_carfo = round(val.x_mnt_carfo + val.x_iuts_net)
                    val.x_total_retenue_cnss = 0.0
            else:
                if self.x_precompte != 0:
                    val.x_total_retenue_cnss = round(val.x_mnt_cnss + val.x_iuts_net + val.x_retrait_prcpt_mois)
                    val.x_total_retenue_carfo = 0.0
                else:
                    val.x_total_retenue_cnss = round(val.x_mnt_cnss + val.x_iuts_net)
                    val.x_total_retenue_carfo = 0.0

    # fonction qui permet d'avoir l'emolument net
    @api.onchange('x_emolument_ctrct', 'x_taux_retenu_emolmt', 'x_mnt_taux_retenu_emolmt')
    def emolument_net_field(self):
        for val in self:
            val.x_mnt_taux_retenu_emolmt = round((val.x_emolument_ctrct * val.x_taux_retenu_emolmt) / 100)
            val.x_emolument_ctrct_net = val.x_emolument_ctrct - val.x_mnt_taux_retenu_emolmt

    # fonction qui permet d'additionner les indemnités
    @api.depends('x_indem_resp', 'x_indem_astr', 'x_indem_techn', 'x_indem_specif', 'x_indem_spec_inspect_trav',
                 'x_indem_spec_inspect_irp', 'x_indem_spec_inspect_ish', 'x_indem_spec_inspect_ifc', 'x_indem_loge',
                 'x_indem_transp', 'x_indem_inform', 'x_indem_exploit', 'x_indem_finance', 'x_indem_garde',
                 'x_indem_risque', 'x_indem_suj', 'x_indem_form', 'x_indem_caisse', 'x_solde_indiciaire',
                 'x_indem_prime_rendement')
    def depend_field(self):
        for val in self:
            val.x_total_indemnites = round(
                val.x_indem_resp + val.x_indem_astr + val.x_indem_techn + val.x_indem_specif +
                val.x_indem_spec_inspect_trav + val.x_indem_spec_inspect_irp + val.x_indem_spec_inspect_ish +
                val.x_indem_spec_inspect_ifc + val.x_indem_loge + val.x_indem_transp + val.x_indem_inform +
                val.x_indem_exploit + val.x_indem_finance + val.x_indem_garde + val.x_indem_risque +
                val.x_indem_suj + val.x_indem_form + val.x_indem_caisse + val.x_indem_prime_rendement)
            # val.total_indemnites = val.x_total_indemnites
            # print("total  des indemnite", val.x_total_indemnites)

    @api.depends('x_salaire_base', 'x_total_indemnites', 'x_emolument_ctrct_net',
                  'x_allocation_familial', 'mnt_total_rappel', 'mnt_total_trop_percu')
    def renum_total_field(self):
        for val in self:
            val.x_remuneration_total = round(
                val.x_salaire_base + val.x_total_indemnites + val.x_allocation_familial)

    # fonction qui permet d'avoir le montant carfo à partir du salaire de base
    @api.onchange('x_type_employe_id', 'x_solde_indiciaire')
    def mnt_carfo_fields(self):
        for val in self:
            if val.x_type_employe_id.code in ('FCT_DETACH', 'FCT_MD'):
                val.x_mnt_carfo = round((val.x_solde_indiciaire * 8) / 100)
                val.x_mnt_patronal_carfo = round((val.x_solde_indiciaire * 15.5) / 100)
                print(val.x_mnt_carfo)
                val.x_mnt_cnss = 0.0
                val.x_mnt_patronal_cnss = 0.0

    # fonction qui permet d'avoir le montant cnss à partir du salaire de base
    @api.depends('x_type_employe_id', 'x_remuneration_total')
    def mnt_cnss_field(self):
        for val in self:
            if val.x_type_employe_id.code == 'CTRCT':
                resul = round((val.x_remuneration_total * 5.5) / 100)
                if resul > 33000:
                    val.x_mnt_cnss = 33000
                    val.x_mnt_patronal_cnss = 96000
                else:
                    val.x_mnt_cnss = round((val.x_remuneration_total * 5.5) / 100)
                    val.x_mnt_patronal_cnss = round((val.x_remuneration_total * 16) / 100)

                val.x_mnt_carfo = 0.0
                val.x_mnt_patronal_carfo = 0.0

    # fonction qui permet d'avoir la base imposable pour les contractuels en fonction de la categorisation
    # @api.depends('x_solde_indiciaire_ctrct','x_mnt_cnss','x_mnt_carfo','x_solde_indiciaire')
    @api.onchange('x_salaire_net_imposable')
    def base_imposable_ctcrt_field(self):
        for val in self:
            val.x_base_imposable_ctrct = val.x_salaire_net_imposable
            if val.x_type_employe_id.name == 'Contractuel' or val.x_type_employe_id.name == 'contractuel' or val.x_type_employe_id.name == 'CONTRACTUEL':
                if val.x_categorie_c_id.name == '1' or val.x_categorie_c_id.name == '2' or val.x_categorie_c_id.name == '6':
                    vals = round(((val.x_solde_indiciaire_ctrct * 80) / 100 - val.x_mnt_cnss) / 100)
                    val.x_base_imposable_ctrct = val.x_salaire_net_imposable
                    # val.x_base_imposable = 0.0
                else:
                    vals1 = round(((val.x_solde_indiciaire_ctrct * 75) / 100 - val.x_mnt_cnss) / 100)
                    val.x_base_imposable_ctrct = val.x_salaire_net_imposable
                    # val.x_base_imposable = 0.0
            else:
                if val.x_type_employe_id.name == 'Fonctionnaire Detaché' or val.x_type_employe_id.name == 'fonctionnaire detaché' or val.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or val.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or val.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION':
                    if val.x_categorie_id.name == 'A' or val.x_categorie_id.name == 'B' or val.x_categorie_id.name == 'P':
                        vals = round(
                            ((val.x_solde_indiciaire * 80) / 100 + val.x_indemnite_residence - val.x_mnt_carfo) / 100)
                        val.x_base_imposable_ctrct = val.x_salaire_net_imposable
                        # val.x_base_imposable_ctrct = 0.0
                    else:
                        vals1 = round(((val.x_solde_indiciaire * 75) / 100 - val.x_mnt_carfo) / 100)
                        val.x_base_imposable_ctrct = val.x_salaire_net_imposable
                        # val.x_base_imposable_ctrct = 0.0

    # fonction qui permet d'avoir la de l'iuts pour les deux
    @api.depends('x_salaire_net_imposable')
    def retenue_iuts_field(self):
        for val in self:
            if 0 <= val.x_salaire_net_imposable <= 30000.0:
                val.x_retenue_iuts = round(val.x_salaire_net_imposable * 0)
            elif 30001.0 <= val.x_salaire_net_imposable <= 50000.0:
                val.x_retenue_iuts = round((val.x_salaire_net_imposable - 30001.0) * 12.1 / 100)
            elif 50001.0 <= val.x_salaire_net_imposable <= 80000.0:
                val.x_retenue_iuts = round(((val.x_salaire_net_imposable - 50001.0) * 13.9 / 100) + 2420)
            elif 80001.0 <= val.x_salaire_net_imposable <= 120000.0:
                val.x_retenue_iuts = round(((val.x_salaire_net_imposable - 80001.0) * 15.7 / 100) + 6590)
            elif 120001.0 <= val.x_salaire_net_imposable <= 170000.0:
                val.x_retenue_iuts = round(((val.x_salaire_net_imposable - 120001.0) * 18.4 / 100) + 12870)
            elif 170001.0 <= val.x_salaire_net_imposable <= 250000.0:
                val.x_retenue_iuts = round(((val.x_salaire_net_imposable - 170001.0) * 21.7 / 100) + 22070)
            else:
                val.x_retenue_iuts = round(((val.x_salaire_net_imposable - 250001.0) * 25 / 100) + 39430)

    # fonction qui permet d'avoir le montant en fonction du nombre de charge pour les deux
    @api.depends('charge', 'x_retenue_iuts')
    def mnt_charge_field(self):
        for val in self:
            if val.charge == 0:
                val.x_montant_charge = round(val.x_retenue_iuts * 0)
            elif val.charge == 1:
                val.x_montant_charge = round((val.x_retenue_iuts * 8) / 100)
            elif val.charge == 2:
                val.x_montant_charge = round((val.x_retenue_iuts * 10) / 100)
            elif val.charge == 3:
                val.x_montant_charge = round((val.x_retenue_iuts * 12) / 100)
            elif val.charge == 4:
                val.x_montant_charge = round((val.x_retenue_iuts * 14) / 100)
            else:
                print("Nombre d'enfant maximum pris en charge atteint donc du coup on prend pour les 4 enfants")
                val.x_montant_charge = round((val.x_retenue_iuts * 14) / 100)

    # fonction qui permet d'avoir le montant net de l'iuts pour le contractuel
    @api.depends('x_retenue_iuts', 'x_montant_charge')
    def net_iuts_fields(self):
        for val in self:
            val.x_iuts_net = round(val.x_retenue_iuts - val.x_montant_charge)

    # fonction qui permet d'avoir le montant net à payer pour le fonctionnaires
    @api.depends('x_remuneration_total', 'mnt_total_retenue')
    def net_payer_field(self):
        for val in self:
            val.x_net_payer = round(
                val.x_remuneration_total - val.mnt_total_retenue)

    # fonction qui permet d'avoir le montant net à payer pour les contractuels 2
    @api.depends('x_type_employe_id', 'x_remuneration_total', 'x_mnt_cnss', 'x_mnt_carfo', 'x_iuts_net',
                 'mnt_total_rappel', 'mnt_total_trop_percu', 'x_retrait_prcpt_mois', 'mnt_rappel_salaire_net')
    def net_payer_ctrct_field(self):
        for val in self:
            if val.x_remuneration_total:
                if val.x_type_employe_id.name == 'Fonctionnaire Detaché' or val.x_type_employe_id.name == 'fonctionnaire detaché' or val.x_type_employe_id.name == 'FONCTIONNAIRE DETACHE' or val.x_type_employe_id.name == 'Fonctionnaire Mis à Disposition' or val.x_type_employe_id.name == 'FONCTIONNAIRE MIS A DISPOSITION':
                    if self.x_precompte != 0:
                        val.x_net_payer_ctrct = round(
                            val.x_remuneration_total - val.x_iuts_net - val.x_mnt_carfo - val.mnt_total_trop_percu - val.x_retrait_prcpt_mois + val.mnt_rappel_salaire_net)
                    else:
                        val.x_net_payer_ctrct = round(
                            val.x_remuneration_total - val.x_iuts_net - val.x_mnt_carfo - val.mnt_total_trop_percu + val.mnt_rappel_salaire_net)
                elif val.x_type_employe_id.name == 'Contractuel' or val.x_type_employe_id.name == 'CONTRACTUEL' or val.x_type_employe_id.name == 'contractuel':
                    if self.x_precompte != 0:
                        val.x_net_payer_ctrct = round(
                            val.x_remuneration_total - val.x_iuts_net - val.x_mnt_cnss - val.mnt_total_trop_percu - val.x_retrait_prcpt_mois + val.mnt_rappel_salaire_net)
                    else:
                        val.x_net_payer_ctrct = round(
                            val.x_remuneration_total - val.x_iuts_net - val.x_mnt_cnss - val.mnt_total_trop_percu + val.mnt_rappel_salaire_net)
                else:
                    if self.x_precompte != 0:
                        val.x_net_payer_ctrct = round(
                            val.x_remuneration_total - val.x_iuts_net - val.mnt_total_trop_percu - val.x_retrait_prcpt_mois + val.mnt_rappel_salaire_net)
                    else:
                        val.x_net_payer_ctrct = round(
                            val.x_remuneration_total - val.x_iuts_net - val.mnt_total_trop_percu + val.mnt_rappel_salaire_net)

    date_debut_pos = fields.Date(string="Pour compter du")
    date_fin_pos = fields.Date(string="AU")

    date_debut_affect = fields.Date(string="Date effet")
    date_fin_affect = fields.Date(string="Date fin")

    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_classees_id = fields.Many2one('hr_classe', string='Classe')
    x_categorie_id = fields.Many2one('hr_categorie', string='Catégorie')
    x_echelle_id = fields.Many2one('hr_echelle', string='Echelle')
    x_echellon_id = fields.Many2one('hr_echellon', string='Echelon')

    x_categorie_c_id = fields.Many2one('hr_categorie', string='Catégorie', required=False)
    x_echelle_c_id = fields.Many2one('hr_echelle', string='Echelle', required=False)
    x_echellon_c_id = fields.Many2one('hr_echellon', required=False, string='Echelon')

    date_debut = fields.Date(string="Date d'engagement", default=date.today())
    date_fin = fields.Date(string="Date fin")
    date_embauche = fields.Date(string="Date d'embauche", default=date.today())
    date_fin_embauche = fields.Date(string="Date fin")

    date_modiff = fields.Date(string='Date effet', default=date.today())
    date_operation = fields.Date(string="Date Opération", default=date.today(), readonly=False)

    # fonction permettant d'enregistrer dans la table historique de l'employé
    @api.multi
    def enregistrer_historique(self):
        val_echelon = int(self.x_echellon_c_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        recup = str(self.date_modiff.strftime("%Y-%m-%d"))
        print('date recupérée', recup)
        date_op = str(self.date_operation.strftime("%Y-%m-%d"))
        print('date opération', date_op)
        val_struct = int(self.company_id)
        val_exo = int(self.x_exercice_id)

        self.env.cr.execute(
            """INSERT INTO hr_employee_historique(employee_id,x_categorie_c_id,x_echelle_c_id,x_echellon_c_id,date_modif,date_op,company_id,x_exercice_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
            (self.id, val_cat, val_echel, val_echelon, recup, date_op, val_struct, val_exo))

        self.env.cr.execute(
            "select no_code from hr_cmpteur_avancer where id_user = %d and company_id = %d" % (self.id, val_struct))
        lo = self.env.cr.fetchone()
        no_lo = lo and lo[0] or 0
        c1 = int(no_lo) + 1
        c = str(no_lo)
        if c == "0":
            ok = str(c1).zfill(6)
            vals = c1
            self.env.cr.execute(
                """INSERT INTO hr_cmpteur_avancer(id_user,company_id,no_code,date_dernier_avancement)  VALUES(%s,%s,%s,'%s')""" % (
                    self.id, val_struct, vals, self.date_modiff))
        else:
            c1 = int(no_lo) + 1
            c = str(no_lo)
            ok = str(c1).zfill(6)
            vals = c1
            self.env.cr.execute(
                "UPDATE hr_cmpteur_avancer SET no_code = %s, date_dernier_avancement = '%s' WHERE id_user = %s and company_id = %d" % (
                    vals, self.date_modiff, self.id, val_struct))

    # Définition des fonctions

    # fonction qui permet d'additioner la valeur de deux champs
    @api.onchange('charge_femme', 'charge_enfant')
    def calcul_total_charge(self):
        for vals in self:
            vals.charge = vals.charge_femme + vals.charge_enfant

            # fonction de recherche permettant de retourner le salaire de base dans la grille des fonctionnaires en fonction des paramètres

    @api.onchange('x_echellon_id', 'x_classees_id', 'x_echelle_id', 'x_categorie_id')
    def sal_base(self):
        val_class = int(self.x_classees_id)
        val_echel = int(self.x_echelle_id)
        val_echellon = int(self.x_echellon_id)
        val_cat = int(self.x_categorie_id)
        if val_class != False and val_echel != False and val_echellon != False and val_cat != False:
            res = self.env['hr_grillesalariale'].search(
                [('x_echellon_id', '=', val_echellon), ('x_class_id', '=', val_class), ('x_categorie_id', '=', val_cat),
                 ('x_echelle_id', '=', val_echel)])
            self.x_solde_indiciaire = round(res.x_salbase)  # x_salbase=solde indiciaire
            print('Solde Indiciare', self.x_solde_indiciaire)
            self.x_indemnite_residence = round((res.x_salbase * 10 / 100) + 0.1)  # 0.1:permet de mieux arrondir
            print('Solde residence', self.x_indemnite_residence)
            self.x_solde_indiciaire_net = self.x_solde_indiciaire + self.x_indemnite_residence  # solde indiciaire_net= salaire de base
            self.x_indice = round(res.x_indice)

    # fonction de recherche permettant de retourner l'indemnité de responsabilité en fonction des paramètres
    @api.onchange('x_fonction_id', 'x_zone_id')
    def indem_resp(self):
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_struct = int(self.company_id)
        if val_fonct != False or val_fonct == False and val_zone != False or val_zone == False and val_struct != False:
            res = self.env['hr_paramindemniteresp'].search(
                [('x_fonction_id', '=', val_fonct), ('x_zone_id', '=', val_zone), ('company_id', '=', val_struct)])
            self.x_indem_resp = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité d'astreinte en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_astr(self):
        val_emploi = int(self.x_emploi_id)
        print("Emploie", val_emploi)
        val_fonct = int(self.x_fonction_id)  # non utilisé pour le moment
        val_zone = int(self.x_zone_id)
        print("Zone", val_zone)
        val_echel = int(self.x_echelle_c_id)
        print("Echelle", val_echel)
        val_cat = int(self.x_categorie_c_id)
        print("Categorie", val_cat)
        val_struct = int(self.company_id)
        print("Structure", val_struct)

        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemniteastr'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_astr = res.x_taux
                print("Taux à servir", self.x_indem_astr)

    # fonction de recherche permettant de retourner l'indemnité de logement en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_loge(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitelogement'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_loge = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité de technicité en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_techn(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitetechnicite'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_techn = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité spécificité GRH en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_spec(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitespecifique'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_specif = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité spécificité IT en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_spec_it(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitespecifique_it'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_spec_inspect_trav = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité spécificité IRP en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_fonction_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_spec_irp(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitespecifique_irp'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_spec_inspect_irp = res.x_taux

                # fonction de recherche permettant de retourner l'indemnité spécificité ISH en fonction des paramètres

    @api.onchange('x_emploi_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_spec_ish(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitespecifique_ish'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_spec_inspect_ish = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité spécificité IFC en fonction des paramètres
    @api.onchange('x_fonction_id', 'x_zone_id', 'x_categorie_c_id')
    def indem_spec_ifc(self):
        # val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        # val_zone = int(self.x_zone_id)
        # val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_fonct != False:
            if val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitespecifique_ifc'].search(
                    [('x_fonction_id', '=', val_fonct), ('x_categorie_c_id', '=', val_cat),
                     ('company_id', '=', val_struct)])
                self.x_indem_spec_inspect_ifc = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité de transport en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_fonction_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_transp(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitetransport'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_transp = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité informatique en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_fonction_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_informatique(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemniteinformatique'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_inform = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité exploitation reseau en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_fonction_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_exploit(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemniteexploireseau'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_exploit = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité resp financière en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_fonction_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_respfinanciere(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemniterespfinanciere'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_finance = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité de garde en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_fonction_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_garde(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitegarde'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_garde = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité de risque de contagion en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_fonction_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_risque(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemniterisquecontagion'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_risque = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité de sujétion géographique de contagion en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_fonction_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_sujetion(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitesujetion'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_suj = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité de formation spécialisée en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_fonction_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_formation(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemniteformation'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_form = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité de caisse en fonction des paramètres
    @api.onchange('x_fonction_id', 'x_categorie_c_id')
    def indem_caisse(self):
        # val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_fonct != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitecaisse'].search(
                    [('x_fonction_id', '=', val_fonct), ('x_categorie_c_id', '=', val_cat),
                     ('company_id', '=', val_struct)])
                self.x_indem_caisse = res.x_taux

    # fonction de recherche permettant de retourner l'indemnité vesttimentaire en fonction des paramètres
    @api.onchange('x_emploi_id', 'x_fonction_id', 'x_zone_id', 'x_echelle_c_id', 'x_categorie_c_id')
    def indem_veste(self):
        val_emploi = int(self.x_emploi_id)
        val_fonct = int(self.x_fonction_id)
        val_zone = int(self.x_zone_id)
        val_echel = int(self.x_echelle_c_id)
        val_cat = int(self.x_categorie_c_id)
        val_struct = int(self.company_id)
        if val_emploi != False:
            if val_zone != False or val_zone == False and val_echel != False or val_echel == False and val_cat != False or val_cat == False and val_struct != False:
                res = self.env['hr_paramindemnitevest'].search(
                    [('x_emploi_id', '=', val_emploi), ('x_zone_id', '=', val_zone), ('x_echelle_c_id', '=', val_echel),
                     ('x_categorie_c_id', '=', val_cat), ('company_id', '=', val_struct)])
                self.x_indem_veste = res.x_taux

    # fonction permettant de gerer l'historisation de salaire net
    @api.onchange('employee_id')
    def historiqueSalEmployee(self):
        structure = int(self.company_id)
        employe = int(self.employee_id)
        salaire = self.env['hr.employee'].search([('id', '=', employe), ('company_id', '=', structure)])
        self.x_salaire_net = salaire.x_net_payer_ctrct

    # fonction permettant de gerer l'historisation de salaire net contractuel
    @api.onchange('employee_id')
    def historiqueSalContEmployee(self):
        structure = int(self.company_id)
        employe = int(self.employee_id)
        salaires = self.env['hr.employee'].search([('id', '=', employe), ('company_id', '=', structure)])
        self.x_salaire_net = salaires.x_net_payer_ctrct

    # ajouter par max pour calcul des arrieres de salaire
    x_is_rappel = fields.Boolean(string='Rappel', required=False)
    x_nbr_mois_rappel = fields.Integer(string='Nombre de mois', required=False)
    #
    x_r_solde_indiciaire_ctrct = fields.Float(string="Salaire de base")  # r mis pour rappel
    x_r_allocation_familial = fields.Float(string="Allocation familiale")
    x_r_indem_resp = fields.Float(string="Indemn.Resp")
    x_r_indem_astr = fields.Float(string="Indemn.Astreinte")
    x_r_indem_techn = fields.Float(string="Indemn.Technicité", )
    x_r_indem_specif = fields.Float(string="Indemn.Spécifique GRH")
    x_r_indem_loge = fields.Float(string="Indemn.Logement")
    x_r_indem_transp = fields.Float(string="Indemn.Transport")
    x_r_indem_inform = fields.Float(string="Indemn.Informatique")
    x_r_indem_exploit = fields.Float(string="Indemn.Exploitation-Réseau", )
    x_r_indem_finance = fields.Float(string="Indemn.Resp.Financière", )
    x_r_indem_garde = fields.Float(string="Indemn.Garde", )
    x_r_indem_risque = fields.Float(string="Indemn.Risque.Contagion", )
    x_r_indem_suj = fields.Float(string="Indemn.Sujétion Géographique", )
    x_r_indem_form = fields.Float(string="Indemn.Formation", )
    x_r_indem_caisse = fields.Float(string="Indemn.Caisse", )
    x_r_indem_veste = fields.Float(string="Indemn.Vestimentaire", )
    x_r_indem_spec_inspect_trav = fields.Float(string="Indemn.Spécifique Inspecteur de Travail")
    x_r_indem_spec_inspect_ifc = fields.Float(string="Indemn.Spécifique Forfaitaire Compensatrice")
    x_r_indem_spec_inspect_irp = fields.Float(string="Indemn.Spécifique de Responsabilité Pécunière", )
    x_r_indem_spec_inspect_ish = fields.Float(string="Indemn.Spécifique Harmonisée Personnel MENA et MESRSI")
    x_r_indem_prime_rendement = fields.Float(string="Prime rendement")
    # Carfo cnss iuts
    x_r_mnt_cnss = fields.Float(string="Montant CNSS")
    x_r_mnt_patronal_cnss = fields.Float(string="Part Patronale CNSS")
    x_r_mnt_carfo = fields.Float(string="Montant CARFO")
    x_r_mnt_patronal_carfo = fields.Float(string="Part Patronale CARFO")
    x_r_retenue_iuts = fields.Float(string="Retenue IUTS")
    x_r_iuts_net = fields.Float(string="IUTS Net", )

    def calcul_arriere_salaire(self):
        self.x_r_solde_indiciaire_ctrct = self.x_solde_indiciaire_ctrct * self.x_nbr_mois_rappel
        self.x_r_allocation_familial = self.x_allocation_familial * self.x_nbr_mois_rappel
        self.x_r_indem_resp = self.x_indem_resp * self.x_nbr_mois_rappel
        self.x_r_indem_astr = self.x_indem_astr * self.x_nbr_mois_rappel
        self.x_r_indem_techn = self.x_indem_techn * self.x_nbr_mois_rappel
        self.x_r_indem_specif = self.x_r_indem_specif * self.x_nbr_mois_rappel
        self.x_r_indem_loge = self.x_indem_loge * self.x_nbr_mois_rappel
        self.x_r_indem_transp = self.x_indem_transp * self.x_nbr_mois_rappel
        self.x_r_indem_inform = self.x_indem_inform * self.x_nbr_mois_rappel
        self.x_r_indem_exploit = self.x_indem_exploit * self.x_nbr_mois_rappel
        self.x_r_indem_finance = self.x_indem_finance * self.x_nbr_mois_rappel
        self.x_r_indem_garde = self.x_indem_garde * self.x_nbr_mois_rappel
        self.x_r_indem_risque = self.x_indem_risque * self.x_nbr_mois_rappel
        self.x_r_indem_suj = self.x_indem_suj * self.x_nbr_mois_rappel
        self.x_r_indem_form = self.x_r_indem_form * self.x_nbr_mois_rappel
        self.x_r_indem_caisse = self.x_indem_caisse * self.x_nbr_mois_rappel
        self.x_r_indem_veste = self.x_indem_veste * self.x_nbr_mois_rappel
        self.x_r_indem_spec_inspect_trav = self.x_indem_spec_inspect_trav * self.x_nbr_mois_rappel
        self.x_r_indem_spec_inspect_ifc = self.x_indem_spec_inspect_ifc * self.x_nbr_mois_rappel
        self.x_r_indem_spec_inspect_irp = self.x_indem_spec_inspect_irp * self.x_nbr_mois_rappel
        self.x_r_indem_spec_inspect_ish = self.x_indem_spec_inspect_ish * self.x_nbr_mois_rappel
        self.x_r_indem_prime_rendement = self.x_indem_prime_rendement * self.x_nbr_mois_rappel
        # Carfo cnss iuts
        self.x_r_mnt_cnss = self.x_mnt_cnss * self.x_nbr_mois_rappel
        self.x_r_mnt_patronal_cnss = self.x_mnt_patronal_cnss * self.x_nbr_mois_rappel
        self.x_r_mnt_carfo = self.x_mnt_carfo * self.x_nbr_mois_rappel
        self.x_r_mnt_patronal_carfo = self.x_mnt_patronal_carfo * self.x_nbr_mois_rappel
        self.x_r_retenue_iuts = self.x_retenue_iuts * self.x_nbr_mois_rappel
        self.x_r_iuts_net = self.x_iuts_net * self.x_nbr_mois_rappel

    @api.onchange('x_is_rappel')
    def desactive_arriere_salaire(self):
        for emp in self:
            if emp.x_is_rappel:
                emp.x_nbr_mois_rappel = 1
                emp.calcul_arriere_salaire()
            else:
                emp.x_nbr_mois_rappel = 0
                emp.calcul_arriere_salaire()

    nature_prcpte_id = fields.Many2one('hr_nature', string='Nature Précompte')
    x_precompte = fields.Float(string='Précompte :', readonly=False)
    x_retrait_prcpt_mois = fields.Float(string='Montant/Mois :')
    x_datedebut_prcpt = fields.Date(string='Date début', default=date.today())
    x_datefin_prcpt = fields.Date(string='Date fin', default=date.today())
    # date_jour = fields.Date(string='Date du jour', default=date.today() )
    duree = fields.Integer(string='Durée', readonly=True)

    # fonction pour contrôler les dates (date de debut ne doit pas etre superieur à la date de fin)
    @api.constrains('x_datedebut_prcpt', 'x_datefin_prcpt')
    def CtrlDate(self):

        for val in self:
            if val.x_datedebut_prcpt > val.x_datefin_prcpt:
                raise ValidationError(_(
                    "Enregistrement impossible. La date de début du precompte doit être toujours inférieure à la date de fin du precompte"))

    # fonction pour contrôler les montants precompte et le montant à prelever par mois
    @api.constrains('x_precompte', 'x_retrait_prcpt_mois')
    def CtrlMontant(self):

        for val in self:
            if val.x_retrait_prcpt_mois > val.x_precompte:
                raise ValidationError(_(
                    "Enregistrement impossible. Le montant du précompte ne doit pas être inférieur au montant à prélever mensuellement."))

    etat_prcpte = fields.Selection([
        ('active', "Activé"),
        ('desactive', "Désactivé"),
    ], required=False, string="Etat")

    enfants_ids = fields.One2many('hr_employee_enfant', 'employee_id', string="Enfant", index=True)

    @api.depends('enfants_ids')
    def calcul_charge_enfant(self):
        for val in self:
            charge_enfant = 0
            for e in val.enfants_ids:
                if e.age <= 18:
                    charge_enfant = charge_enfant + 1
            val.charge_enfant = charge_enfant

class HrEmployeesEnfant(models.Model):
    _name = "hr_employee_enfant"

    name = fields.Char(string="Nom et Prénoms", required=True)
    date_naissance = fields.Date(string='Date naissance', required=True, default=date.today())
    age = fields.Integer(string="Age", compute="calcul_age")

    sexe = fields.Selection([
        ('M', 'Masculin'),
        ('F', 'Feminin'),
    ], 'Sexe', default='M', index=True, required=True)


    employee_id = fields.Many2one('hr.employee', string='Employé', required=True)

    @api.depends('date_naissance')
    def calcul_age(self):
        for val in self:
            val.age = 0
            if val.date_naissance:
                start_date = date.today()
                end_date = val.date_naissance
                val.age = (start_date - end_date).days / 365