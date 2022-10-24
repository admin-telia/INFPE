from odoo import fields, api, models, tools, _
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from num2words import num2words
from odoo.exceptions import UserError, ValidationError


class HrReportBanque(models.Model):
    _name = "hr_reportbanque"
    _rec_name = 'x_banq_id'
    financiers_id = fields.Many2one('res.users', string="Financier", required=True)
    drhs_id = fields.Many2one('res.users', string="DRH", required=True)
    description = fields.Text(string='Description')
    x_banq_id = fields.Many2one('res.bank', string='Nom banque', required=True)
    x_date_debut = fields.Date(string='Date début',
                               default=lambda self: fields.Date.to_string(date.today().replace(day=1)), required=True)
    v_mois = fields.Char(string='mois')
    v_annee = fields.Char(string='mois')
    concat = fields.Char(store=True, readonly=True, string='Période')
    x_date_fin = fields.Date(string='Date fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_ids = fields.One2many('hr_reportbanque_line', 'x_report_id', string="Liste des concernés")
    x_mnts = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')
    x_moi = fields.Selection([
        ('janvier', 'Janvier'),
        ('fevrier', 'Février'),
        ('mars', 'Mars'),
        ('avril', 'Avril'),
        ('mai', 'Mai'),
        ('juin', 'Juin'),
        ('juillet', 'Juillet'),
        ('aout', 'Août'),
        ('septembre', 'Septembre'),
        ('octobre', 'Octobre'),
        ('novembre', 'Novembre'),
        ('decembre', 'Décembre'),
    ], string="Mois", readonly=True)
    date_op = fields.Datetime(string='Date impression', default=datetime.today(), readonly=True)
    v_mois = fields.Char(string='mois')

    # fonction pour retourner le mois en fonction de la date saisie
    @api.onchange('x_date_debut')
    def CtrlMois(self):
        for vals in self:
            if vals.x_date_debut:
                mois = vals.x_date_debut
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
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)

    # fonction de remplissage du tableau
    def remplissages(self):
        if self.x_banq_id and self.x_date_debut and self.x_date_fin:
            elements = self.env['hr.payslip'].search([('banque.id', '=', self.x_banq_id.id),
                                                      ('date_from', '<=', self.x_date_debut),
                                                      ('date_to', '>=', self.x_date_fin),
                                                      ('state', '=', 'done')])
            # ('state', '=', 'done')
            elements_lines = []
            # delete old payslip lines
            self.x_line_ids.unlink()
            self.x_mnts = 0
            for e in elements:
                amount = 0
                for l in e.line_ids:
                    if l.code == 'net_payer':
                        amount = l.amount
                if e.employee_id.x_type_employe_id.code in ('FCT_DETACH', 'FCT_MD'):
                    matricule = e.x_matricule_fct
                else:
                    matricule = e.x_matricule_ctrct

                elements_lines.append((0, 0,
                                       {'name': e.employee_id.name, 'x_matricule': matricule,
                                        'x_sal_net': amount, 'numb': e.numcompte,
                                        'x_emploi': e.x_emploi,
                                        'x_fonction': e.x_fonction,
                                        }))
                self.x_mnts = self.x_mnts + amount

            self.x_line_ids = elements_lines
            self.x_mnt_en_lettre = num2words(self.x_mnts, lang='fr')

    def numOrdreb(self):
        num = 0
        for x in self.x_line_ids:
            x.numero = num + 1
            num = num + 1


# class permettant de recueillir les lignes de la requête
class HrReportBanqueLine(models.Model):
    _name = "hr_reportbanque_line"
    x_report_id = fields.Many2one('hr_reportbanque', ondelete="cascade")

    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Matricule')
    name = fields.Char(string='Employé')
    numb = fields.Char(string='N° Compte')
    x_emploi = fields.Char(string='Emploi')
    x_fonction = fields.Char(string='Fonction')
    x_sal_net = fields.Float(string='Salaire net')
    x_mnt = fields.Float(string='Montant')


# classe mère des etats des avoirs
class HrReportAvoirs(models.Model):
    _name = "hr_reportavoir"
    name = fields.Char(string='Nom')
    _rec_name = 'lib_long'
    financiers_id = fields.Many2one('res.users', string="Financier", required=True)
    drhs_id = fields.Many2one('res.users', string="DRH", required=True)

    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=True)
    x_elt_sal_id = fields.Many2one('hr.salary.rule', string='Element de salaire', required=True)
    lib_long = fields.Char(string='Intitulé Etat', required=True)
    x_date_debut = fields.Date(string='Date début',
                               default=lambda self: fields.Date.to_string(date.today().replace(day=1)), required=True)
    x_date_fin = fields.Date(string='Date fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    v_mois = fields.Char(string='mois')
    v_annee = fields.Char(string='mois')
    concat = fields.Char(store=True, readonly=True, string='Période')
    x_mnts = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')
    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))
    x_line_ids = fields.One2many('hr_reportavoir_line', 'x_reportavoir_id', string="Liste des élements")
    x_moi = fields.Selection([
        ('janvier', 'Janvier'),
        ('fevrier', 'Février'),
        ('mars', 'Mars'),
        ('avril', 'Avril'),
        ('mai', 'Mai'),
        ('juin', 'Juin'),
        ('juillet', 'Juillet'),
        ('aout', 'Août'),
        ('septembre', 'Septembre'),
        ('octobre', 'Octobre'),
        ('novembre', 'Novembre'),
        ('decembre', 'Décembre'),
    ], string="Mois", readonly=True)
    date_op = fields.Date(string='Date Opération', default=date.today(), readonly=True)
    v_mois = fields.Char(string='mois')

    # fonction pour retourner le mois en fonction de la date saisie
    @api.onchange('x_date_debut')
    def CtrlMois(self):
        for vals in self:
            if vals.x_date_debut:
                mois = vals.x_date_debut
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
                    vals.concat = str(vals.x_moi) + " - " + str(vals.v_annee)

    # fonction de remplissage du tableau des avoirs
    def avoir(self):
        if self.x_type_employe_id and self.x_elt_sal_id and self.x_date_debut and self.x_date_fin:
            elements = self.env['hr.payslip.line'].search([('slip_id.struct_id', '=', self.x_type_employe_id.id),
                                                           ('slip_id.date_from', '<=', self.x_date_debut),
                                                           ('slip_id.date_to', '>=', self.x_date_fin),
                                                           ('salary_rule_id', '=', self.x_elt_sal_id.id),
                                                           ('slip_id.state', '=', 'done')])
            # ('state', '=', 'done') 01 03
            elements_lines = []
            # delete old payslip lines
            self.x_line_ids.unlink()
            self.x_mnts = 0
            numero = 0
            for e in elements:
                numero = numero + 1
                if e.employee_id.x_type_employe_id.code in ('FCT_DETACH', 'FCT_MD'):
                    matricule = e.slip_id.x_matricule_fct
                else:
                    matricule = e.slip_id.x_matricule_ctrct
                elements_lines.append((0, 0,
                                       {'name': e.employee_id.name, 'x_matricule': matricule,
                                        'x_mnt': e.amount, 'numero': numero
                                        }))
                self.x_mnts = self.x_mnts + e.amount

            self.x_line_ids = elements_lines
            self.x_mnt_en_lettre = num2words(self
                                             .x_mnts, lang='fr')

    def numOrdrea(self):
        num = 0
        for x in self.x_line_ids:
            x.numero = num + 1
            num = num + 1


class HrReportAvoirsLine(models.Model):
    _name = "hr_reportavoir_line"
    name = fields.Char(string='Employé')
    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Mle Fonctionnaire')
    x_matricule_c = fields.Char(string='Mle Contractuel')
    x_reportavoir_id = fields.Many2one('hr_reportavoir')
    x_mnt = fields.Float(string='Montant')


# Etat cotisation Part employe
class HrEtatCotisation(models.Model):
    _name = 'hr_etat_cot'
    _rec_name = 'x_type_employe_id'

    name = fields.Char(string='Intitulé', required=False)
    code = fields.Char(string='code', required=False, default="/")
    financiers_id = fields.Many2one('res.users', string="Financier", required=True)
    drhs_id = fields.Many2one('res.users', string="DRH", required=True)

    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=False)
    x_type_employe_code = fields.Char(string='code', required=False, store=True, related="x_type_employe_id.code")
    x_elt_sal_id = fields.Many2one('hr.salary.rule', string='Element de salaire', required=False)
    # lib_long = fields.Char(string='Intitulé Etat', required=True)
    x_date_debut = fields.Date(string='Date début',
                               default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                               required=True)
    x_date_fin = fields.Date(string='Date fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    periode = fields.Char(store=True, readonly=True, string='Période')
    date_op = fields.Date(string='Date Opération', default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_etat_cot_line', 'x_element_id', string="Liste des élements")

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    x_mnts = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')

    # fonction pour retourner le mois en fonction de la date saisie
    @api.onchange('x_date_debut')
    def calcul_periode(self):
        for vals in self:
            if vals.x_date_debut:
                valeur_mois = str(vals.x_date_debut.month)
                valeur_annee = str(vals.x_date_debut.year)
                if valeur_mois == '1':
                    vals.periode = 'Janvier' + " - " + str(valeur_annee)
                elif valeur_mois == '2':
                    vals.periode = 'Février' + " - " + str(valeur_annee)
                elif valeur_mois == '3':
                    vals.periode = 'Mars' + " - " + str(valeur_annee)
                elif valeur_mois == '4':
                    vals.periode = 'Avril' + " - " + str(valeur_annee)
                elif valeur_mois == '5':
                    vals.periode = 'Mai' + " - " + str(valeur_annee)
                elif valeur_mois == '6':
                    vals.periode = 'Juin' + " - " + str(valeur_annee)
                elif valeur_mois == '7':
                    vals.periode = 'Juillet' + " - " + str(valeur_annee)
                elif valeur_mois == '8':
                    vals.periode = 'Août' + " - " + str(valeur_annee)
                elif valeur_mois == '9':
                    vals.periode = 'Septembre' + " - " + str(valeur_annee)
                elif valeur_mois == '10':
                    vals.periode = 'Octobre' + " - " + str(valeur_annee)
                elif valeur_mois == '11':
                    vals.periode = 'Novembre' + " - " + str(valeur_annee)
                else:
                    vals.periode = 'Décembre' + " - " + str(valeur_annee)

    # fonction de remplissage du tableau des avoirs
    def avoir(self):
        if self.x_type_employe_id and self.x_date_debut and self.x_date_fin:
            if self.x_type_employe_id.code in ('FCT_DETACH', 'FCT_MD'):
                code = 'carfo'
            else:
                code = 'cnss'

            elements = self.env['hr.payslip.line'].search([('slip_id.date_from', '<=', self.x_date_debut),
                                                           ('slip_id.date_to', '>=', self.x_date_fin),
                                                           ('code', '=', code),
                                                           ('slip_id.state', '=', 'done')])
            elements_lines = []
            # delete old payslip lines
            self.x_line_ids.unlink()
            x_mnts = 0
            numero = 0
            for e in elements:
                numero = numero + 1

                if self.x_type_employe_id.code in ('FCT_DETACH', 'FCT_MD'):
                    x_matricule = e.employee_id.matricule
                    x_num_cnss = '-'
                else:
                    x_matricule = e.employee_id.matricule_genere
                    x_num_cnss = e.employee_id.num_declaration
                elements_lines.append((0, 0,
                                       {'name': e.employee_id.name, 'x_matricule': x_matricule,
                                        'x_num_cnss': x_num_cnss, 'numero': numero,
                                        'x_mnt': e.amount
                                        }))
                x_mnts = x_mnts + e.amount

            self.x_mnts = x_mnts
            self.x_line_ids = elements_lines
            self.x_mnt_en_lettre = num2words(self
                                             .x_mnts, lang='fr')

    def numOrdrea(self):
        pass


class HrEtatCotisationLine(models.Model):
    _name = "hr_etat_cot_line"
    name = fields.Char(string='Employé')
    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Mle Fonctionnaire')
    x_num_cnss = fields.Char(string='Référence')
    x_element_id = fields.Many2one('hr_etat_cot')
    x_mnt = fields.Float(string='Montant')


# Etat cotisation Part employeur
class HrEtatCotisationEmployeur(models.Model):
    _name = 'hr_etat_cot_emp'
    _rec_name = 'x_type_employe_id'

    name = fields.Char(string='Intitulé', required=False)
    code = fields.Char(string='code', required=False, default="/")
    financiers_id = fields.Many2one('res.users', string="Financier", required=True)
    drhs_id = fields.Many2one('res.users', string="DRH", required=True)

    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=False)
    x_elt_sal_id = fields.Many2one('hr.salary.rule', string='Element de salaire', required=False)
    # lib_long = fields.Char(string='Intitulé Etat', required=True)
    x_date_debut = fields.Date(string='Date début',
                               default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                               required=True)
    x_date_fin = fields.Date(string='Date fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    periode = fields.Char(store=True, readonly=True, string='Période')
    date_op = fields.Date(string='Date Opération', default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_etat_cot_emp_line', 'x_element_id', string="Liste des élements")

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    x_mnts = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')

    # fonction pour retourner le mois en fonction de la date saisie
    @api.onchange('x_date_debut')
    def calcul_periode(self):
        for vals in self:
            if vals.x_date_debut:
                valeur_mois = str(vals.x_date_debut.month)
                valeur_annee = str(vals.x_date_debut.year)
                if valeur_mois == '1':
                    vals.periode = 'Janvier' + " - " + str(valeur_annee)
                elif valeur_mois == '2':
                    vals.periode = 'Février' + " - " + str(valeur_annee)
                elif valeur_mois == '3':
                    vals.periode = 'Mars' + " - " + str(valeur_annee)
                elif valeur_mois == '4':
                    vals.periode = 'Avril' + " - " + str(valeur_annee)
                elif valeur_mois == '5':
                    vals.periode = 'Mai' + " - " + str(valeur_annee)
                elif valeur_mois == '6':
                    vals.periode = 'Juin' + " - " + str(valeur_annee)
                elif valeur_mois == '7':
                    vals.periode = 'Juillet' + " - " + str(valeur_annee)
                elif valeur_mois == '8':
                    vals.periode = 'Août' + " - " + str(valeur_annee)
                elif valeur_mois == '9':
                    vals.periode = 'Septembre' + " - " + str(valeur_annee)
                elif valeur_mois == '10':
                    vals.periode = 'Octobre' + " - " + str(valeur_annee)
                elif valeur_mois == '11':
                    vals.periode = 'Novembre' + " - " + str(valeur_annee)
                else:
                    vals.periode = 'Décembre' + " - " + str(valeur_annee)

    # fonction de remplissage du tableau des avoirs
    def avoir(self):
        if self.x_type_employe_id and self.x_date_debut and self.x_date_fin:
            if self.x_type_employe_id.code in ('FCT_DETACH', 'FCT_MD'):
                code = 'part_carfo'
            else:
                code = 'part_cnss'

            elements = self.env['hr.payslip.line'].search([('slip_id.date_from', '<=', self.x_date_debut),
                                                           ('slip_id.date_to', '>=', self.x_date_fin),
                                                           ('code', '=', code),
                                                           ('slip_id.state', '=', 'done')])
            elements_lines = []
            # delete old payslip lines
            self.x_line_ids.unlink()
            x_mnts = 0
            numero = 0
            for e in elements:
                numero = numero + 1

                if self.x_type_employe_id.code in ('FCT_DETACH', 'FCT_MD'):
                    x_matricule = e.employee_id.matricule
                    x_num_cnss = '-'
                else:
                    x_matricule = e.employee_id.matricule_genere
                    x_num_cnss = e.employee_id.num_declaration
                elements_lines.append((0, 0,
                                       {'name': e.employee_id.name, 'x_matricule': x_matricule,
                                        'x_num_cnss': x_num_cnss, 'numero': numero,
                                        'x_mnt': e.amount
                                        }))
                x_mnts = x_mnts + e.amount

            self.x_mnts = x_mnts
            self.x_line_ids = elements_lines
            self.x_mnt_en_lettre = num2words(self
                                             .x_mnts, lang='fr')

    def numOrdrea(self):
        pass


class HrEtatCotisationEmployeurLine(models.Model):
    _name = "hr_etat_cot_emp_line"
    name = fields.Char(string='Employé')
    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Mle Fonctionnaire')
    x_num_cnss = fields.Char(string='Référence')
    x_element_id = fields.Many2one('hr_etat_cot_emp')
    x_mnt = fields.Float(string='Montant')


# Etat cotisation Part agent/employe
class HrEtatCotisationAgentEmployeur(models.Model):
    _name = 'hr_etat_cot_ag_emp'
    _rec_name = 'x_type_employe_id'

    name = fields.Char(string='Intitulé', required=False)
    code = fields.Char(string='code', required=False, default="/")
    financiers_id = fields.Many2one('res.users', string="Financier", required=True)
    drhs_id = fields.Many2one('res.users', string="DRH", required=True)

    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=False)
    x_elt_sal_id = fields.Many2one('hr.salary.rule', string='Element de salaire', required=False)
    # lib_long = fields.Char(string='Intitulé Etat', required=True)
    x_date_debut = fields.Date(string='Date début',
                               default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                               required=True)
    x_date_fin = fields.Date(string='Date fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    periode = fields.Char(store=True, readonly=True, string='Période')
    date_op = fields.Date(string='Date Opération', default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_etat_cot_ag_emp_line', 'x_element_id', string="Liste des élements")

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    x_mnts = fields.Float(string='Montant Total')
    x_mnts_emp = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')

    # fonction pour retourner le mois en fonction de la date saisie
    @api.onchange('x_date_debut')
    def calcul_periode(self):
        for vals in self:
            if vals.x_date_debut:
                valeur_mois = str(vals.x_date_debut.month)
                valeur_annee = str(vals.x_date_debut.year)
                if valeur_mois == '1':
                    vals.periode = 'Janvier' + " - " + str(valeur_annee)
                elif valeur_mois == '2':
                    vals.periode = 'Février' + " - " + str(valeur_annee)
                elif valeur_mois == '3':
                    vals.periode = 'Mars' + " - " + str(valeur_annee)
                elif valeur_mois == '4':
                    vals.periode = 'Avril' + " - " + str(valeur_annee)
                elif valeur_mois == '5':
                    vals.periode = 'Mai' + " - " + str(valeur_annee)
                elif valeur_mois == '6':
                    vals.periode = 'Juin' + " - " + str(valeur_annee)
                elif valeur_mois == '7':
                    vals.periode = 'Juillet' + " - " + str(valeur_annee)
                elif valeur_mois == '8':
                    vals.periode = 'Août' + " - " + str(valeur_annee)
                elif valeur_mois == '9':
                    vals.periode = 'Septembre' + " - " + str(valeur_annee)
                elif valeur_mois == '10':
                    vals.periode = 'Octobre' + " - " + str(valeur_annee)
                elif valeur_mois == '11':
                    vals.periode = 'Novembre' + " - " + str(valeur_annee)
                else:
                    vals.periode = 'Décembre' + " - " + str(valeur_annee)

    # fonction de remplissage du tableau des avoirs
    def avoir(self):
        if self.x_type_employe_id and self.x_date_debut and self.x_date_fin:
            if self.x_type_employe_id.code in ('FCT_DETACH', 'FCT_MD'):
                code = 'carfo'
                code_pat = 'part_carfo'
            else:
                code = 'cnss'
                code_pat = 'part_cnss'
            elements = self.env['hr.payslip'].search([('date_from', '<=', self.x_date_debut),
                                                      ('date_to', '>=', self.x_date_fin),
                                                      ('state', '=', 'done')])
            elements_lines = []
            # delete old payslip lines
            self.x_line_ids.unlink()
            numero = 0
            x_mnts = 0
            x_mnts_emp = 0
            for e in elements:
                x_mnt = 0
                x_mnt_emp = 0
                for l in e.line_ids:
                    if l.code == code:
                        x_mnt = l.amount
                    if l.code == code_pat:
                        x_mnt_emp = l.amount
                if x_mnt or x_mnt_emp:
                    numero = numero + 1

                    if self.x_type_employe_id.code in ('FCT_DETACH', 'FCT_MD'):
                        x_matricule = e.employee_id.matricule
                        x_num_cnss = '-'
                    else:
                        x_matricule = e.employee_id.matricule_genere
                        x_num_cnss = e.employee_id.num_declaration

                    elements_lines.append((0, 0,
                                           {'name': e.employee_id.name, 'x_matricule': x_matricule,
                                            'x_num_cnss': x_num_cnss, 'numero': numero,
                                            'x_mnt': x_mnt, 'x_mnt_emp': x_mnt_emp,
                                            }))
                    x_mnts = x_mnts + x_mnt
                    x_mnts_emp = x_mnts_emp + x_mnt_emp

            self.x_mnts = x_mnts
            self.x_mnts_emp = x_mnts_emp
            self.x_line_ids = elements_lines
            self.x_mnt_en_lettre = num2words(self
                                             .x_mnts, lang='fr')

    def numOrdrea(self):
        pass


class HrEtatCotisationAgentEmployeurLine(models.Model):
    _name = "hr_etat_cot_ag_emp_line"
    name = fields.Char(string='Employé')
    numero = fields.Integer(string='N°', readonly=True)
    x_matricule = fields.Char(string='Matricule')
    x_num_cnss = fields.Char(string='Référence')
    x_element_id = fields.Many2one('hr_etat_cot_ag_emp')
    x_mnt = fields.Float(string='Part Agent')
    x_mnt_emp = fields.Float(string='Part Employeur')


# Etat Precompte employe
class HrEtatPrecompte(models.Model):
    _name = 'hr_etat_precompte'

    name = fields.Char(string='Intitulé', required=False)
    code = fields.Char(string='code', required=False, default="/")
    financiers_id = fields.Many2one('res.users', string="Financier", required=True)
    drhs_id = fields.Many2one('res.users', string="DRH", required=True)

    x_type_employe_id = fields.Many2one("hr.payroll.structure", string="Type employé", required=False)
    x_type_employe_code = fields.Char(string='code', required=False, store=True, related="x_type_employe_id.code")
    x_elt_sal_id = fields.Many2one('hr_paie_precompte_element', string='Element de Precompte', required=False)
    # lib_long = fields.Char(string='Intitulé Etat', required=True)
    x_date_debut = fields.Date(string='Date début',
                               default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                               required=True)
    x_date_fin = fields.Date(string='Date fin', default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()), required=True)
    periode = fields.Char(store=True, readonly=True, string='Période')
    date_op = fields.Date(string='Date Opération', default=date.today(), readonly=True)
    x_line_ids = fields.One2many('hr_etat_precompte_line', 'x_element_id', string="Liste des élements")

    company_id = fields.Many2one('res.company', string="Structure", default=lambda self: self.env.user.company_id.id)
    x_exercice_id = fields.Many2one('ref_exercice',
                                    default=lambda self: self.env['ref_exercice'].search([('etat', '=', 1)]))

    x_mnts = fields.Float(string='Montant Total')
    x_mnt_en_lettre = fields.Char(string='Montant en lettres')

    # fonction pour retourner le mois en fonction de la date saisie
    @api.onchange('x_date_debut')
    def calcul_periode(self):
        for vals in self:
            if vals.x_date_debut:
                valeur_mois = str(vals.x_date_debut.month)
                valeur_annee = str(vals.x_date_debut.year)
                if valeur_mois == '1':
                    vals.periode = 'Janvier' + " - " + str(valeur_annee)
                elif valeur_mois == '2':
                    vals.periode = 'Février' + " - " + str(valeur_annee)
                elif valeur_mois == '3':
                    vals.periode = 'Mars' + " - " + str(valeur_annee)
                elif valeur_mois == '4':
                    vals.periode = 'Avril' + " - " + str(valeur_annee)
                elif valeur_mois == '5':
                    vals.periode = 'Mai' + " - " + str(valeur_annee)
                elif valeur_mois == '6':
                    vals.periode = 'Juin' + " - " + str(valeur_annee)
                elif valeur_mois == '7':
                    vals.periode = 'Juillet' + " - " + str(valeur_annee)
                elif valeur_mois == '8':
                    vals.periode = 'Août' + " - " + str(valeur_annee)
                elif valeur_mois == '9':
                    vals.periode = 'Septembre' + " - " + str(valeur_annee)
                elif valeur_mois == '10':
                    vals.periode = 'Octobre' + " - " + str(valeur_annee)
                elif valeur_mois == '11':
                    vals.periode = 'Novembre' + " - " + str(valeur_annee)
                else:
                    vals.periode = 'Décembre' + " - " + str(valeur_annee)

    # fonction de remplissage du tableau des avoirs
    def avoir(self):
        if self.x_date_debut and self.x_date_fin:

            elements = self.env['hr_paie_precompte_line'].search([('x_date_debut', '<=', self.x_date_debut),
                                                                  ('x_date_fin', '>=', self.x_date_fin),
                                                                  ('precompte_id.x_precompte_id', '=', self.x_elt_sal_id.id),
                                                                  ('state', '=', 'P')])
            elements_lines = []
            # delete old payslip lines ('x_date_debut', '>=', self.x_date_debut),
            #                                                                   ('x_date_fin', '<=', self.x_date_fin),
            self.x_line_ids.unlink()
            x_mnts = 0
            numero = 0
            for e in elements:
                numero = numero + 1

                if e.precompte_id.x_employe_id.x_type_employe_id.code in ('FCT_DETACH', 'FCT_MD'):
                    x_matricule = e.precompte_id.x_employe_id.matricule
                else:
                    x_matricule = e.precompte_id.x_employe_id.matricule_genere
                elements_lines.append((0, 0,
                                       {'name': e.precompte_id.x_employe_id.name,
                                        'x_matricule': x_matricule,
                                        'x_reference': e.precompte_id.name, 'x_mnt': e.precompte_id.montant,
                                        'x_mnt_ret_mens': e.montant, 'x_mnt_rem': e.precompte_id.montant_paye,
                                        'x_mnt_rest': e.precompte_id.montant_reste
                                        }))
                # x_mnts = x_mnts + e.amount

            self.x_mnts = x_mnts
            self.x_line_ids = elements_lines
            self.x_mnt_en_lettre = num2words(self.x_mnts, lang='fr')

    def numOrdrea(self):
        pass


class HrEtatCotisationLine(models.Model):
    _name = "hr_etat_precompte_line"
    name = fields.Char(string='Employé')
    numero = fields.Integer(string='N°', readonly=True)
    x_reference = fields.Char(string='Reference')
    x_matricule = fields.Char(string='Mle Fonctionnaire')
    x_mnt = fields.Float(string='Mt initial')
    x_mnt_ret_mens = fields.Float(string='Ret. Mens.')
    x_mnt_rem = fields.Float(string='Mt. Remb')
    x_mnt_rest = fields.Float(string='Reste')

    x_element_id = fields.Many2one('hr_etat_cot')